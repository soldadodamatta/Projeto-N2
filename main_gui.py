
#!/usr/bin/env python3
"""
Sabor Express - Sistema de Gerenciamento de Restaurantes
Aplicação com interface gráfica usando Tkinter
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def main():
    """Função principal da aplicação"""
    try:
        # Importar a interface GUI
        from gui_interface import RestaurantGUI
        
        # Criar janela principal
        root = tk.Tk()
        
        # Configurações da janela
        root.title("🍽️ Sabor Express")
        
        # Centralizar janela na tela
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1200
        window_height = 800
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Inicializar aplicação
        app = RestaurantGUI(root)
        
        # Iniciar loop principal
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"Erro ao importar módulos necessários: {e}\n\n"
        error_msg += "Certifique-se de que todos os arquivos estão no diretório correto:\n"
        error_msg += "- restaurant_manager.py\n"
        error_msg += "- gui_interface.py\n"
        error_msg += "- main_gui.py"
        
        # Tentar mostrar messagebox, senão print no console
        try:
            messagebox.showerror("Erro de Importação", error_msg)
        except:
            print("ERRO:", error_msg)
        
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Erro inesperado ao iniciar a aplicação: {e}"
        
        try:
            messagebox.showerror("Erro", error_msg)
        except:
            print("ERRO:", error_msg)
        
        sys.exit(1)

if __name__ == "__main__":
    print("🍽️ Iniciando Sabor Express...")
    print("Sistema de Gerenciamento de Restaurantes")
    print("-" * 50)
    main()

