"""Chapter 10: when does self-hosting beat a hosted API? Illustrative assumptions."""
import math

API_PRICE = 1.00            # dollars per million tokens, blended input and output
GPU_MONTH = 1_825           # one rented GPU server: $2.50 an hour for 730 hours
PEOPLE_MONTH = 10_500       # half an engineer, on-call cover and monitoring
MIN_GPUS = 2                # one is not enough: you need a spare for failures
TOKENS_PER_SECOND = 2_500   # per GPU, with requests batched together
SECONDS_PER_MONTH = 730 * 3600
ASSIST_TOKENS_M = 310       # PayFlow Assist, million tokens a month (Chapter 18)


# [listing]
def self_host_cost(million_tokens, utilization):
    """Monthly dollars to serve the volume on rented GPUs you operate."""
    per_gpu = TOKENS_PER_SECOND * SECONDS_PER_MONTH * utilization / 1_000_000
    gpus = max(MIN_GPUS, math.ceil(million_tokens / per_gpu))
    return gpus * GPU_MONTH + PEOPLE_MONTH, gpus


def break_even(utilization, api_price):
    """Smallest volume, in million tokens, where self-hosting is cheaper."""
    per_gpu = TOKENS_PER_SECOND * SECONDS_PER_MONTH * utilization / 1_000_000
    if GPU_MONTH / per_gpu >= api_price:
        return None     # each extra token costs more on your GPUs than on the API
    volume = 100
    while self_host_cost(volume, utilization)[0] >= volume * api_price:
        volume += 100
    return volume
# [end listing]


def main():
    print("Million tokens/month   Hosted API   Self-host (40% busy)   GPUs")
    for volume in (ASSIST_TOKENS_M, 3_000, 10_000, 30_000, 60_000):
        cost, gpus = self_host_cost(volume, 0.40)
        print(f"{volume:>20,}{volume * API_PRICE:>13,.0f}{cost:>23,.0f}{gpus:>7}")
    print()
    print("Break-even volume in million tokens a month")
    print("API price per million   GPUs 20% busy   40% busy   70% busy")
    for price in (0.50, 1.00, 5.00):
        row = f"{price:>21.2f}     "
        for utilization in (0.20, 0.40, 0.70):
            volume = break_even(utilization, price)
            row += f"{'never' if volume is None else format(volume, ','):>11}"
        print(row)


if __name__ == "__main__":
    main()
