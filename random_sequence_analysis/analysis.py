from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

import numpy as np

try:
    from scipy.stats import chi2
except Exception:  # pragma: no cover - optional dependency
    chi2 = None


DEFAULT_SEED = 0.15
DEFAULT_K = 4


@dataclass
class SequenceSummary:
    sequence: np.ndarray
    period: int
    aperiodicity: int
    chi_square: float
    p_value: Optional[float]
    bins: int
    generator: str

    @property
    def mean(self) -> float:
        return float(np.mean(self.sequence))

    @property
    def std(self) -> float:
        return float(np.std(self.sequence))


def middle_square_sequence(size: int, seed: float = DEFAULT_SEED, k: int = DEFAULT_K) -> np.ndarray:
    """
    Middle-square PRNG variant for floats in [0, 1).
    seed: 0 < seed < 1, k even digit count.
    """
    if size <= 0:
        raise ValueError("size must be positive")
    if not (0 < seed < 1):
        raise ValueError("seed must be between 0 and 1 (exclusive)")
    if k <= 0 or k % 2 != 0:
        raise ValueError("k must be a positive even integer")

    seq = np.empty(size)
    seq[0] = seed
    half = 10 ** (k // 2)
    scale = 10**k
    for i in range(1, size):
        val = seq[i - 1] ** 2
        fractional = math.modf(val * half)[0]
        seq[i] = int(fractional * scale) / scale
    return seq


def generate_uniform_sequence(
    size: int,
    *,
    method: str = "numpy",
    seed: Optional[float | int] = None,
    k: int = DEFAULT_K,
) -> np.ndarray:
    """Generate uniform values on [0, 1) using NumPy or middle-square."""
    if method == "numpy":
        seed_to_use = seed
        if isinstance(seed_to_use, float) and float(seed_to_use).is_integer():
            seed_to_use = int(seed_to_use)
        rng = np.random.default_rng(seed_to_use)
        return rng.random(size)
    if method == "middle-square":
        return middle_square_sequence(size, seed=seed or DEFAULT_SEED, k=k)
    raise ValueError(f"Unknown generator method: {method}")


def compute_period(sequence: Iterable[float], *, precision: int = 12) -> Tuple[int, int]:
    """
    Return (period, aperiodicity) where aperiodicity is the index where cycle starts.
    Uses rounding to given precision to mitigate float noise.
    """
    seen = {}
    seq_list = list(sequence)
    for idx, val in enumerate(seq_list):
        key = round(float(val), precision)
        if key in seen:
            start = seen[key]
            return idx - start, start
        seen[key] = idx
    return 0, len(seq_list)


def chi_square_uniform(sequence: Iterable[float], num_bins: int) -> Tuple[float, Optional[float]]:
    """Chi-square statistic (and optional p-value) against uniform [0,1)."""
    seq = np.asarray(list(sequence), dtype=float)
    if num_bins <= 0:
        raise ValueError("num_bins must be positive")
    n = len(seq)
    bin_counts, _ = np.histogram(seq, bins=np.linspace(0, 1, num_bins + 1))
    expected = n / num_bins
    chi_square = float(np.sum((bin_counts - expected) ** 2 / expected))
    p_value = float(chi2.sf(chi_square, num_bins - 1)) if chi2 else None
    return chi_square, p_value


def analyze_sequence(
    *,
    size: int = 5000,
    method: str = "numpy",
    seed: Optional[float | int] = None,
    k: int = DEFAULT_K,
    bins: int = 13,
    precision: int = 12,
) -> SequenceSummary:
    seq = generate_uniform_sequence(size, method=method, seed=seed, k=k)
    period, aperiodicity = compute_period(seq, precision=precision)
    chi_sq, p_val = chi_square_uniform(seq, num_bins=bins)
    return SequenceSummary(
        sequence=seq,
        period=period,
        aperiodicity=aperiodicity,
        chi_square=chi_sq,
        p_value=p_val,
        bins=bins,
        generator=method,
    )


def _format_summary(summary: SequenceSummary, top_n: int = 8) -> str:
    lines = [
        f"Generator: {summary.generator}",
        f"Samples: {len(summary.sequence)}, bins: {summary.bins}",
        f"Mean: {summary.mean:.6f}, Std: {summary.std:.6f}",
        f"Period: {summary.period}, Aperiodicity: {summary.aperiodicity}",
        f"Chi-square: {summary.chi_square:.4f}"
        + (f", p-value: {summary.p_value:.4f}" if summary.p_value is not None else ""),
        "First {top_n} samples: ".format(top_n=top_n)
        + ", ".join(f"{x:.6f}" for x in summary.sequence[:top_n]),
    ]
    return "\n".join(lines)


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Generate and analyse a random sequence.")
    parser.add_argument("-n", "--size", type=int, default=5000, help="Sequence length.")
    parser.add_argument("-g", "--generator", choices=["numpy", "middle-square"], default="numpy")
    parser.add_argument("--seed", type=float, default=None, help="Seed for generator.")
    parser.add_argument("-k", type=int, default=DEFAULT_K, help="k for middle-square (even).")
    parser.add_argument("-b", "--bins", type=int, default=13, help="Bins for chi-square test.")
    parser.add_argument("-p", "--precision", type=int, default=12, help="Rounding precision for period detection.")
    args = parser.parse_args(argv)

    summary = analyze_sequence(
        size=args.size,
        method=args.generator,
        seed=args.seed,
        k=args.k,
        bins=args.bins,
        precision=args.precision,
    )
    print(_format_summary(summary))


if __name__ == "__main__":  # pragma: no cover
    main()
