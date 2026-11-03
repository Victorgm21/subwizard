import os
import re
import random
import base64
import subprocess
import shutil
import json
from .fmpeg_installer import ensure_ffmpeg, ensure_ffprobe


VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.mov', '.avi', '.flv', '.webm']
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.aac', '.flac']


def get_video_resolution(video_path):
    """
    Obtiene el ancho (width) y alto (height) de un video usando ffprobe.
    """
    try:
        ffprobe_path = ensure_ffprobe()
        cmd = [
            ffprobe_path,
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "json",
            video_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=False
        )

        data = json.loads(result.stdout)
        stream = data["streams"][0]

        width = int(stream["width"])
        height = int(stream["height"])

        return width, height

    except Exception as e:
        print("Error al detectar la resolucion:", e)
        return 1920, 1080


def create_srt_file(output_path, srt_lines, file_name, extension):
    """
    Crea el archivo de subtítulos (.srt o .ass) en la carpeta de destino.
    """
    if output_path and os.path.isdir(output_path):
        full_output_path = os.path.join(output_path, file_name + extension)
    elif not output_path:
        full_output_path = os.path.join(os.getcwd(), file_name + extension)
    else:
        full_output_path = output_path

    with open(full_output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    return full_output_path


def format_timestamp(seconds: float):
    milliseconds = int(round(seconds * 1000))
    hours = milliseconds // 3_600_000
    minutes = (milliseconds % 3_600_000) // 60_000
    seconds = (milliseconds % 60_000) // 1000
    ms = milliseconds % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def get_temp_folder_path(temp_folder="temp_files"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sub_wizard_dir = os.path.dirname(base_dir)
    return os.path.join(sub_wizard_dir, temp_folder)


def extract_audio_from_video(video_path, temp_folder="temp_files"):
    """
    Extrae el audio de un archivo de video usando FFmpeg y devuelve:
    (ruta_audio_temporal, width, height)
    """
    width, height = get_video_resolution(video_path=video_path)

    temp_path = get_temp_folder_path(temp_folder)
    os.makedirs(temp_path, exist_ok=True)

    audio_filename = "temp_audio.wav"
    audio_path = os.path.join(temp_path, audio_filename)

    if os.path.exists(audio_path):
        os.remove(audio_path)

    ffmpeg_path = ensure_ffmpeg()

    command = [
        ffmpeg_path,
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path,
        "-y"
    ]

    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception as e:
        print("Error during separation of audio from video:", e)

    return audio_path, width, height


def is_video_file(filename):
    extension = os.path.splitext(filename)[1].lower()
    return extension in VIDEO_EXTENSIONS


def is_audio_file(filename):
    extension = os.path.splitext(filename)[1].lower()
    return extension in AUDIO_EXTENSIONS


def is_media_file(filename):
    return is_video_file(filename) or is_audio_file(filename)


def get_media_files_in_folder(folder_path):
    """
    Devuelve una lista con todos los archivos de video o audio
    que estén únicamente en esa carpeta (sin entrar en subcarpetas).
    """
    if not os.path.isdir(folder_path):
        return []

    media_files = []
    for entry in sorted(os.listdir(folder_path)):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path) and is_media_file(full_path):
            media_files.append(full_path)

    return media_files


def delete_temporal_files(temp_folder="temp_files"):
    """
    Elimina los archivos temporales generados durante la extracción de audio.
    """
    temp_path = get_temp_folder_path(temp_folder)
    if os.path.exists(temp_path):
        for entry in os.listdir(temp_path):
            file_path = os.path.join(temp_path, entry)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"No se pudo borrar archivo temporal {file_path}: {e}")


def get_system_fonts():
    """
    Obtiene la lista ordenada de fuentes instaladas en el sistema (Windows)
    tanto a nivel de equipo (HKLM) como de usuario (HKCU).
    """
    fonts = set()

    if os.name == "nt":
        import winreg

        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"),
        ]

        for root, path in reg_paths:
            try:
                with winreg.OpenKey(root, path) as key:
                    i = 0
                    while True:
                        try:
                            name, _, _ = winreg.EnumValue(key, i)
                            clean = re.sub(r"\s*\(.*?\).*$", "", name)
                            for part in clean.split("&"):
                                part = re.sub(
                                    r"\s+(Bold|Italic|Regular|Light|Medium|SemiBold|SemiLight|Demibold|Black|Thin)(\s+(Italic|Oblique))?$",
                                    "",
                                    part.strip(),
                                    flags=re.IGNORECASE,
                                )
                                part = part.strip()
                                if part and not part.startswith("@"):
                                    fonts.add(part)
                            i += 1
                        except OSError:
                            break
            except OSError:
                pass

    if not fonts:
        fonts = {"Arial", "Impact", "Montserrat", "Segoe UI", "Tahoma", "Verdana"}

    return sorted(fonts)


def get_video_info(video_path):
    """
    Obtiene (width, height, duration) de un video usando ffprobe.
    """
    width, height = 1920, 1080
    duration = 0.0
    try:
        ffprobe_path = ensure_ffprobe()
        cmd = [
            ffprobe_path,
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration:format=duration",
            "-of", "json",
            video_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        data = json.loads(result.stdout)
        if data.get("streams"):
            stream = data["streams"][0]
            width = int(stream.get("width", 1920))
            height = int(stream.get("height", 1080))
            if stream.get("duration"):
                duration = float(stream["duration"])
        if duration <= 0 and data.get("format", {}).get("duration"):
            duration = float(data["format"]["duration"])
    except Exception as e:
        print("Error reading video info:", e)

    return width, height, duration


def extract_random_frame(input_path):
    """
    Extrae un fotograma aleatorio del video (o del primer video de la carpeta)
    y lo devuelve en base64 junto con su resolución real (width, height).
    """
    video_path = None
    if input_path and os.path.isdir(input_path):
        for f in get_media_files_in_folder(input_path):
            if is_video_file(f):
                video_path = f
                break
    elif input_path and os.path.isfile(input_path) and is_video_file(input_path):
        video_path = input_path

    if not video_path:
        return {"ok": False, "width": 1920, "height": 1080, "data_url": None}

    width, height, duration = get_video_info(video_path)
    seek_time = random.uniform(duration * 0.1, duration * 0.85) if duration > 1.0 else 0.0

    try:
        ffmpeg_path = ensure_ffmpeg()
        cmd = [
            ffmpeg_path,
            "-ss", f"{seek_time:.2f}",
            "-i", video_path,
            "-frames:v", "1",
            "-f", "image2pipe",
            "-vcodec", "mjpeg",
            "-q:v", "4",
            "-",
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
        if res.stdout:
            b64 = base64.b64encode(res.stdout).decode("ascii")
            return {
                "ok": True,
                "width": width,
                "height": height,
                "data_url": f"data:image/jpeg;base64,{b64}",
                "video_name": os.path.basename(video_path),
            }
    except Exception as e:
        print("Error extracting random frame:", e)

    return {"ok": False, "width": width, "height": height, "data_url": None}

