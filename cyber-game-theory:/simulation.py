from game_model import DEFAULT_ATTACKS, DEFAULT_DEFENSES, DEFAULT_PAYOFF, solve_zero_sum_game
r=solve_zero_sum_game(DEFAULT_PAYOFF)
print("Payoff matrix:\n",DEFAULT_PAYOFF)
print("\nAttacker strategy:")
for a,p in zip(DEFAULT_ATTACKS,r["p"]): print(f"  {a}: {p:.3f}")
print("\nDefender strategy:")
for a,p in zip(DEFAULT_DEFENSES,r["q"]): print(f"  {a}: {p:.3f}")
print(f"\nEquilibrium attacker utility: {r['value']:.3f}")
