from concurrent.futures import ThreadPoolExecutor, as_completed
from src.renderer import render_single


def render_with_multithreading(width, height, transformation_configs, processor, num_threads):
    canvases = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(render_single, width, height, config.transformation, config.iterations, config.world, config.samples, config.symmetry)
            for config in transformation_configs
        ]
        for future in as_completed(futures):
            canvases.append(future.result())
    return canvases
