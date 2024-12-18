from unittest.mock import patch
import io
from src.main import main


def test_main() -> None:
    # Подменяем sys.argv для теста
    test_args = [
        "main.py",  # имя программы
        "--mode", "compare",  # обязательный аргумент
        "--num_threads", "2",
        "--width", "800",  # пример аргумента ширины
        "--height", "600",  # пример аргумента высоты
        "--transformations", "2",  # количество трансформаций
    ]

    # Подменяем ввод пользователя
    user_input = "\n".join([
        "PDJTransformation",  # Название трансформации #1
        "a=1.0, b=2.0, c=3.0, d=4.0",  # Пример параметров трансформации #1
        "8",  # Количество итераций
        "x=-1, y=-1, width=2, height=2",  # Границы мира
        "25000",  # Количество сэмплов
        "2",  # Симметрия
        "SphericalTransformation",  # Название трансформации #2
        "8",  # Количество итераций
        "x=-1, y=-1, width=1, height=1",  # Границы мира
        "30000",  # Количество сэмплов
        "4",  # Симметрия

        "2.2",  # Гамма-коррекция
        "1.0",  # Масштаб
        "plasma",  # Цветовая карта
        "0.2",  # Смещение яркости

        "y",  # Сохранить?
        "fractal_config_test.json",  # Имя файла для сохранения
    ])

    with patch("sys.argv", test_args), \
            patch("sys.stdin", io.StringIO(user_input)), \
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        try:
            main()
        except SystemExit as e:
            # Проверяем, что программа завершилась корректно
            assert e.code == 0

        # Проверяем, что программа вывела ожидаемые строки
        output = mock_stdout.getvalue()
        assert "Однопоточная версия:" in output
        assert "Сохранено: fractal_single.png"
        assert "Многопроцессорная версия:" in output
        assert "Сохранено: fractal_multi.png" in output
        assert "Конфигурация успешно сохранена в файл: fractal_config_test.json"
