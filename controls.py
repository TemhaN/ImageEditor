import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class ControlPanel:
    def __init__(self, parent, processor, update_callback, ui):
        self.parent = parent
        self.processor = processor
        self.update_callback = update_callback
        self.ui = ui
        self.bg_color = "#2b2b2b" if ui.config["theme"] == "dark" else "#ffffff"
        self.fg_color = "#ffffff" if ui.config["theme"] == "dark" else "#000000"
        self.button_fg_color = "#3b8ed0" if ui.config["theme"] == "dark" else "#1f6aa5"
        self.button_text_color = "#ffffff"
        self.tab_names = {}
        self.create_controls()

    def create_controls(self):
        self.tabview = ctk.CTkTabview(
            self.parent,
            fg_color=self.bg_color,
            segmented_button_fg_color=self.button_fg_color,
            segmented_button_selected_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            segmented_button_selected_hover_color="#7bb0e0" if self.ui.config["theme"] == "dark" else "#3a8cd4",
            text_color=self.button_text_color
        )
        self.tabview.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

        self.tab_names["basic_tab"] = self.ui._("basic_tab")
        self.tab_names["colors_tab"] = self.ui._("colors_tab")
        self.tab_names["advanced_tab"] = self.ui._("advanced_tab")

        self.tab_basic = self.tabview.add(self.tab_names["basic_tab"])
        self.tab_colors = self.tabview.add(self.tab_names["colors_tab"])
        self.tab_advanced = self.tabview.add(self.tab_names["advanced_tab"])

        self.create_basic_controls(self.tab_basic)
        self.create_color_controls(self.tab_colors)
        self.create_advanced_controls(self.tab_advanced)

        self.reset_button = ctk.CTkButton(
            self.parent,
            text="",
            command=self.reset_all,
            font=("Arial", 12),
            width=150,
            height=30,
            fg_color=self.button_fg_color,
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf"
        )
        self.reset_button.pack(pady=5)

        self.update_texts()

    def create_basic_controls(self, parent):
        scrollable_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.bg_color
        )
        scrollable_frame.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

        self.brightness_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.brightness_label.pack(pady=2)
        self.brightness_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_brightness,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(pady=2)

        self.contrast_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.contrast_label.pack(pady=2)
        self.contrast_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_contrast,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.contrast_slider.set(0)
        self.contrast_slider.pack(pady=2)

        self.saturation_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.saturation_label.pack(pady=2)
        self.saturation_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_saturation,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.saturation_slider.set(0)
        self.saturation_slider.pack(pady=2)

    def create_color_controls(self, parent):
        scrollable_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.bg_color
        )
        scrollable_frame.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

        self.white_balance_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.white_balance_label.pack(pady=2)
        self.white_balance_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_white_balance,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.white_balance_slider.set(0)
        self.white_balance_slider.pack(pady=2)

        self.hue_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.hue_label.pack(pady=2)
        self.hue_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_hue,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.hue_slider.set(0)
        self.hue_slider.pack(pady=2)

        self.temperature_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.temperature_label.pack(pady=2)
        self.temperature_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_temperature,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.temperature_slider.set(0)
        self.temperature_slider.pack(pady=2)

        self.exposure_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.exposure_label.pack(pady=2)
        self.exposure_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_exposure,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.exposure_slider.set(0)
        self.exposure_slider.pack(pady=2)

        self.shadows_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.shadows_label.pack(pady=2)
        self.shadows_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_shadows,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.shadows_slider.set(0)
        self.shadows_slider.pack(pady=2)

        self.highlights_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.highlights_label.pack(pady=2)
        self.highlights_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_highlights,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.highlights_slider.set(0)
        self.highlights_slider.pack(pady=2)

        self.blacks_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.blacks_label.pack(pady=2)
        self.blacks_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_blacks,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.blacks_slider.set(0)
        self.blacks_slider.pack(pady=2)

        self.whites_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.whites_label.pack(pady=2)
        self.whites_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_whites,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.whites_slider.set(0)
        self.whites_slider.pack(pady=2)

        self.warmth_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.warmth_label.pack(pady=2)
        self.warmth_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=-1,
            to=1,
            number_of_steps=200,
            command=self.update_warmth,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.warmth_slider.set(0)
        self.warmth_slider.pack(pady=2)

    def create_advanced_controls(self, parent):
        scrollable_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.bg_color
        )
        scrollable_frame.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

        self.details_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.details_label.pack(pady=2)
        self.details_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.details_slider.set(0.5)
        self.details_slider.pack(pady=2)
        self.apply_details_button = ctk.CTkButton(
            scrollable_frame,
            text="",
            command=lambda: self.apply_details(self.details_slider.get()),
            font=("Arial", 12),
            width=150,
            height=30,
            fg_color=self.button_fg_color,
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf"
        )
        self.apply_details_button.pack(pady=2)

        self.sharpen_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.sharpen_label.pack(pady=2)
        self.sharpen_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.sharpen_slider.set(0.5)
        self.sharpen_slider.pack(pady=2)
        self.apply_sharpen_button = ctk.CTkButton(
            scrollable_frame,
            text="",
            command=lambda: self.apply_sharpen(self.sharpen_slider.get()),
            font=("Arial", 12),
            width=150,
            height=30,
            fg_color=self.button_fg_color,
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf"
        )
        self.apply_sharpen_button.pack(pady=2)

        self.noise_reduction_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.noise_reduction_label.pack(pady=2)
        self.noise_reduction_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.noise_reduction_slider.set(0.5)
        self.noise_reduction_slider.pack(pady=2)
        self.apply_noise_reduction_button = ctk.CTkButton(
            scrollable_frame,
            text="",
            command=lambda: self.apply_noise_reduction(self.noise_reduction_slider.get()),
            font=("Arial", 12),
            width=150,
            height=30,
            fg_color=self.button_fg_color,
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf"
        )
        self.apply_noise_reduction_button.pack(pady=2)

        self.smoothing_label = ctk.CTkLabel(
            scrollable_frame,
            text="",
            font=("Arial", 12),
            text_color=self.fg_color
        )
        self.smoothing_label.pack(pady=2)
        self.smoothing_slider = ctk.CTkSlider(
            scrollable_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            width=150,
            fg_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf",
            progress_color=self.button_fg_color
        )
        self.smoothing_slider.set(0.5)
        self.smoothing_slider.pack(pady=2)
        self.apply_smoothing_button = ctk.CTkButton(
            scrollable_frame,
            text="",
            command=lambda: self.apply_smoothing(self.smoothing_slider.get()),
            font=("Arial", 12),
            width=150,
            height=30,
            fg_color=self.button_fg_color,
            text_color=self.button_text_color,
            hover_color="#5a9bd4" if self.ui.config["theme"] == "dark" else "#2a7bbf"
        )
        self.apply_smoothing_button.pack(pady=2)

    def update_texts(self):
        self.brightness_label.configure(text=self.ui._("brightness"))
        self.contrast_label.configure(text=self.ui._("contrast"))
        self.saturation_label.configure(text=self.ui._("saturation"))
        self.white_balance_label.configure(text=self.ui._("white_balance"))
        self.hue_label.configure(text=self.ui._("hue"))
        self.temperature_label.configure(text=self.ui._("temperature"))
        self.exposure_label.configure(text=self.ui._("exposure"))
        self.shadows_label.configure(text=self.ui._("shadows"))
        self.highlights_label.configure(text=self.ui._("highlights"))
        self.blacks_label.configure(text=self.ui._("blacks"))
        self.whites_label.configure(text=self.ui._("whites"))
        self.warmth_label.configure(text=self.ui._("warmth"))
        self.details_label.configure(text=self.ui._("details"))
        self.sharpen_label.configure(text=self.ui._("sharpen"))
        self.noise_reduction_label.configure(text=self.ui._("noise_reduction"))
        self.smoothing_label.configure(text=self.ui._("smoothing"))
        self.apply_details_button.configure(text=self.ui._("apply_details"))
        self.apply_sharpen_button.configure(text=self.ui._("apply_sharpen"))
        self.apply_noise_reduction_button.configure(text=self.ui._("apply_noise_reduction"))
        self.apply_smoothing_button.configure(text=self.ui._("apply_smoothing"))
        self.reset_button.configure(text=self.ui._("reset_all"))

    def update_brightness(self, value):
        self.processor.update_adjustment("brightness", value)
        self.update_callback(fast_mode=True)

    def update_contrast(self, value):
        self.processor.update_adjustment("contrast", value)
        self.update_callback(fast_mode=True)

    def update_saturation(self, value):
        self.processor.update_adjustment("saturation", value)
        self.update_callback(fast_mode=True)

    def update_white_balance(self, value):
        self.processor.update_adjustment("white_balance", value)
        self.update_callback(fast_mode=True)

    def update_hue(self, value):
        self.processor.update_adjustment("hue", value)
        self.update_callback(fast_mode=True)

    def update_temperature(self, value):
        self.processor.update_adjustment("temperature", value)
        self.update_callback(fast_mode=True)

    def update_exposure(self, value):
        self.processor.update_adjustment("exposure", value)
        self.update_callback(fast_mode=True)

    def update_shadows(self, value):
        self.processor.update_adjustment("shadows", value)
        self.update_callback(fast_mode=True)

    def update_highlights(self, value):
        self.processor.update_adjustment("highlights", value)
        self.update_callback(fast_mode=True)

    def update_blacks(self, value):
        self.processor.update_adjustment("blacks", value)
        self.update_callback(fast_mode=True)

    def update_whites(self, value):
        self.processor.update_adjustment("whites", value)
        self.update_callback(fast_mode=True)

    def update_warmth(self, value):
        self.processor.update_adjustment("warmth", value)
        self.update_callback(fast_mode=True)

    def apply_details(self, intensity):
        try:
            self.parent.winfo_toplevel().event_generate("<<ShowLoading>>")
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self.ui._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_details(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
        except Exception as e:
            CTkMessagebox(
                title=self.ui._("error"),
                message=self.ui._("effect_error", effect=self.ui._("details"), error=str(e)),
                icon="cancel"
            )
        finally:
            self.ui.hide_loading()

    def apply_sharpen(self, intensity):
        try:
            self.parent.winfo_toplevel().event_generate("<<ShowLoading>>")
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self.ui._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_sharpen(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
        except Exception as e:
            CTkMessagebox(
                title=self.ui._("error"),
                message=self.ui._("effect_error", effect=self.ui._("sharpen"), error=str(e)),
                icon="cancel"
            )
        finally:
            self.ui.hide_loading()

    def apply_noise_reduction(self, intensity):
        try:
            self.parent.winfo_toplevel().event_generate("<<ShowLoading>>")
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self.ui._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_noise_reduction(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
        except Exception as e:
            CTkMessagebox(
                title=self.ui._("error"),
                message=self.ui._("effect_error", effect=self.ui._("noise_reduction"), error=str(e)),
                icon="cancel"
            )
        finally:
            self.ui.hide_loading()

    def apply_smoothing(self, intensity):
        try:
            self.parent.winfo_toplevel().event_generate("<<ShowLoading>>")
            if not self.processor.image and not self.processor.original_image:
                raise ValueError(self.ui._("image_not_loaded"))
            self.processor.image = self.processor.effects.apply_smoothing(
                self.processor.image if self.processor.image else self.processor.original_image,
                intensity
            )
            self.processor.cached_image = None
            self.processor.save_to_history()
            self.update_callback(fast_mode=False)
        except Exception as e:
            CTkMessagebox(
                title=self.ui._("error"),
                message=self.ui._("effect_error", effect=self.ui._("smoothing"), error=str(e)),
                icon="cancel"
            )
        finally:
            self.ui.hide_loading()

    def reset_all(self):
        self.brightness_slider.set(0)
        self.contrast_slider.set(0)
        self.saturation_slider.set(0)
        self.white_balance_slider.set(0)
        self.hue_slider.set(0)
        self.temperature_slider.set(0)
        self.exposure_slider.set(0)
        self.shadows_slider.set(0)
        self.highlights_slider.set(0)
        self.blacks_slider.set(0)
        self.whites_slider.set(0)
        self.warmth_slider.set(0)
        self.details_slider.set(0.5)
        self.sharpen_slider.set(0.5)
        self.noise_reduction_slider.set(0.5)
        self.smoothing_slider.set(0.5)
        self.processor.reset_adjustments()
        self.update_callback(fast_mode=True)