import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, BoundaryNorm
from pathlib import Path

# Load aggregated results
results_path = Path("/Users/joshuafonseca/dev/introspection/results.json")
with results_path.open() as f:
    raw = json.load(f)

rows = []
for key, stats in raw.items():
    concept = stats["concept"]
    if concept == "NONE":
        continue  # skip controls on the heatmap
    strength = float(stats["strength"])

    if stats["brain_damage"] > 0:
        status = "brain damage"
    elif stats["misidentifications"] > 0:
        status = "misidentification"
    elif stats["successes"] > 0 or stats["detections"] > 0:
        status = "success"
    else:
        status = "no detection"

    rows.append({
        "concept": concept,
        "strength": strength,
        "status": status
    })

df = pd.DataFrame(rows)
df["strength"] = df["strength"].astype(float)

# Order strengths/concepts for readability
strength_order = sorted(df["strength"].unique())
concept_order = sorted(df["concept"].unique())

# Select up to 10 concepts: all that achieved success, plus fillers.
success_concepts = df.loc[df["status"] == "success", "concept"].unique().tolist()
other_concepts = [c for c in concept_order if c not in success_concepts]
selected_concepts = success_concepts[:10]
remaining_slots = 10 - len(selected_concepts)
if remaining_slots > 0:
    selected_concepts.extend(other_concepts[:remaining_slots])

status_levels = ["no detection", "misidentification", "success", "brain damage"]
status_to_val = {status: idx for idx, status in enumerate(status_levels)}
df["status_val"] = df["status"].map(status_to_val)

pivot = df.pivot(index="concept", columns="strength", values="status_val")
pivot = pivot.reindex(index=selected_concepts, columns=strength_order)
pivot = pivot.fillna(status_to_val["no detection"])

# Colour palette (tweak to taste)
colors = [
    "#f5f5f5",  # no detection
    "#fdbb84",  # misidentification
    "#66c2a5",  # success
    "#d73027",  # brain damage
]
cmap = ListedColormap(colors)
bounds = np.arange(len(status_levels) + 1) - 0.5
norm = BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(12, 9), dpi=150)
sns.heatmap(
    pivot,
    ax=ax,
    cmap=cmap,
    norm=norm,
    cbar=False,
    linewidths=0.5,
    linecolor="#ffffff"
)

ax.set_title("DeepSeek 7B Introspection Outcomes by Concept & Strength", fontsize=16, pad=16)
ax.set_xlabel("Steering strength")
ax.set_ylabel("Concept")
ax.set_xticklabels([str(int(s)) if s.is_integer() else str(s) for s in pivot.columns])
ax.tick_params(axis="x", rotation=0)
ax.tick_params(axis="y", rotation=0)

# Legend
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color=colors[i], ec="black", lw=0.4)
    for i in range(len(status_levels))
]
ax.legend(
    legend_handles,
    status_levels,
    title="Outcome",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    borderaxespad=0.
)

plt.tight_layout()
plt.savefig("deepseek_introspection_heatmap.png", dpi=300)
plt.show()