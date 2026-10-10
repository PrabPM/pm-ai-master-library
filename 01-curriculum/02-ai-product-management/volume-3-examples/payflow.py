"""Shared, made-up numbers for PayFlow Assist. PayFlow is a fictional company.

Every script in this folder imports its inputs from here, so the book's
figures stay consistent with each other.
"""

# Support workload per month ------------------------------------------------
SIMPLE_TICKETS = 3_200       # payout tickets with one known cause, 8 minutes each
COMPLEX_TICKETS = 4_800      # payout tickets that need several records, 18 minutes
AGENT_COST_PER_MIN = 0.70    # fully loaded cost of a support agent, in dollars

# Release 1: Assist drafts cited answers for agents on complex payout tickets
ANSWERS_PER_TICKET = 2.4
MINUTES_BEFORE = 18
MINUTES_AFTER = 12
TASK_SUCCESS = 0.92          # share of answers a reviewer accepts as right
RESOLVED_BEFORE = 0.71       # tickets resolved at first contact, before Assist
RESOLVED_AFTER = 0.78

# Illustrative prices, dollars per million tokens. Not any provider's price list.
LARGE = {"input": 4.00, "cached": 0.40, "output": 16.00}
SMALL = {"input": 0.40, "cached": 0.04, "output": 1.60}

# Tokens in one Assist answer ----------------------------------------------
PREFIX = 1_800        # system instruction and tool definitions (cacheable)
HISTORY = 600         # earlier turns of the conversation
EVIDENCE = 5 * 400    # five retrieved passages of about 400 tokens
TOOL_RESULTS = 700    # payout record and bank verification log
QUESTION = 60
OUTPUT = 320
CACHE_HIT_RATE = 0.70
RETRY_RATE = 0.04     # answers generated twice (timeout or invalid output)
SEARCH_COST = 0.0006  # embedding, vector search, rerank and tool calls, dollars


def dollars(tokens: float, price_per_million: float) -> float:
    return tokens * price_per_million / 1_000_000


# Release 2: Assist answers merchants directly in the dashboard
MERCHANT_QUESTIONS = 22_000      # per month
ANSWERS_PER_SESSION = 3.1
SESSIONS_RESOLVED = 0.62         # no ticket opened within 72 hours
WRONG_ANSWER_MINUTES = 3         # agent time lost noticing and redoing a bad draft
