__all__ = ['none_min', 'none_max', 'json_safe']


def none_min(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    return min(a, b)


def none_max(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    return max(a, b)


def json_safe(data):
    import numpy as np

    if isinstance(data, dict):
        return {k: json_safe(v) for k, v in data.items()}
    elif isinstance(data, (tuple, list, np.ndarray)):
        return [json_safe(v) for v in data]
    else:
        try:
            if np.isscalar(data):
                return None if not np.isfinite(data) else data
        except Exception as e:
            pass

        return data

