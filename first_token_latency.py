import sys
import time
import requests

if len(sys.argv) < 2:
    print("Usage: python first_token_latency.py <model>")
    sys.exit(1)

model = sys.argv[1]
url = "http://localhost:11434/api/generate"
prompt = "Say hello in one sentence."

start_time = time.time()
first_token_time = None

with requests.post(url, json={"model": model, "prompt": prompt, "stream": True}, stream=True) as r:
    for line in r.iter_lines():
        if line:
            if first_token_time is None:
                first_token_time = time.time()
                print(f"First token latency: {first_token_time - start_time:.3f} sec")
            # Uncomment below to see tokens
            # print(line.decode('utf-8'))

if first_token_time is None:
    print("No tokens received — check model/server.")
