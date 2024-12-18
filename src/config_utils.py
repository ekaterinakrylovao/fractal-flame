import json

from src.config import TRANSFORMATIONS_MAP, TRANSFORMATION_PARAMS
from src.domain import Rect
from src.transformation_config import TransformationConfig


def load_config_from_file(config_file_path):
    """
    Загружает конфигурации трансформаций из файла.

    Параметры:
        config_file_path (str или Path): Путь к файлу конфигурации.

    Returns:
        list: Список объектов TransformationConfig, загруженных из файла.

    Exceptions:
        Если при чтении файла или создании объектов возникает ошибка,
        выводится сообщение об ошибке, и возвращается пустой список.
    """
    try:
        with open(config_file_path, "r") as f:
            configs = json.load(f)
        transformation_configs = []
        for conf in configs:
            transformation_class = TRANSFORMATIONS_MAP[conf["transformation"]]
            params = conf.get("params", {})
            transformation = transformation_class(**params)
            transformation_configs.append(
                TransformationConfig(
                    transformation=transformation,
                    iterations=conf["iterations"],
                    world=Rect(**conf["world"]),
                    samples=conf["samples"],
                    symmetry=conf["symmetry"],
                )
            )
        return transformation_configs
    except Exception as e:
        print(f"Ошибка при загрузке конфигурационного файла: {e}")
        return []


def save_config_to_file(configs, output_file):
    """
    Сохраняет список конфигураций трансформаций в файл.

    Параметры:
        configs (list): Список объектов TransformationConfig, которые нужно сохранить.
        output_file (str или Path): Путь к файлу для сохранения конфигураций.

    Exceptions:
        Если возникает ошибка при сохранении, выводится сообщение об ошибке.
    """
    try:
        serialized_configs = []
        for conf in configs:
            serialized_configs.append({
                "transformation": conf.transformation.__class__.__name__,
                "params": vars(conf.transformation),
                "iterations": conf.iterations,
                "world": vars(conf.world),
                "samples": conf.samples,
                "symmetry": conf.symmetry,
            })
        with open(output_file, "w") as f:
            json.dump(serialized_configs, f, indent=4)
        print(f"Конфигурация успешно сохранена в файл: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении конфигурации: {e}")


def get_transformation_config():
    """
    Запрашивает у пользователя параметры трансформации и возвращает объект TransformationConfig.

    Returns:
        TransformationConfig: Объект, содержащий выбранную трансформацию и её параметры.

    Exceptions:
        Выводит сообщение об ошибке, если введены неверные или некорректные параметры.
    """
    print("Введите параметры трансформации:")

    while True:
        # Выбор трансформации
        transformation_name = input(f"Название трансформации ({', '.join(TRANSFORMATIONS_MAP.keys())}): ")
        if transformation_name in TRANSFORMATIONS_MAP:
            transformation_class = TRANSFORMATIONS_MAP[transformation_name]
            break
        print("Неверное имя трансформации. Попробуйте ещё раз.")

    # Вывод примера параметров для выбранной трансформации
    example_params = TRANSFORMATION_PARAMS.get(transformation_name, "")
    if example_params:
        print(f"Пример параметров: {example_params}")
    else:
        print("Эта трансформация не требует параметров или их можно оставить пустыми.")

    # Проверка, какие параметры ожидаются
    try:
        init_method = transformation_class.__init__
        if hasattr(init_method, "__code__"):  # Проверяем, можно ли получить __code__
            expected_args = init_method.__code__.co_varnames[1:init_method.__code__.co_argcount]
        else:
            expected_args = []  # Если __init__ встроенный
    except AttributeError:
        expected_args = []  # Если класс не имеет явного __init__

    # Если трансформация не требует параметров, пропускаем ввод
    if not expected_args:  # Если нет параметров кроме self
        params_dict = {}
        transformation = transformation_class(**params_dict)
    else:
        # Проверка параметров с обработкой ошибок
        while True:
            params = input("Введите параметры (оставьте пустым для значений по умолчанию): ")
            try:
                if params:
                    params_dict = eval(f"dict({params})")
                    # Проверка, что параметры соответствуют аргументам конструктора
                    invalid_args = [key for key in params_dict if key not in expected_args]
                    if invalid_args:
                        raise ValueError(
                            f"Недопустимые параметры: {', '.join(invalid_args)}. "
                            f"Ожидаемые параметры: {', '.join(expected_args)}")
                else:
                    params_dict = {}
                transformation = transformation_class(**params_dict)  # Создание экземпляра трансформации
                break  # Выход из цикла, если параметры корректны
            except (SyntaxError, ValueError, TypeError) as e:
                print(f"Ошибка: {e}. Попробуйте ещё раз или оставьте пустым для значений по умолчанию.")

    # Ввод остальных параметров
    while True:
        try:
            iterations = int(input("Количество итераций (8 по умолчанию): ") or 8)
            if iterations <= 0:
                raise ValueError("Количество итераций должно быть положительным.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте ещё раз или оставьте пустым для значения по умолчанию (8).")

    while True:
        world_input = input("Границы мира (формат: x=-1, y=-1, width=2, height=2, по умолчанию): ")
        try:
            world_params = eval(f"dict({world_input})") if world_input else {"x": -1, "y": -1, "width": 2, "height": 2}
            world = Rect(**world_params)
            break
        except (SyntaxError, ValueError, TypeError) as e:
            print(f"Ошибка: {e}. Попробуйте ещё раз или оставьте пустым для значения по умолчанию.")

    while True:
        try:
            samples = int(input("Количество сэмплов (100000 по умолчанию): ") or 100000)
            if samples <= 0:
                raise ValueError("Количество сэмплов должно быть положительным.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте ещё раз или оставьте пустым для значения по умолчанию (100000).")

    while True:
        try:
            symmetry = int(input("Симметрия (1 по умолчанию): ") or 1)
            if symmetry <= 0:
                raise ValueError("Симметрия должна быть положительным числом.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте ещё раз или оставьте пустым для значения по умолчанию (1).")

    return TransformationConfig(
        transformation=transformation,
        iterations=iterations,
        world=world,
        samples=samples,
        symmetry=symmetry,
    )
