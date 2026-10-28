# Random Sequence Analysis Toolkit

[![CI](https://github.com/Raphailinc/Random-Sequence-Analysis-Toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphailinc/Random-Sequence-Analysis-Toolkit/actions/workflows/ci.yml)

[English](README.md) · [Русский](README.ru.md)

A statistical learning project for generating and inspecting sequences on `[0, 1)`.

## What it does

- Generate seeded NumPy or deterministic middle-square sequences.
- Summarize mean and standard deviation.
- Inspect first-repeat period indicators and chi-square uniformity statistics.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m random_sequence_analysis -n 5000 -b 13 -g numpy --seed 42
```

## Checks

```bash
python -m pytest
```

## Scope and implementation notes

Period detection is based on observed repeats and configured precision. The statistical output is an educational diagnostic, not proof that a generator is suitable for cryptography.
