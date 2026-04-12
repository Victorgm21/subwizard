def format_timestamp(seconds: float):
    import math
    milliseconds = int(round(seconds * 1000))
    hours = milliseconds // 3_600_000
    minutes = (milliseconds % 3_600_000) // 60_000
    seconds = (milliseconds % 60_000) // 1000
    ms = milliseconds % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


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
            srt_lines.append(f"{index}\n{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n{text}\n")
            index += 1
            i += max_words_per_line
    # Save remaining words
    if group:
        start = format_timestamp(group[0].start)
        end = format_timestamp(group[-1].end)
        text = " ".join(w.word for w in group)
        srt_lines.append(f"{index}\n{start} --> {end}\n{text}\n")

    return srt_lines