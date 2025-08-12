param (
    [string]$model
)

# CSV file path
$csvFile = "ollama_benchmarks.csv"

# Function to get VRAM usage in MB
function Get-VRAM {
    $nvidia = nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits
    return [int]$nvidia
}

Write-Host "Benchmarking $model..."

# Step 1: VRAM before load
$vramBefore = Get-VRAM
Write-Host "VRAM before load: $vramBefore MB"

# Step 2: Cold start time
$coldTime = (Measure-Command {
    ollama run $model "Say hello" | Out-String -Stream | ForEach-Object { $_ }
}).TotalSeconds
Write-Host "Cold start time: $coldTime sec"

# Step 3: VRAM after load
$vramAfter = Get-VRAM
Write-Host "VRAM after load: $vramAfter MB"

# Step 4: Warm run time
$warmTime = (Measure-Command {
    ollama run $model "Say hello" | Out-String -Stream | ForEach-Object { $_ }
}).TotalSeconds
Write-Host "Warm start time: $warmTime sec"

# Step 5: Tokens/sec via Python script (UTF-8 safe)
$tps = & python -X utf8 tps_test.py $model 2>&1
$tps = $tps -replace '[^\x00-\x7F]', ''  # remove any non-ASCII chars
Write-Host "Tokens/sec: $tps"

# Step 6: Append to CSV
if (-not (Test-Path $csvFile)) {
    "model,vram_before_mb,vram_after_mb,cold_start_sec,warm_start_sec,tokens_per_sec" | Out-File $csvFile -Encoding UTF8
}
"$model,$vramBefore,$vramAfter,$coldTime,$warmTime,$tps" | Out-File $csvFile -Append -Encoding UTF8

Write-Host "Benchmark complete. Results saved to $csvFile"
