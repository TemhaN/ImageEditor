import numpy as np
from PIL import Image

class NoiseEffect:
    @staticmethod
    def apply_noise(image, noise_level):
        if noise_level <= 0:
            return image

        img_array = np.array(image).astype(float)

        noise = np.random.normal(0, noise_level * 50, img_array.shape)
        img_array += noise
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)