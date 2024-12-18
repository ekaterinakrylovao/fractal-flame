"""
Тест производительности с различным числом процессов и трансформаций.

Описание:
Этот тест оценивает производительность системы при рендеринге фрактальных изображений
с использованием различных трансформаций и количества процессов. Он варьирует число
трансформаций и процессов, измеряя время выполнения задачи. Результаты выводятся в
табличной форме (если требуется) и визуализируются в 3D-графике.

Параметры:
- `width` (int): Ширина изображения.
- `height` (int): Высота изображения.
- `max_processes` (int): Максимальное число процессов, определяется по количеству ядер CPU.
- `process_counts` (range): Диапазон количества процессов от 2 до `max_processes`.
- `TRANSFORMATION_CONFIGS` (list): Набор конфигураций для различных трансформаций.

Этапы теста:
1. Перебор числа процессов от минимального (2) до максимального (max_processes).
2. Для каждого числа процессов перебирается количество трансформаций от 2 до максимального числа в
                                                                                        `TRANSFORMATION_CONFIGS`.
3. Для каждого набора измеряется время выполнения рендеринга:
   - Используется пул процессов с заданным количеством процессов.
   - Частичный рендеринг выполняется для каждой конфигурации трансформации.
   - Результаты объединяются в единое изображение.
4. Результаты времени выполнения записываются и выводятся в табличной форме.
5. При наличии библиотеки matplotlib строится 3D-график зависимости времени выполнения от числа процессов и
                                                                                                трансформаций.

Вывод:
- Таблица с результатами производительности в консоли (если запустить в режиме -s).
- График сохраняется в `tests/output/multi_dimensional_performance.png`.

Зависимости:
- `matplotlib` для построения графиков (опционально).
- Модули `pytest`, `numpy`, `multiprocessing`, `time` для проведения теста.

Примечание:
Для вывода результатов в консоли при запуске теста используйте опцию `-s`.
"""
import numpy as np
import pytest
import time
from multiprocessing import cpu_count, Pool
from functools import partial
from src.domain import Rect, FractalImage
from src.renderer import render_single, merge_canvases
from src.transformation_config import TransformationConfig
from src.transformations import (
    CurlTransformation,
    PopcornTransformation,
    HyperbolicTransformation,
    HandkerchiefTransformation,
    SphericalTransformation,
    SpiralTransformation,
    HeartTransformation,
    SinusoidalTransformation,
    PDJTransformation,
    PolarTransformation,
    DiscTransformation,
    DiamondTransformation,
    SwirlTransformation,
)

TRANSFORMATION_CONFIGS = [
    TransformationConfig(CurlTransformation(0.2, 0.8), 10, Rect(-2, -2, 4, 4), 30000),
    TransformationConfig(PopcornTransformation(0.4, 0.6), 50, Rect(-1.5, -1.5, 3, 3), 30000),
    TransformationConfig(HyperbolicTransformation(0.8), 1, Rect(-1, -1, 2, 2), 100000),
    TransformationConfig(HandkerchiefTransformation(), 1, Rect(-1, -1, 2, 2), 100000),
    TransformationConfig(SphericalTransformation(), 1, Rect(-1, -1, 2, 2), 100000),
    TransformationConfig(SpiralTransformation(), 8, Rect(-1.5, -1.5, 3, 3), 100000),
    TransformationConfig(HeartTransformation(), 8, Rect(-1.5, -1.5, 3, 3), 100000),
    TransformationConfig(SinusoidalTransformation(3.0, 8.0), 1, Rect(-1, -1, 2, 2), 100000),
    TransformationConfig(PDJTransformation(1.0, 1.2, 1.0, 1.5), 8, Rect(-1.5, -1.5, 3, 3), 100000),
    TransformationConfig(PolarTransformation(2.5, 1.0), 8, Rect(-1, -1, 2, 2), 300000, 2),
    TransformationConfig(DiscTransformation(), 1, Rect(-1, -1, 2, 2), 800000, 8),
    TransformationConfig(DiamondTransformation(0.6), 1, Rect(-1, -1, 2, 2), 1000000),
    TransformationConfig(SwirlTransformation(), 1, Rect(-1, -1, 2, 2), 1500000),
]


@pytest.mark.performance
def test_performance_with_varied_process_and_transformations():
    width, height = 600, 400
    max_processes = cpu_count()
    process_counts = range(2, max_processes + 1)  # От 2 до максимального количества процессоров
    results = []

    for num_processes in process_counts:
        for n in range(2, len(TRANSFORMATION_CONFIGS) + 1):
            configs = TRANSFORMATION_CONFIGS[:n]
            start_time = time.time()

            with Pool(processes=num_processes) as pool:
                render_partial = partial(render_single, width=width, height=height)
                canvases_multi_process = pool.map(
                    render_partial, configs, chunksize=max(1, len(configs) // num_processes)
                )
            canvas_multi_process = FractalImage(width, height)
            merge_canvases(canvas_multi_process, canvases_multi_process)
            elapsed_time = time.time() - start_time

            results.append((num_processes, n, elapsed_time))

    # Вывод результатов в таблицу
    # Для вывода воспользоваться опцией -s при запуске теста
    print(f"{'Processes':<15}{'Transformations':<15}{'Time (s)':<10}")
    for result in results:
        print(f"{result[0]:<15}{result[1]:<15}{result[2]:<10.2f}")

    # Построение графика
    try:
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection="3d")

        processes = [r[0] for r in results]
        transformations = [r[1] for r in results]
        times = [r[2] for r in results]

        transformations = np.array(transformations, dtype=float)
        times = np.array(times, dtype=float)
        scatter = ax.scatter(processes, transformations, times, c=times, cmap="viridis", marker="o")
        ax.set_xlabel("Number of Processes")
        ax.set_ylabel("Number of Transformations")
        ax.set_zlabel("Time (s)")
        ax.set_title("Performance: Processes vs Transformations vs Time")
        fig.colorbar(scatter, ax=ax, label="Execution Time (s)")
        plt.savefig("tests/output/multi_dimensional_performance.png")
        print("График сохранён в tests/output/multi_dimensional_performance.png")
    except ImportError:
        print("Модуль matplotlib не установлен, график не построен.")
