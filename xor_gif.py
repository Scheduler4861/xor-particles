import numpy as np
import matplotlib.pyplot as plt
import imageio


class XORCausalDynamics:
    def __init__(self, size=120, noise=0.01):
        self.size = size
        self.grid = np.zeros((size, size), dtype=np.uint8)
        self.noise = noise

    def add_pattern(self, pattern, x, y):
        h, w = pattern.shape
        x_end = min(x + h, self.size)
        y_end = min(y + w, self.size)
        self.grid[x:x_end, y:y_end] ^= pattern[:x_end - x, :y_end - y]

    def step(self):
        g = self.grid

        new = (
            np.roll(g, 1, axis=0) ^
            np.roll(g, -1, axis=0) ^
            np.roll(g, 1, axis=1) ^
            np.roll(g, -1, axis=1)
        )

        if self.noise > 0:
            noise_mask = (np.random.rand(self.size, self.size) < self.noise)
            new ^= noise_mask.astype(np.uint8)

        self.grid = new

    def run(self, steps):
        history = []
        for _ in range(steps):
            history.append(self.grid.copy())
            self.step()
        return history


def seed_diagonal():
    p = np.zeros((4, 4), dtype=np.uint8)
    np.fill_diagonal(p, 1)
    return p


def detect_persistent(history, threshold_ratio=0.2):
    acc = np.zeros_like(history[0], dtype=int)
    for g in history:
        acc += g
    threshold = int(len(history) * threshold_ratio)
    return acc >= threshold


def make_gif(filename="simulation.gif", steps=120):
    model = XORCausalDynamics(size=120, noise=0.01)

    p1 = seed_diagonal()
    p2 = np.flip(p1, axis=1)

    model.add_pattern(p1, 30, 40)
    model.add_pattern(p2, 80, 40)

    history = model.run(steps)
    particles = detect_persistent(history)

    images = []

    fig, ax = plt.subplots(figsize=(3, 3), dpi=80)

    for g in history:
        ax.clear()

        ax.imshow(g, cmap="gray", vmin=0, vmax=1)
        ax.imshow(particles, cmap="Reds", alpha=0.35)

        ax.axis("off")

        fig.canvas.draw()
        image = np.array(fig.canvas.renderer.buffer_rgba())[:, :, :3]
        images.append(image)

    plt.close(fig)

    imageio.mimsave(filename, images, duration=0.08)


if __name__ == "__main__":
    make_gif()
