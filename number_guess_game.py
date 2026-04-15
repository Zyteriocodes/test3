#!/usr/bin/env python3
"""Simple number guessing game."""

from __future__ import annotations

import random


def main() -> None:
    print("Welcome to the Number Guessing Game!")
    print("I am thinking of a number between 1 and 100.")
    print("Type q to quit.\n")

    secret = random.randint(1, 100)
    attempts = 0

    while True:
        user_input = input("Enter your guess: ").strip()

        if user_input.lower() == "q":
            print(f"You quit. The number was {secret}.")
            return

        if not user_input.isdigit():
            print("Please enter a valid whole number.")
            continue

        guess = int(user_input)
        if guess < 1 or guess > 100:
            print("Please guess a number from 1 to 100.")
            continue

        attempts += 1

        if guess < secret:
            print("Too low. Try again.\n")
        elif guess > secret:
            print("Too high. Try again.\n")
        else:
            print(f"Correct! You guessed it in {attempts} tries.")
            return


if __name__ == "__main__":
    main()
