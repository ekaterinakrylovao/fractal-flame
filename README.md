# Фрактальное пламя

Этот проект позволяет создавать яркие и необычные фрактальные изображения, используя набор трансформаций (вариаций).

## Запуск проекта

Чтобы запустить проект, вам потребуется [Poetry](https://python-poetry.org/). После установки Poetry выполните следующие команды в терминале:

### 1. Клонируйте репозиторий

```bash
git clone <URL_репозитория>
cd <название_репозитория>
```

### 2. Установите зависимости

```bash
poetry install
```

- Если вдруг необходимые зависимости не установятся, воспользуйтесь

    ```bash
    pip install -r requirements.txt
    ```

## Запуск

Для генерации фрактального изображения используйте следующую команду:
```bash
python -m src.main --width WIDTH --height HEIGHT --transformations NUMBER_OF_TRANSFORMATIONS --config_file CONFIG_JSON_FILE_NAME --mode MODE --num_threads NUMBER_OF_THREADS
```
### Параметры запуска:
- `--width` (обязательный): ширина изображения в пикселях.
- `--height` (обязательный): высота изображения в пикселях.
- `--transformations`: количество используемых трансформаций в текущей генерации. Если трансформации заданы конфигурационным файлом, то не передаётся.
- `--config_file`: имя файла с конфигурацией для генерации по значениям из него.
- `--mode` (обязательный): необходимо выбрать режим запуска из 
  - `single`: однопоточный запуск (рекомендуется при генерации пламени из одной трансформации).
  - `multi`: многопроцессорный запуск (рекомендуется при генерации пламени по более чем 2-м трансформациям).
  - `compare`: режим сравнения однопоточного и многопроцессорного режимов (можно посмотреть на выигрыш по времени многопроцессорного режима).
- `--num_threads` (используется в режимах `multi` и `compare`): число процессов задействуемых для генерации сложных изображений. Его можно и не устанавливать, так как далее, в процессе работы программы, если этот параметр не будет обнаружен, программа сама потребует ввести значение, перед запуском многопроцессорного режима. (Рекомендуется заранее узнать число процессоров на вашей машине.)

### Пример:
```bash
python -m src.main --width 1200 --height 800 --config_file fractal_config.json --mode compare --num_threads 8
```

## Поддерживаемые вариации

1. **Sinusoidal** (Синусоидальная):
   - Преобразование синусоидально изменяет координаты точки.
   - Параметры:
     - `scale_x`: масштаб по оси X (по умолчанию 1.0).
     - `scale_y`: масштаб по оси Y (по умолчанию 1.0).

2. **Spherical** (Сферическая):
   - Отображение точки на сферу с использованием обратного квадрата расстояния.
   - Параметров нет.

3. **Swirl** (Вихрь):
   - Вращает точки в зависимости от их расстояния до начала координат.
   - Параметров нет.

4. **Polar** (Полярная):
   - Преобразует координаты в полярные.
   - Параметры:
     - `angle_scale`: масштаб угла (по умолчанию 1.0).
     - `radius_offset`: смещение радиуса (по умолчанию 0.0).

5. **Handkerchief** (Платок):
   - Генерирует сложные узоры с перекрытием радиальных и угловых компонент.
   - Параметров нет.

6. **Heart** (Сердце):
   - Создает изображение с использованием формы сердца.
   - Параметров нет.

7. **Disc** (Диск):
   - Генерирует узоры с радиальной симметрией.
   - Параметров нет.

8. **Spiral** (Спираль):
   - Создает узоры в форме спирали.
   - Параметров нет.

9. **Hyperbolic** (Гиперболическая):
   - Использует гиперболическую функцию для искажения координат.
   - Параметры:
     - `scale`: масштаб (по умолчанию 1.0).
     - `jitter`: случайные отклонения (по умолчанию 0.01)

10. **Diamond** (Бриллиант):
    - Создает узоры с симметрией по форме ромба.
    - Параметры:
      - `scale`: масштаб (по умолчанию 1.0).
      - `jitter`: случайные отклонения (по умолчанию 0.07)

11. **Popcorn** (Попкорн):
    - Преобразует точки с использованием синусоидального тангенса.
    - Параметры:
      - `c`: коэффициент смещения по X (по умолчанию 0.5).
      - `d`: коэффициент смещения по Y (по умолчанию 0.5).

12. **PDJ** (Параметрическое преобразование):
    - Использует четыре параметра для создания сложных фракталов.
    - Параметры:
      - `a`, `b`, `c`, `d`: параметры преобразования (по умолчанию все 1.0).

13. **Curl** (Кручение):
    - Добавляет эффект "вихря" вокруг координат.
    - Параметры:
      - `p`, `q`: параметры интенсивности (по умолчанию оба 0.5).
      
## Для каждой из трансформаций

Имеются следующие параметры:
- Название трансформации: будет предложено выбрать из реализованных (*SinusoidalTransformation*, *SphericalTransformation*, *SwirlTransformation*, *PolarTransformation*, *HandkerchiefTransformation*, *HeartTransformation*, *DiscTransformation*, *SpiralTransformation*, *HyperbolicTransformation*, *DiamondTransformation*, *PopcornTransformation*, *PDJTransformation*, *CurlTransformation*).
- Параметры трансформации: 
  - если трансформация их подразумевает, то будет приведён пример полей и их значений;
  - если же трансформация их не подразумевает, то об этом будет сказано и этот шаг будет пропущен.
- Количество итераций: по умолчанию стоит 8, как нечто оптимальное, но можно экспериментировать.
- Границы мира: ограничитель области генерации той или иной трансформации. Требуемый формат ввода также приводится программой.
- Количество сэмплов: задаёт количество точек участвующих в трансформации.
- Симметрия (1 по умолчанию): спокойно можно экспериментировать со значением.

## Обработка изображения

Программа использует *логарифмическую гамма-коррекцию* с настройкой следующих параметров:
- `gamma`: степень коррекции (по умолчанию 2.0).
- `scale`: масштаб для логарифмической шкалы (по умолчанию 1.0).
- `colormap`: цветовая карта для окрашивания изображения (по умолчанию `inferno`). Можно пробовать любые, а посмотреть их можно например [тут](https://matplotlib.org/stable/users/explain/colors/colormaps.html).
- `brightness_shift`: смещение яркости для увеличения разнообразия (по умолчанию 0.1).

## Результат

Получаем картинку `fractal_single.png` или же `fractal_multi.png` (в зависимости от установленного режима программы).

---

## Тесты

Проект сопровождается тестами для проверки генерации изображений и производительности.

### Тесты изображений:
`tests/test_images.py`

Генерируются примеры изображений для всех доступных вариаций и сохраняются в папке `tests/output`.

Для запуска:
```bash
pytest tests/test_images.py
```

### Тесты производительности:
Сравнивается время выполнения программы при использовании одного и нескольких потоков.

1. `tests/test_performance.py`
    Производит замеры времени времени однопоточной и многопроцессорной версий от одной до максимума (13-ти) трансформаций в генерации и приводит график ускорения времени генерации в зависимотсти от числа трансформаций `tests/output/performance_comparison.png`.

    Для запуска:
    ```bash
    pytest tests/test_performance.py
    ```
    Пример графика:
    ![performance_comparison](https://github.com/user-attachments/assets/738bc508-7ac2-4a65-9d58-287b62fb839e)

2. `tests/test_multi_performance.py`
    Производит замеры времени для многопроцессорной версии.
    Для количества процессов от 2-х до максимума системы запускается генерация изображений от 2-х до 13-ти трансформаций и приводится трёхмерный график для анализа эффективности `tests/output/multi_dimensional_performance.png`.

    Для запуска:
    ```bash
    pytest tests/test_multi_performance.py
    ```
   Пример графика:
    ![multi_dimensional_performance](https://github.com/user-attachments/assets/c7e4b16c-42f2-4fc7-a517-731934cbb961)

3. `tests/test_main.py`
    Проверяет общий функционал работы программы имитируя ввод пользователем.
    
    Можно использовать равноценно запуску программы с заранее установленными всеми параметрами генерации.
    
    Для запуска:
    ```bash
    pytest tests/test_main.py
    ```

Для запуска всех тестов выполните команду:
```bash
pytest
```

---

Теперь вы можете тоже генерировать Фрактальное пламя из набора имеющихся трансформаций или же расширить не реализованными мной трансформациями.

Вдохновиться на расширение программы можно [тут](https://flam3.com/flame_draves.pdf).

---

### Примеры

![fractal_HeartSpiral](https://github.com/user-attachments/assets/a4c8edd1-6663-4097-adc4-58b4ed0e589d)

![fractal_Handkerchief_6](https://github.com/user-attachments/assets/f64b9a48-e0aa-416c-ad71-3ec215611e2e)

![SwirlHandkSpiralPDJ_inferno](https://github.com/user-attachments/assets/029783a2-484a-4d1d-adf7-5e265925623a)

![fractal_cute](https://github.com/user-attachments/assets/27ebf7d4-7778-409b-bb02-27f3c8bb71b4)

---

P.S. Если не хочется слишком много разбираться с параметрами и тем, как и что устроено, то можно подсмотреть значения конфигураций в 'tests/test_images.py', а также при выдумывании идей опираться на картинки, полученные при запуске этого теста.
