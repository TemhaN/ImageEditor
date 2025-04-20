import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import time
import json
import os
import math
import sys
from controls import ControlPanel
from dialogs import (ResizeDialog, NoiseDialog, PixelationDialog, VignetteDialog, 
                    GlowDialog, InvertDialog, EmbossDialog, BlurDialog, 
                    OilPaintingDialog, SepiaDialog, GrayscaleDialog, PosterizeDialog)
from utils import smooth_zoom
from translator import Translator

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)
  
class ImageEditorUI:
    def __init__(self, root, processor):
        self.root = root
        self.processor = processor
        self.translator = Translator()
        self.zoom_level = 1.0
        self.target_zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.photo = None
        self.welcome_window = None
        self.last_update = 0
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.main_frame = None
        self.last_drag_update = 0
        self.drag_update_interval = 0.05
        self.full_img_width = 0
        self.full_img_height = 0
        self.loading_label = None
        self.is_updating = False
        self.last_zoom_time = 0
        self.zoom_debounce_interval = 0.05
        self.is_zooming = False
        self.config_file = "config.json"
        self.load_config()
        self.apply_theme()
        self.root.withdraw()
        
        def on_welcome_closing():
            self.close_welcome_window()
            self.root.destroy()
            sys.exit(0)
            
        self.root.protocol("WM_DELETE_WINDOW", on_welcome_closing)

    def load_config(self):
        default_config = {"theme": "dark", "language": "ru"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
        if "language" not in self.config:
            self.config["language"] = "ru"
        ctk.set_appearance_mode(self.config["theme"])
        ctk.set_default_color_theme("blue")

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def apply_theme(self):
        ctk.set_appearance_mode(self.config["theme"])
        self.bg_color = "#2b2b2b" if self.config["theme"] == "dark" else "#ffffff"
        self.fg_color = "#ffffff" if self.config["theme"] == "dark" else "#000000"
        self.button_text_color = "#ffffff"
        if self.main_frame:
            self.create_main_ui()
        if self.welcome_window:
            self.show_welcome_window()

    def setup_ui(self):
        if not hasattr(self, 'config'):
            self.load_config()
        self.show_welcome_window()
        self.root.bind("<Control-z>", self.undo)
        self.root.bind("<<ShowLoading>>", lambda e: self.show_loading())

    def _(self, text_id, **kwargs):
        return self.translator.get_text(text_id, self.config["language"], **kwargs)

    def create_main_ui(self):
        if self.main_frame:
            self.main_frame.destroy()
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_menu()
        self.create_canvas()
        self.create_control_frame()
        self.controls = ControlPanel(self.control_frame, self.processor, self.update_image, self)
        self.update_texts()

    def create_menu(self):
        menu_frame = ctk.CTkFrame(self.main_frame, fg_color=self.bg_color)
        menu_frame.pack(fill=tk.X, padx=10, pady=5)

        buttons = [
            ("open", self.open_image),
            ("save", self.processor.save_image),
            ("undo", self.undo),
            ("resize", self.open_resize_dialog),
            ("settings", self.open_settings_dialog),
            ("exit", self.quit_application)
        ]

        self.menu_buttons = {}
        for text_id, command in buttons[:4]:
            btn = ctk.CTkButton(
                menu_frame,
                text="",
                command=command,
                font=("Arial", 12),
                width=120,
                height=25,
                fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
                text_color=self.button_text_color,
                hover_color="#5a9bd4" if self.config["theme"] == "dark" else "#2a7bbf"
            )
            btn.pack(side=tk.LEFT, padx=5, pady=3)
            self.menu_buttons[text_id] = btn

        self.effects_menu = ctk.CTkOptionMenu(
            menu_frame,
            values=[""],
            command=self.apply_effect,
            font=("Arial", 12),
            width=120,
            height=25,
            fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
            text_color=self.button_text_color,
            dropdown_fg_color=self.bg_color,
            dropdown_text_color=self.fg_color,
            dropdown_font=("Arial", 12)
        )
        self.effects_menu.pack(side=tk.LEFT, padx=5, pady=3)

        for text_id, command in buttons[4:]:
            btn = ctk.CTkButton(
                menu_frame,
                text="",
                command=command,
                font=("Arial", 12),
                width=120,
                height=25,
                fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
                text_color=self.button_text_color,
                hover_color="#5a9bd4" if self.config["theme"] == "dark" else "#2a7bbf"
            )
            btn.pack(side=tk.LEFT, padx=5, pady=3)
            self.menu_buttons[text_id] = btn

    def quit_application(self):
        if self.welcome_window:
            self.welcome_window.destroy()
        self.root.destroy()
        sys.exit(0)
  
    def apply_effect(self, choice):
        if choice == self._("effects"):
            return
        effects_mapping = {
            self._("color_match"): self.processor.match_colors,
            self._("noise"): self.open_noise_dialog,
            self._("pixelation"): self.open_pixelation_dialog,
            self._("vignette"): self.open_vignette_dialog,
            self._("glow"): self.open_glow_dialog,
            self._("invert"): self.open_invert_dialog,
            self._("emboss"): self.open_emboss_dialog,
            self._("blur"): self.open_blur_dialog,
            self._("oil_painting"): self.open_oil_painting_dialog,
            self._("sepia"): self.open_sepia_dialog,
            self._("grayscale"): self.open_grayscale_dialog,
            self._("posterize"): self.open_posterize_dialog
        }
        if choice in effects_mapping:
            effects_mapping[choice]()
        else:
            messagebox.showwarning(
                self._("error"),
                self._("effect_not_implemented", effect=choice)
            )

    def open_settings_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(self._("settings_title"))
        dialog.geometry("250x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=self._("select_theme"),
            font=("Arial", 12),
            text_color=self.fg_color
        ).pack(pady=5)

        theme_var = tk.StringVar(value=self.config["theme"])
        theme_menu = ctk.CTkOptionMenu(
            dialog,
            values=["dark", "light"],
            variable=theme_var,
            font=("Arial", 12),
            fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
            text_color=self.button_text_color
        )
        theme_menu.pack(pady=5)

        ctk.CTkLabel(
            dialog,
            text=self._("select_language"),
            font=("Arial", 12),
            text_color=self.fg_color
        ).pack(pady=5)

        language_var = tk.StringVar(value=self.config["language"])
        language_menu = ctk.CTkOptionMenu(
            dialog,
            values=["ru", "en", "kz"],
            variable=language_var,
            font=("Arial", 12),
            fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
            text_color=self.button_text_color
        )
        language_menu.pack(pady=5)

        def apply():
            self.config["theme"] = theme_var.get()
            self.config["language"] = language_var.get()
            self.save_config()
            self.apply_theme()
            self.update_texts()
            dialog.destroy()

        ctk.CTkButton(
            dialog,
            text=self._("apply"),
            command=apply,
            font=("Arial", 12),
            width=150,
            height=30,
            fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.config["theme"] == "dark" else "#2a7bbf"
        ).pack(pady=10)

    def create_canvas(self):
        self.canvas_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.bg_color,
            corner_radius=15
        )
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        zoom_frame = ctk.CTkFrame(self.canvas_frame, fg_color=self.bg_color)
        zoom_frame.pack(fill=tk.X, pady=5)

        ctk.CTkButton(
            zoom_frame,
            text="+",
            command=lambda: self.adjust_zoom(0.1),
            width=40,
            height=25,
            font=("Arial", 12),
            fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.config["theme"] == "dark" else "#2a7bbf"
        ).pack(side=tk.LEFT, padx=(10, 5))

        ctk.CTkButton(
            zoom_frame,
            text="-",
            command=lambda: self.adjust_zoom(-0.1),
            width=40,
            height=25,
            font=("Arial", 12),
            fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.config["theme"] == "dark" else "#2a7bbf"
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.resolution_label = ctk.CTkLabel(
            zoom_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.resolution_label.pack(side=tk.LEFT, expand=True)

        self.loading_label = ctk.CTkLabel(
            self.canvas_frame,
            text="",
            font=("Arial", 14),
            text_color=self.fg_color
        )
        self.loading_label.pack_forget()

    def create_control_frame(self):
        self.control_frame = ctk.CTkFrame(self.main_frame, width=250, fg_color=self.bg_color)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

    def show_welcome_window(self):
        if self.welcome_window or self.processor.image:
            return

        self.welcome_window = ctk.CTk()
        self.welcome_window.iconbitmap("icon.ico")
        self.welcome_window.title(self._("welcome_title"))

        window_width = 400
        window_height = 250
        self.welcome_window.geometry(f"{window_width}x{window_height}")

        screen_width = self.welcome_window.winfo_screenwidth()
        screen_height = self.welcome_window.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        self.welcome_window.geometry(f"+{position_x}+{position_y}")

        self.welcome_window.resizable(False, False)

        def on_welcome_closing():
            self.close_welcome_window()
            self.root.destroy()
            sys.exit(0)
        
        self.welcome_window.protocol("WM_DELETE_WINDOW", on_welcome_closing)
            
        self.welcome_label = ctk.CTkLabel(
            self.welcome_window,
            text="",
            font=("Arial", 16, "bold"),
            wraplength=350,
            justify="center",
            text_color=self.fg_color
        )
        self.welcome_label.pack(pady=(30, 15))

        self.welcome_sub_label = ctk.CTkLabel(
            self.welcome_window,
            text="",
            font=("Arial", 12),
            wraplength=350,
            justify="center",
            text_color=self.fg_color
        )
        self.welcome_sub_label.pack(pady=15)

        self.welcome_button = ctk.CTkButton(
            self.welcome_window,
            text="",
            font=("Arial", 12),
            command=self.open_image,
            width=150,
            height=30,
            fg_color="#3b8ed0" if self.config["theme"] == "dark" else "#1f6aa5",
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.config["theme"] == "dark" else "#2a7bbf"
        )
        self.welcome_button.pack(pady=20)

        self.update_texts()
        self.welcome_window.update()

    def close_welcome_window(self):
        if self.welcome_window:
            self.welcome_window.destroy()
            self.welcome_window = None

    def show_loading(self):
        if self.is_updating or not self.main_frame:
            return
        self.loading_label.pack(pady=5)
        self.root.config(cursor="wait")
        self.root.update()

    def hide_loading(self):
        if self.is_updating or not self.main_frame:
            return
        self.loading_label.pack_forget()
        self.root.config(cursor="")
        self.root.update()

    def open_image(self):
        if self.processor.open_image():
            self.close_welcome_window()
            if not self.main_frame:
                self.create_main_ui()
            self.root.deiconify()
            self.offset_x = 0
            self.offset_y = 0
            self.zoom_level = 1.0
            self.target_zoom = 1.0
            full_img = self.processor.get_processed_image()
            self.full_img_width, self.full_img_height = full_img.size
            self.update_image()

    def undo(self, event=None):
        if not self.main_frame:
            return
        self.show_loading()
        if self.processor.undo():
            self.update_image()
        self.hide_loading()

    def open_resize_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        ResizeDialog(self.root, self.processor, self.update_image, self)

    def open_noise_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        NoiseDialog(self.root, self.processor, self.update_image, self)

    def open_pixelation_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        PixelationDialog(self.root, self.processor, self.update_image, self)

    def open_vignette_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        VignetteDialog(self.root, self.processor, self.update_image, self)

    def open_glow_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        GlowDialog(self.root, self.processor, self.update_image, self)

    def open_invert_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        InvertDialog(self.root, self.processor, self.update_image, self)

    def open_emboss_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        EmbossDialog(self.root, self.processor, self.update_image, self)

    def open_blur_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        BlurDialog(self.root, self.processor, self.update_image, self)

    def open_oil_painting_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        OilPaintingDialog(self.root, self.processor, self.update_image, self)

    def open_sepia_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        SepiaDialog(self.root, self.processor, self.update_image, self)

    def open_grayscale_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        GrayscaleDialog(self.root, self.processor, self.update_image, self)

    def open_posterize_dialog(self):
        if not self.processor.original_image:
            messagebox.showwarning(
                self._("error"),
                self._("image_not_loaded")
            )
            return
        PosterizeDialog(self.root, self.processor, self.update_image, self)

    def update_resolution_label(self):
        if self.processor.original_image:
            width = self.processor.adjustments.get("width", self.processor.original_image.width)
            height = self.processor.adjustments.get("height", self.processor.original_image.height)
            self.resolution_label.configure(
                text=self._("resolution", width=width, height=height)
            )
        else:
            self.resolution_label.configure(
                text=self._("resolution_not_loaded")
            )

    def update_texts(self):
        if self.welcome_window:
            self.welcome_window.title(self._("welcome_title"))
            self.welcome_label.configure(text=self._("welcome_message"))
            self.welcome_sub_label.configure(text=self._("welcome_submessage"))
            self.welcome_button.configure(text=self._("load_image"))

        if self.main_frame:
            self.root.title(self._("app_title"))
            for text_id, btn in self.menu_buttons.items():
                btn.configure(text=self._(text_id))
            self.effects_menu.configure(values=[
                self._("effects"),
                self._("color_match"),
                self._("noise"),
                self._("pixelation"),
                self._("vignette"),
                self._("glow"),
                self._("invert"),
                self._("emboss"),
                self._("blur"),
                self._("oil_painting"),
                self._("sepia"),
                self._("grayscale"),
                self._("posterize")
            ])
            self.effects_menu.set(self._("effects"))
            self.loading_label.configure(text=self._("processing"))
            self.update_resolution_label()
            if self.controls:
                self.controls.update_texts()

    def zoom(self, event):
        if not self.processor.image:
            return

        current_time = time.time()
        if current_time - self.last_zoom_time < self.zoom_debounce_interval:
            return
        self.last_zoom_time = current_time

        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 600

        min_zoom = min(canvas_width / self.full_img_width, canvas_height / self.full_img_height) / 2
        if event.type == tk.EventType.MouseWheel:
            delta = 0.1 if event.delta > 0 else -0.1
        else:
            delta = 0.1 if event.num == 4 else -0.1 if event.num == 5 else 0
        if delta == 0:
            return

        prev_zoom = self.zoom_level
        self.target_zoom = max(min_zoom, self.zoom_level + delta)
        self.target_zoom = min(self.target_zoom, 10.0)

        mouse_x = event.x
        mouse_y = event.y
        center_x = canvas_width / 2 + self.offset_x
        center_y = canvas_height / 2 + self.offset_y
        rel_x = (mouse_x - center_x) / prev_zoom
        rel_y = (mouse_y - center_y) / prev_zoom

        new_center_x = mouse_x - rel_x * self.target_zoom
        new_center_y = mouse_y - rel_y * self.target_zoom
        self.offset_x = new_center_x - canvas_width / 2
        self.offset_y = new_center_y - canvas_height / 2

        if not self.is_zooming:
            smooth_zoom(self)

    def start_drag(self, event):
        if self.processor.image:
            self.dragging = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def drag(self, event):
        if self.dragging and self.processor.image:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.offset_x += dx
            self.offset_y += dy
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            current_time = time.time()
            if current_time - self.last_drag_update >= self.drag_update_interval:
                self.update_image()
                self.last_drag_update = current_time

    def stop_drag(self, event):
        self.dragging = False
        self.update_image()

    def adjust_zoom(self, delta):
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 600
        min_zoom = min(canvas_width / self.full_img_width, canvas_height / self.full_img_height) / 2
        self.target_zoom = max(min_zoom, self.zoom_level + delta)
        self.target_zoom = min(self.target_zoom, 10.0)
        if not self.is_zooming:
            smooth_zoom(self)

    def on_canvas_resize(self, event):
        if self.is_updating or not self.processor.image:
            return
        self.update_image()

    def update_image(self, fast_mode=False):
        if self.is_updating or not self.processor.image or not self.canvas:
            return

        self.is_updating = True
        start_time = time.time()
        try:
            self.show_loading()
            img = self.processor.get_processed_image(fast_mode=fast_mode)
            if not img:
                return

            canvas_width = self.canvas.winfo_width() or 800
            canvas_height = self.canvas.winfo_height() or 600

            img_width, img_height = self.full_img_width, self.full_img_height

            min_zoom = min(canvas_width / img_width, canvas_height / img_height) / 2
            if self.zoom_level < min_zoom and not self.dragging:
                self.zoom_level = min_zoom
                self.target_zoom = min_zoom
            self.zoom_level = min(self.zoom_level, 10.0)

            pos_x = canvas_width / 2 + self.offset_x
            pos_y = canvas_height / 2 + self.offset_y

            scaled_width = int(img_width * self.zoom_level)
            scaled_height = int(img_height * self.zoom_level)

            img_left = pos_x - scaled_width / 2
            img_top = pos_y - scaled_height / 2
            img_right = pos_x + scaled_width / 2
            img_bottom = pos_y + scaled_height / 2

            visible_left = max(0, img_left)
            visible_top = max(0, img_top)
            visible_right = min(canvas_width, img_right)
            visible_bottom = min(canvas_height, img_bottom)

            if visible_right <= visible_left or visible_bottom <= visible_top:
                self.canvas.delete("all")
                return

            crop_left = max(0, (visible_left - img_left) / self.zoom_level)
            crop_top = max(0, (visible_top - img_top) / self.zoom_level)
            crop_right = min(img_width, (visible_right - img_left) / self.zoom_level)
            crop_bottom = min(img_height, (visible_bottom - img_top) / self.zoom_level)

            if crop_right <= crop_left or crop_bottom <= crop_top:
                self.canvas.delete("all")
                return

            crop_box = (int(crop_left), int(crop_top), int(crop_right), int(crop_bottom))
            cropped_img = img.crop(crop_box)

            crop_width = crop_right - crop_left
            crop_height = crop_bottom - crop_top
            new_size = (int(crop_width * self.zoom_level), int(crop_height * self.zoom_level))

            if fast_mode:
                resized = cropped_img.resize(new_size, Image.Resampling.BILINEAR)
            else:
                if self.zoom_level > 1:
                    resized = cropped_img.resize(new_size, Image.Resampling.LANCZOS)
                else:
                    resized = cropped_img.resize(new_size, Image.Resampling.BILINEAR)

            self.photo = ImageTk.PhotoImage(resized)

            self.canvas.delete("all")

            display_pos_x = visible_left
            display_pos_y = visible_top

            corner_radius = 15
            points = []

            for i in range(16):
                angle = math.radians(90 + i * 5.625)
                x = corner_radius + corner_radius * math.cos(angle)
                y = corner_radius + corner_radius * math.sin(angle)
                points.extend([x, y])

            for i in range(16):
                angle = math.radians(0 + i * 5.625)
                x = canvas_width - corner_radius + corner_radius * math.cos(angle)
                y = corner_radius + corner_radius * math.sin(angle)
                points.extend([x, y])

            for i in range(16):
                angle = math.radians(270 + i * 5.625)
                x = canvas_width - corner_radius + corner_radius * math.cos(angle)
                y = canvas_height - corner_radius + corner_radius * math.sin(angle)
                points.extend([x, y])

            for i in range(16):
                angle = math.radians(180 + i * 5.625)
                x = corner_radius + corner_radius * math.cos(angle)
                y = canvas_height - corner_radius + corner_radius * math.sin(angle)
                points.extend([x, y])

            clip_id = self.canvas.create_polygon(
                points,
                fill="",
                outline="",
                tags="clip"
            )

            image_id = self.canvas.create_image(
                display_pos_x,
                display_pos_y,
                image=self.photo,
                anchor="nw"
            )

            self.canvas.itemconfig(image_id, tags=("image",))
            self.canvas.tag_lower(image_id, clip_id)

            self.canvas.clip = clip_id
            self.canvas.image = image_id
            self.canvas.tag_bind("image", "<ButtonPress-1>", self.start_drag)
            self.canvas.tag_bind("image", "<B1-Motion>", self.drag)
            self.canvas.tag_bind("image", "<ButtonRelease-1>", self.stop_drag)

            self.canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
            self.canvas.clip_to = lambda: self.canvas.coords(
                clip_id,
                *[item for sublist in [
                    [corner_radius + corner_radius * math.cos(math.radians(90 + i * 5.625)),
                     corner_radius + corner_radius * math.sin(math.radians(90 + i * 5.625))]
                    for i in range(16)
                ] + [
                    [canvas_width - corner_radius + corner_radius * math.cos(math.radians(0 + i * 5.625)),
                     corner_radius + corner_radius * math.sin(math.radians(0 + i * 5.625))]
                    for i in range(16)
                ] + [
                    [canvas_width - corner_radius + corner_radius * math.cos(math.radians(270 + i * 5.625)),
                     canvas_height - corner_radius + corner_radius * math.sin(math.radians(270 + i * 5.625))]
                    for i in range(16)
                ] + [
                    [corner_radius + corner_radius * math.cos(math.radians(180 + i * 5.625)),
                     canvas_height - corner_radius + corner_radius * math.sin(math.radians(180 + i * 5.625))]
                    for i in range(16)
                ] for item in sublist]
            )

            self.canvas.clip_to()

            self.update_resolution_label()

            if time.time() - start_time > 5:
                raise TimeoutError("Image processing took too long")

        except Exception as e:
            messagebox.showerror(
                self._("error"),
                self._("update_image_error", error=str(e))
            )
        finally:
            self.hide_loading()
            self.is_updating = False