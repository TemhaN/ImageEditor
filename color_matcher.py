from PIL import Image
import numpy as np
from tkinter import filedialog, messagebox

class ColorMatcher:
    def __init__(self):
        self.source_image = None
        self.reference_image = None

    def match_colors(self, source_image):
        self.source_image = source_image.convert("RGB")
        reference_path = filedialog.askopenfilename(
            title="Выберите референтное изображение",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not reference_path:
            return None

        try:
            self.reference_image = Image.open(reference_path).convert("RGB")
            src_array = np.array(self.source_image).astype(float)
            ref_array = np.array(self.reference_image).astype(float)
            src_array = src_array / 255.0
            ref_array = ref_array / 255.0
            src_mean = np.mean(src_array, axis=(0, 1))
            src_std = np.std(src_array, axis=(0, 1))
            ref_mean = np.mean(ref_array, axis=(0, 1))
            ref_std = np.std(ref_array, axis=(0, 1))
            adjusted = np.zeros_like(src_array)
            for channel in range(3):
                if src_std[channel] != 0:
                    adjusted[:, :, channel] = (src_array[:, :, channel] - src_mean[channel]) * (ref_std[channel] / src_std[channel]) + ref_mean[channel]
                else:
                    adjusted[:, :, channel] = src_array[:, :, channel]
            adjusted = np.clip(adjusted * 255, 0, 255).astype(np.uint8)
            result = Image.fromarray(adjusted)
            messagebox.showinfo("Успех", "Цветокоррекция по образцу выполнена!")
            return result
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить цветокоррекцию: {str(e)}")
            return None