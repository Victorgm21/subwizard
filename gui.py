import webview
import os
import sys
import subprocess
import json


CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

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


class Api:

    def test_connection(self):
        print("Python recibió la llamada desde HTML")
        return "Conexión OK"

    def select_input_file(self):
        file_types = ('Video files (*.mp4;*.mov;*.mkv)', 'Audio files (*.mp3;*.aac;*.wav)')
        result = webview.windows[0].create_file_dialog(
            webview.FileDialog.OPEN,
            allow_multiple=False,
            file_types=file_types,
        )
        if result:
            return result[0]
        return None

    def select_output_folder(self):
        result = webview.windows[0].create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            return result[0]
        return None

    def get_config(self):
        if not os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
            return DEFAULT_CONFIG

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_config(self, cfg):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
            return "Settings saved successfully"
        except Exception as e:
            return f"Error saving config: {str(e)}"

    def receive_form_data(self, data):
        if not data["input_path"]:
            return "Error: No input video"

        if not data["output_path"]:
            return "Error: No folder output"

        # -------------------------
        # Detectar modo ejecución
        # -------------------------
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        py_path = os.path.join(base_path, "subwizard.py")
        script_path = sys.argv[0]

        if script_path.endswith(".exe"):
            command = ["subwizard.exe"]
        else:
            command = [sys.executable, py_path]

        # Construcción del comando
        command.extend([
            data["input_path"],
            "--max-words", str(data["words_per_line"]),
            "--performance", data["performance"],
            "--output-name", data["output_filename"],
            "--output-path", data["output_path"],
            "--output-type", data["output_format"],
            "--style", data["sub_style"],
        ])

        if data["language"] and data["language"] != "auto":
            command.extend(["--lang", data["language"]])

        printable_cmd = " ".join(
            f'"{c}"' if " " in c else c for c in command
        )
        print("\nComando generado:")
        print(printable_cmd)

        # -------------------------
        # Ejecutar
        # -------------------------
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=False
            )

            if result.returncode != 0:
                print("STDERR:")
                print(result.stderr)
                return f"Error:\n{result.stderr}"

            print("STDOUT:")
            print(result.stdout)
            return "Subtitling completed successfully"

        except Exception as e:
            return f"Critical error: {str(e)}"


if __name__ == "__main__":
    api = Api()
    webview.create_window(
        title="subwizard",
        url="gui/gui.html",
        js_api=api,
        width=600,
        height=800,
        resizable=False,
    )
    webview.start()