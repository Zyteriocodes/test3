#!/usr/bin/env python3
import argparse
import secrets
import string


def generate_password(length: int, include_symbols: bool) -> str:
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.?"

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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    include_symbols = not args.no_symbols

    if args.count < 1:
        raise ValueError("Count must be at least 1.")

    for _ in range(args.count):
        print(generate_password(args.length, include_symbols))


if __name__ == "__main__":
    main()
