import json
import os
from datetime import datetime


def segments_to_json(segments, output_path, save_to_disk=False):
    """
    Convierte los segments de Faster Whisper en una lista plana de palabras con timestamps.

    Args:
        segments:       Generador de segments devuelto por model.transcribe()
        output_path:    Directorio donde se guardará el JSON si save_to_disk=True
        save_to_disk:   Si True, guarda el archivo JSON en output_path (modo debug)

    Returns:
        dict: Estructura con metadata y lista plana de palabras
    """

    words = []

    for segment in segments:
        for word in segment.words:
            words.append({
                "word":  word.word,
                "start": round(word.start, 3),
                "end":   round(word.end, 3)
            })

    data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_words":  len(words)
        },
        "words": words
    }

    if save_to_disk:
        json_path = os.path.join(output_path, "segments_debug.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[DEBUG] JSON guardado en: {json_path}")

    return data