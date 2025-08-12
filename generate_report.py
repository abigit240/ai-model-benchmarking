import pandas as pd
import matplotlib.pyplot as plt

csv_file = "ollama_benchmarks.csv"
df = pd.read_csv(csv_file)

# Group by model, compute mean & std
stats = df.groupby("model").agg(["mean", "std"])
stats = stats.round(2)

# Generate Markdown table
md = "| Model | Cold Start (s) | Warm Start (s) | TPS | VRAM Before (MB) | VRAM After (MB) |\n"
md += "|-------|----------------|----------------|-----|------------------|-----------------|\n"
for model in stats.index:
    md += f"| {model} | {stats.loc[model, ('cold_start_sec','mean')]} ± {stats.loc[model, ('cold_start_sec','std')]} | "
    md += f"{stats.loc[model, ('warm_start_sec','mean')]} ± {stats.loc[model, ('warm_start_sec','std')]} | "
    md += f"{stats.loc[model, ('tokens_per_sec','mean')]} ± {stats.loc[model, ('tokens_per_sec','std')]} | "
    md += f"{stats.loc[model, ('vram_before_mb','mean')]} ± {stats.loc[model, ('vram_before_mb','std')]} | "
    md += f"{stats.loc[model, ('vram_after_mb','mean')]} ± {stats.loc[model, ('vram_after_mb','std')]} |\n"

with open("benchmark_report.md", "w") as f:
    f.write("# LLM Benchmark Results\n\n")
    f.write(md)

print("✅ Markdown table saved to benchmark_report.md")
print(md)

# Plot comparison
fig, ax = plt.subplots(1, 3, figsize=(12,4))

metrics = ["cold_start_sec", "warm_start_sec", "tokens_per_sec"]
titles = ["Cold Start (s)", "Warm Start (s)", "Tokens/sec"]

for i, metric in enumerate(metrics):
    stats_metric = df.groupby("model")[metric].mean()
    stats_metric.plot(kind="bar", ax=ax[i])
    ax[i].set_title(titles[i])
    ax[i].set_ylabel(metric)
    ax[i].grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig("benchmark_plot.png")
print("📊 Plot saved to benchmark_plot.png")
