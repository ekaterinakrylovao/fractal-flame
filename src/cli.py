import argparse


def parse_args():
    """
    Функция для парсинга аргументов командной строки.

    Эта функция использует argparse для парсинга различных параметров, которые могут быть переданы
    при запуске программы. Аргументы включают параметры для ширины и высоты холста, количество
    трансформаций, путь к конфигурационному файлу, режим работы и количество потоков для многопроцессорного режима.

    Returns:
        argparse.Namespace: Объект с парсированными аргументами командной строки.
    """
    parser = argparse.ArgumentParser(description="Фрактальный рендеринг с выбором параметров.")
    parser.add_argument("--width", type=int, default=600, help="Ширина холста.")
    parser.add_argument("--height", type=int, default=400, help="Высота холста.")
    parser.add_argument("--transformations", type=int, required=False, help="Количество трансформаций для рендеринга.")
    parser.add_argument("--config_file", type=str, required=False, help="Путь к конфигурационному файлу.")
    parser.add_argument("--mode", choices=["single", "multi", "compare"], required=True, help="Режим работы.")
    parser.add_argument("--num_threads", type=int, default=None, help="Число потоков для многопроцессорного режима.")
    return parser.parse_args()
