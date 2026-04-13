import os
import subprocess
from .fmpeg_installer import ensure_ffmpeg, ensure_ffprobe
import shutil
from pathlib import Path
import shutil
import tempfile
import uuid
import re
import shlex
import json


def get_video_resolution(video_path):
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

        return height, width

    except Exception as e:
        print("Error al detectar la resolucion", e)
        return 1080, 1920



def create_srt_file(output_path, srt_lines, file_name, extension):


    # Si output_path se especifica y es un directorio → escribir en esa carpeta
    if output_path and os.path.isdir(output_path):
        output_path = os.path.join(output_path, file_name + extension)


    # Si no hay ni video_path ni output_path, usar el directorio actual
    elif not output_path:
        output_path = os.path.join(os.getcwd(), file_name + extension)


    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    return output_path
    

def format_timestamp(seconds: float):
    import math
    milliseconds = int(round(seconds * 1000))
    hours = milliseconds // 3_600_000
    minutes = (milliseconds % 3_600_000) // 60_000
    seconds = (milliseconds % 60_000) // 1000
    ms = milliseconds % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def extract_audio_from_video(video_path, temp_folder="temp_files"):
    """
    Extrae el audio de un archivo de video usando FFmpeg.
    Guarda el archivo en una carpeta temporal dentro del proyecto (donde está ubicado este script).
    """

    width, height = get_video_resolution(video_path=video_path)


    # Ruta base: donde está este archivo (utils.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sub_wizard_dir = os.path.dirname(base_dir)

    # Ruta absoluta de la carpeta temporal
    temp_path = os.path.join(sub_wizard_dir, temp_folder)
    os.makedirs(temp_path, exist_ok=True)

    # Ruta completa del archivo de audio
    audio_filename = "temp_audio.wav"
    audio_path = os.path.join(temp_path, audio_filename)

    # Borrar si ya existe
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # Obtener ruta a ffmpeg
    ffmpeg_path = ensure_ffmpeg()

    # Comando FFmpeg para extraer audio
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
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("error during separation of audio from video")
        
    return audio_path, width, height


def is_video_file(filename):
    video_extensions = ['.mp4', '.mkv', '.mov', '.avi', '.flv', '.webm']
    extension = os.path.splitext(filename)[1].lower()
    if extension in video_extensions:
        return True
    return False


def is_audio_file(filename):
    video_extensions = ['.mp3', '.wav', '.aac', '.flac']
    extension = os.path.splitext(filename)[1].lower()
    if extension in video_extensions:
        return True
    return False


def delete_temporal_files():
    pass


