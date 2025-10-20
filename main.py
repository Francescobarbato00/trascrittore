import customtkinter as ctk
from tkinter import filedialog, messagebox, PhotoImage
from moviepy.editor import VideoFileClip
import threading
import whisper
import os
import subprocess
import pyperclip
import time
import math


# =============================
#  SOFTWARE ING. FRANCESCO BARBATO
# =============================

class SplashScreen(ctk.CTkToplevel):
    """Splash screen con logo e fade animato"""
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("600x360+600+300")
        self.overrideredirect(True)
        self.configure(fg_color="#111")
        self.attributes("-alpha", 0.0)
        self.attributes("-topmost", True)

        try:
            icon_path = os.path.join(os.path.dirname(__file__), "icona", "icona.ico")
            if os.path.exists(icon_path):
                self.icon_image = PhotoImage(file=icon_path)
                ctk.CTkLabel(self, image=self.icon_image, text="").pack(pady=(40, 10))
        except Exception:
            ctk.CTkLabel(self, text="🎧", font=("Titillium Web", 55)).pack(pady=(40, 10))

        ctk.CTkLabel(self, text="ING. Francesco Barbato",
                     font=("Titillium Web", 22, "bold"),
                     text_color="#00B472").pack()
        ctk.CTkLabel(self, text="Software di Trascrizione Audio & Video",
                     font=("Titillium Web", 16, "italic"), text_color="#bbb").pack(pady=(5, 20))

        self.progress = ctk.CTkProgressBar(self, width=320)
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.alpha = 0
        self.progress_value = 0

        self.after(30, self.fade_in)

    def fade_in(self):
        """Fade in splash"""
        if self.alpha < 1:
            self.alpha += 0.05
            self.attributes("-alpha", self.alpha)
            self.after(50, self.fade_in)
        else:
            self.animate_progress()

    def animate_progress(self):
        """Animazione barra splash"""
        if self.progress_value < 100:
            self.progress_value += 2
            self.progress.set(self.progress_value / 100)
            self.after(40, self.animate_progress)
        else:
            self.after(400, self.fade_out)

    def fade_out(self):
        """Fade out splash"""
        if self.alpha > 0:
            self.alpha -= 0.05
            self.attributes("-alpha", self.alpha)
            self.after(40, self.fade_out)
        else:
            self.destroy()


