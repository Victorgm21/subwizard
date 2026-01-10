import webview
import os
import sys
import subprocess
import sys


class Api:
    def test_connection(self):
        print("Python recibió la llamada desde HTML")
        return "Conexión OK"
    
    def select_input_file(self):
       file_types = file_types = ('Video files (*.mp4;*.mov;*.mkv)', 'Audio files (*.mp3;*.aac;*.wav)')

       result = webview.windows[0].create_file_dialog(
          webview.FileDialog.OPEN,
          allow_multiple= False,
          file_types = file_types,
       )

       if result:
          return result[0]
       return None;


    def select_output_folder(self):
       result = webview.windows[0].create_file_dialog(
          webview.FileDialog.FOLDER)
       if result:
          return result[0]
       return None


    def receive_form_data(self, data):
        if not data["input_path"]:
            return "Error: No input video"

        if not data["output_path"]:
            return "Error: No Folder output"
        

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
        # Idioma opcional
        if data["language"] and data["language"] != "auto":
            command.extend(["--lang", data["language"]])

        # Debug visual
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
     resizable= False,
  )

  webview.start()
