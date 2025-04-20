import customtkinter as ctk
import tkinter as tk
from image_processor import ImageProcessor
from ui import ImageEditorUI
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def main():
    root = ctk.CTk()
    root.geometry("1200x700")
    processor = ImageProcessor()
    
    ui = ImageEditorUI(root, processor)
    ui.setup_ui()
    
    icon_path = resource_path("icon.ico")
    try:
        root.iconbitmap(icon_path)
    except tk.TclError as e:
        print(f"Ошибка установки иконки: {e}")

    def on_closing():
        if ui.welcome_window:
            ui.welcome_window.destroy()
        root.destroy()
        sys.exit(0) 

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()