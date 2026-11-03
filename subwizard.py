# Standard library
import os
import re
import json
import warnings
import subprocess

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
    vad_filter=True,
):
    """
    Transcribe un archivo de audio usando el modelo ya cargado y genera
    el archivo de subtítulos (.srt o .ass) según el estilo elegido.
    """
    cfg = config_loader.load_config()
    font_cfg = cfg.get("font", {})
    use_uppercase = bool(font_cfg.get("uppercase", False))
    remove_punct = bool(font_cfg.get("remove_punctuation", False))
    banned_set = {
        str(bw).strip().lower()
        for bw in cfg.get("banned_words", [])
        if str(bw).strip()
    }

    print(f"Generating transcription for: {os.path.basename(audio_path)}")

    transcribe_kwargs = {
        "beam_size": beam_size,
        "word_timestamps": True,
        "vad_filter": bool(vad_filter),
    }
    if language and language != "auto":
        transcribe_kwargs["language"] = language

    segments, _info = model.transcribe(audio_path, **transcribe_kwargs)

    segments = list(segments)
    word_data = segments_to_json.segments_to_json(segments, output_path, save_to_disk=False)
    words = word_data["words"]

    # Aplicar censura de palabras baneadas y formato de texto (puntuación / mayúsculas)
    censored_intervals = []
    if banned_set or remove_punct or use_uppercase:
        formatted_words = []
        for w in words:
            text = w["word"].strip()
            clean_word = re.sub(r"^[^\w]+|[^\w]+$", "", text, flags=re.UNICODE).lower()
            if banned_set and clean_word in banned_set:
                text = re.sub(r"\w", "*", text, flags=re.UNICODE)
                censored_intervals.append((w["start"], w["end"]))
            if remove_punct:
                text = re.sub(r"[.,!?;:¡¿\"“”«»()\[\]{}…]+", "", text).strip()
            if use_uppercase:
                text = text.upper()
            if text:
                formatted_words.append({
                    "word": text,
                    "start": w["start"],
                    "end": w["end"],
                })
        words = formatted_words

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

    return subtitles_path, censored_intervals


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
    vad_filter=True,
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
            sub_file_path, censored_intervals = transcribe_to_subtitles(
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
                vad_filter=vad_filter,
            )

            # Si el usuario eligió "mp4" (solo video) o "both" (video + subtítulos)
            if output_format in ("mp4", "both"):
                cfg = config_loader.load_config()
                audio_censor_cfg = cfg.get("banned_audio", {})
                beep_enabled = bool(audio_censor_cfg.get("enabled", True))
                beep_volume = float(audio_censor_cfg.get("volume", 35))

                render_video.render_video(
                    file_path,
                    output_name,
                    sub_file_path,
                    output_folder,
                    censored_intervals=censored_intervals,
                    beep_enabled=beep_enabled,
                    beep_volume=beep_volume,
                )

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
            vad_filter=vad_filter,
        )
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


# =====================================================================
#                        INTERFAZ GRÁFICA (API)
# =====================================================================

