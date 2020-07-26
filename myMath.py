from math import sqrt


def factors(n):
    """
    Generates all factors of n. Iterates from sqrt(n) down to zero.
    When a factor x is found, another factor must be n divided by x.
    If n is odd, only odd numbers need to be checked.

    Taken from https://codereview.stackexchange.com/questions/147916/finding-all-factors-of-n-efficiently
    """
    root = sqrt(n)
    start = int(root)  # Default starting number is sqrt(n)

    if n % 2 == 0:
        step = -1  # n is even, so check both evens and odds
    else:
        step = -2  # n is odd, so check only odds
        start = start // 2 * 2 + 1  # Round start to odd number

    if root.is_integer():
        yield int(root)  # sqrt(n) is a factor of n
        # Start at numbers < sqrt(n), so that sqrt(n) is not yielded twice
        start += step

    for x in range(start, 0, step):
        if n % x == 0:
            yield x
            yield n // x
