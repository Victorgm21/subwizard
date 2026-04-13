def ass_header(width, height):
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
        "Style: Default,Montserrat,50,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,4,0,2,80,80,100,1",
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


def zoom_in_style(words, max_words_per_line, width, height, anim_duration=150, start_scale=25, accel=3):
    """
    Genera subtítulos donde cada grupo de palabras aparece con un zoom suave
    de entrada con curva cúbica de salida (empieza rápido, termina lento).

    Args:
        words:              Lista de dicts con keys 'word', 'start', 'end'
        max_words_per_line: Cantidad de palabras por línea
        width:              Ancho del video
        height:             Alto del video
        anim_duration:      Duración de la animación de entrada en ms (default 180ms)
        start_scale:        Escala inicial del zoom en % (default 40%)
        accel:              Aceleración de la curva: >1 = ease out (default 3)
    """

    if max_words_per_line < 1:
        max_words_per_line = 1

    ass_lines = []
    ass_lines.extend(ass_header(width, height))

    i = 0
    while i < len(words):
        group = words[i:i + max_words_per_line]

        start_time = group[0]["start"]

        if i + max_words_per_line < len(words):
            end_time = words[i + max_words_per_line]["start"]
        else:
            end_time = group[-1]["end"]

        text = " ".join(w["word"] for w in group)

        # Estado inicial: pequeño y transparente
        # \t() anima hacia tamaño normal y opaco con curva de aceleración
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