#!/usr/bin/env python3
import argparse
import math
import secrets
import string
import subprocess
import sys


# Characters often confused (0/O, 1/l/I, etc.) — excluded when asked.
_AMBIGUOUS = frozenset("0Ool1LI")


def _filter_ambiguous(chars: str) -> str:
    return "".join(c for c in chars if c not in _AMBIGUOUS)


def generate_password(
    length: int, include_symbols: bool, exclude_ambiguous: bool = False
) -> str:
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.?"

    if exclude_ambiguous:
        letters = _filter_ambiguous(letters)
        digits = _filter_ambiguous(digits)

    pool = letters + digits + (symbols if include_symbols else "")

    # Ensure the password has at least one letter and one digit.
    required = [
        secrets.choice(letters),
        secrets.choice(digits),
    ]

    if include_symbols:
        required.append(secrets.choice(symbols))

    if length < len(required):
        raise ValueError(
            f"Length must be at least {len(required)} when current options are enabled."
        )

    remaining = [secrets.choice(pool) for _ in range(length - len(required))]
    chars = required + remaining

    # Cryptographically secure shuffle.
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]

    return "".join(chars)


def estimate_entropy_bits(password: str, pool_size: int) -> float:
    """Shannon bits if each char were IID uniform from a pool of size N."""
    if pool_size < 2:
        return 0.0
    return len(password) * math.log2(pool_size)


def copy_to_clipboard(text: str) -> None:
    if sys.platform != "darwin":
        raise RuntimeError("--copy is only supported on macOS (pbcopy).")
    subprocess.run(
        ["pbcopy"],
        input=text,
        text=True,
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate secure random passwords.")
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
        help="Length of each password (default: 16).",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols and use only letters + digits.",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="How many passwords to generate (default: 1).",
    )
    parser.add_argument(
        "--exclude-ambiguous",
        action="store_true",
        help="Omit easy-to-confuse characters (e.g. 0/O, 1/l/I).",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print estimated entropy (bits) after each password.",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy generated text to clipboard (macOS only). All passwords if count > 1.",
    )
    return parser.parse_args()


def _pool_size(include_symbols: bool, exclude_ambiguous: bool) -> int:
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.?"
    if exclude_ambiguous:
        letters = _filter_ambiguous(letters)
        digits = _filter_ambiguous(digits)
    n = len(letters) + len(digits)
    if include_symbols:
        n += len(symbols)
    return n


def main() -> None:
    args = parse_args()
    include_symbols = not args.no_symbols

    if args.count < 1:
        raise ValueError("Count must be at least 1.")

    passwords: list[str] = []
    pool_size = _pool_size(include_symbols, args.exclude_ambiguous)

    for _ in range(args.count):
        pw = generate_password(
            args.length, include_symbols, exclude_ambiguous=args.exclude_ambiguous
        )
        passwords.append(pw)
        print(pw, flush=True)
        if args.stats:
            bits = estimate_entropy_bits(pw, pool_size)
            print(
                f"  (~{bits:.1f} bits if IID from charset of size {pool_size})",
                file=sys.stderr,
            )

    if args.copy:
        copy_to_clipboard("\n".join(passwords))


if __name__ == "__main__":
    main()
