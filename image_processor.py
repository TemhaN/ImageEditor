from tkinter import filedialog
from PIL import Image
from color_matcher import ColorMatcher
from noise_effect import NoiseEffect
from effects import Effects

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.image = None
        self.cached_image = None
        self.adjustments = {
            "width": 0, "height": 0, "brightness": 0, "contrast": 0, "saturation": 0,
            "white_balance": 0, "hue": 0, "temperature": 0, "exposure": 0,
            "shadows": 0, "highlights": 0, "blacks": 0, "whites": 0, "warmth": 0,
            "resize_method": "resize", "crop_side": "center"
        }
        self.history = []
        self.history_index = -1
        self.color_matcher = ColorMatcher()
        self.noise_effect = NoiseEffect()
        self.effects = Effects()

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path).convert("RGB")
                self.image = self.original_image.copy()
                self.adjustments["width"], self.adjustments["height"] = self.original_image.size
                self.history = []
                self.history_index = -1
                self.save_to_history()
                return True
            except Exception as e:
                return False
        return False

    def save_image(self):
        if not self.image:
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            try:
                processed_image = self.get_processed_image()
                processed_image.save(file_path)
            except Exception as e:
                print(f"Ошибка при сохранении изображения: {e}")

    def update_adjustment(self, key, value):
        self.adjustments[key] = value
        self.cached_image = None

    def crop_image(self, img, target_width, target_height, crop_side):
        orig_width, orig_height = img.size

        if target_width <= orig_width and target_height <= orig_height:
            if crop_side == "center":
                left = (orig_width - target_width) // 2
                top = (orig_height - target_height) // 2
            elif crop_side == "top":
                left = (orig_width - target_width) // 2
                top = 0
            elif crop_side == "bottom":
                left = (orig_width - target_width) // 2
                top = orig_height - target_height
            elif crop_side == "left":
                left = 0
                top = (orig_height - target_height) // 2
            elif crop_side == "right":
                left = orig_width - target_width
                top = (orig_height - target_height) // 2

            right = left + target_width
            bottom = top + target_height
            img = img.crop((left, top, right, bottom))
            return img

        else:
            if crop_side == "center":
                left = (orig_width - min(target_width, orig_width)) // 2
                top = (orig_height - min(target_height, orig_height)) // 2
            elif crop_side == "top":
                left = (orig_width - min(target_width, orig_width)) // 2
                top = 0
            elif crop_side == "bottom":
                left = (orig_width - min(target_width, orig_width)) // 2
                top = orig_height - min(target_height, orig_height)
            elif crop_side == "left":
                left = 0
                top = (orig_height - min(target_height, orig_height)) // 2
            elif crop_side == "right":
                left = orig_width - min(target_width, orig_width)
                top = (orig_height - min(target_height, orig_height)) // 2

            right = left + min(target_width, orig_width)
            bottom = top + min(target_height, orig_height)
            cropped_img = img.crop((left, top, right, bottom))

            new_img = Image.new("RGB", (target_width, target_height), (0, 0, 0))
            paste_x = (target_width - cropped_img.width) // 2
            paste_y = (target_height - cropped_img.height) // 2
            new_img.paste(cropped_img, (paste_x, paste_y))
            return new_img

    def get_processed_image(self, fast_mode=False):
        if not self.image:
            return None

        if self.cached_image and fast_mode:
            return self.cached_image

        img = self.image.copy()

        method = self.adjustments.get("resize_method", "resize")
        target_width = self.adjustments.get("width", img.width)
        target_height = self.adjustments.get("height", img.height)
        crop_side = self.adjustments.get("crop_side", "center")

        if target_width > 0 and target_height > 0:
            if method == "resize":
                if target_width != img.width or target_height != img.height:
                    img = self.resize_image(img, target_width, target_height)
            elif method == "crop":
                img = self.crop_image(img, target_width, target_height, crop_side)

        if self.adjustments["brightness"] != 0:
            img = self.effects.adjust_brightness(img, self.adjustments["brightness"])

        if self.adjustments["contrast"] != 0:
            img = self.effects.adjust_contrast(img, self.adjustments["contrast"])

        if self.adjustments["saturation"] != 0:
            img = self.effects.adjust_saturation(img, self.adjustments["saturation"])

        if self.adjustments["exposure"] != 0:
            img = self.effects.adjust_exposure(img, self.adjustments["exposure"])

        if self.adjustments["shadows"] != 0:
            img = self.effects.adjust_shadows(img, self.adjustments["shadows"])

        if self.adjustments["highlights"] != 0:
            img = self.effects.adjust_highlights(img, self.adjustments["highlights"])

        if self.adjustments["blacks"] != 0:
            img = self.effects.adjust_blacks(img, self.adjustments["blacks"])

        if self.adjustments["whites"] != 0:
            img = self.effects.adjust_whites(img, self.adjustments["whites"])

        if self.adjustments["hue"] != 0:
            img = self.effects.adjust_hue(img, self.adjustments["hue"])

        if self.adjustments["temperature"] != 0:
            img = self.effects.adjust_temperature(img, self.adjustments["temperature"])

        if self.adjustments["white_balance"] != 0:
            img = self.effects.adjust_white_balance(img, self.adjustments["white_balance"])

        if self.adjustments["warmth"] != 0:
            img = self.effects.adjust_warmth(img, self.adjustments["warmth"])

        self.cached_image = img if fast_mode else None
        return img

    def save_to_history(self):
        if self.image:
            self.history = self.history[:self.history_index + 1]
            self.history.append(self.image.copy())
            self.history_index += 1
            if len(self.history) > 10:
                self.history.pop(0)
                self.history_index -= 1

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.history[self.history_index].copy()
            self.cached_image = None
            return True
        return False

    def match_colors(self):
        self.image = self.color_matcher.match_colors(self.image if self.image else self.original_image)
        self.cached_image = None
        self.save_to_history()

    def apply_noise(self, intensity, noise_type):
        self.image = self.noise_effect.apply_noise(
            self.image if self.image else self.original_image,
            intensity,
            noise_type
        )
        self.cached_image = None
        self.save_to_history()

    def resize_image(self, img, width, height):
        resized_img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
        return resized_img

    def apply_pixelation(self, pixel_size):
        self.image = self.effects.apply_pixelation(
            self.image if self.image else self.original_image,
            pixel_size
        )
        self.cached_image = None
        self.save_to_history()

    def apply_vignette(self, intensity):
        self.image = self.effects.apply_vignette(
            self.image if self.image else self.original_image,
            intensity
        )
        self.cached_image = None
        self.save_to_history()

    def apply_glow(self, intensity, radius):
        self.image = self.effects.apply_glow(
            self.image if self.image else self.original_image,
            radius,
            intensity
        )
        self.cached_image = None
        self.save_to_history()

    def apply_invert(self):
        self.image = self.effects.apply_invert(
            self.image if self.image else self.original_image,
            1.0
        )
        self.cached_image = None
        self.save_to_history()

    def apply_emboss(self, intensity):
        self.image = self.effects.apply_emboss(
            self.image if self.image else self.original_image,
            intensity
        )
        self.cached_image = None
        self.save_to_history()

    def apply_blur(self, radius):
        self.image = self.effects.apply_blur(
            self.image if self.image else self.original_image,
            radius,
            "gaussian"
        )
        self.cached_image = None
        self.save_to_history()

    def apply_oil_painting(self, radius, levels):
        self.image = self.effects.apply_oil_painting(
            self.image if self.image else self.original_image,
            radius,
            levels
        )
        self.cached_image = None
        self.save_to_history()

    def apply_sepia(self, intensity):
        self.image = self.effects.apply_sepia(
            self.image if self.image else self.original_image,
            intensity
        )
        self.cached_image = None
        self.save_to_history()

    def apply_grayscale(self, intensity):
        self.image = self.effects.apply_grayscale(
            self.image if self.image else self.original_image,
            intensity
        )
        self.cached_image = None
        self.save_to_history()

    def apply_posterize(self, bits):
        self.image = self.effects.apply_posterize(
            self.image if self.image else self.original_image,
            bits
        )
        self.cached_image = None
        self.save_to_history()