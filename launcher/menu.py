from launcher.config import load_selected_version, save_selected_version
from launcher.minecraft import install_minecraft, launch_minecraft, show_available_versions 
from launcher.launcher_paths import get_launcher_directory

def start_game():
    version = load_selected_version()
    launcher_dir = get_launcher_directory()
    
    print("")
    print(f"Versão selecionada: {version}")
    print(f"Pasta do launcher: {launcher_dir}")
    
    install_minecraft(version)
    launch_minecraft(version)
    
def choose_version():
    print("")
    print("Exemplo de versões:")
    print("1.20.1")
    print("1.19.4")
    print("1.18.2")
    print("1.17.1")
    print("1.16.5")
    print("")
    
    version = input("Digite a versão do Minecraft que deseja jogar (ex: 1.20.1): ").strip()
    
    if not version:
        print("Nenhuma versão digitada.")
        return
    
    save_selected_version(version)
    print("")
    print(f"Versão {version} salva com sucesso!")
    
def show_menu():
    select_version = load_selected_version()
    print("")
    print("====================================")
    print("    BEM VINDO AO RADKELAUNCHER")
    print("====================================")
    print(f"Versão atual: {select_version}")
    print("")
    print("1 - Iniciar Minecraft")
    print("2 - Escolher Versão")
    print("3 - Ver versões disponíveis")
    print("4 - Sair")
    print("")
    
def run_menu():
    while True:
        show_menu()
        option = input("Escolha uma opção: ").strip()
        
        if option == "1":
            start_game()
        
        elif option == "2":
            choose_version()
            
        elif option == "3":
            show_available_versions()
            
        elif option == "4":
            print("")
            print("Saindo do launcher. Até a próxima!")
            break
        
        else:
            print("")
            print("Opção inválida. Por favor, escolha uma opção válida.")