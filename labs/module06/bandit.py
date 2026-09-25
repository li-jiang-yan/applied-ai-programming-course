"""A small learning agent in a simulated environment; standard library only."""
import random

def simulate(seed=42, steps=200):
    rng = random.Random(seed)
    values = [0.0, 0.0]
    counts = [0, 0]
    total = 0
    for _ in range(steps):
        # 20% exploration; otherwise choose the action with highest learned reward.
        action = rng.randrange(2) if rng.random() < 0.2 else max(range(2), key=lambda a: values[a])
        # Synthetic user satisfaction: detailed answers suit this population better.
        reward = int(rng.random() < [0.35, 0.75][action])
        counts[action] += 1
        values[action] += (reward - values[action]) / counts[action]
        total += reward
    return {"counts": counts, "estimated_rewards": values, "total_reward": total}

if __name__ == "__main__":
    print("Actions: 0=brief, 1=detailed. Rewards are simulated, not user feedback.")
    print(simulate())
