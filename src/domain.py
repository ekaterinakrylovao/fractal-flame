from dataclasses import dataclass


@dataclass
class Pixel:
    """
    Класс для представления пикселя изображения.

    Атрибуты:
        r (int): Красная составляющая цвета пикселя (от 0 до 255).
        g (int): Зеленая составляющая цвета пикселя (от 0 до 255).
        b (int): Синяя составляющая цвета пикселя (от 0 до 255).
        hit_count (int): Число попаданий в данный пиксель.
    """
    r: int = 0
    g: int = 0
    b: int = 0
    hit_count: int = 0


class FractalImage:
    """
    Класс для представления фрактального изображения.

    Атрибуты:
        width (int): Ширина изображения.
        height (int): Высота изображения.
        data (list[list[Pixel]]): Двумерный список пикселей, представляющий изображение.

    Методы:
        contains(x, y): Проверяет, находятся ли координаты (x, y) внутри изображения.
        pixel(x, y): Возвращает пиксель изображения по заданным координатам (x, y).
    """
    def __init__(self, width: int, height: int):
        """
        Инициализирует фрактальное изображение с заданными размерами.

        Параметры:
            width (int): Ширина изображения.
            height (int): Высота изображения.
        """
        self.width = width
        self.height = height
        self.data = [[Pixel() for _ in range(width)] for _ in range(height)]

    def contains(self, x: int, y: int) -> bool:
        """
        Проверяет, находятся ли координаты (x, y) внутри изображения.

        Параметры:
            x (int): Координата по оси X.
            y (int): Координата по оси Y.

        Returns:
            bool: True, если координаты находятся внутри изображения, иначе False.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def pixel(self, x: int, y: int) -> Pixel:
        """
        Возвращает пиксель изображения по заданным координатам (x, y).

        Параметры:
            x (int): Координата по оси X.
            y (int): Координата по оси Y.

        Returns:
            Pixel: Пиксель изображения в заданных координатах.

        Exceptions:
            ValueError: Если координаты выходят за пределы изображения.
        """
        if self.contains(x, y):
            return self.data[y][x]
        raise ValueError(f"Coordinates ({x}, {y}) are out of bounds")


@dataclass
class Point:
    """
    Класс для представления точки на плоскости.

    Атрибуты:
        x (float): Координата точки по оси X.
        y (float): Координата точки по оси Y.
    """
    x: float
    y: float


@dataclass
class Rect:
    """
    Класс для представления прямоугольной области на плоскости.

    Атрибуты:
        x (float): Координата левого верхнего угла прямоугольника по оси X.
        y (float): Координата левого верхнего угла прямоугольника по оси Y.
        width (float): Ширина прямоугольника.
        height (float): Высота прямоугольника.

    Методы:
        contains(p: Point): Проверяет, лежит ли точка внутри прямоугольника.
    """
    x: float
    y: float
    width: float
    height: float

    def contains(self, p: Point) -> bool:
        """
        Проверяет, лежит ли точка внутри прямоугольника.

        Параметры:
            p (Point): Точка, которая проверяется на попадание в прямоугольник.

        Returns:
            bool: True, если точка лежит внутри прямоугольника, иначе False.
        """
        return self.x <= p.x < self.x + self.width and self.y <= p.y < self.y + self.height
