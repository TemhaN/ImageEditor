import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from translator import Translator

class BaseDialog:
    def __init__(self, parent, processor, update_callback, ui):
        self.parent = parent
        self.processor = processor
        self.update_callback = update_callback
        self.ui = ui
        self.translator = Translator()
        self.lang = self.ui.config.get("language", "ru")
        self.bg_color = "#2b2b2b" if ui.config["theme"] == "dark" else "#ffffff"
        self.fg_color = "#ffffff" if ui.config["theme"] == "dark" else "#000000"
        self.button_fg_color = "#3b8ed0" if ui.config["theme"] == "dark" else "#1f6aa5"
        self.create_dialog()

    def create_dialog(self):
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.parent.iconbitmap("icon.ico")
        self.dialog.iconbitmap("icon.ico")
        self.setup_widgets()

    def setup_widgets(self):
        raise NotImplementedError("Subclasses should implement this method")

    def apply(self):
        raise NotImplementedError("Subclasses should implement this method")

    def _(self, text_id, **kwargs):
        return self.translator.get_text(text_id, self.lang, **kwargs)

class ResizeDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("resize_title"))
        self.dialog.geometry("400x640")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("resize_image"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("resize_method"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.resize_method_var = tk.StringVar(value=self._("resize_method_resize"))
        resize_method_menu = ctk.CTkOptionMenu(
            self.dialog,
            values=[self._("resize_method_resize"), self._("resize_method_crop")],
            variable=self.resize_method_var,
            font=("Arial", 14),
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        )
        resize_method_menu.pack(pady=5)

        ctk.CTkLabel(
            self.dialog,
            text=self._("width"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.width_entry = ctk.CTkEntry(
            self.dialog,
            font=("Arial", 14),
            width=200,
            text_color=self.fg_color
        )
        self.width_entry.pack(pady=5)

        ctk.CTkLabel(
            self.dialog,
            text=self._("height"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.height_entry = ctk.CTkEntry(
            self.dialog,
            font=("Arial", 14),
            width=200,
            text_color=self.fg_color
        )
        self.height_entry.pack(pady=5)

        ctk.CTkLabel(
            self.dialog,
            text=self._("units"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.unit_var = tk.StringVar(value=self._("unit_pixels"))
        unit_menu = ctk.CTkOptionMenu(
            self.dialog,
            values=[self._("unit_pixels"), self._("unit_percent")],
            variable=self.unit_var,
            font=("Arial", 14),
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        )
        unit_menu.pack(pady=5)

        self.keep_ratio_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            self.dialog,
            text=self._("keep_ratio"),
            variable=self.keep_ratio_var,
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)

        ctk.CTkLabel(
            self.dialog,
            text=self._("crop_side"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        crop_frame = ctk.CTkFrame(self.dialog, fg_color=self.bg_color)
        crop_frame.pack(pady=5)

        self.crop_side_var = tk.StringVar(value="center")
        self.crop_buttons = {}

        for side in ["top", "left", "center", "right", "bottom"]:
            canvas = tk.Canvas(crop_frame, width=40, height=40, highlightthickness=0, bg=self.bg_color)
            canvas.create_rectangle(0, 0, 40, 40, outline="gray", fill="white")
            if side == "center":
                canvas.create_rectangle(10, 10, 30, 30, outline="black", fill="white")
            elif side == "top":
                canvas.create_rectangle(10, 0, 30, 20, outline="black", fill="white")
            elif side == "bottom":
                canvas.create_rectangle(10, 20, 30, 40, outline="black", fill="white")
            elif side == "left":
                canvas.create_rectangle(0, 10, 20, 30, outline="black", fill="white")
            elif side == "right":
                canvas.create_rectangle(20, 10, 40, 30, outline="black", fill="white")
            canvas.bind("<Button-1>", lambda e, s=side: self.select_crop_side(s))
            self.crop_buttons[side] = canvas

        self.crop_buttons["top"].grid(row=0, column=1, padx=5, pady=5)
        self.crop_buttons["left"].grid(row=1, column=0, padx=5, pady=5)
        self.crop_buttons["center"].grid(row=1, column=1, padx=5, pady=5)
        self.crop_buttons["right"].grid(row=1, column=2, padx=5, pady=5)
        self.crop_buttons["bottom"].grid(row=2, column=1, padx=5, pady=5)

        self.select_crop_side("center")

        self.width = self.processor.adjustments.get("width", self.processor.original_image.width)
        self.height = self.processor.adjustments.get("height", self.processor.original_image.height)
        self.orig_width = self.processor.original_image.width
        self.orig_height = self.processor.original_image.height

        def update_fields():
            if self.unit_var.get() == self._("unit_percent"):
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, f"{(self.width / self.orig_width * 100):.1f}")
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, f"{(self.height / self.orig_height * 100):.1f}")
            else:
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, str(self.width))
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, str(self.height))

        update_fields()
        self.unit_var.trace("w", lambda *args: update_fields())

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=10)

        def update_height(*args):
            if self.keep_ratio_var.get() and self.width_entry.get():
                try:
                    w = float(self.width_entry.get())
                    ratio = self.orig_height / self.orig_width
                    if self.unit_var.get() == self._("unit_percent"):
                        h = w
                    else:
                        h = int(w * ratio)
                    self.height_entry.delete(0, tk.END)
                    self.height_entry.insert(0, str(h) if self.unit_var.get() == self._("unit_pixels") else f"{h:.1f}")
                except ValueError:
                    pass

        def update_width(*args):
            if self.keep_ratio_var.get() and self.height_entry.get():
                try:
                    h = float(self.height_entry.get())
                    ratio = self.orig_width / self.orig_height
                    if self.unit_var.get() == self._("unit_percent"):
                        w = h
                    else:
                        w = int(h * ratio)
                    self.width_entry.delete(0, tk.END)
                    self.width_entry.insert(0, str(w) if self.unit_var.get() == self._("unit_pixels") else f"{w:.1f}")
                except ValueError:
                    pass

        self.width_entry.bind("<KeyRelease>", update_height)
        self.height_entry.bind("<KeyRelease>", update_width)

    def select_crop_side(self, side):
        self.crop_side_var.set(side)
        for s, canvas in self.crop_buttons.items():
            canvas.delete("all")
            canvas.create_rectangle(0, 0, 40, 40, outline="gray", fill="white")
            if s == "center":
                canvas.create_rectangle(10, 10, 30, 30, outline="black", fill="white")
            elif s == "top":
                canvas.create_rectangle(10, 0, 30, 20, outline="black", fill="white")
            elif s == "bottom":
                canvas.create_rectangle(10, 20, 30, 40, outline="black", fill="white")
            elif s == "left":
                canvas.create_rectangle(0, 10, 20, 30, outline="black", fill="white")
            elif s == "right":
                canvas.create_rectangle(20, 10, 40, 30, outline="black", fill="white")
        self.crop_buttons[side].delete("all")
        self.crop_buttons[side].create_rectangle(0, 0, 40, 40, outline="black", fill="lightblue")
        if side == "center":
            self.crop_buttons[side].create_rectangle(10, 10, 30, 30, outline="black", fill="white")
        elif side == "top":
            self.crop_buttons[side].create_rectangle(10, 0, 30, 20, outline="black", fill="white")
        elif side == "bottom":
            self.crop_buttons[side].create_rectangle(10, 20, 30, 40, outline="black", fill="white")
        elif side == "left":
            self.crop_buttons[side].create_rectangle(0, 10, 20, 30, outline="black", fill="white")
        elif side == "right":
            self.crop_buttons[side].create_rectangle(20, 10, 40, 30, outline="black", fill="white")

    def apply(self):
        try:
            self.ui.show_loading()
            w = float(self.width_entry.get())
            h = float(self.height_entry.get())
            if self.unit_var.get() == self._("unit_percent"):
                w = int(self.orig_width * w / 100)
                h = int(self.orig_height * h / 100)
            else:
                w = int(w)
                h = int(h)
            if w <= 0 or h <= 0:
                raise ValueError(self._("dimensions_error"))

            method = "resize" if self.resize_method_var.get() == self._("resize_method_resize") else "crop"
            self.processor.update_adjustment("resize_method", method)
            self.processor.update_adjustment("width", w)
            self.processor.update_adjustment("height", h)
            self.processor.update_adjustment("crop_side", self.crop_side_var.get())

            canvas_width = self.ui.canvas.winfo_width() or 800
            canvas_height = self.ui.canvas.winfo_height() or 600
            min_zoom = min(canvas_width / w, canvas_height / h) / 2
            self.ui.zoom_level = min_zoom
            self.ui.target_zoom = min_zoom
            self.ui.offset_x = 0
            self.ui.offset_y = 0
            full_img = self.processor.get_processed_image()
            self.ui.full_img_width, self.ui.full_img_height = full_img.size
            self.update_callback()
            self.dialog.destroy()
        except ValueError as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("invalid_values", error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class NoiseDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("noise_title"))
        self.dialog.geometry("400x250")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("add_noise"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("noise_intensity"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.intensity_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200
        )
        self.intensity_slider.set(0.5)
        self.intensity_slider.pack(pady=5)

        ctk.CTkLabel(
            self.dialog,
            text=self._("noise_type"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.noise_type = ctk.CTkOptionMenu(
            self.dialog,
            values=[self._("noise_type_gaussian"), self._("noise_type_salt_pepper")],
            font=("Arial", 14),
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        )
        self.noise_type.set(self._("noise_type_gaussian"))
        self.noise_type.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            noise_level = self.intensity_slider.get()
            type_map = {
                self._("noise_type_gaussian"): "gaussian",
                self._("noise_type_salt_pepper"): "salt_pepper"
            }
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_noise(
                self.processor.image if self.processor.image else self.processor.original_image,
                noise_level,
                type_map[self.noise_type.get()]
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("noise_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class PixelationDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("pixelation_title"))
        self.dialog.geometry("400x200")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("pixelation_title"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("block_size"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.block_size_entry = ctk.CTkEntry(
            self.dialog,
            font=("Arial", 14),
            width=200,
            placeholder_text="10",
            text_color=self.fg_color
        )
        self.block_size_entry.insert(0, "10")
        self.block_size_entry.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            block_size = int(self.block_size_entry.get())
            if block_size < 1 or block_size > 50:
                raise ValueError(self._("invalid_block_size"))
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_pixelation(
                self.processor.image if self.processor.image else self.processor.original_image,
                block_size
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except ValueError as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("invalid_levels", error=str(e)),
                icon="icon.ico"
            )
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("pixelation_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class VignetteDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("vignette_title"))
        self.dialog.geometry("400x200")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("vignette_title"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("intensity"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.intensity_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200
        )
        self.intensity_slider.set(0.5)
        self.intensity_slider.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            intensity = self.intensity_slider.get()
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_vignette(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("vignette_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class GlowDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("glow_title"))
        self.dialog.geometry("400x250")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("glow_title"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("radius"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.radius_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=10,
            number_of_steps=100,
            width=200
        )
        self.radius_slider.set(5)
        self.radius_slider.pack(pady=5)

        ctk.CTkLabel(
            self.dialog,
            text=self._("intensity"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.intensity_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200
        )
        self.intensity_slider.set(0.5)
        self.intensity_slider.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            radius = self.radius_slider.get()
            intensity = self.intensity_slider.get()
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_glow(
                self.processor.image if self.processor.image else self.processor.original_image,
                radius,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("glow_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class InvertDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("invert_title"))
        self.dialog.geometry("400x200")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("invert_colors"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("intensity"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.intensity_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200
        )
        self.intensity_slider.set(1.0)
        self.intensity_slider.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            intensity = self.intensity_slider.get()
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_invert(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("invert_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class EmbossDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("emboss_title"))
        self.dialog.geometry("400x200")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("emboss_effect"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("intensity"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.intensity_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200
        )
        self.intensity_slider.set(1.0)
        self.intensity_slider.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            intensity = self.intensity_slider.get()
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_emboss(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("emboss_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class BlurDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("blur_title"))
        self.dialog.geometry("400x250")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("blur_title"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("blur_radius"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.radius_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=10,
            number_of_steps=100,
            width=200
        )
        self.radius_slider.set(2)
        self.radius_slider.pack(pady=5)

        ctk.CTkLabel(
            self.dialog,
            text=self._("blur_type"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.blur_type = ctk.CTkOptionMenu(
            self.dialog,
            values=[self._("blur_type_gaussian"), self._("blur_type_box")],
            font=("Arial", 14),
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        )
        self.blur_type.set(self._("blur_type_gaussian"))
        self.blur_type.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            radius = self.radius_slider.get()
            type_map = {
                self._("blur_type_gaussian"): "gaussian",
                self._("blur_type_box"): "box"
            }
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_blur(
                self.processor.image if self.processor.image else self.processor.original_image,
                radius,
                type_map[self.blur_type.get()]
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("blur_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class OilPaintingDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("oil_painting_title"))
        self.dialog.geometry("400x250")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("oil_painting_title"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("oil_painting_radius"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.radius_slider = ctk.CTkSlider(
            self.dialog,
            from_=1,
            to=5,
            number_of_steps=4,
            width=200
        )
        self.radius_slider.set(3)
        self.radius_slider.pack(pady=5)

        ctk.CTkLabel(
            self.dialog,
            text=self._("intensity"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.intensity_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200
        )
        self.intensity_slider.set(0.5)
        self.intensity_slider.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            radius = int(self.radius_slider.get())
            intensity = self.intensity_slider.get()
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_oil_painting(
                self.processor.image if self.processor.image else self.processor.original_image,
                radius,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("oil_painting_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class SepiaDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("sepia_title"))
        self.dialog.geometry("400x200")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("sepia_effect"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("intensity"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.intensity_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200
        )
        self.intensity_slider.set(1.0)
        self.intensity_slider.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            intensity = self.intensity_slider.get()
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_sepia(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("sepia_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class GrayscaleDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("grayscale_title"))
        self.dialog.geometry("400x200")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("grayscale_effect"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("intensity"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.intensity_slider = ctk.CTkSlider(
            self.dialog,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200
        )
        self.intensity_slider.set(1.0)
        self.intensity_slider.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            intensity = self.intensity_slider.get()
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_grayscale(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("grayscale_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()

class PosterizeDialog(BaseDialog):
    def create_dialog(self):
        super().create_dialog()
        self.dialog.title(self._("posterize_title"))
        self.dialog.geometry("400x200")

    def setup_widgets(self):
        ctk.CTkLabel(
            self.dialog,
            text=self._("posterize_title"),
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        ).pack(pady=10)

        ctk.CTkLabel(
            self.dialog,
            text=self._("posterize_levels"),
            font=("Arial", 14),
            text_color=self.fg_color
        ).pack(pady=5)
        self.levels_entry = ctk.CTkEntry(
            self.dialog,
            font=("Arial", 14),
            width=200,
            placeholder_text="4",
            text_color=self.fg_color
        )
        self.levels_entry.insert(0, "4")
        self.levels_entry.pack(pady=5)

        ctk.CTkButton(
            self.dialog,
            text=self._("apply"),
            command=self.apply,
            font=("Arial", 14),
            width=200,
            height=40,
            fg_color=self.button_fg_color,
            text_color=self.fg_color
        ).pack(pady=20)

    def apply(self):
        try:
            self.ui.show_loading()
            levels = int(self.levels_entry.get())
            levels = max(2, min(8, levels))
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_posterize(
                self.processor.image if self.processor.image else self.processor.original_image,
                levels
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
            self.dialog.destroy()
        except ValueError as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("invalid_levels", error=str(e)),
                icon="icon.ico"
            )
        except Exception as e:
            CTkMessagebox(
                title=self._("error"),
                message=self._("effect_error", effect=self._("posterize_title").lower(), error=str(e)),
                icon="icon.ico"
            )
        finally:
            self.ui.hide_loading()