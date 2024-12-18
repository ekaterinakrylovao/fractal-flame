from PIL import Image
from pathlib import Path
from src.domain import FractalImage
from src.processors import ImageProcessor


class ImageUtils:
    """
    Утилиты для работы с изображениями фракталов.

    Этот класс предоставляет статические методы для сохранения фрактальных изображений
    в различные форматы и для применения обработки изображений перед сохранением.

    Методы:
        save(image: FractalImage, filename: Path, format: str = "PNG"):
            Сохраняет изображение фрактала в файл с указанным именем и форматом.

        save_with_processing(image: FractalImage, processor: ImageProcessor, filename: Path, format: str = "PNG"):
            Применяет обработку изображения с помощью указанного процессора и сохраняет результат.
    """

    @staticmethod
    def save(image: FractalImage, filename: Path, format: str = "PNG"):
        """
        Сохраняет изображение фрактала в файл.

        Параметры:
            image (FractalImage): Изображение фрактала, которое необходимо сохранить.
            filename (Path): Путь к файлу, в который будет сохранено изображение.
            format (str, по умолчанию "PNG"): Формат изображения. Например, "PNG" или "JPEG".

        Примечание:
            Каждый пиксель в изображении сохраняется с использованием цветовых значений RGB.
        """
        img = Image.new("RGB", (image.width, image.height))
        for y in range(image.height):
            for x in range(image.width):
                pixel = image.pixel(x, y)
                img.putpixel((x, y), (pixel.r, pixel.g, pixel.b))
        img.save(filename, format=format)

    @staticmethod
    def save_with_processing(image: FractalImage, processor: ImageProcessor, filename: Path, format: str = "PNG"):
        """
        Применяет обработку изображения и сохраняет результат.

        Параметры:
            image (FractalImage): Изображение фрактала, которое необходимо сохранить.
            processor (ImageProcessor): Процессор, который будет применен для обработки изображения.
            filename (Path): Путь к файлу, в который будет сохранено обработанное изображение.
            format (str, по умолчанию "PNG"): Формат изображения. Например, "PNG" или "JPEG".
        """
        processor.process(image)
        ImageUtils.save(image, filename, format)
