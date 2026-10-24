# Game-Theoretic Analysis of Cyber Attack and Defense Strategies

## Abstract
This project models attacker-defender interactions as a finite two-player zero-sum game. Linear programming calculates optimal mixed strategies and equilibrium utility. A Streamlit dashboard provides payoff heatmaps, strategy distributions, scenario comparisons and sensitivity analysis.

## Problem Statement
Attackers and defenders make decisions while anticipating the other side. Game theory provides a structured way to compare choices under explicit utility assumptions.

## Objectives
1. Model attacker and defender strategies.
2. Construct a payoff matrix.
3. Compute equilibrium mixed strategies.
4. Compare six hypothetical scenarios.
5. Analyze sensitivity to utility assumptions.
6. Export data to CSV.

## Methodology
The attacker maximizes expected utility and the defender minimizes it. Expected utility is E(p,q)=pᵀAq. Linear programming computes the equilibrium strategies and game value.

## Implementation
Python, NumPy, SciPy, Pandas, Matplotlib and Streamlit. The app contains overview, strategy analysis, scenario comparison, sensitivity analysis and methodology tabs.

## Results
The dashboard displays equilibrium utility, strategy probabilities, expected payoffs, scenario ranking and sensitivity tables. Insert screenshots captured from the running app. All values are hypothetical and do not establish real-world control effectiveness.

## Limitations and Conclusion
The model assumes rational players, known utilities and zero-sum preferences. The app is an educational model and does not scan networks or execute attacks. It demonstrates how equilibrium and recommendations change when assumptions change.

## References
1. von Neumann & Morgenstern (1944), *Theory of Games and Economic Behavior*.
2. Nash (1950), “Equilibrium points in n-person games,” *PNAS* 36(1), 48–49.
3. Osborne (2004), *An Introduction to Game Theory*.
4. SciPy and Streamlit documentation.
