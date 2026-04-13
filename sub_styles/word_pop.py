from utils.config_loader import get_ass_config


def ass_header(width, height, cfg):
    return [
        "[Script Info]",
        "Title: Word Pop Style Subtitles",
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


def ass_word_pop(word, active=False, cfg=None, pop_scale=130):
    if active:
        highlight = cfg["highlight_color"] if cfg else "&H00E48200&"
        primary   = cfg["primary_color"]   if cfg else "&H00FFFFFF&"
        return (
            f"{{\\fscx{pop_scale}\\fscy{pop_scale}\\c{highlight}}}"
            f"{word}"
            f"{{\\fscx100\\fscy100\\c{primary}}}"
        )
    return word


def format_timestamp_ass(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def word_pop_style(words, max_words_per_line, width, height):

    if max_words_per_line < 2:
        max_words_per_line = 2

    cfg       = get_ass_config("word_pop")
    pop_scale = cfg["style_params"].get("pop_scale", 130)

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
                ass_word_pop(w["word"], active=(j == idx), cfg=cfg, pop_scale=pop_scale)
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