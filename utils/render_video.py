import os
import subprocess
import shutil
import tempfile
import uuid
import re
import shlex
from .utils import is_video_file
from .fmpeg_installer import ensure_ffmpeg


def _find_ffmpeg_executable(ffmpeg_path):
    """
    Devuelve la ruta al ejecutable de ffmpeg o lanza FileNotFoundError.
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


def _merge_intervals(intervals, pad=0.02):
    """
    Fusiona intervalos de tiempo superpuestos o muy cercanos para construir
    una expresión compacta de censura de audio en FFmpeg.
    """
    if not intervals:
        return []
    padded = sorted(
        (max(0.0, float(s) - pad), max(0.0, float(e) + pad))
        for s, e in intervals
        if float(e) > float(s)
    )
    if not padded:
        return []
    merged = [padded[0]]
    for s, e in padded[1:]:
        prev_s, prev_e = merged[-1]
        if s <= prev_e + 0.03:
            merged[-1] = (prev_s, max(prev_e, e))
        else:
            merged.append((s, e))
    return merged


def burn_subtitles_into_video(
    new_video_name,
    video_path,
    srt_path,
    output_path=None,
    censored_intervals=None,
    beep_enabled=True,
    beep_volume=35,
):
    """
    Quema (burn) un archivo de subtítulos (.srt o .ass) dentro del video usando ffmpeg,
    y opcionalmente aplica un pitido suave sobre las palabras baneadas.
    Devuelve la ruta del vídeo generado.
    """
    ffmpeg_path = ensure_ffmpeg()
    ffmpeg_exec = _find_ffmpeg_executable(ffmpeg_path)

    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")
    if not os.path.isfile(srt_path):
        raise FileNotFoundError(f"Subtitle file not found: {srt_path}")

    # Construir ruta de salida
    if output_path:
        if os.path.isdir(output_path) or output_path.endswith(os.sep) or os.path.splitext(output_path)[1] == "":
            os.makedirs(output_path, exist_ok=True)
            video_output_path = os.path.join(output_path, f"{new_video_name}.mp4")
        else:
            video_output_path = output_path
    else:
        video_output_path = f"{new_video_name}.mp4"

    # Evitar que el archivo de salida sobrescriba al archivo de entrada mientras ffmpeg lo lee
    if os.path.abspath(video_output_path) == os.path.abspath(video_path):
        base, ext = os.path.splitext(video_output_path)
        video_output_path = f"{base}_sub{ext}"

    print("VIDEO SALIDA:", video_output_path)
    print("VIDEO ORIGINAL:", video_path)

    # Crear copia temporal del subtítulo conservando su extensión (.srt o .ass)
    temp_dir = tempfile.gettempdir()
    sub_ext = os.path.splitext(srt_path)[1].lower() or ".srt"
    srt_temp_file_name = f"sub_{uuid.uuid4().hex}{sub_ext}"
    srt_temp_path = os.path.join(temp_dir, srt_temp_file_name)
    shutil.copy2(srt_path, srt_temp_path)

    # Preparar filtro subtitles para ffmpeg
    abs_srt = os.path.abspath(srt_temp_path).replace("\\", "/")
    if os.name == "nt" and re.match(r"^[A-Za-z]:", abs_srt):
        # Escapar el ":" después de la letra de unidad (C: -> C\:)
        abs_srt = abs_srt[0] + r"\:" + abs_srt[2:]
        vf_arg = f"subtitles='{abs_srt}'"
    else:
        vf_arg = f"subtitles={shlex.quote(abs_srt)}"

    merged_censor = _merge_intervals(censored_intervals) if beep_enabled else []

    if merged_censor:
        cond = "+".join(f"between(t,{s:.3f},{e:.3f})" for s, e in merged_censor)
        vol_pct = max(0.0, min(100.0, float(beep_volume)))

        if vol_pct <= 0.0:
            # Solo silenciar las palabras baneadas sin pitido
            cmd = [
                ffmpeg_exec,
                "-y",
                "-i", video_path,
                "-vf", vf_arg,
                "-af", f"volume=0:enable='{cond}'",
                "-c:a", "aac",
                "-b:a", "192k",
                video_output_path,
            ]
        else:
            # Silenciar voz original y mezclar pitido suave (750Hz filtrado)
            gain = (vol_pct / 100.0) * 1.8
            filter_complex = (
                f"[0:a]volume=0:enable='{cond}'[a_clean];"
                f"sine=frequency=750,lowpass=f=1200,volume=0:enable='not({cond})',volume={gain:.3f}[beep];"
                f"[a_clean][beep]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
            )
            cmd = [
                ffmpeg_exec,
                "-y",
                "-i", video_path,
                "-vf", vf_arg,
                "-filter_complex", filter_complex,
                "-map", "0:v:0",
                "-map", "[aout]",
                "-c:a", "aac",
                "-b:a", "192k",
                video_output_path,
            ]
    else:
        cmd = [
            ffmpeg_exec,
            "-y",
            "-i", video_path,
            "-vf", vf_arg,
            "-c:a", "copy",
            video_output_path,
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


def render_video(
    video_path,
    video_name,
    srt_file_path,
    output_path,
    censored_intervals=None,
    beep_enabled=True,
    beep_volume=35,
):
    if not is_video_file(video_path):
        raise ValueError("Invalid video file")

    return burn_subtitles_into_video(
        video_name,
        video_path,
        srt_file_path,
        output_path,
        censored_intervals=censored_intervals,
        beep_enabled=beep_enabled,
        beep_volume=beep_volume,
    )
