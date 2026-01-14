# Random Sequence Analysis Toolkit

Генерация и анализ псевдослучайных последовательностей на отрезке `[0, 1)`. Поддерживаются два генератора: стандартный NumPy и детерминированный middle-square. Есть расчёт периода/апериодичности и проверка равномерности через критерий хи‑квадрат (с p-value при наличии SciPy).

## Установка и запуск
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m random_sequence_analysis -n 5000 -b 13 -g numpy --seed 42
```

Пример вывода:
```
Generator: numpy
Samples: 5000, bins: 13
Mean: 0.501821, Std: 0.286542
Period: 0, Aperiodicity: 5000
Chi-square: 8.7221, p-value: 0.7245
First 8 samples: 0.773956, 0.438878, 0.858598, 0.697368, 0.094178, 0.975622, 0.761140, 0.786064
```

## Основные функции
- `generate_uniform_sequence(size, method="numpy", seed=None, k=4)`: равномерные числа (`method` — `numpy` или `middle-square`).
- `middle_square_sequence(size, seed=0.15, k=4)`: middle-square PRNG с фиксированной точностью (k — чётное число цифр).
- `compute_period(sequence, precision=12)`: возвращает `(period, aperiodicity)` по первым повторам.
- `chi_square_uniform(sequence, num_bins)`: хи‑квадрат и p-value (если SciPy доступна).
- `analyze_sequence(...)`: полный цикл генерации, оценки периода и проверки равномерности, возвращает `SequenceSummary`.

CLI: `python -m random_sequence_analysis --help`

## Тесты
```bash
pytest
```

## Идеи развития
- Добавить больше генераторов (LCG, crypto).
- Визуализация гистограмм и вывод в CSV/JSON.
- Настраиваемая точность и проверка автокорреляций.
