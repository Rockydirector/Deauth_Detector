import numpy as np

def trilaterate(positions, distances):
    # positions: list of (x, y)
    # distances: list of distances to attacker
    # Simple least squares trilateration
    A = []
    b = []
    for i in range(1, len(positions)):
        x0, y0 = positions[0]
        xi, yi = positions[i]
        di2 = distances[i] ** 2
        d02 = distances[0] ** 2
        A.append([2*(xi-x0), 2*(yi-y0)])
        b.append(di2 - d02 - xi**2 + x0**2 - yi**2 + y0**2)
    A = np.array(A)
    b = np.array(b)
    pos, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return pos[0], pos[1]
