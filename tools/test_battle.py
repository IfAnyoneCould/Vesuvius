import matplotlib.pyplot as plt
import numpy as np

from engine.core.container import HandlerContainer
from engine.systems.battle import battle
from engine.core.config import load_config
from engine.entities.unit import new_unit, remove_unit

N = 100_000
mod = 2

wins = np.zeros(N)
err1 = np.zeros(N)
err2 = np.zeros(N)

config = load_config()
handlers = HandlerContainer(config)

for i in range(N):
    unit1 = new_unit("warrior", handlers)
    unit2 = new_unit("warrior", handlers)
    handlers.damage_handler.set_damage_mod(unit1, mod)

    winner, dealt, damage, health = battle(unit1, unit2, handlers)

    max_dmg = max(damage[0], damage[1])
    exp1 = health[1] * damage[0] / (2 * max_dmg)
    exp2 = health[0] * damage[1] / (2 * max_dmg)

    wins[i] = 1 if winner == 0 else 0
    err1[i] = dealt[0] - exp1
    err2[i] = dealt[1] - exp2

    remove_unit(unit1, handlers)
    remove_unit(unit2, handlers)

print(f"unit1 win rate: {wins.mean():.1%}")
print(f"mean error  unit1: {err1.mean():.3f}  unit2: {err2.mean():.3f}")

plt.hist(err1, bins=50, alpha=0.5, label="unit1 (stronger)")
plt.hist(err2, bins=50, alpha=0.5, label="unit2")
plt.axvline(0, color="black", linestyle="--")
plt.xlabel("dealt[0] - dealt[1]")
plt.ylabel("battles")
plt.legend()
plt.show()
