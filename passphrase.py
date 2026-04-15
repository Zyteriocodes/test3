#!/usr/bin/env python3
"""
Generate memorable passphrases by sampling words uniformly from a fixed list (secrets).
Not compatible with the Diceware 7776-word standard — this is a lighter-weight tool.
"""
from __future__ import annotations

import argparse
import math
import secrets
import sys

# Embedded word list (uniform random choice per word via secrets).
_WORDS: tuple[str, ...] = tuple(
    """
    able acid acre aged also aqua atom auto away axis band barn belt best
    bird blue boat body bold book boot boxy brim bulb bump calm camp card
    cash city clay clip clock cloud coast coral craft creek dark dawn dell
    dial dock door dove draw drift drill drive dune dust each east echo edge
    elk elm emit epic fact fair farm fast field finch fire fish flame flare
    flat fleet flow foam foil fork form fort free fresh front frost full
    garden gate ghost glad globe glow gold grass green group grow gulf gull
    habit half hand happy harbor hawk head help hill hive home honor hope
    horse hotel hover huge icon idea idle image inch inner input invent island
    jewel joint jump june junk kayak keen keep key kick kilo kind kite known
    label lake lamp land lark last latch learn lens light limp lion list lumen
    lunar mad map march match maze merry metal meter mimic minor mist model
    month moon motor mount mouse movie music name narrow nature neat neon nest
    noble north notch novel oak ocean offer olive onion open orbit outer oval
    paint palm panel paper park path patio pearl pilot pine pixel plain plume
    polar pond porch print prism proof proud pulse puppy quest quilt quiet
    radar radio rain rally ranch rapid react reef relax rhythm ridge river
    roast robot rocky round rover rural rust sail sand scarf scene scope scout
    scrub seize shadow sharp shelf shell shine shoe shore shrub silent silk
    silver simple sketch skill skull slate sleep slide slope small smart smile
    smoke snake sneak snow solar solid sonic sound south spark speech spice
    spirit split spoke spray spring square stack stamp stand star static steel
    stick stone storm story strand stream stripe strong stump style sugar
    summit sun surf swarm sweat swift table talent talk tape task taste teach
    tent term thrift throw thumb thunder ticket timber titan toast token tonic
    track trail train trait tramp trend trial truce trunk trust tumble tunnel
    turf tutor twirl uncle undead unify union urban valid value vapor vessel
    vivid vocal voice vowel wagon water weave wheat whisper wide wind wire
    wisp wolf world woven write year yield young zebra zenith zesty zonal zoom
    """.split()
)


def generate_passphrase(word_count: int, separator: str) -> str:
    if word_count < 1:
        raise ValueError("Word count must be at least 1.")
    parts = [secrets.choice(_WORDS) for _ in range(word_count)]
    return separator.join(parts)


def estimated_entropy_bits(word_count: int) -> float:
    return word_count * math.log2(len(_WORDS))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Generate memorable passphrases from a fixed embedded word list "
            "(cryptographically random picks)."
        )
    )
    p.add_argument(
        "-w",
        "--words",
        type=int,
        default=6,
        help="Number of words per passphrase (default: 6).",
    )
    p.add_argument(
        "-s",
        "--separator",
        default="-",
        help="Separator between words (default: hyphen).",
    )
    p.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="How many passphrases to print (default: 1).",
    )
    p.add_argument(
        "--stats",
        action="store_true",
        help="Print estimated bits of entropy to stderr (IID word model).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.count < 1:
        raise ValueError("Count must be at least 1.")

    for _ in range(args.count):
        phrase = generate_passphrase(args.words, args.separator)
        print(phrase, flush=True)
        if args.stats:
            bits = estimated_entropy_bits(args.words)
            print(
                f"  (~{bits:.1f} bits, IID model over {len(_WORDS)} words)",
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
