import pandas as pd
import matplotlib.pyplot as plt

log_file = "gpu_usage_log.csv"
df = pd.read_csv(log_file, parse_dates=["timestamp"])

fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot GPU utilization (%)
ax1.set_xlabel("Time")
ax1.set_ylabel("GPU Utilization (%)", color="tab:blue")
ax1.plot(df["timestamp"], df["gpu_util"], color="tab:blue", label="GPU Util (%)")
ax1.tick_params(axis="y", labelcolor="tab:blue")

# VRAM usage on secondary axis
ax2 = ax1.twinx()
ax2.set_ylabel("VRAM Used (MB)", color="tab:red")
ax2.plot(df["timestamp"], df["vram_used_mb"], color="tab:red", linestyle="--", label="VRAM Used (MB)")
ax2.tick_params(axis="y", labelcolor="tab:red")

fig.tight_layout()
plt.title("GPU Usage During Benchmark")
plt.savefig("gpu_usage_plot.png")
print("📊 GPU usage plot saved as gpu_usage_plot.png")
