from utils import config_loader




def ass_header(width, height, cfg):
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
        f"Style: Default,"
        f"{cfg['font_family']},"
        f"{cfg['font_size']},"
        f"{cfg['primary_color']},"
        f"{cfg['highlight_color']},"
        f"{cfg['outline_color']},"
        f"{cfg['back_color']},"
        f"{cfg['bold']},"
        f"{cfg['italic']},"
        f"0,0,100,100,0,0,1,"
        f"{cfg['outline_size']},"
        f"0,"
        f"{cfg['alignment']},"
        f"80,80,"
        f"{cfg['margin_v']},"
        f"1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        ""
    ]


def ass_word(word, active=False, cfg=None):
    if active:
        primary   = cfg["primary_color"]   if cfg else "&H00FFFFFF&"
        highlight = cfg["highlight_color"] if cfg else "&H00E48200&"
        return f"{{\\c{highlight}}}{word}{{\\c{primary}}}"
    return word


def format_timestamp_ass(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def karaoke_style(words, max_words_per_line, width, height):

    if max_words_per_line < 2:
        max_words_per_line = 2

    cfg = config_loader.get_ass_config("karaoke")

    ass_lines = []
    ass_lines.extend(ass_header(width, height, cfg))

    i = 0
    while i < len(words):
        group = words[i:i + max_words_per_line]

        if i + max_words_per_line < len(words):
            group_end_time = words[i + max_words_per_line]["start"]
        else:
            group_end_time = group[-1]["end"]

        for idx, word in enumerate(group):
            start_time = word["start"]

            if idx + 1 < len(group):
                end_time = group[idx + 1]["start"]
            else:
                end_time = group_end_time

            rendered_words = [
                ass_word(w["word"], j == idx, cfg)
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

        i += max_words_per_line

    return ass_lines