"""
Тест рендеринга изображений фракталов для различных трансформаций.

Описание:
Этот тест проверяет корректность генерации изображений фракталов для ряда трансформаций.
Для каждой трансформации создаётся фрактальное изображение, которое сохраняется после применения постобработки.
Тест проверяет, что файл с изображением успешно создан.

Параметры:
- `transformation` (Transformation): Трансформация, применяемая при рендеринге.
- `filename` (str): Имя файла для сохранения результата рендеринга.

Этапы теста:
1. Создается канва для рендеринга с заданными размерами (`width=600`, `height=400`).
2. Выполняется рендеринг фрактального изображения с указанной трансформацией.
3. Применяется постобработка (логарифмическая гамма-коррекция).
4. Изображение сохраняется в директорию `tests/output` с заданным именем файла.
5. Проверяется существование файла с изображением.

Используемые трансформации (все из реализованных):
- `SinusoidalTransformation`
- `SphericalTransformation`
- `SwirlTransformation`
- `PolarTransformation`
- `HandkerchiefTransformation`
- `HeartTransformation`
- `DiscTransformation`
- `SpiralTransformation`
- `HyperbolicTransformation`
- `DiamondTransformation`
- `PopcornTransformation`
- `PDJTransformation`
- `CurlTransformation`

Результат:
- Успешное прохождение теста подтверждает, что каждое изображение фрактала было сгенерировано
  и сохранено корректно.

Директория для вывода:
- Все изображения сохраняются в `tests/output`.

Зависимости:
- `pytest` для параметризации тестов.
- `os`, `pathlib.Path` для работы с файловой системой.
- Модули `FractalImage`, `render`, и `ImageUtils` для рендеринга и сохранения изображений.
"""
import pytest
from src.domain import Rect, FractalImage
from src.renderer import render
from src.transformations import (
    SinusoidalTransformation,
    SphericalTransformation,
    SwirlTransformation,
    PolarTransformation,
    HandkerchiefTransformation,
    HeartTransformation,
    DiscTransformation,
    SpiralTransformation,
    HyperbolicTransformation,
    DiamondTransformation,
    PopcornTransformation,
    PDJTransformation,
    CurlTransformation,
)
from src.utils import ImageUtils
from pathlib import Path
import os

from src.processors import LogGammaCorrectionProcessor

os.makedirs("tests/output", exist_ok=True)


@pytest.mark.parametrize("transformation,filename", [
    (SinusoidalTransformation(scale_x=3.0, scale_y=8.0), "sinusoidal_fractal.png"),
    (SphericalTransformation(), "spherical_fractal.png"),
    (SwirlTransformation(), "swirl_fractal.png"),
    (PolarTransformation(angle_scale=1.5, radius_offset=0.5), "polar_fractal.png"),
    (HandkerchiefTransformation(), "handkerchief_fractal.png"),
    (HeartTransformation(), "heart_fractal.png"),
    (DiscTransformation(), "disc_fractal.png"),
    (SpiralTransformation(), "spiral_fractal.png"),
    (HyperbolicTransformation(scale=0.8), "hyperbolic_fractal.png"),
    (DiamondTransformation(scale=0.6), "diamond_fractal.png"),
    (PopcornTransformation(c=0.4, d=0.6), "popcorn_fractal.png"),
    (PDJTransformation(a=1.0, b=1.2, c=1.0, d=1.5), "pdj_fractal.png"),
    (CurlTransformation(p=0.2, q=0.8), "curl_fractal.png"),
])
def test_transformation_image(transformation, filename):
    width, height = 600, 400
    samples, iterations = 100000, 8
    world = Rect(-1, -1, 2, 2)

    canvas = FractalImage(width, height)

    render(canvas, world, [transformation], samples, iterations, seed=42)

    processor = LogGammaCorrectionProcessor()
    output_path = Path(f"tests/output/{filename}")
    ImageUtils.save_with_processing(canvas, processor, output_path)
    assert output_path.exists()