class VideoAudioExtractor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.withdraw()
        splash = SplashScreen(self)
        self.wait_visibility(splash)
        self.after(3000, lambda: self._start_app(splash))

    def _start_app(self, splash):
        try:
            splash.destroy()
        except:
            pass

        self.deiconify()
        self.title("🎙️ Trascrizione Audio/Video — Ing. Barbato")
        self.state("zoomed")
        self.minsize(1200, 800)

        # Icona
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "icona", "icona.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass

        # Variabili
        self.video_path = None
        self.output_path = None
        self.transcribed_text = ""
        self.save_dir = os.getcwd()
        self.selected_model = "base"
        self.selected_lang = "it"
        self.theme_mode = "light"
        self.progress_running = False

        # Layout
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self._setup_layout()
        self._setup_sidebar()
        self._setup_main()

    # ========== STRUTTURA ==========
    def _setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _setup_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=280, corner_radius=15)
        sidebar.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)
        sidebar.grid_propagate(False)

        ctk.CTkLabel(sidebar, text="⚙️ Impostazioni", font=("Titillium Web", 20, "bold")).pack(pady=(15, 10))

        # Lingua
        ctk.CTkLabel(sidebar, text="Lingua Trascrizione:", font=("Titillium Web", 14)).pack(pady=(5, 0))
        self.lang_menu = ctk.CTkOptionMenu(sidebar, values=["it", "en", "es", "fr", "de"],
                                           command=self.set_language)
        self.lang_menu.set("it")
        self.lang_menu.pack(pady=5)

        # Modello
        ctk.CTkLabel(sidebar, text="Modello Whisper:", font=("Titillium Web", 14)).pack(pady=(10, 0))
        self.model_menu = ctk.CTkOptionMenu(sidebar, values=["tiny", "base", "small", "medium"],
                                            command=self.set_model)
        self.model_menu.set("base")
        self.model_menu.pack(pady=5)

        # Cartella
        ctk.CTkLabel(sidebar, text="Cartella di Salvataggio:", font=("Titillium Web", 14)).pack(pady=(15, 0))
        self.dir_label = ctk.CTkLabel(sidebar, text=self.save_dir, wraplength=240,
                                      text_color="#888", font=("Titillium Web", 11))
        self.dir_label.pack(pady=(0, 5))
        ctk.CTkButton(sidebar, text="📁 Cambia cartella", width=200,
                      fg_color="#6A1B9A", command=self.change_save_dir).pack(pady=5)

        # Tema
        ctk.CTkLabel(sidebar, text="Tema:", font=("Titillium Web", 14)).pack(pady=(20, 0))
        self.theme_switch = ctk.CTkSwitch(sidebar, text="🌙 / ☀️ Modalità Scura",
                                          onvalue="dark", offvalue="light",
                                          command=self.toggle_theme)
        self.theme_switch.deselect()
        self.theme_switch.pack(pady=5)

        # Footer
        ctk.CTkLabel(sidebar,
                     text="© 2025 Ing. Francesco Barbato\nMinistero della Giustizia",
                     font=("Titillium Web", 11, "italic"), text_color="#777").pack(side="bottom", pady=20)

    def _setup_main(self):
        main = ctk.CTkFrame(self, corner_radius=15)
        main.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

        ctk.CTkLabel(main, text="🎧 Estrazione Testo da File Audio o Video",
                     font=("Titillium Web", 26, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(main, text="Software professionale creato dall’Ing. Francesco Barbato",
                     font=("Titillium Web", 15, "italic")).pack()

        self.load_button = ctk.CTkButton(main, text="📂 Carica File Audio o Video", width=280,
                                         command=self.load_file)
        self.load_button.pack(pady=15)

        self.progress = ctk.CTkProgressBar(main, width=900)
        self.progress.set(0)
        self.progress.pack(pady=(15, 5))
        self.progress_label = ctk.CTkLabel(main, text="", font=("Titillium Web", 14))
        self.progress_label.pack()

        self.extract_button = ctk.CTkButton(main, text="📝 Avvia Trascrizione", width=280,
                                            command=self.start_transcription)
        self.extract_button.pack(pady=20)

        self.output_label = ctk.CTkLabel(main, text="", wraplength=900, font=("Titillium Web", 13))
        self.output_label.pack(pady=10)

        self.text_preview = ctk.CTkTextbox(main, width=900, height=300, wrap="word",
                                           font=("Titillium Web", 13))
        self.text_preview.pack(pady=10)
        self.text_preview.insert("1.0", "La trascrizione apparirà qui...")
        self.text_preview.configure(state="disabled")

        # Pulsanti azione
        actions = ctk.CTkFrame(main, fg_color="transparent")
        actions.pack(pady=10)
        ctk.CTkButton(actions, text="📋 Copia Testo", width=180, fg_color="#1E88E5",
                      command=self.copy_text).grid(row=0, column=0, padx=15)
        ctk.CTkButton(actions, text="💾 Salva come...", width=180, fg_color="#009E60",
                      command=self.save_text_as).grid(row=0, column=1, padx=15)

        self.open_folder_button = ctk.CTkButton(main, text="📁 Apri cartella di destinazione",
                                                width=280, fg_color="#6A1B9A",
                                                command=self.open_folder)
        self.open_folder_button.pack(pady=20)
        self.open_folder_button.configure(state="disabled")

    # ========== FUNZIONI ==========
    def toggle_theme(self):
        mode = "light" if self.theme_mode == "dark" else "dark"
        self.theme_mode = mode
        ctk.set_appearance_mode(mode)

    def set_language(self, lang):
        self.selected_lang = lang

    def set_model(self, model):
        self.selected_model = model

    def change_save_dir(self):
        folder = filedialog.askdirectory(title="Seleziona cartella di salvataggio")
        if folder:
            self.save_dir = folder
            self.dir_label.configure(text=folder)

    def load_file(self):
        filetypes = [("File audio/video", "*.mp4 *.mkv *.avi *.mov *.mp3 *.wav *.m4a *.flac")]
        path = filedialog.askopenfilename(title="Seleziona un file", filetypes=filetypes)
        if path:
            self.video_path = path
            self.output_label.configure(text=f"✅ File caricato: {os.path.basename(path)}", text_color="#00B472")

    def start_transcription(self):
        if not self.video_path:
            messagebox.showwarning("Nessun file", "Seleziona prima un file audio o video.")
            return
        threading.Thread(target=self.extract_media).start()

    def extract_media(self):
        try:
            clip = VideoFileClip(self.video_path)
            temp_audio = "temp_audio.wav"
            clip.audio.write_audiofile(temp_audio, logger=None)
            clip.close()

            model = whisper.load_model(self.selected_model)
            duration = clip.duration
            self.progress.set(0)
            self.progress_label.configure(text="Elaborazione 0%...")

            result = model.transcribe(temp_audio, language=self.selected_lang, fp16=False)

            text = result["text"].strip()
            self.transcribed_text = text
            output_txt = os.path.join(
                self.save_dir,
                os.path.splitext(os.path.basename(self.video_path))[0] + "_trascrizione.txt"
            )

            with open(output_txt, "w", encoding="utf-8") as f:
                f.write(text)

            # Barra realistica
            for i in range(0, 101):
                self.progress.set(i / 100)
                self.progress_label.configure(text=f"Elaborazione {i}%...")
                self.update_idletasks()
                time.sleep(0.02)

            self.output_label.configure(text=f"✅ Trascrizione completata!\nFile salvato in:\n{output_txt}",
                                        text_color="#00B472")
            self.text_preview.configure(state="normal")
            self.text_preview.delete("1.0", "end")
            self.text_preview.insert("1.0", text)
            self.text_preview.configure(state="disabled")
            self.open_folder_button.configure(state="normal")

            os.remove(temp_audio)

        except Exception as e:
            self.progress_label.configure(text="❌ Errore durante la trascrizione")
            self.output_label.configure(text=str(e), text_color="red")

    def copy_text(self):
        if self.transcribed_text:
            pyperclip.copy(self.transcribed_text)
            messagebox.showinfo("Copiato", "Testo copiato negli appunti!")

    def save_text_as(self):
        if not self.transcribed_text:
            messagebox.showwarning("Nessun testo", "Devi prima effettuare una trascrizione.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("File di testo", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.transcribed_text)
            messagebox.showinfo("Salvato", f"File salvato come:\n{path}")

    def open_folder(self):
        if self.save_dir and os.path.exists(self.save_dir):
            subprocess.Popen(f'explorer "{self.save_dir}"')


if __name__ == "__main__":
    app = VideoAudioExtractor()
    app.mainloop()
