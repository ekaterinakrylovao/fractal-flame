import random
import numpy as np
from src.domain import FractalImage, Rect, Point
from src.transformations import Transformation


def render(
    canvas: FractalImage,
    world: Rect,
    variations: list[Transformation],
    samples: int,
    iter_per_sample: int,
    seed: int,
    symmetry: int = 1,
):
    """
    Рендерит фрактальное изображение с учётом симметрии и преобразований.

    Параметры:
        canvas (FractalImage): Объект фрактального изображения, на котором будет происходить рендеринг.
        world (Rect): Прямоугольная область, в пределах которой генерируются точки.
        variations (list[Transformation]): Список преобразований, применяемых к точкам.
        samples (int): Количество генерируемых точек.
        iter_per_sample (int): Количество итераций для каждой точки.
        seed (int): Значение для генератора случайных чисел, чтобы обеспечить стабильность.
        symmetry (int): Количество симметрий (по умолчанию 1, без симметрии).

    Returns:
        None. Изменяет состояние объекта `canvas` напрямую.
    """
    random.seed(seed)
    for _ in range(samples):
        # Генерация случайной точки в пределах области
        pw = Point(
            random.uniform(world.x, world.x + world.width),
            random.uniform(world.y, world.y + world.height),
        )
        for _ in range(iter_per_sample):
            # Применение случайного преобразования к точке
            variation = random.choice(variations)
            pw = variation(pw)

            for s in range(symmetry):
                # Применение симметрии
                theta2 = s * (2 * np.pi / symmetry)
                pwr = Point(
                    pw.x * np.cos(theta2) - pw.y * np.sin(theta2),
                    pw.x * np.sin(theta2) + pw.y * np.cos(theta2),
                )
                if not world.contains(pwr):
                    continue

                # Переводим точку в координаты пикселя на холсте
                x = int((pwr.x - world.x) / world.width * canvas.width)
                y = int((pwr.y - world.y) / world.height * canvas.height)
                if canvas.contains(x, y):
                    pixel = canvas.pixel(x, y)
                    pixel.hit_count += 1
                    pixel.r = min(255, pixel.r + 10)
                    pixel.g = min(255, pixel.g + 5)
                    pixel.b = min(255, pixel.b + 5)


def render_single(config, width, height):
    """
    Рендерит одно фрактальное изображение с использованием заданной конфигурации.

    Параметры:
        config: Объект конфигурации, содержащий параметры мира, преобразования, количество образцов,
                                                                                    итераций и симметрии.
        width (int): Ширина изображения.
        height (int): Высота изображения.

    Returns:
        FractalImage: Отрендеренное изображение.
    """
    canvas = FractalImage(width, height)
    render(
        canvas=canvas,
        world=config.world,
        variations=[config.transformation],
        samples=config.samples,
        iter_per_sample=config.iterations,
        seed=42,
        symmetry=config.symmetry,
    )
    return canvas


def merge_canvases(target, sources):
    """
    Сливает несколько холстов в один, накапливая данные пикселей.

    Параметры:
        target (FractalImage): Целевой холст, в который будут добавляться данные.
        sources (list[FractalImage]): Список исходных холстов, которые будут слиты в целевой.

    Returns:
        None. Изменяет целевой объект `target` напрямую.
    """
    for canvas in sources:
        for y in range(target.height):
            for x in range(target.width):
                target_pixel = target.pixel(x, y)
                source_pixel = canvas.pixel(x, y)
                target_pixel.hit_count += source_pixel.hit_count
                target_pixel.r = min(255, target_pixel.r + source_pixel.r)
                target_pixel.g = min(255, target_pixel.g + source_pixel.g)
                target_pixel.b = min(255, target_pixel.b + source_pixel.b)
