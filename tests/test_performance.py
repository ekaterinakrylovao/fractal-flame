"""
Тест сравнения производительности однопоточной и многопроцессорной обработки.

Описание:
Этот тест измеряет производительность рендеринга фрактальных изображений при использовании
одного потока (single-thread) и пула процессов (multi-process). Сравнивается время выполнения
для различного числа трансформаций. Результаты визуализируются графиком и выводятся в таблицу (если требуется).

Параметры:
- `width` (int): Ширина изображения.
- `height` (int): Высота изображения.
- `num_threads` (int): Количество потоков, определяется по числу ядер CPU.
- `TRANSFORMATION_CONFIGS` (list): Набор конфигураций для тестирования с различными трансформациями.

Этапы теста:
1. Перебираются значения `n`, соответствующие количеству трансформаций от 1 до их максимального числа.
2. Для каждого набора `n` выполняются:
   - **Однопоточная обработка**:
     - Для каждой трансформации выполняется рендеринг фрактала в одном потоке.
     - Время выполнения записывается.
   - **Многопроцессорная обработка**:
     - Рендеринг выполняется параллельно с использованием пула процессов.
     - Канвасы объединяются в одно изображение.
     - Время выполнения записывается.
3. Вычисляется ускорение (speedup) как отношение времени однопоточной обработки к многопроцессорной.
4. Результаты сохраняются.

Вывод:
- Таблица с результатами (если запустить в режиме -s), содержащая количество трансформаций,
время однопоточной и многопроцессорной обработки, а также ускорение.

- Построение графика ускорения в зависимости от числа трансформаций.
- График сохраняется в `tests/output/performance_comparison.png`.

Зависимости:
- `matplotlib` для построения графиков (опционально).
- Модули `pytest`, `numpy`, `multiprocessing`, `time` для выполнения теста.

Примечание:
Для вывода результатов в консоли при запуске теста используйте опцию `-s`.
"""
import numpy as np
import pytest
import time
from multiprocessing import cpu_count
from src.domain import Rect, FractalImage
from src.renderer import render, render_single
from src.renderer import merge_canvases
from functools import partial
from multiprocessing import Pool
from src.transformation_config import TransformationConfig
from src.transformations import (
    SwirlTransformation,
    CurlTransformation,
    PopcornTransformation,
    PolarTransformation,
    DiamondTransformation,
    DiscTransformation,
    SpiralTransformation,
    PDJTransformation,
    HeartTransformation,
    HyperbolicTransformation,
    HandkerchiefTransformation,
    SphericalTransformation,
    SinusoidalTransformation,
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
def test_multi_vs_single_performance():
    width, height = 600, 400
    results = []
    num_threads = cpu_count()

    for n in range(1, len(TRANSFORMATION_CONFIGS) + 1):
        configs = TRANSFORMATION_CONFIGS[:n]

        # Однопоточная версия
        start_single = time.time()
        canvas_single_thread = FractalImage(width, height)
        for config in configs:
            render(
                canvas=canvas_single_thread,
                world=config.world,
                variations=[config.transformation],
                samples=config.samples,
                iter_per_sample=config.iterations,
                seed=42,
                symmetry=config.symmetry,
            )
        single_thread_time = time.time() - start_single

        # Многопроцессорная версия
        start_multi = time.time()
        with Pool(processes=num_threads) as pool:
            render_partial = partial(render_single, width=width, height=height)
            canvases_multi_process = pool.map(
                render_partial, configs, chunksize=max(1, len(configs) // num_threads)
            )
        canvas_multi_process = FractalImage(width, height)
        merge_canvases(canvas_multi_process, canvases_multi_process)
        multi_process_time = time.time() - start_multi

        # Сохранение результатов
        results.append(
            (n, single_thread_time, multi_process_time, single_thread_time / multi_process_time)
        )

    # Вывод результатов в таблицу
    # Для вывода воспользоваться опцией -s при запуске теста
    print(f"{'Transformations':<15}{'Single Thread':<15}{'Multi Process':<15}{'Speedup':<10}")
    for result in results:
        print(f"{result[0]:<15}{result[1]:<15.2f}{result[2]:<15.2f}{result[3]:<10.2f}")

    # Генерация графика
    try:
        import matplotlib.pyplot as plt

        transformations = [r[0] for r in results]
        speedups = [r[3] for r in results]

        plt.figure(figsize=(10, 6))
        transformations = np.array(transformations, dtype=float)
        speedups = np.array(speedups, dtype=float)
        plt.plot(transformations, speedups, marker="o", label="Speedup")
        plt.xlabel("Number of Transformations")
        plt.ylabel("Speedup (Single / Multi)")
        plt.title("Performance Comparison: Single vs Multi")
        plt.legend()
        plt.grid()
        plt.savefig("tests/output/performance_comparison.png")
        print("График сохранён в tests/output/performance_comparison.png")
    except ImportError:
        print("Модуль matplotlib не установлен, график не построен.")
