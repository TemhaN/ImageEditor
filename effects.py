from PIL import Image, ImageFilter, ImageEnhance, ImageColor
import numpy as np
import cv2

class Effects:
    @staticmethod
    def apply_noise(image, noise_level, noise_type):
        img_array = np.array(image)
        if noise_type == "gaussian":
            noise = np.random.normal(0, noise_level * 255, img_array.shape).astype(np.uint8)
            noise = np.clip(noise, 0, 255)
            noisy_img = cv2.add(img_array, noise)
        elif noise_type == "salt_pepper":
            noise = np.random.random(img_array.shape[:2])
            noisy_img = img_array.copy()
            noisy_img[noise < noise_level / 2] = 0
            noisy_img[noise > 1 - noise_level / 2] = 255
        return Image.fromarray(noisy_img)

    @staticmethod
    def apply_pixelation(image, block_size):
        img = image.copy()
        width, height = img.size
        img = img.resize((width // block_size, height // block_size), Image.Resampling.NEAREST)
        img = img.resize((width, height), Image.Resampling.NEAREST)
        return img

    @staticmethod
    def apply_vignette(image, intensity):
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        center_x, center_y = width / 2, height / 2
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        vignette = 1 - (distance / max_distance) * intensity
        vignette = np.clip(vignette, 0, 1)
        if len(img_array.shape) == 3:
            vignette = vignette[:, :, np.newaxis]
        vignette_img = (img_array * vignette).astype(np.uint8)
        return Image.fromarray(vignette_img)

    @staticmethod
    def apply_glow(image, radius, intensity):
        img = image.copy()
        blurred = img.filter(ImageFilter.GaussianBlur(radius=radius))
        img_array = np.array(img)
        blurred_array = np.array(blurred)
        glow = (blurred_array + img_array * intensity).clip(0, 255).astype(np.uint8)
        return Image.fromarray(glow)

    @staticmethod
    def apply_invert(image, intensity):
        img_array = np.array(image)
        inverted = 255 - img_array
        result = (img_array * (1 - intensity) + inverted * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def apply_emboss(image, intensity):
        img = image.copy()
        embossed = img.filter(ImageFilter.EMBOSS)
        img_array = np.array(img)
        embossed_array = np.array(embossed)
        result = (img_array * (1 - intensity) + embossed_array * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def apply_blur(image, radius, blur_type):
        img = image.copy()
        if blur_type == "gaussian":
            return img.filter(ImageFilter.GaussianBlur(radius=radius))
        elif blur_type == "box":
            return img.filter(ImageFilter.BoxBlur(radius=radius))

    @staticmethod
    def apply_oil_painting(image, radius, intensity):
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        result = img_array.copy()
        for y in range(radius, height - radius):
            for x in range(radius, width - radius):
                region = img_array[y - radius:y + radius + 1, x - radius:x + radius + 1]
                avg_color = np.mean(region, axis=(0, 1)).astype(np.uint8)
                result[y, x] = (result[y, x] * (1 - intensity) + avg_color * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def apply_sepia(image, intensity):
        img_array = np.array(image)
        sepia_matrix = np.array([[0.393, 0.769, 0.189],
                                 [0.349, 0.686, 0.168],
                                 [0.272, 0.534, 0.131]])
        sepia_img = np.dot(img_array[..., :3], sepia_matrix.T).clip(0, 255).astype(np.uint8)
        result = (img_array * (1 - intensity) + sepia_img * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def apply_grayscale(image, intensity):
        img = image.copy()
        grayscale = img.convert("L").convert("RGB")
        img_array = np.array(img)
        grayscale_array = np.array(grayscale)
        result = (img_array * (1 - intensity) + grayscale_array * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def apply_posterize(image, levels):
        img = image.copy()
        return img.convert("P", palette=Image.Palette.ADAPTIVE, colors=levels).convert("RGB")

    @staticmethod
    def apply_details(image, intensity):
        img = image.copy()
        enhanced = img.filter(ImageFilter.UnsharpMask(radius=2, percent=int(150 * intensity), threshold=3))
        img_array = np.array(img)
        enhanced_array = np.array(enhanced)
        result = (img_array * (1 - intensity) + enhanced_array * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def apply_sharpen(image, intensity):
        img = image.copy()
        sharpened = img.filter(ImageFilter.SHARPEN)
        img_array = np.array(img)
        sharpened_array = np.array(sharpened)
        result = (img_array * (1 - intensity) + sharpened_array * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def apply_noise_reduction(image, intensity):
        img = image.copy()
        img_array = np.array(img)
        kernel_size = 3 + int(4 * intensity)
        kernel_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
        denoised = cv2.medianBlur(img_array, kernel_size)
        result = (img_array * (1 - intensity) + denoised * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def apply_smoothing(image, intensity):
        img = image.copy()
        radius = intensity * 5
        smoothed = img.filter(ImageFilter.GaussianBlur(radius=radius))
        img_array = np.array(img)
        smoothed_array = np.array(smoothed)
        result = (img_array * (1 - intensity) + smoothed_array * intensity).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def adjust_brightness(image, factor):
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(1 + factor)

    @staticmethod
    def adjust_contrast(image, factor):
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(1 + factor)

    @staticmethod
    def adjust_saturation(image, factor):
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(1 + factor)

    @staticmethod
    def adjust_white_balance(image, factor):
        img_array = np.array(image).astype(np.float32)
        if factor > 0:
            img_array[:, :, 2] = img_array[:, :, 2] * (1 + factor)
            img_array[:, :, 0] = img_array[:, :, 0] * (1 - factor)
        else:
            img_array[:, :, 0] = img_array[:, :, 0] * (1 - factor)
            img_array[:, :, 2] = img_array[:, :, 2] * (1 + factor)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)

    @staticmethod
    def adjust_hue(image, factor):
        img_array = np.array(image.convert("HSV")).astype(np.float32)
        img_array[:, :, 0] = (img_array[:, :, 0] + factor * 180) % 360
        img_array = img_array.astype(np.uint8)
        return Image.fromarray(img_array, mode="HSV").convert("RGB")

    @staticmethod
    def adjust_temperature(image, factor):
        img_array = np.array(image).astype(np.float32)
        if factor > 0:
            img_array[:, :, 2] = img_array[:, :, 2] * (1 + factor)
            img_array[:, :, 0] = img_array[:, :, 0] * (1 - factor * 0.5)
        else:
            img_array[:, :, 0] = img_array[:, :, 0] * (1 - factor)
            img_array[:, :, 2] = img_array[:, :, 2] * (1 + factor * 0.5)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)

    @staticmethod
    def adjust_exposure(image, factor):
        img_array = np.array(image).astype(np.float32)
        img_array = img_array * (1 + factor)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)

    @staticmethod
    def adjust_shadows(image, factor):
        img_array = np.array(image).astype(np.float32)
        mask = img_array < 128
        if factor > 0:
            img_array[mask] = img_array[mask] * (1 + factor)
        else:
            img_array[mask] = img_array[mask] * (1 + factor)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)

    @staticmethod
    def adjust_highlights(image, factor):
        img_array = np.array(image).astype(np.float32)
        mask = img_array > 128
        if factor > 0:
            img_array[mask] = img_array[mask] * (1 + factor)
        else:
            img_array[mask] = img_array[mask] * (1 + factor)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)

    @staticmethod
    def adjust_blacks(image, factor):
        img_array = np.array(image).astype(np.float32)
        img_array = img_array + factor * 50
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)

    @staticmethod
    def adjust_whites(image, factor):
        img_array = np.array(image).astype(np.float32)
        img_array = img_array + factor * 50
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)

    @staticmethod
    def adjust_warmth(image, factor):
        img_array = np.array(image).astype(np.float32)
        if factor > 0:
            img_array[:, :, 2] = img_array[:, :, 2] * (1 + factor)
            img_array[:, :, 1] = img_array[:, :, 1] * (1 + factor * 0.5)
        else:
            img_array[:, :, 0] = img_array[:, :, 0] * (1 - factor)
            img_array[:, :, 1] = img_array[:, :, 1] * (1 - factor * 0.5)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array)

    @staticmethod
    def match_colors(source, reference):
        source_array = np.array(source).astype(np.float32)
        reference_array = np.array(reference).astype(np.float32)
        source_mean = np.mean(source_array, axis=(0, 1))
        reference_mean = np.mean(reference_array, axis=(0, 1))
        source_std = np.std(source_array, axis=(0, 1))
        reference_std = np.std(reference_array, axis=(0, 1))
        source_array = (source_array - source_mean) / source_std
        source_array = source_array * reference_std + reference_mean
        source_array = np.clip(source_array, 0, 255).astype(np.uint8)
        return Image.fromarray(source_array)