class Api:

    def __init__(self):
        self._preview_window = None
        self._preview_input_path = ""
        self._preview_cfg = None
        self._preview_style = "simple"
        self._preview_words_per_line = 5

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
                "folder": os.path.dirname(selected_file),
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
                "folder": folder_path,
                "count": len(media_files),
            }
        return None

    def select_output_folder(self):
        result = webview.windows[0].create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            return result[0]
        return None

    def get_installed_models(self):
        """
        Devuelve la lista de modelos de Whisper guardados en la caché de Hugging Face.
        """
        hub_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
        if not os.path.isdir(hub_dir):
            return []

        model_friendly_names = {
            "models--systran--faster-whisper-tiny": "Tiny (Very fast)",
            "models--systran--faster-whisper-tiny.en": "Tiny English",
            "models--systran--faster-whisper-base": "Base (Efficient)",
            "models--systran--faster-whisper-base.en": "Base English",
            "models--systran--faster-whisper-small": "Small (Normal)",
            "models--systran--faster-whisper-small.en": "Small English",
            "models--systran--faster-whisper-medium": "Medium (Detailed)",
            "models--systran--faster-whisper-medium.en": "Medium English",
            "models--systran--faster-whisper-large-v1": "Large v1 (Ultra-detailed)",
            "models--systran--faster-whisper-large-v2": "Large v2 (Ultra-detailed)",
            "models--systran--faster-whisper-large-v3": "Large v3 (Ultra-detailed)",
            "models--systran--faster-whisper-large-v3-turbo": "Large v3 Turbo",
        }

        models = []
        try:
            for item in sorted(os.listdir(hub_dir)):
                if "whisper" in item.lower():
                    full_path = os.path.join(hub_dir, item)
                    if os.path.isdir(full_path):
                        total_bytes = 0
                        for root, _, files in os.walk(full_path):
                            for f in files:
                                fp = os.path.join(root, f)
                                if os.path.isfile(fp):
                                    total_bytes += os.path.getsize(fp)
                        size_mb = total_bytes / (1024 * 1024)
                        size_str = (
                            f"{size_mb / 1024:.2f} GB"
                            if size_mb >= 1000
                            else f"{size_mb:.1f} MB"
                        )
                        friendly = model_friendly_names.get(
                            item.lower(),
                            item.replace("models--Systran--", "").replace("models--", ""),
                        )
                        models.append({
                            "id": item,
                            "name": friendly,
                            "folder": item,
                            "size_bytes": total_bytes,
                            "size_str": size_str,
                            "path": full_path,
                        })
        except Exception as e:
            print("Error listing whisper models:", e)
        return models

    def delete_installed_model(self, model_id):
        """
        Elimina la carpeta de un modelo de Whisper para liberar espacio en disco.
        """
        hub_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
        target_dir = os.path.abspath(os.path.join(hub_dir, model_id))
        if not target_dir.startswith(os.path.abspath(hub_dir)):
            return {"ok": False, "message": "Invalid model directory path."}
        if not os.path.isdir(target_dir):
            return {"ok": False, "message": "Model directory not found."}
        try:
            shutil.rmtree(target_dir, ignore_errors=False)
            return {"ok": True, "message": "Model deleted successfully!"}
        except Exception as e:
            return {"ok": False, "message": f"Could not delete model: {str(e)}"}

    def open_models_cache_folder(self):
        hub_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
        os.makedirs(hub_dir, exist_ok=True)
        try:
            if os.name == "nt":
                os.startfile(hub_dir)
            else:
                subprocess.Popen(["xdg-open", hub_dir])
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def open_output_folder(self, folder_path):
        folder_path = (folder_path or "").strip()
        if not folder_path or not os.path.isdir(folder_path):
            return {"ok": False, "message": "Destination folder does not exist yet."}
        try:
            if os.name == "nt":
                os.startfile(folder_path)
            else:
                subprocess.Popen(["xdg-open", folder_path])
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def get_preview_frame(self, input_path):
        return utils.extract_random_frame((input_path or "").strip())

    def get_initial_preview_data(self):
        cfg = self._preview_cfg or config_loader.load_config()
        frame = utils.extract_random_frame(self._preview_input_path)
        return {
            "cfg": cfg,
            "input_path": self._preview_input_path,
            "sub_style": self._preview_style,
            "words_per_line": self._preview_words_per_line,
            "frame": frame,
        }

    def get_live_preview_state(self):
        return {
            "cfg": self._preview_cfg or config_loader.load_config(),
            "input_path": self._preview_input_path,
            "sub_style": self._preview_style,
            "words_per_line": self._preview_words_per_line,
        }

    def set_preview_style(self, style):
        self._preview_style = style or "simple"
        try:
            if webview.windows:
                safe_style = json.dumps(self._preview_style)
                webview.windows[0].evaluate_js(
                    f"document.getElementById('select-sub-style').value = {safe_style};"
                )
        except Exception:
            pass
        return {"ok": True}

    def open_preview_window(self, state=None):
        state = state or {}
        self._preview_input_path = (state.get("input_path") or "").strip()
        if state.get("sub_style"):
            self._preview_style = state["sub_style"]
        if state.get("words_per_line"):
            try:
                self._preview_words_per_line = max(1, int(state["words_per_line"]))
            except ValueError:
                pass
        if state.get("cfg"):
            self._preview_cfg = state["cfg"]
        elif not self._preview_cfg:
            self._preview_cfg = config_loader.load_config()

        if self._preview_window and self._preview_window in webview.windows:
            try:
                frame = utils.extract_random_frame(self._preview_input_path)
                payload = json.dumps({
                    "cfg": self._preview_cfg,
                    "input_path": self._preview_input_path,
                    "sub_style": self._preview_style,
                    "words_per_line": self._preview_words_per_line,
                })
                frame_json = json.dumps(frame)
                self._preview_window.evaluate_js(
                    f"window.receivePreviewUpdate && window.receivePreviewUpdate({payload}, {frame_json})"
                )
                return {"ok": True}
            except Exception:
                self._preview_window = None

        preview_url = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "gui", "preview.html"
        )
        self._preview_window = webview.create_window(
            title="SubWizard — Live Preview",
            url=preview_url,
            js_api=self,
            width=960,
            height=640,
            min_size=(680, 460),
            resizable=True,
            background_color="#141416",
        )
        return {"ok": True}

    def sync_preview_state(self, state=None):
        state = state or {}
        new_input = (state.get("input_path") or "").strip()
        input_changed = new_input != self._preview_input_path
        self._preview_input_path = new_input
        if state.get("sub_style"):
            self._preview_style = state["sub_style"]
        if state.get("words_per_line"):
            try:
                self._preview_words_per_line = max(1, int(state["words_per_line"]))
            except ValueError:
                pass
        if state.get("cfg"):
            self._preview_cfg = state["cfg"]

        if self._preview_window and self._preview_window in webview.windows:
            try:
                payload = json.dumps({
                    "cfg": self._preview_cfg,
                    "input_path": self._preview_input_path,
                    "sub_style": self._preview_style,
                    "words_per_line": self._preview_words_per_line,
                })
                if input_changed:
                    frame = utils.extract_random_frame(self._preview_input_path)
                    frame_json = json.dumps(frame)
                    self._preview_window.evaluate_js(
                        f"window.receivePreviewUpdate && window.receivePreviewUpdate({payload}, {frame_json})"
                    )
                else:
                    self._preview_window.evaluate_js(
                        f"window.receivePreviewUpdate && window.receivePreviewUpdate({payload})"
                    )
            except Exception:
                pass
        return {"ok": True}

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
        vad_filter = bool(data.get("vad_filter", True))

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
                    vad_filter=vad_filter,
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
        title="SubWizard — No Cloud • No Subscriptions • Lightweight • All-in-One",
        url="gui/gui.html",
        js_api=api,
        width=1260,
        height=840,
        min_size=(960, 680),
        resizable=True,
    )
    webview.start()
