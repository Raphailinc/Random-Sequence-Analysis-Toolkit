import numpy as np
import subprocess
import sys

from random_sequence_analysis import (
    analyze_sequence,
    chi_square_uniform,
    compute_period,
    generate_uniform_sequence,
    middle_square_sequence,
)


def test_middle_square_sequence_deterministic():
    seq = middle_square_sequence(5, seed=0.15, k=4)
    assert np.allclose(seq[:3], [0.15, 0.25, 0.25])
    assert (seq >= 0).all() and (seq < 1).all()


def test_compute_period_simple_repeat():
    period, aperiodic = compute_period([0.1, 0.2, 0.1, 0.2])
    assert period == 2
    assert aperiodic == 0


def test_chi_square_uniform_and_p_value():
    seq = generate_uniform_sequence(1000, method="numpy", seed=123)
    chi, p = chi_square_uniform(seq, num_bins=10)
    assert chi > 0
    assert p is None or 0 <= p <= 1


def test_analyze_sequence_summary_fields():
    summary = analyze_sequence(size=500, method="numpy", seed=42, bins=8)
    assert summary.period >= 0
    assert summary.aperiodicity >= 0
    assert summary.sequence.shape == (500,)
    assert summary.bins == 8
    assert summary.generator == "numpy"


def test_cli_runs():
    cmd = [
        sys.executable,
        "-m",
        "random_sequence_analysis",
        "-n",
        "200",
        "-b",
        "8",
        "-g",
        "middle-square",
        "--seed",
        "0.15",
        "-k",
        "4",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert "Generator" in result.stdout
    assert "Chi-square" in result.stdout
