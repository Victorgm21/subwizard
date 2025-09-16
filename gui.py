import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
from utils import utils
import threading
import sys

class SubWizardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SubWizard - Automatic Subtitler")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_name = tk.StringVar(value="subwizard")
        self.output_path = tk.StringVar()
        self.max_words = tk.IntVar(value=5)
        self.output_type = tk.StringVar(value="srt")
        self.performance = tk.StringVar(value="normal")
        self.lang = tk.StringVar(value="auto")
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TCombobox', font=('Arial', 10))
        
        # Crear widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="SubWizard", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Input File", padding=10)
        input_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        ttk.Label(input_frame, text="Video/Audio:").grid(row=0, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.input_file, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_input).grid(row=0, column=2)
        
        # Sección de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=10)
        config_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        # Fila 1

        #PALABRAS MÁXIMAS POR LINEA ENTRADA

        ttk.Label(config_frame, text="Words per line:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Spinbox(config_frame, from_=1, to=20, textvariable=self.max_words, width=5).grid(row=0, column=1, sticky="w", padx=5)

        # ENTRADA MODO DEL MODELO DE IA
        
        ttk.Label(config_frame, text="Performance:").grid(row=0, column=2, sticky="w", padx=5)
        perf_combo = ttk.Combobox(config_frame, textvariable=self.performance, 
                                values=["efficient", "normal", "detailed", "ultra-detailed"], 
                                state="readonly", width=15)
        perf_combo.grid(row=0, column=3, sticky="w", padx=5)
        
        # Fila 2

        
        # FORMATO DE SALIDA ENTRADA

        ttk.Label(config_frame, text="Output format:").grid(row=1, column=0, sticky="w", padx=5)
        type_combo = ttk.Combobox(config_frame, textvariable=self.output_type, 
                                values=["srt", "mp4"], state="readonly", width=10)
        type_combo.grid(row=1, column=1, sticky="w", padx=5)

        # IDIOMA ENTRADA

        ttk.Label(config_frame, text="Language (optional):").grid(row=1, column=2, sticky="w", padx=5)
        lang_combo = ttk.Combobox(config_frame, 
                                  textvariable=self.lang, 
                                  values=["auto","eng", "esp", "fr", "de", "jp", "kr"], 
                                  state="readonly", 
                                  width=15)
        lang_combo.grid(row=1, column=3, sticky="w", padx=5)
        
        # Sección de salida

        output_frame = ttk.LabelFrame(main_frame, text="Output File", padding=10)
        output_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        ttk.Label(output_frame, text="File name:").grid(row=0, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.output_name, width=20).grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(output_frame, text="Destination folder:").grid(row=1, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.output_path, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=1, column=2)
        
        # Botón de procesar
        process_btn = ttk.Button(main_frame, text="Generate Subtitles", command=self.process)
        process_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        # Etiqueta de estado
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.grid(row=6, column=0, columnspan=3)
        
    def browse_input(self):
        filetypes = (
            ('Media files', '*.mp4 *.mkv *.avi *.mov *.mp3 *.wav *.aac'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        if filename:
            self.input_file.set(filename)
            
            # Establecer nombre de salida por defecto
            base_name = os.path.splitext(os.path.basename(filename))[0]
            self.output_name.set(base_name)
            
            # Si es video, establecer mp4 como formato por defecto
            if utils.is_video_file(filename):
                self.output_type.set("mp4")
            else:
                self.output_type.set("srt")
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select destination folder")
        if folder:
            self.output_path.set(folder)
    
    def process(self):
        # Validar entrada
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file")
            return
            
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "The input file does not exist")
            return
            
        # Configurar barra de progreso
        self.progress["value"] = 0
        self.status_label.config(text="Processing...", foreground="blue")
        self.root.update()
        
        # Obtener parámetros
        params = {
            "video": self.input_file.get(),
            "--output-path": self.output_path.get() if self.output_path.get() else None,
            "--max-words": self.max_words.get(),
            "--performance": self.performance.get(),
            "--output-name": self.output_name.get(),
            "--output-type": self.output_type.get(),
            "--lang": self.lang.get() if self.lang.get() else None,
            "--srt-path": None  # Mantener como None si no se usa en GUI
        }
        
        # Ejecutar en un hilo separado para no bloquear la interfaz
        thread = threading.Thread(target=self.run_subwizard, args=(params,))
        thread.start()
    
    def run_subwizard(self, params):
        try:
            # Simular progreso
            for i in range(10, 110, 10):
                self.progress["value"] = i
                self.root.update()
                self.root.after(100)
            
   

            # Construir comando CLI
            command = ["python", "sub_wizard.py"] 

            # Detectar si estamos corriendo como .exe o .py
            py_path = os.path.join(os.path.dirname(__file__), "sub_wizard.py")


            script_path = sys.argv[0]
            if script_path.endswith('.exe'):
                print("El script se está ejecutando como un archivo .exe")
                print("⚡ Running compiled version (sub_wizard.exe)")
                command = ["sub_wizard.exe"]
            elif script_path.endswith('.py'):
                print("El script se está ejecutando como un archivo .py")
                print("🐍 Running Python version (sub_wizard.py)")
                command = [sys.executable, py_path]
            else:
                print("No se pudo determinar el tipo de archivo")
                

            # Argumento obligatorio (video)
            command.append(params["video"])

            # Argumentos opcionales
            for key, value in params.items():
                if key == "video" or value in [None, ""]:
                    continue
                command.append(key)
                # Solo agregar valor si no es un flag
                if not isinstance(value, bool):
                    command.append(str(value))
            
            print("Executing command:", " ".join(command))

            # Ejecutar el proceso
            result = subprocess.run(command,
                                    capture_output=True, 
                                    text=True,
                                    encoding="utf-8",
                                    errors="replace",
                                    env={**os.environ, "PYTHONUTF8": "1"}  # 👈 aquí forzamos UTF-8
                                     )

            if result.returncode != 0:
                print(result.stderr)
                raise Exception(result.stderr)
                
            
            # Actualizar interfaz
            self.progress["value"] = 100
            self.status_label.config(text="Subtitles generated successfully!", foreground="green")
            messagebox.showinfo("Success", "The process has completed successfully")
            
        except Exception as e:
            self.progress["value"] = 0
            self.status_label.config(text="Processing error", foreground="red")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = SubWizardGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
