"""Adversarial environment canary for E14 G6/G7.

This probe does not import the admission scanner or vendor code. It tests the externally supplied
container envelope and writes only to the temporary /output probe mount.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from typing import Any


EXPECTED_A1_TERMINAL = "33C3035DC90D7758A6D92BDE3D9CA629088AB94B1347881E929CEA21AED11879"
EXPECTED_SCANNER = "D8D51375723E8B705736CD9492825FCE03BC65CDACCE0DD6BE7791E3E51259C7"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def read_status() -> dict[str, str]:
    result: dict[str, str] = {}
    for line in Path("/proc/self/status").read_text(encoding="ascii").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key] = value.strip()
    return result


def net_counters() -> dict[str, dict[str, int]]:
    lines = Path("/proc/net/dev").read_text(encoding="ascii").splitlines()[2:]
    result: dict[str, dict[str, int]] = {}
    for line in lines:
        interface, values = line.split(":", 1)
        fields = [int(value) for value in values.split()]
        result[interface.strip()] = {"rx_bytes": fields[0], "tx_bytes": fields[8]}
    return result


def denied_write(path: Path) -> dict[str, Any]:
    try:
        with path.open("ab") as handle:
            handle.write(b"x")
    except OSError as exc:
        return {"denied": True, "errno": exc.errno, "error": type(exc).__name__}
    return {"denied": False}


def main() -> int:
    before_network = net_counters()
    network_attempt: dict[str, Any]
    try:
        with socket.create_connection(("1.1.1.1", 443), timeout=0.5):
            network_attempt = {"denied": False}
    except OSError as exc:
        network_attempt = {"denied": True, "errno": exc.errno, "error": type(exc).__name__}
    after_network = net_counters()

    child_attempt: dict[str, Any]
    try:
        child = subprocess.run(
            ["/bin/true"],
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1,
        )
        child_attempt = {"denied": False, "returncode": child.returncode}
    except (OSError, subprocess.SubprocessError) as exc:
        child_attempt = {
            "denied": True,
            "errno": getattr(exc, "errno", None),
            "error": type(exc).__name__,
        }

    status = read_status()
    interpreter = Path("/proc/self/exe").resolve()
    scanner = Path("/tool/e14_admission.py")
    terminal = Path("/input/terminal-receipt.json")
    scanner_hash = digest(scanner)
    terminal_hash = digest(terminal)

    report = {
        "schema": "sana.e14.a3-boot-net-probe.v1",
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "uid": os.getuid(),
        "gid": os.getgid(),
        "interfaces": sorted(path.name for path in Path("/sys/class/net").iterdir()),
        "network_before": before_network,
        "network_after": after_network,
        "external_connect_attempt": network_attempt,
        "child_attempt": child_attempt,
        "proc_status": {
            "CapEff": status.get("CapEff"),
            "NoNewPrivs": status.get("NoNewPrivs"),
            "Seccomp": status.get("Seccomp"),
            "Threads": status.get("Threads"),
            "NSpid": status.get("NSpid"),
        },
        "cgroup": {
            "pids_max": Path("/sys/fs/cgroup/pids.max").read_text(encoding="ascii").strip(),
            "memory_max": Path("/sys/fs/cgroup/memory.max").read_text(encoding="ascii").strip(),
            "cpu_max": Path("/sys/fs/cgroup/cpu.max").read_text(encoding="ascii").strip(),
        },
        "mount_write_tests": {
            "input": denied_write(Path("/input/terminal-receipt.json")),
            "tool": denied_write(scanner),
            "rootfs": denied_write(Path("/etc/e14-probe")),
        },
        "input_terminal_sha256": terminal_hash,
        "input_terminal_matches": terminal_hash == EXPECTED_A1_TERMINAL,
        "scanner_sha256": scanner_hash,
        "scanner_matches": scanner_hash == EXPECTED_SCANNER,
        "interpreter_path": str(interpreter),
        "interpreter_sha256": digest(interpreter),
        "python_version": sys.version,
        "isolated_flag": sys.flags.isolated,
        "no_site_flag": sys.flags.no_site,
        "dont_write_bytecode": sys.dont_write_bytecode,
        "sys_path": sys.path,
        "ambient_rfc8785_spec": importlib.util.find_spec("rfc8785") is not None,
        "module_origins": sorted(
            {
                str(getattr(module, "__file__", "built-in"))
                for module in sys.modules.values()
                if module is not None
            }
        ),
        "authority_effect": "NONE",
        "admission_executed": False,
    }
    output = Path("/output/probe-ready.json")
    output.write_text(
        json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    time.sleep(8)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))

    success = all(
        [
            report["pid"] == 1,
            report["ppid"] == 0,
            report["interfaces"] == ["lo"],
            network_attempt["denied"],
            before_network == after_network,
            child_attempt["denied"],
            report["proc_status"]["CapEff"] == "0000000000000000",
            report["proc_status"]["NoNewPrivs"] == "1",
            report["cgroup"]["pids_max"] == "1",
            report["cgroup"]["memory_max"] == "536870912",
            all(item["denied"] for item in report["mount_write_tests"].values()),
            report["input_terminal_matches"],
            report["scanner_matches"],
            report["isolated_flag"] == 1,
            report["no_site_flag"] == 1,
            report["dont_write_bytecode"],
            not report["ambient_rfc8785_spec"],
        ]
    )
    return 0 if success else 3


if __name__ == "__main__":
    raise SystemExit(main())
