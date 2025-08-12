import sys
import time
import subprocess

model = sys.argv[1]
prompts = [
    "Write a short poem about the moon.",
    "Explain quantum physics in simple terms.",
    "List 10 animals that can fly."
]

total_tokens = 0
total_time = 0.0

for prompt in prompts:
    start = time.time()
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True
    )
    end = time.time()
    tokens = len(result.stdout.split())  # Rough token count
    total_tokens += tokens
    total_time += (end - start)

tps = total_tokens / total_time
print(round(tps, 2))
