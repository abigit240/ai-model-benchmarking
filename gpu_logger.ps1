param (
    [string]$outfile = "gpu_usage_log.csv",
    [int]$intervalSec = 15
)

# CSV header
"timestamp,gpu_util,vram_used_mb" | Out-File $outfile -Encoding utf8

Write-Host " Logging GPU usage to $outfile every $intervalSec sec..."
while ($true) {
    try {
        $data = nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits
        $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        $gpuUtil, $vramUsed = $data -split ","
        Add-Content -Path $outfile -Value "$timestamp,$gpuUtil,$vramUsed"
    }
    catch {
        Write-Warning "Error logging GPU data: $_"
    }
    Start-Sleep -Seconds $intervalSec
}
