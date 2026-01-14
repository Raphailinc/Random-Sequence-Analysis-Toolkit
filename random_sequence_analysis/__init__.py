"""
Random sequence analysis toolkit.

Provides utilities to generate uniform sequences (NumPy or middle-square),
estimate period/aperiodicity, and run chi-square tests for uniformity.
"""

from .analysis import (
    SequenceSummary,
    analyze_sequence,
    chi_square_uniform,
    compute_period,
    generate_uniform_sequence,
    middle_square_sequence,
)

__all__ = [
    "SequenceSummary",
    "analyze_sequence",
    "chi_square_uniform",
    "compute_period",
    "generate_uniform_sequence",
    "middle_square_sequence",
]
