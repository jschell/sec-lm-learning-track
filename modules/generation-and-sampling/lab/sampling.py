"""Small original sampling calculations for an explicitly authored score vector."""
import math
import random


def probabilities(logits: list[float], temperature: float = 1.0, top_k: int = 0) -> list[float]:
    """Apply top-k then temperature/softmax; ties retain the earlier token index."""
    if not logits or any(not math.isfinite(x) for x in logits):
        raise ValueError('logits must be a nonempty finite score vector')
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError('temperature must be positive and finite')
    if type(top_k) is not int or top_k < 0:
        raise ValueError('top_k must be a nonnegative integer')
    indices = sorted(range(len(logits)), key=lambda i: (-logits[i], i))
    keep = indices[:top_k] if top_k else indices
    maximum = max(logits)
    weights = [math.exp((value - maximum) / temperature) if i in keep else 0.0
               for i,value in enumerate(logits)]
    total = sum(weights)
    return [value / total for value in weights]


def example(seed: int = 7) -> dict:
    """Calculate, don't impersonate a model: these four scores are authored."""
    logits = [2.0, 1.0, 0.0, -1.0]
    rows = []
    for temperature in (0.5, 1.0, 1.5):
        probs = probabilities(logits, temperature)
        rng = random.Random(seed)
        rows.append({'temperature':temperature, 'probabilities':probs,
                     'ten_samples':rng.choices(range(4), weights=probs, k=10)})
    return {'source':'authored four-token scores; no model inference', 'logits':logits,
            'greedy_token_index':0, 'rows':rows,
            'top_k_2_at_temperature_1':probabilities(logits,1.0,2)}
