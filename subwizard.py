# Standard library
import os
import json
import warnings

# Ignore pkg_resources deprecation warning from dependencies
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API",
    category=UserWarning
)

# Third-party
import av
import torch
import webview
from faster_whisper import WhisperModel

# Parche de compatibilidad para versiones nuevas de PyAV (av >= 14 / Python 3.14):
# faster-whisper pasa 'metadata_errors="ignore"' a av.open(), pero versiones
# recientes de PyAV eliminaron ese argumento y lanzan TypeError.
_original_av_open = av.open


def _compatible_av_open(*args, **kwargs):
    try:
        return _original_av_open(*args, **kwargs)
    except TypeError:
        kwargs.pop("metadata_errors", None)
        return _original_av_open(*args, **kwargs)


av.open = _compatible_av_open

# Local modules
from utils import utils, render_video, config_loader
from sub_styles import karaoke, simple, segments_to_json, word_pop, zoom_in


# =====================================================================
#                     CONFIGURACIÓN DE RENDIMIENTO
# =====================================================================

PERF_SETTINGS = {
    "efficient":      {"model": "base",   "beam": 3,  "compute": "int8"},
    "normal":         {"model": "small",  "beam": 5,  "compute": "int8"},
    "detailed":       {"model": "medium", "beam": 10, "compute": "float32"},
    "ultra-detailed": {"model": "large",  "beam": 20, "compute": "float32"},
}


# =====================================================================
#                   FUNCIONES DE TRANSCRIPCIÓN Y VIDEO
# =====================================================================

