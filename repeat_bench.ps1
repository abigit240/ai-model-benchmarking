param (
    [string[]]$models = @("llama3", "gpt-oss:20b"),
    [int]$runs = 3
)

foreach ($model in $models) {
    Write-Host "=== Running $model for $runs runs ==="
    for ($i = 1; $i -le $runs; $i++) {
        Write-Host "Run $i of $runs..."
        .\ollama_bench.ps1 $model
    }
}
Write-Host "✅ All runs complete. Results are in ollama_benchmarks.csv"
