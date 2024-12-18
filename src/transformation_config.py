from typing import NamedTuple

from src.domain import Rect
from src.transformations import Transformation


class TransformationConfig(NamedTuple):
    """
    Конфигурация для применения трансформаций.

    Этот класс хранит параметры, необходимые для применения трансформаций к точкам на плоскости.
    Включает информацию о самой трансформации, количестве итераций, мире координат, количестве выборок
    и симметрии, которая применяется при отрисовке.

    Атрибуты:
        transformation (Transformation): Трансформация, которая будет применена к точкам.
        iterations (int): Количество итераций для каждой выборки.
        world (Rect): Прямоугольник, определяющий область, в которой будут размещаться точки.
        samples (int): Количество выборок (точек), которые будут преобразованы.
        symmetry (int, по умолчанию 1): Число симметричных повторений каждой трансформированной точки.
    """
    transformation: Transformation
    iterations: int
    world: Rect
    samples: int
    symmetry: int = 1
