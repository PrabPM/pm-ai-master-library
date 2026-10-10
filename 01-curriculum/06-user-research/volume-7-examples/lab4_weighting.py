"""Lab 4: does the survey's top answer survive weighting by device?

Respondents were mostly on computers; the merchants who gave up were mostly on
phones. Weight each device group back to its share of the people surveyed.
"""
FRAME_SHARE = {"phone": 564 / 840, "computer": 276 / 840}   # who gave up
RESPONDENTS = {"phone": 95, "computer": 121}                # who answered
PICKED = {                                                  # answer, by device
    "No document to hand": {"phone": 44, "computer": 34},
    "Did not understand a question": {"phone": 16, "computer": 25},
    "Lost my progress": {"phone": 21, "computer": 11},
    "Taking too long": {"phone": 3, "computer": 8},
}


def main():
    n = sum(RESPONDENTS.values())
    print(f"phones: {FRAME_SHARE['phone']:.0%} of those who gave up, "
          f"{RESPONDENTS['phone'] / n:.0%} of those who answered\n")
    print(f"{'answer':<32}{'as collected':>13}{'weighted':>10}")
    for answer, by_device in PICKED.items():
        raw = sum(by_device.values()) / n
        weighted = sum(FRAME_SHARE[d] * by_device[d] / RESPONDENTS[d]
                       for d in RESPONDENTS)
        print(f"{answer:<32}{raw:>13.0%}{weighted:>10.0%}")


if __name__ == "__main__":
    main()
