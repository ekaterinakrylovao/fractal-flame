import logging
import platform
from pathlib import Path
import time
from multiprocessing import Pool
from functools import partial

from src.cli import parse_args
from src.config_utils import load_config_from_file, save_config_to_file, get_transformation_config
from src.domain import FractalImage
from src.processors import LogGammaCorrectionProcessor
from src.renderer import render, render_single, merge_canvases
from src.utils import ImageUtils

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    args = parse_args()

    logger.info(platform.python_version())

    width, height = args.width, args.height

    # Выбор источника конфигурации
    transformation_configs = []
    if args.config_file:
        print(f"Загрузка конфигураций из файла: {args.config_file}")
        transformation_configs = load_config_from_file(args.config_file)
    else:
        num_transformations = args.transformations or int(input("Введите количество трансформаций: "))
        for i in range(num_transformations):
            print(f"\n=== Конфигурация трансформации #{i + 1} ===")
            config = get_transformation_config()
            transformation_configs.append(config)

    print("\n=== Настройка параметров обработки изображения ===")
    gamma = float(input("Параметр гамма-коррекции (по умолчанию: 2.0): ") or 2.0)
    scale = float(input("Масштабный коэффициент (по умолчанию: 1.0): ") or 1.0)
    colormap = input("Цветовая карта (например, inferno, plasma; по умолчанию: inferno): ") or "inferno"
    brightness_shift = float(input("Смещение яркости (по умолчанию: 0.1): ") or 0.1)

    processor = LogGammaCorrectionProcessor(
        gamma=gamma, scale=scale, colormap=colormap, brightness_shift=brightness_shift
    )

    if args.mode in ["single", "compare"]:
        start_time = time.time()
        canvas_single_thread = FractalImage(width, height)
        for config in transformation_configs:
            render(
                canvas=canvas_single_thread,
                world=config.world,
                variations=[config.transformation],
                samples=config.samples,
                iter_per_sample=config.iterations,
                seed=42,
                symmetry=config.symmetry,
            )
        single_thread_time = time.time() - start_time
        output_path_single = Path("fractal_single.png")
        ImageUtils.save_with_processing(canvas_single_thread, processor, output_path_single)
        print(f"Однопоточная версия: {single_thread_time:.2f} секунд. Сохранено: {output_path_single}")

    if args.mode in ["multi", "compare"]:
        num_threads = args.num_threads or int(input("Введите количество потоков: "))
        start_time = time.time()
        with Pool(processes=num_threads) as pool:
            render_partial = partial(render_single, width=width, height=height)
            canvases_multi_process = pool.map(render_partial, transformation_configs,
                                              chunksize=len(transformation_configs) // num_threads or 1)

        canvas_multi_process = FractalImage(width, height)
        merge_canvases(canvas_multi_process, canvases_multi_process)
        multi_process_time = time.time() - start_time
        output_path_multi = Path("fractal_multi.png")
        ImageUtils.save_with_processing(canvas_multi_process, processor, output_path_multi)
        print(f"Многопроцессорная версия: {multi_process_time:.2f} секунд. Сохранено: {output_path_multi}")

    # Предложение сохранить конфигурацию
    save_choice = input("Хотите сохранить текущую конфигурацию трансформаций в файл? (y/n): ").lower()
    if save_choice == "y":
        output_file = (input("Введите имя файла для сохранения (по умолчанию: fractal_config.json): ") or
                       "fractal_config.json")
        save_config_to_file(transformation_configs, output_file)


if __name__ == "__main__":
    main()
