from utils.config_loader import get_ass_config


def ass_header(width, height, cfg):
    return [
        "[Script Info]",
        "Title: Zoom In Style Subtitles",
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


def format_timestamp_ass(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def zoom_in_style(words, max_words_per_line, width, height):

    if max_words_per_line < 1:
        max_words_per_line = 1

    cfg           = get_ass_config("zoom_in")
    anim_duration = cfg["style_params"].get("anim_duration", 90)
    start_scale   = cfg["style_params"].get("start_scale", 25)
    accel         = cfg["style_params"].get("accel", 5)

    ass_lines = []
    ass_lines.extend(ass_header(width, height, cfg))

    i = 0
    while i < len(words):
        group = words[i:i + max_words_per_line]

        start_time = group[0]["start"]

        if i + max_words_per_line < len(words):
            end_time = words[i + max_words_per_line]["start"]
        else:
            end_time = group[-1]["end"]

        text = " ".join(w["word"] for w in group)

        animated_text = (
            f"{{\\fscx{start_scale}\\fscy{start_scale}\\alpha&HFF&"
            f"\\t(0,{anim_duration},{accel},\\fscx100\\fscy100\\alpha&H00&)}}{text}"
        )

        ass_lines.append(
            f"Dialogue: 0,"
            f"{format_timestamp_ass(start_time)},"
            f"{format_timestamp_ass(end_time)},"
            f"Default,,0,0,0,,"
            f"{animated_text}"
        )

        i += max_words_per_line

    return ass_lines