# Local
from utils import utils
import os

def render_video(video_path, video_name, srt_file_path, output_path):
    if utils.is_video_file(video_path):
        try:
            utils.burn_subtitles_into_video(video_name, video_path, srt_file_path, output_path)
        except Exception as e:
            print(f"error: {e}")
        finally:
            pass
    else:
        print("invalid video file")


def sort_in_srt(segments, max_words_per_line):

    srt_lines = []
    group = []
    index = 1
    for segment in segments:
        words = segment.words
        i = 0

        while i < len(words):
            group = words[i:i+max_words_per_line]
            start_time = group[0].start
            if i + max_words_per_line < len(words):
                end_time = words[i + max_words_per_line].start
            else:
                end_time = group[-1].end

            text = " ".join(w.word for w in group)
            srt_lines.append(f"{index}\n{utils.format_timestamp(start_time)} --> {utils.format_timestamp(end_time)}\n{text}\n")
            index += 1
            i += max_words_per_line
    # Save remaining words
    if group:
        start = utils.format_timestamp(group[0].start)
        end = utils.format_timestamp(group[-1].end)
        text = " ".join(w.word for w in group)
        srt_lines.append(f"{index}\n{start} --> {end}\n{text}\n")

    return srt_lines


#
#
# FUNCIONES PARA EL ESTILO KARAOKE
#
#

def ass_header(width, height):
    return [
        "[Script Info]",
        "Title: Karaoke Style Subtitles",
        "ScriptType: v4.00+",
        f"PlayResX: {height}",
        f"PlayResY: {width}",
        "WrapStyle: 2",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,Montserrat,96,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,4,0,2,80,80,220,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        ""
    ]


def ass_word(word, active=False):
    if active:
        # morado → blanco
        return f"{{\\c&H00FF00FF&}}{word}{{\\c&H00FFFFFF&}}"
    return word



def format_timestamp_ass(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"



def karaoke_style(segments, max_words_per_line, width, height):

    # palabras minimas por linea
    if max_words_per_line < 2:
        max_words_per_line = 2
    ass_lines = []
    ass_lines.extend(ass_header(width, height))

    for segment in segments:
        words = segment.words
        i = 0

        while i < len(words):
            # 🔒 BLOQUE FIJO
            group = words[i:i + max_words_per_line]

            # fin del bloque
            if i + max_words_per_line < len(words):
                group_end_time = words[i + max_words_per_line].start
            else:
                group_end_time = group[-1].end

            for idx, word in enumerate(group):
                start_time = word.start

                # ⏱️ timing exacto
                if idx + 1 < len(group):
                    end_time = group[idx + 1].start
                else:
                    end_time = group_end_time

                rendered_words = [
                    ass_word(w.word, j == idx)
                    for j, w in enumerate(group)
                ]

                text = " ".join(rendered_words)

                ass_lines.append(
                    f"Dialogue: 0,"
                    f"{format_timestamp_ass(start_time)},"
                    f"{format_timestamp_ass(end_time)},"
                    f"Default,,0,0,0,,"
                    f"{text}"
                )

            i += max_words_per_line  # ⬅️ CLAVE

    return ass_lines


