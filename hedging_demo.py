# (1)  --- Imports ---
import os                             # (2)
import numpy as np                    # (3)
import pandas as pd                   # (4)
import matplotlib.pyplot as plt       # (5)

# (6)  --- Scenario Setup ---
spot = 0.85                           # (7)  current EUR/GBP spot rate today
forward_rate = 0.86                   # (8)  3-month forward rate agreed today
strike = 0.86                         # (9)  option strike (EUR call / GBP put)
premium_pct = 0.02                    # (10) option premium as % of notional (2%)
notional_eur = 1_000_000              # (11) exposure: €1,000,000 payable in 3 months

# (12) --- Future scenarios (what EUR/GBP could be in 3 months) ---
future_rates = np.linspace(0.80, 0.95, 16)   # (13) evenly spaced values 0.80→0.95 (16 points)

# (14) --- Helper: Convert EUR premium to GBP at today's spot (paid upfront) ---
premium_gbp = (premium_pct * notional_eur) / spot   # (15)

# (16) --- Payoff functions (GBP cost to buy €1m under each strategy) ---
def gbp_cost_no_hedge(rate: float) -> float:        # (17)
    return notional_eur / rate                      # (18)

def gbp_cost_forward() -> float:                    # (19)
    return notional_eur / forward_rate              # (20)

def gbp_cost_option(rate: float) -> float:          # (21)
    core_fx_cost = (notional_eur / strike) if rate > strike else (notional_eur / rate)  # (22)
    return core_fx_cost + premium_gbp              # (23)

# (24) --- Build results table for each future rate ---
rows = []                                          # (25)
for r in future_rates:                             # (26)
    rows.append({                                  # (27)
        "EUR/GBP in 3m": round(float(r), 3),       # (28)
        "No Hedge (GBP)": gbp_cost_no_hedge(r),    # (29)
        "Forward Hedge (GBP)": gbp_cost_forward(), # (30)
        "Option Hedge (GBP)": gbp_cost_option(r),  # (31)
    })

df = pd.DataFrame(rows)                            # (32)

# (33) --- Pretty print to terminal ---
pd.options.display.float_format = "{:,.0f}".format # (34)
print("\n--- Payoff Table (GBP cost to buy €1,000,000) ---\n")  # (35)
print(df.to_string(index=False))                   # (36)

# (37) --- Ensure results directory exists ---
os.makedirs("results", exist_ok=True)              # (38)

# (39) --- Save table for your repo/docs ---
df.to_csv("results/payoff_table.csv", index=False) # (40)

# --- Decision metrics (save to file) ---
F = notional_eur / forward_rate                 
prem = premium_gbp                              
max_option_cost = (notional_eur / strike) + prem
min_option_cost = (notional_eur / future_rates.max()) + prem  

den = (1/forward_rate) - (prem / notional_eur)
opt_vs_fwd_breakeven = float('nan') if den <= 0 else 1/den

metrics_text = []
metrics_text.append("\n--- Decision Metrics ---")
metrics_text.append(f"Forward cost (locked): £{F:,.0f}")
metrics_text.append(f"Option max cost (if EUR > {strike}): £{max_option_cost:,.0f}")
metrics_text.append(f"Option min cost in our grid: £{min_option_cost:,.0f}")
if den <= 0:
    metrics_text.append("Option vs Forward breakeven: none (premium too large for breakeven below strike).")
else:
    metrics_text.append(f"Option vs Forward breakeven rate (below strike): EUR/GBP ≈ {opt_vs_fwd_breakeven:.4f}")
metrics_text.append("Interpretation: If future EUR/GBP falls below the breakeven, "
                    "the option (with premium) beats the forward; otherwise the forward is cheaper.")

# Print to terminal
print("\n".join(metrics_text))

# Save to file
with open("results/decision_metrics.txt", "w") as f:
    f.write("\n".join(metrics_text))

# (41) --- Plot comparison ---
plt.figure(figsize=(10, 6))                         # (42)
plt.plot(df["EUR/GBP in 3m"], df["No Hedge (GBP)"], label="No Hedge", marker="o")          
plt.plot(df["EUR/GBP in 3m"], df["Forward Hedge (GBP)"], label="Forward Hedge", linestyle="--") 
plt.plot(df["EUR/GBP in 3m"], df["Option Hedge (GBP)"], label="Option Hedge", linestyle=":")    

plt.xlabel("EUR/GBP in 3 months")                  
plt.ylabel("GBP Cost to Buy €1,000,000")           
plt.title("FX Hedging Strategies: No Hedge vs Forward vs Option")  
plt.legend()                                       
plt.grid(True)                                     

plt.tight_layout()                                 
plt.savefig("results/hedging_comparison.png", dpi=300)  
plt.show()                                         

# (39) --- Save table for your repo/docs ---
df.to_csv("results/payoff_table.csv", index=False) # (40)

# --- Decision metrics (comes before plotting now) ---
F = notional_eur / forward_rate
prem = premium_gbp
max_option_cost = (notional_eur / strike) + prem
min_option_cost = (notional_eur / future_rates.max()) + prem  

den = (1/forward_rate) - (prem / notional_eur)
opt_vs_fwd_breakeven = float('nan') if den <= 0 else 1/den

metrics_text = []
metrics_text.append("\n--- Decision Metrics ---")
metrics_text.append(f"Forward cost (locked): £{F:,.0f}")
metrics_text.append(f"Option max cost (if EUR > {strike}): £{max_option_cost:,.0f}")
metrics_text.append(f"Option min cost in our grid: £{min_option_cost:,.0f}")
if den <= 0:
    metrics_text.append("Option vs Forward breakeven: none (premium too large for breakeven below strike).")
else:
    metrics_text.append(f"Option vs Forward breakeven rate (below strike): EUR/GBP ≈ {opt_vs_fwd_breakeven:.4f}")
metrics_text.append("Interpretation: If future EUR/GBP falls below the breakeven, "
                    "the option (with premium) beats the forward; otherwise the forward is cheaper.")

# Print to terminal
print("\n".join(metrics_text))

# Save to file
with open("results/decision_metrics.txt", "w") as f:
    f.write("\n".join(metrics_text))

# (41) --- Plot comparison ---
plt.figure(figsize=(10, 6))
...


