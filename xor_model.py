import numpy as np
import matplotlib.pyplot as plt


class XORCausalDynamics:
    def __init__(self, size=100):
        self.size = size
        self.grid = np.zeros((size, size), dtype=np.uint8)

    def add_pattern(self, pattern, x, y):
        h, w = pattern.shape
        x_end = min(x + h, self.size)
        y_end = min(y + w, self.size)
        self.grid[x:x_end, y:y_end] ^= pattern[:x_end - x, :y_end - y]

    def step(self):
        g = self.grid
        self.grid = (
            np.roll(g, 1, axis=0) ^
            np.roll(g, -1, axis=0) ^
            np.roll(g, 1, axis=1) ^
            np.roll(g, -1, axis=1)
        )

    def run(self, steps):
        history = []
        for _ in range(steps):
            history.append(self.grid.copy())
            self.step()
        return history


def K(x):
    return (
        np.roll(x, 1, axis=0) ^
        np.roll(x, -1, axis=0) ^
        np.roll(x, 1, axis=1) ^
        np.roll(x, -1, axis=1)
    )


def invariant(grid, weight):
    return int(np.sum(grid * weight) % 2)


def is_fixed_point(w):
    return np.array_equal(K(w), w)


def generate_weight_constant(size):
    return np.ones((size, size), dtype=np.uint8)


def generate_weight_local(size, radius=3):
    w = np.zeros((size, size), dtype=np.uint8)
    c = size // 2
    w[c-radius:c+radius+1, c-radius:c+radius+1] = 1
    return w


def test_invariance(history, weight):
    values = [invariant(g, weight) for g in history]
    return len(set(values)) == 1


def seed_diagonal():
    p = np.zeros((4, 4), dtype=np.uint8)
    np.fill_diagonal(p, 1)
    return p


def detect_persistent(history, ratio=0.15):
    threshold = int(len(history) * ratio)
    acc = np.zeros_like(history[0], dtype=int)
    for g in history:
        acc += g
    return acc >= threshold


def centroid(grid):
    coords = np.argwhere(grid > 0)
    return None if len(coords) == 0 else coords.mean(axis=0)


def velocity(history):
    pos = [c for g in history if (c := centroid(g)) is not None]
    return None if len(pos) < 2 else np.diff(np.array(pos), axis=0).mean(axis=0)


def stable(history, tol=1.0):
    sizes = np.array([g.sum() for g in history])
    return len(sizes) > 1 and np.std(sizes) < tol


def visualize(history, particles=None, interval=0.08):
    plt.figure(figsize=(6, 6))
    for t, g in enumerate(history):
        plt.clf()
        plt.imshow(g, cmap="gray", alpha=0.7)
        if particles is not None:
            plt.imshow(particles, cmap="Reds", alpha=0.5)
        plt.title(f"t = {t}")
        plt.axis("off")
        plt.pause(interval)
    plt.show(block=True)


def experiment():
    size = 120
    model = XORCausalDynamics(size)

    p1 = seed_diagonal()
    p2 = np.flip(p1, axis=1)

    model.add_pattern(p1, 30, 40)
    model.add_pattern(p2, 80, 40)

    history = model.run(120)
    particles = detect_persistent(history)

    w_global = generate_weight_constant(size)
    w_local = generate_weight_local(size, 3)

    return {
        "history": history,
        "particles": particles,
        "global_invariant": test_invariance(history, w_global),
        "local_invariant": test_invariance(history, w_local),
        "global_fixed": is_fixed_point(w_global),
        "local_fixed": is_fixed_point(w_local)
    }


if __name__ == "__main__":
    result = experiment()

    print("Global invariant:", result["global_invariant"])
    print("Local invariant:", result["local_invariant"])
    print("Global fixed point:", result["global_fixed"])
    print("Local fixed point:", result["local_fixed"])
    print("Velocity:", velocity(result["history"]))
    print("Stable:", stable(result["history"]))

    visualize(result["history"], result["particles"])
