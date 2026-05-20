import threading
import customtkinter as ctk

from launcher.config import load_selected_version, save_selected_version
from launcher.minecraft import start_minecraft, get_available_versions
from launcher.launcher_paths import get_launcher_directory


class LauncherInterface:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.window = ctk.CTk()
        self.window.title("Meu Launcher Minecraft")
        self.window.geometry("900x560")
        self.window.resizable(False, False)

        self.selected_version = ctk.StringVar(value=load_selected_version())

        self.create_layout()

    def create_layout(self):
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=3)
        self.window.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(
            self.window,
            width=220,
            corner_radius=0
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(8, weight=1)

        title = ctk.CTkLabel(
            sidebar,
            text="MEU\nLAUNCHER",
            font=ctk.CTkFont(size=28, weight="bold"),
            justify="left"
        )
        title.grid(row=0, column=0, padx=25, pady=(35, 10), sticky="w")

        subtitle = ctk.CTkLabel(
            sidebar,
            text="Minecraft Launcher",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        subtitle.grid(row=1, column=0, padx=25, pady=(0, 30), sticky="w")

        self.status_indicator = ctk.CTkLabel(
            sidebar,
            text="● Pronto",
            font=ctk.CTkFont(size=14),
            text_color="#55ff99"
        )
        self.status_indicator.grid(row=2, column=0, padx=25, pady=10, sticky="w")

        version_label = ctk.CTkLabel(
            sidebar,
            text="Versão atual:",
            font=ctk.CTkFont(size=13),
            text_color="gray70"
        )
        version_label.grid(row=3, column=0, padx=25, pady=(25, 5), sticky="w")

        self.version_entry = ctk.CTkEntry(
            sidebar,
            textvariable=self.selected_version,
            width=165,
            height=36,
            placeholder_text="Ex: 1.20.1"
        )
        self.version_entry.grid(row=4, column=0, padx=25, pady=5, sticky="w")

        save_button = ctk.CTkButton(
            sidebar,
            text="Salvar versão",
            width=165,
            height=36,
            command=self.save_version
        )
        save_button.grid(row=5, column=0, padx=25, pady=8, sticky="w")

        folder_button = ctk.CTkButton(
            sidebar,
            text="Pasta do launcher",
            width=165,
            height=36,
            fg_color="gray25",
            hover_color="gray35",
            command=self.show_launcher_folder
        )
        folder_button.grid(row=6, column=0, padx=25, pady=8, sticky="w")

        exit_button = ctk.CTkButton(
            sidebar,
            text="Sair",
            width=165,
            height=36,
            fg_color="#8b1e1e",
            hover_color="#a52828",
            command=self.window.destroy
        )
        exit_button.grid(row=9, column=0, padx=25, pady=25, sticky="s")

    def create_main_area(self):
        main = ctk.CTkFrame(
            self.window,
            corner_radius=0,
            fg_color="#151515"
        )
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            main,
            height=120,
            fg_color="transparent"
        )
        header.grid(row=0, column=0, sticky="ew", padx=35, pady=(35, 10))
        header.grid_columnconfigure(0, weight=1)

        welcome = ctk.CTkLabel(
            header,
            text="Bem-vindo ao seu launcher",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        welcome.grid(row=0, column=0, sticky="w")

        description = ctk.CTkLabel(
            header,
            text="Escolha a versão, instale e inicie o Minecraft pelo seu próprio sistema.",
            font=ctk.CTkFont(size=15),
            text_color="gray70"
        )
        description.grid(row=1, column=0, pady=(8, 0), sticky="w")

        card = ctk.CTkFrame(
            main,
            corner_radius=18,
            fg_color="#202020"
        )
        card.grid(row=1, column=0, sticky="ew", padx=35, pady=20)
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        selected_label = ctk.CTkLabel(
            card,
            text="Versão selecionada",
            font=ctk.CTkFont(size=15),
            text_color="gray70"
        )
        selected_label.grid(row=0, column=0, padx=30, pady=(25, 5), sticky="w")

        self.version_display = ctk.CTkLabel(
            card,
            text=self.selected_version.get(),
            font=ctk.CTkFont(size=34, weight="bold")
        )
        self.version_display.grid(row=1, column=0, padx=30, pady=(0, 25), sticky="w")

        play_button = ctk.CTkButton(
            card,
            text="JOGAR",
            font=ctk.CTkFont(size=24, weight="bold"),
            width=210,
            height=70,
            corner_radius=16,
            command=self.start_game_thread
        )
        play_button.grid(row=0, column=1, rowspan=2, padx=30, pady=30, sticky="e")

        actions_frame = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )
        actions_frame.grid(row=2, column=0, sticky="ew", padx=35, pady=(0, 10))
        actions_frame.grid_columnconfigure((0, 1), weight=1)

        versions_button = ctk.CTkButton(
            actions_frame,
            text="Ver versões disponíveis",
            height=42,
            fg_color="gray25",
            hover_color="gray35",
            command=self.show_versions_thread
        )
        versions_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        clear_button = ctk.CTkButton(
            actions_frame,
            text="Limpar status",
            height=42,
            fg_color="gray25",
            hover_color="gray35",
            command=self.clear_status
        )
        clear_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        log_label = ctk.CTkLabel(
            main,
            text="Status do launcher",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        log_label.grid(row=3, column=0, padx=35, pady=(15, 5), sticky="w")

        self.status_box = ctk.CTkTextbox(
            main,
            width=610,
            height=190,
            corner_radius=14,
            fg_color="#101010",
            text_color="gray90"
        )
        self.status_box.grid(row=4, column=0, padx=35, pady=(0, 25), sticky="ew")
        self.status_box.configure(state="disabled")

        self.add_status("Launcher iniciado.")
        self.add_status(f"Versão atual: {self.selected_version.get()}")

    def add_status(self, message):
        self.status_box.configure(state="normal")
        self.status_box.insert("end", message + "\n")
        self.status_box.see("end")
        self.status_box.configure(state="disabled")

    def clear_status(self):
        self.status_box.configure(state="normal")
        self.status_box.delete("1.0", "end")
        self.status_box.configure(state="disabled")

    def set_status_indicator(self, text, color):
        self.status_indicator.configure(text=text, text_color=color)

    def save_version(self):
        version = self.selected_version.get().strip()

        if not version:
            self.add_status("Erro: digite uma versão válida.")
            return

        save_selected_version(version)
        self.version_display.configure(text=version)

        self.add_status(f"Versão salva: {version}")

    def start_game_thread(self):
        thread = threading.Thread(target=self.start_game)
        thread.daemon = True
        thread.start()

    def start_game(self):
        version = self.selected_version.get().strip()

        if not version:
            self.add_status("Erro: digite uma versão válida.")
            return

        save_selected_version(version)
        self.version_display.configure(text=version)

        try:
            self.set_status_indicator("● Instalando", "#ffd966")
            self.add_status(f"Iniciando processo para Minecraft {version}...")

            start_minecraft(version, self.add_status)

            self.set_status_indicator("● Jogo aberto", "#55ff99")
            self.add_status("Minecraft iniciado com sucesso.")

        except Exception as error:
            self.set_status_indicator("● Erro", "#ff5555")
            self.add_status(f"Erro ao iniciar Minecraft: {error}")

    def show_versions_thread(self):
        thread = threading.Thread(target=self.show_versions)
        thread.daemon = True
        thread.start()

    def show_versions(self):
        try:
            self.set_status_indicator("● Buscando", "#ffd966")
            self.add_status("Buscando versões disponíveis...")

            versions = get_available_versions(limit=30)

            self.add_status("Versões encontradas:")

            for version in versions:
                self.add_status(f'{version["id"]} | tipo: {version["type"]}')

            self.set_status_indicator("● Pronto", "#55ff99")

        except Exception as error:
            self.set_status_indicator("● Erro", "#ff5555")
            self.add_status(f"Erro ao buscar versões: {error}")

    def show_launcher_folder(self):
        folder = get_launcher_directory()
        self.add_status(f"Pasta do launcher: {folder}")

    def run(self):
        self.window.mainloop()