def load_whisper_model(performance="normal"):
    """
    Carga y devuelve el modelo de Faster-Whisper junto con el beam_size.
    Se llama una sola vez por lote para no recargar el modelo en cada archivo.
    """
    settings = PERF_SETTINGS.get(performance, PERF_SETTINGS["normal"])
    model_size = settings["model"]
    beam_size = settings["beam"]
    compute_type = settings["compute"]
    device = "cpu"

    if torch.cuda.is_available():
        print("Detected: GPU available! Optimizing for maximum speed.")
        device = "cuda"
        compute_type = "float16"
    else:
        print("No GPU detected. Proceeding with CPU, which may be slower.")

    print(f"Loading '{model_size}' model on {device}...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    return model, beam_size


def transcribe_to_subtitles(
    model,
    beam_size,
    audio_path,
    style="simple",
    output_path=None,
    max_words_per_line=5,
    file_name="subs",
    language=None,
    video_width=1920,
    video_height=1080,
):
    """
    Transcribe un archivo de audio usando el modelo ya cargado y genera
    el archivo de subtítulos (.srt o .ass) según el estilo elegido.
    """
    config_loader.load_config()

    print(f"Generating transcription for: {os.path.basename(audio_path)}")

    if language is None or language == "auto":
        segments, _info = model.transcribe(
            audio_path,
            beam_size=beam_size,
            word_timestamps=True
        )
    else:
        segments, _info = model.transcribe(
            audio_path,
            beam_size=beam_size,
            word_timestamps=True,
            language=language
        )

    segments = list(segments)
    word_data = segments_to_json.segments_to_json(segments, output_path, save_to_disk=False)
    words = word_data["words"]

    # Generar líneas según el estilo seleccionado
    if style == "karaoke":
        extension = ".ass"
        srt_lines = karaoke.karaoke_style(words, max_words_per_line, video_width, video_height)
    elif style == "word-pop":
        extension = ".ass"
        srt_lines = word_pop.word_pop_style(words, max_words_per_line, video_width, video_height)
    elif style == "zoom-in":
        extension = ".ass"
        srt_lines = zoom_in.zoom_in_style(words, max_words_per_line, video_width, video_height)
    else:
        extension = ".srt"
        srt_lines = simple.sort_in_srt(words, max_words_per_line)

    # Guardar archivo de subtítulos en disco
    subtitles_path = utils.create_srt_file(output_path, srt_lines, file_name, extension)
    print("Subtitles saved at:", subtitles_path)

    return subtitles_path


def process_single_file(
    file_path,
    output_folder,
    output_name,
    model,
    beam_size,
    max_words,
    style,
    output_format,
    language,
):
    """
    Procesa un único archivo de video o audio:
    - Si es video: extrae audio, genera subtítulos y (si se pidió mp4 o ambos) quema los subtítulos.
    - Si es audio: genera el archivo de subtítulos directamente.
    """
    if utils.is_video_file(file_path):
        print(f"Video detected: {file_path}. Extracting audio...")
        temp_audio_path, video_width, video_height = utils.extract_audio_from_video(file_path)

        try:
            sub_file_path = transcribe_to_subtitles(
                model=model,
                beam_size=beam_size,
                audio_path=temp_audio_path,
                style=style,
                output_path=output_folder,
                max_words_per_line=max_words,
                file_name=output_name,
                language=language,
                video_width=video_width,
                video_height=video_height,
            )

            # Si el usuario eligió "mp4" (solo video) o "both" (video + subtítulos)
            if output_format in ("mp4", "both"):
                render_video.render_video(file_path, output_name, sub_file_path, output_folder)

                # Si solo quería el video .mp4, borramos el archivo .srt/.ass intermedio
                if output_format == "mp4" and os.path.exists(sub_file_path):
                    os.remove(sub_file_path)
        finally:
            utils.delete_temporal_files()

    elif utils.is_audio_file(file_path):
        print(f"Audio detected: {file_path}. Transcribing directly...")
        transcribe_to_subtitles(
            model=model,
            beam_size=beam_size,
            audio_path=file_path,
            style=style,
            output_path=output_folder,
            max_words_per_line=max_words,
            file_name=output_name,
            language=language,
            video_width=1920,
            video_height=1080,
        )
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


# =====================================================================
#                        INTERFAZ GRÁFICA (API)
# =====================================================================

class Api:

    def update_status(self, message, color="#a5a9d4"):
        """
        Actualiza el texto de estado en la ventana de la interfaz en tiempo real.
        """
        try:
            if webview.windows:
                safe_msg = json.dumps(message)
                safe_color = json.dumps(color)
                webview.windows[0].evaluate_js(
                    f"updateProgressStatus({safe_msg}, {safe_color})"
                )
        except Exception:
            pass

    def select_input_file(self):
        file_types = (
            "Media files (*.mp4;*.mov;*.mkv;*.avi;*.flv;*.webm;*.mp3;*.aac;*.wav;*.flac)",
            "Video files (*.mp4;*.mov;*.mkv;*.avi;*.flv;*.webm)",
            "Audio files (*.mp3;*.aac;*.wav;*.flac)",
        )
        result = webview.windows[0].create_file_dialog(
            webview.FileDialog.OPEN,
            allow_multiple=False,
            file_types=file_types,
        )
        if result:
            selected_file = result[0]
            base_name = os.path.splitext(os.path.basename(selected_file))[0]
            return {
                "mode": "file",
                "path": selected_file,
                "default_name": base_name,
            }
        return None

    def select_input_folder(self):
        result = webview.windows[0].create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            folder_path = result[0]
            media_files = utils.get_media_files_in_folder(folder_path)
            return {
                "mode": "folder",
                "path": folder_path,
                "count": len(media_files),
            }
        return None

    def select_output_folder(self):
        result = webview.windows[0].create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            return result[0]
        return None

    def get_config(self):
        return config_loader.load_config()

    def get_system_fonts(self):
        return utils.get_system_fonts()

    def save_config(self, cfg):
        try:
            return config_loader.save_config(cfg)
        except Exception as e:
            return f"Error saving config: {str(e)}"

    def receive_form_data(self, data):
        input_path = (data.get("input_path") or "").strip()
        output_folder = (data.get("output_path") or "").strip()
        custom_name = (data.get("output_filename") or "").strip()

        if not input_path:
            return {"ok": False, "message": "Error: Please select an input file or folder."}

        if not os.path.exists(input_path):
            return {"ok": False, "message": "Error: The selected input path does not exist."}

        if not output_folder:
            return {"ok": False, "message": "Error: Please select a destination folder."}

        os.makedirs(output_folder, exist_ok=True)

        try:
            max_words = max(1, int(data.get("words_per_line", 5)))
        except ValueError:
            max_words = 5

        performance = data.get("performance", "normal")
        output_format = data.get("output_format", "mp4").lower()
        language = data.get("language", "auto")
        style = data.get("sub_style", "simple")

        # Determinar lista de archivos a procesar (1 archivo o carpeta entera)
        is_folder_mode = os.path.isdir(input_path)
        if is_folder_mode:
            files_to_process = utils.get_media_files_in_folder(input_path)
            if not files_to_process:
                return {
                    "ok": False,
                    "message": "Error: No video or audio files found in that folder.",
                }
        else:
            if not utils.is_media_file(input_path):
                return {
                    "ok": False,
                    "message": "Error: Selected file is not a valid video or audio file.",
                }
            files_to_process = [input_path]

        # Cargar modelo Whisper una sola vez para todo el proceso
        try:
            self.update_status(f"Loading Whisper ({performance}) model...", "#ffd60a")
            model, beam_size = load_whisper_model(performance)
        except Exception as e:
            return {"ok": False, "message": f"Error loading Whisper model: {str(e)}"}

        total_files = len(files_to_process)

        # Procesar cada archivo
        try:
            for index, file_path in enumerate(files_to_process, start=1):
                original_base = os.path.splitext(os.path.basename(file_path))[0]

                if is_folder_mode:
                    # En modo carpeta: conservar nombre original + sufijo opcional
                    output_name = f"{original_base}{custom_name}" if custom_name else original_base
                else:
                    # En modo archivo individual: usar el nombre escrito o el original
                    output_name = custom_name if custom_name else original_base

                self.update_status(
                    f"Processing ({index}/{total_files}): {os.path.basename(file_path)}...",
                    "#ffd60a"
                )

                process_single_file(
                    file_path=file_path,
                    output_folder=output_folder,
                    output_name=output_name,
                    model=model,
                    beam_size=beam_size,
                    max_words=max_words,
                    style=style,
                    output_format=output_format,
                    language=language,
                )

            if total_files == 1:
                return {"ok": True, "message": "Subtitling completed successfully!"}
            return {
                "ok": True,
                "message": f"Batch completed! {total_files} files processed successfully.",
            }

        except Exception as e:
            print("Critical error during processing:", e)
            return {"ok": False, "message": f"Error: {str(e)}"}


if __name__ == "__main__":
    api = Api()
    webview.create_window(
        title="SubWizard",
        url="gui/gui.html",
        js_api=api,
        width=1120,
        height=820,
        min_size=(920, 680),
        resizable=True,
    )
    webview.start()
