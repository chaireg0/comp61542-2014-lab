
def mean(X):
    n = len(X)
    if n > 0:
        return float(sum(X)) / float(len(X))
    return 0


def median(X):
    n = len(X)
    if n == 0:
        return 0
    L = sorted(X)
    if n % 2:
        return L[n / 2]
    return mean(L[(n / 2) - 1:(n / 2) + 1])

def mode(X):
    n = len(X)
    if n == 0:
        return []

    d = {}
    max = 0
    for item in X:
        if d.has_key(item):
            d[item] += 1
        else:
            d[item] = 1
        
        if d[item] > max:
            max = d[item]

    m = []
    for key in d.keys():
        if d[key] == max:
            m.append(key)
    m.sort()
    return m 
