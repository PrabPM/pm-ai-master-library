"""Chapter 18: rank an experiment backlog with ICE (impact, confidence, ease)."""
BACKLOG = {  # idea: (impact, confidence, ease), each scored 1 to 10 by the team
    "Guided setup checklist": (8, 7, 5),
    "Fix mobile bank-link handoff": (6, 9, 8),
    "Shorter sign-up form": (4, 5, 9),
    "Assist setup concierge": (7, 3, 2),
    "Animated welcome video": (2, 3, 6),
}



def ice(scores):
    impact, confidence, ease = scores
    return impact * confidence * ease


print(f"{'Idea':<30}{'I':>3}{'C':>3}{'E':>3}{'ICE':>6}")
for idea, scores in sorted(BACKLOG.items(), key=lambda item: -ice(item[1])):
    print(f"{idea:<30}{scores[0]:>3}{scores[1]:>3}{scores[2]:>3}{ice(scores):>6}")
