import json
import os

# Ruta del config.json relativa al programa principal
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")

DEFAULT_CONFIG = {
    "font": {
        "family": "Montserrat",
        "size": 80,
        "bold": True,
        "italic": False
    },
    "colors": {
        "text": "#FFFFFF",
        "highlight": "#E48200",
        "outline": "#000000",
        "background": "#000000",
        "background_opacity": 100
    },
    "outline_size": 4,
    "position": {
        "alignment": "bottom_center",
        "offset_y": 50
    },
    "styles": {
        "karaoke": {},
        "word_pop": {
            "pop_scale": 130
        },
        "zoom_in": {
            "anim_duration": 150,
            "start_scale": 25,
            "accel": 3
        }
    }
}

ALIGNMENT_MAP = {
    "top_center":    8,
    "middle_center": 5,
    "bottom_center": 2
}


def hex_to_ass(hex_color: str, opacity: int = 0) -> str:
    """
    Convierte color HEX (#RRGGBB) al formato ASS (&HAABBGGRR&).

    Args:
        hex_color:  Color en formato #RRGGBB
        opacity:    Opacidad en % (0 = totalmente visible, 100 = invisible)

    Returns:
        String en formato ASS &HAABBGGRR&
    """
    hex_color = hex_color.lstrip("#")
    r = hex_color[0:2]
    g = hex_color[2:4]
    b = hex_color[4:6]
    alpha = int((opacity / 100) * 255)
    aa = f"{alpha:02X}"
    return f"&H{aa}{b}{g}{r}&"


def load_config() -> dict:
    """
    Carga el config.json desde la raíz del programa.
    Si no existe, lo genera con los valores por defecto.

    Returns:
        dict con la configuración lista para usar
    """
    if not os.path.exists(CONFIG_PATH):
        print("[CONFIG] config.json no encontrado, generando con valores por defecto...")
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config


def get_ass_config(style: str = None) -> dict:
    """
    Carga la config y devuelve los valores ya convertidos al formato ASS,
    listos para usar directamente en los archivos de estilo.

    Args:
        style:  Nombre del estilo ('karaoke', 'word_pop', 'zoom_in') para
                incluir sus parámetros específicos. None para config general.

    Returns:
        dict con todos los valores procesados
    """
    config = load_config()

    primary_color   = hex_to_ass(config["colors"]["text"])
    highlight_color = hex_to_ass(config["colors"]["highlight"])
    outline_color   = hex_to_ass(config["colors"]["outline"])
    back_color      = hex_to_ass(
        config["colors"]["background"],
        opacity=config["colors"].get("background_opacity", 100)
    )

    alignment = ALIGNMENT_MAP.get(config["position"]["alignment"], 2)
    margin_v  = config["position"]["offset_y"]

    bold   = 1 if config["font"]["bold"]   else 0
    italic = 1 if config["font"]["italic"] else 0

    ass_config = {
        "font_family":      config["font"]["family"],
        "font_size":        config["font"]["size"],
        "bold":             bold,
        "italic":           italic,
        "primary_color":    primary_color,
        "highlight_color":  highlight_color,
        "outline_color":    outline_color,
        "back_color":       back_color,
        "outline_size":     config["outline_size"],
        "alignment":        alignment,
        "margin_v":         margin_v,
    }

    # Agrega parametros especificos del estilo si se solicita
    if style and style in config.get("styles", {}):
        ass_config["style_params"] = config["styles"][style]
    else:
        ass_config["style_params"] = {}

    return ass_config