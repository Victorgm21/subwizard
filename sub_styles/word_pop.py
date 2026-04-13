def ass_header(width, height):
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
        "Style: Default,Montserrat,50,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,4,0,2,80,80,100,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        ""
    ]


def ass_word_pop(word, active=False, pop_scale=130):
    """
    Renderiza una palabra. Si está activa, aplica scale up (pop).

    Args:
        word:       Texto de la palabra
        active:     Si es la palabra activa en este momento
        pop_scale:  Porcentaje de escala para la palabra activa (default 130 = 130%)
    """
    if active:
        return f"{{\\fscx{pop_scale}\\fscy{pop_scale}}}{word}{{\\fscx100\\fscy100}}"
    return word


def format_timestamp_ass(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def word_pop_style(words, max_words_per_line, width, height, pop_scale=130):
    """
    Genera subtítulos estilo Word Pop: la palabra activa hace zoom
    mientras el resto de la línea permanece en tamaño normal.

    Args:
        words:              Lista de dicts con keys 'word', 'start', 'end'
        max_words_per_line: Cantidad de palabras por línea
        width:              Ancho del video
        height:             Alto del video
        pop_scale:          Escala de zoom de la palabra activa (default 130%)
    """

    if max_words_per_line < 2:
        max_words_per_line = 2

    ass_lines = []
    ass_lines.extend(ass_header(width, height))

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
                ass_word_pop(w["word"], active=(j == idx), pop_scale=pop_scale)
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