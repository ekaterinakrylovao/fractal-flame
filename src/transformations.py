import numpy as np
from src.domain import Point


class Transformation:
    """
    Базовый класс для преобразования точек.

    Все подклассы должны реализовать метод __call__, который будет преобразовывать точку.

    Атрибуты:
        None

    Методы:
        __call__(point: Point) -> Point:
            Преобразует точку. Этот метод должен быть переопределен в подклассах.
    """
    def __call__(self, point: Point) -> Point:
        raise NotImplementedError("Subclasses must implement this method")


class SinusoidalTransformation(Transformation):  # Variation 1
    """
    Атрибуты:
        scale_x (float): Масштаб по оси X.
        scale_y (float): Масштаб по оси Y.
    """
    def __init__(self, scale_x=1.0, scale_y=1.0):
        self.scale_x = scale_x
        self.scale_y = scale_y

    def __call__(self, point: Point) -> Point:
        return Point(
            np.sin(self.scale_x * point.x),
            np.sin(self.scale_y * point.y),
        )


class SphericalTransformation(Transformation):  # Variation 2
    def __call__(self, point: Point) -> Point:
        r2 = point.x ** 2 + point.y ** 2
        return Point(point.x / r2, point.y / r2) if r2 != 0 else Point(0, 0)


class SwirlTransformation(Transformation):  # Variation 3
    def __call__(self, point: Point) -> Point:
        r2 = point.x ** 2 + point.y ** 2
        return Point(
            point.x * np.sin(r2) - point.y * np.cos(r2),
            point.x * np.cos(r2) + point.y * np.sin(r2),
        )


class PolarTransformation(Transformation):  # Variation 5
    """
    Атрибуты:
        angle_scale (float): Масштаб угла.
        radius_offset (float): Смещение радиуса.
    """
    def __init__(self, angle_scale=1.0, radius_offset=0.0):
        self.angle_scale = angle_scale
        self.radius_offset = radius_offset

    def __call__(self, point: Point) -> Point:
        r = np.sqrt(point.x ** 2 + point.y ** 2)
        theta = np.arctan2(point.y, point.x)
        return Point(theta / np.pi, r - 1)


class HandkerchiefTransformation(Transformation):  # Variation 6
    def __call__(self, point: Point) -> Point:
        r = np.sqrt(point.x ** 2 + point.y ** 2)
        theta = np.arctan2(point.y, point.x)
        return Point(r * np.sin(theta + r), r * np.cos(theta - r))


class HeartTransformation(Transformation):  # Variation 7
    def __call__(self, point: Point) -> Point:
        r = np.sqrt(point.x ** 2 + point.y ** 2)
        theta = np.arctan2(point.y, point.x)
        return Point(r * np.sin(theta * r), -r * np.cos(theta * r))


class DiscTransformation(Transformation):  # Variation 8
    def __call__(self, point: Point) -> Point:
        r = np.sqrt(point.x ** 2 + point.y ** 2)
        theta = np.arctan2(point.y, point.x)
        return Point(theta / np.pi * np.sin(np.pi * r), theta / np.pi * np.cos(np.pi * r))


class SpiralTransformation(Transformation):  # Variation 9
    def __call__(self, point: Point) -> Point:
        r = np.sqrt(point.x ** 2 + point.y ** 2)
        theta = np.arctan2(point.y, point.x)
        return Point(
            (np.cos(theta) + np.sin(r)) / r if r != 0 else 0,
            (np.sin(theta) - np.cos(r)) / r if r != 0 else 0,
        )


class HyperbolicTransformation(Transformation):  # Variation 10
    """
    Атрибуты:
        scale (float): Масштаб.
        jitter (float): Параметр для случайных отклонений.
    """
    def __init__(self, scale=1.0, jitter=0.01):
        self.scale = scale
        self.jitter = jitter

    def __call__(self, point: Point) -> Point:
        r = np.sqrt(point.x ** 2 + point.y ** 2)
        theta = np.arctan2(point.y, point.x)
        return Point(
            np.sin(theta) / r if r != 0 else 0,
            np.cos(theta) * r,
        )


class DiamondTransformation(Transformation):  # Variation 11
    """
    Атрибуты:
        scale (float): Масштаб.
        jitter (float): Параметр для случайных отклонений.
    """
    def __init__(self, scale=1.0, jitter=0.07):
        self.scale = scale
        self.jitter = jitter

    def __call__(self, point: Point) -> Point:
        r = np.sqrt(point.x ** 2 + point.y ** 2)
        theta = np.arctan2(point.y, point.x)
        x = self.scale * np.sin(theta) * np.cos(r)
        y = self.scale * np.cos(theta) * np.sin(r)
        return Point(x, y)


# === Interesting section ===
class PopcornTransformation(Transformation):  # Variation 17
    """
    Атрибуты:
        c (float): Параметр для синусоидальной функции по оси X.
        d (float): Параметр для синусоидальной функции по оси Y.
    """
    def __init__(self, c=0.5, d=0.5):
        self.c = c
        self.d = d

    def __call__(self, point: Point) -> Point:
        new_x = point.x + self.c * np.sin(np.tan(3 * point.y))
        new_y = point.y + self.d * np.sin(np.tan(3 * point.x))
        return Point(new_x, new_y)


class PDJTransformation(Transformation):  # Variation 24
    """
    Атрибуты:
        a, b, c, d (float): Параметры для синусоидальных и косинусоидальных функций.
    """
    def __init__(self, a=1.0, b=1.0, c=1.0, d=1.0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __call__(self, point: Point) -> Point:
        new_x = np.sin(self.a * point.y) - np.cos(self.b * point.x)
        new_y = np.sin(self.c * point.x) - np.cos(self.d * point.y)
        return Point(new_x, new_y)


class CurlTransformation(Transformation):  # Variation 39
    """
    Атрибуты:
        p (float): Параметр, влияющий на масштаб по оси X.
        q (float): Параметр, влияющий на масштаб по оси Y.
    """
    def __init__(self, p=0.5, q=0.5):
        self.p = p
        self.q = q

    def __call__(self, point: Point) -> Point:
        denom = point.x ** 2 + point.y ** 2 + 1e-6  # Защита от деления на ноль
        new_x = (point.x + self.p * point.y) / denom
        new_y = (point.y - self.q * point.x) / denom
        return Point(new_x, new_y)
