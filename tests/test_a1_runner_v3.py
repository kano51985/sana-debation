import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-08-27-p6-p3-1-e14-a0-download-only-runner-v3.ps1"
)


HARNESS = r"""
$ErrorActionPreference = 'Stop'
$source = Get-Content -LiteralPath $env:SANA_RUNNER_UNDER_TEST -Raw
$start = $source.IndexOf('Set-StrictMode -Version Latest')
$end = $source.IndexOf('$manifest = $null')
if ($start -lt 0 -or $end -le $start) {
    throw 'Unable to isolate runner definitions.'
}
Invoke-Expression $source.Substring($start, $end - $start)

$orderedInventory = @(
    [ordered]@{ path = 'a'; bytes = [int64]7; sha256 = 'A' },
    [ordered]@{ path = 'b'; bytes = [int64]11; sha256 = 'B' }
)
$sum = Get-InventoryTotalBytes -Inventory $orderedInventory
if ($sum -ne 18) {
    throw "OrderedDictionary sum mismatch: $sum"
}

$overflowRejected = $false
try {
    Get-InventoryTotalBytes -Inventory @(
        [ordered]@{ path = 'max'; bytes = [int64]::MaxValue; sha256 = 'A' },
        [ordered]@{ path = 'one'; bytes = [int64]1; sha256 = 'B' }
    ) | Out-Null
}
catch {
    $overflowRejected = $_.Exception.Message -match 'ACQUISITION_OUTPUT_SIZE_INVALID'
}
if (-not $overflowRejected) {
    throw 'Inventory byte-count overflow was not rejected.'
}

$script:OutputRoot = [IO.Path]::GetFullPath($env:SANA_TERMINAL_TEST_ROOT)
$script:TerminalWritten = $false
$script:RequestCount = 2
$script:TotalResponseBytes = 10
$caps = [pscustomobject]@{ output_files = 8; total_output_bytes = 1024 }
Write-TerminalReceipt -State 'ACQUISITION_COMPLETE_AWAITING_G1' `
    -FailureCode $null -FailureMessage $null -PackageFacts $null -Caps $caps

$terminalPath = Join-Path $script:OutputRoot 'terminal-receipt.json'
if (-not (Test-Path -LiteralPath $terminalPath -PathType Leaf)) {
    throw 'Terminal receipt was not written.'
}
$terminal = Get-Content -LiteralPath $terminalPath -Raw | ConvertFrom-Json
if ($terminal.state -ne 'ACQUISITION_COMPLETE_AWAITING_G1') {
    throw "Unexpected terminal state: $($terminal.state)"
}
if (@($terminal.inventory).Count -ne 2) {
    throw "Unexpected pre-terminal inventory count: $(@($terminal.inventory).Count)"
}
"RUNNER_V3_TERMINAL_SEAL_OK"
"""


class A1RunnerV3Tests(unittest.TestCase):
    def test_ordered_dictionary_inventory_and_terminal_seal(self) -> None:
        self.assertTrue(RUNNER.is_file(), f"runner is missing: {RUNNER}")
        with tempfile.TemporaryDirectory(prefix="sana-a1-v3-") as temp_dir:
            root = Path(temp_dir)
            (root / "alpha.bin").write_bytes(b"abc")
            (root / "beta.bin").write_bytes(b"1234567")
            env = os.environ.copy()
            env["SANA_RUNNER_UNDER_TEST"] = str(RUNNER)
            env["SANA_TERMINAL_TEST_ROOT"] = str(root)
            completed = subprocess.run(
                ["pwsh", "-NoProfile", "-NonInteractive", "-Command", HARNESS],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        self.assertIn("RUNNER_V3_TERMINAL_SEAL_OK", completed.stdout)


if __name__ == "__main__":
    unittest.main()
