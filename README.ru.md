# Random Sequence Analysis Toolkit

[![CI](https://github.com/Raphailinc/Random-Sequence-Analysis-Toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphailinc/Random-Sequence-Analysis-Toolkit/actions/workflows/ci.yml)

[English](README.md) · [Русский](README.ru.md)

Учебный статистический проект: генерация и анализ последовательностей на [0, 1).

## Возможности

- Генератор NumPy с seed и детерминированный метод середины квадратов.
- Расчёт среднего и стандартного отклонения.
- Поиск наблюдаемых повторов и статистика хи-квадрат для равномерности.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m random_sequence_analysis -n 5000 -b 13 -g numpy --seed 42
```

## Проверки

```bash
python -m pytest
```

## Условия запуска и границы проекта

Период оценивается по наблюдаемым повторам с выбранной точностью. Статистика служит учебной диагностикой и не доказывает криптографическую пригодность генератора.
