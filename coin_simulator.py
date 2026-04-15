#!/usr/bin/env python3
"""
Simple coin toss simulator with optional bias and streak reporting.
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationResult:
    flips: int
    heads: int
    tails: int
    longest_heads_streak: int
    longest_tails_streak: int

    @property
    def heads_pct(self) -> float:
        return (self.heads / self.flips) * 100 if self.flips else 0.0

    @property
    def tails_pct(self) -> float:
        return (self.tails / self.flips) * 100 if self.flips else 0.0


def simulate(flips: int, p_heads: float) -> SimulationResult:
    heads = 0
    tails = 0

    longest_heads = 0
    longest_tails = 0
    current_heads = 0
    current_tails = 0

    for _ in range(flips):
        is_heads = random.random() < p_heads
        if is_heads:
            heads += 1
            current_heads += 1
            current_tails = 0
            if current_heads > longest_heads:
                longest_heads = current_heads
        else:
            tails += 1
            current_tails += 1
            current_heads = 0
            if current_tails > longest_tails:
                longest_tails = current_tails

    return SimulationResult(
        flips=flips,
        heads=heads,
        tails=tails,
        longest_heads_streak=longest_heads,
        longest_tails_streak=longest_tails,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulate coin flips and print distribution + streak stats."
    )
    parser.add_argument(
        "-n",
        "--flips",
        type=int,
        default=100,
        help="Number of flips to simulate (default: 100).",
    )
    parser.add_argument(
        "--p-heads",
        type=float,
        default=0.5,
        help="Probability of heads from 0 to 1 (default: 0.5).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for reproducible runs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.flips < 1:
        raise ValueError("Flips must be at least 1.")
    if not 0.0 <= args.p_heads <= 1.0:
        raise ValueError("--p-heads must be between 0 and 1.")

    if args.seed is not None:
        random.seed(args.seed)

    result = simulate(args.flips, args.p_heads)

    print(f"Coin simulator: {result.flips} flips")
    print(f"Heads: {result.heads} ({result.heads_pct:.2f}%)")
    print(f"Tails: {result.tails} ({result.tails_pct:.2f}%)")
    print(
        "Longest streaks -> "
        f"Heads: {result.longest_heads_streak}, "
        f"Tails: {result.longest_tails_streak}"
    )


if __name__ == "__main__":
    main()
