from .utils import is_video_file
import os
import subprocess
from .fmpeg_installer import ensure_ffmpeg
import shutil
from pathlib import Path
import shutil
import tempfile
import uuid
import re
import shlex


def _find_ffmpeg_executable(ffmpeg_path):
    """
    Acepta:
      - ruta al ejecutable ("/usr/bin/ffmpeg" o "C:\\path\\ffmpeg.exe")
      - o directorio que contiene el ejecutable
      - o nombre simple "ffmpeg" (se asume que está en PATH)
    Devuelve ruta al ejecutable o lanza FileNotFoundError.
    """
    if not ffmpeg_path:
        raise FileNotFoundError("ensure_ffmpeg() returned empty/None")

    if os.path.isdir(ffmpeg_path):
        candidates = ["ffmpeg.exe" if os.name == "nt" else "ffmpeg"]
        for c in candidates:
            p = os.path.join(ffmpeg_path, c)
            if os.path.isfile(p) and os.access(p, os.X_OK):
                return p
        raise FileNotFoundError(f"ffmpeg executable not found inside directory: {ffmpeg_path}")

    return ffmpeg_path


def burn_subtitles_into_video(new_video_name, video_path, srt_path, output_path=None):
    """
    Quema (burn) un .srt dentro del video usando ffmpeg.
    Devuelve la ruta del vídeo generado.
    Requisitos: función ensure_ffmpeg() existente que devuelva la ruta de ffmpeg.
    """
    # --- Obtener ffmpeg ---
    ffmpeg_path = ensure_ffmpeg()
    ffmpeg_exec = _find_ffmpeg_executable(ffmpeg_path)

    # --- Validaciones ---
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")
    if not os.path.isfile(srt_path):
        raise FileNotFoundError(f"Subtitle file not found: {srt_path}")

    # --- Construir ruta de salida ---
    if output_path:
        if os.path.isdir(output_path) or output_path.endswith(os.sep) or os.path.splitext(output_path)[1] == "":
            os.makedirs(output_path, exist_ok=True)
            video_output_path = os.path.join(output_path, f"{new_video_name}.mp4")
        else:
            video_output_path = output_path
    else:
        video_output_path = f"{new_video_name}.mp4"

    print("VIDEO SALIDA:", video_output_path)
    print("VIDEO ORIGINAL:", video_path)

    # --- Crear copia temporal del .srt ---
    temp_dir = tempfile.gettempdir()
    srt_temp_file_name = f"sub_{uuid.uuid4().hex}.srt"
    srt_temp_path = os.path.join(temp_dir, srt_temp_file_name)
    shutil.copy2(srt_path, srt_temp_path)

    # --- Preparar filtro subtitles ---
    abs_srt = os.path.abspath(srt_temp_path).replace("\\", "/")
    if os.name == "nt" and re.match(r"^[A-Za-z]:", abs_srt):
        # Escapar el ":" después de la letra de unidad (C: -> C\:)
        abs_srt = abs_srt[0] + r"\:" + abs_srt[2:]
        vf_arg = f"subtitles='{abs_srt}'"
    else:
        vf_arg = f"subtitles={shlex.quote(abs_srt)}"

    # --- Comando ffmpeg ---
    cmd = [
        ffmpeg_exec,
        "-y",
        "-i", video_path,
        "-vf", vf_arg,
        "-c:a", "copy",
        video_output_path
    ]

    try:
        print("COMANDO A EJECUTAR:", " ".join(shlex.quote(x) for x in cmd))
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffmpeg falló con código {e.returncode}") from e
    finally:
        try:
            if os.path.exists(srt_temp_path):
                os.remove(srt_temp_path)
        except Exception:
            pass

    print("Video generado correctamente:", video_output_path)
    return video_output_path


def render_video(video_path, video_name, srt_file_path, output_path):
    if is_video_file(video_path):
        try:
            burn_subtitles_into_video(video_name, video_path, srt_file_path, output_path)
        except Exception as e:
            print(f"error: {e}")
        finally:
            pass
    else:
        print("invalid video file")