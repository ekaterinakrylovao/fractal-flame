"""
Модуль для обработки изображений фракталов с использованием методов коррекции.
"""
import matplotlib
import numpy as np

from src.domain import FractalImage


class ImageProcessor:
    """
    Абстрактный класс для обработки изображений фракталов.

    Этот класс задаёт интерфейс для всех процессоров, которые могут обрабатывать
    изображения типа FractalImage. Конкретные реализации должны переопределять
    метод process.

    Методы:
        process(image: FractalImage): Метод для обработки изображения, должен быть реализован в дочерних классах.
    """
    def process(self, image: FractalImage):
        raise NotImplementedError("Subclasses must implement this method")


class GammaCorrectionProcessor(ImageProcessor):
    """
    Устаревший класс для применения гамма-коррекции.

    Этот класс применяет гамма-коррекцию ко всем пикселям изображения. Использует простую
    формулу для коррекции яркости пикселей. **Важно:** Этот класс является пережитком
    прошлого и не используется в текущей версии программы.

    Параметры:
        gamma (float): Параметр гамма-коррекции (по умолчанию 2.0).

    Методы:
        process(image: FractalImage): Применяет гамма-коррекцию ко всем пикселям изображения.
    """
    def __init__(self, gamma: float = 2.0):
        self.gamma = gamma

    def process(self, image: FractalImage):
        """
        Применяет гамма-коррекцию ко всем пикселям изображения.

        Каждый пиксель (r, g, b) преобразуется по формуле гамма-коррекции:
        value' = (value / 255) ** (1 / gamma) * 255.

        Параметры:
            image (FractalImage): Изображение для обработки.
        """
        for row in image.data:
            for pixel in row:
                pixel.r = int((pixel.r / 255) ** (1 / self.gamma) * 255)
                pixel.g = int((pixel.g / 255) ** (1 / self.gamma) * 255)
                pixel.b = int((pixel.b / 255) ** (1 / self.gamma) * 255)


class LogGammaCorrectionProcessor(ImageProcessor):
    """
    Класс для применения логарифмической гамма-коррекции с использованием цветовой карты.

    Этот процессор нормализует значение пикселя, применяет логарифмическую коррекцию,
    а затем гамма-коррекцию. После этого цвет каждого пикселя определяется с использованием
    цветовой карты и корректируется по яркости.

    Параметры:
        gamma (float): Параметр гамма-коррекции (по умолчанию 2.0).
        scale (float): Масштабный коэффициент для логарифмической коррекции (по умолчанию 1.0).
        colormap (str): Название цветовой карты из matplotlib (по умолчанию "inferno").
        brightness_shift (float): Смещение яркости для повышения вариативности цветов (по умолчанию 0.1).

    Методы:
        process(image: FractalImage): Применяет логарифмическую гамма-коррекцию и окрашивает изображение.
    """
    def __init__(self, gamma: float = 2.0, scale: float = 1.0, colormap="inferno", brightness_shift=0.1):
        """
        Инициализирует процессор с параметрами для логарифмической гамма-коррекции.

        Параметры:
            gamma (float): Параметр гамма-коррекции.
            scale (float): Масштаб для логарифмической коррекции.
            colormap (str): Название цветовой карты (по умолчанию "inferno").
            brightness_shift (float): Смещение яркости для окрашивания (по умолчанию 0.1).
        """
        self.gamma = gamma
        self.scale = scale
        self.colormap = matplotlib.colormaps.get_cmap(colormap)
        self.brightness_shift = brightness_shift

    def process(self, image: FractalImage):
        """
        Применяет логарифмическую гамма-коррекцию и окрашивает изображение с использованием цветовой карты.

        Для каждого пикселя:
        1. Нормализует hit_count пикселя.
        2. Применяет логарифмическую коррекцию.
        3. Применяет гамма-коррекцию.
        4. Применяет цветовую карту и корректирует яркость.

        Параметры:
            image (FractalImage): Изображение для обработки.
        """
        max_hit_count = max(pixel.hit_count for row in image.data for pixel in row)
        if max_hit_count == 0:
            return

        for row in image.data:
            for pixel in row:
                normalized_hit = pixel.hit_count / max_hit_count

                corrected_hit = np.log1p(normalized_hit * self.scale)

                gamma_corrected_hit = corrected_hit ** (1 / self.gamma)

                color = self.colormap(gamma_corrected_hit + self.brightness_shift)

                pixel.r = int(min(255, color[0] * 255))
                pixel.g = int(min(255, color[1] * 255))
                pixel.b = int(min(255, color[2] * 255))
