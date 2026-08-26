"""External controller for the E14 G6/G7 environment canary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import uuid
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IMAGE_ID = "sha256:c459db0b82f43b3b8fe0fb7b5d12d902c449764e9f1260c8483ce459514b9e89"
IMAGE_REPO_DIGEST = (
    "sana-calibration-s4-preflight@"
    "sha256:c459db0b82f43b3b8fe0fb7b5d12d902c449764e9f1260c8483ce459514b9e89"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def docker(*args: str, timeout: int = 30) -> str:
    completed = subprocess.run(
        ["docker", *args],
        check=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return completed.stdout.strip()


def selected_inspect(raw: dict[str, Any]) -> dict[str, Any]:
    host = raw["HostConfig"]
    config = raw["Config"]
    return {
        "image": raw["Image"],
        "user": config["User"],
        "cmd": config["Cmd"],
        "working_dir": config["WorkingDir"],
        "environment": sorted(config["Env"]),
        "network_mode": host["NetworkMode"],
        "readonly_rootfs": host["ReadonlyRootfs"],
        "pids_limit": host["PidsLimit"],
        "memory": host["Memory"],
        "memory_swap": host["MemorySwap"],
        "nano_cpus": host["NanoCpus"],
        "cap_drop": host["CapDrop"],
        "security_opt": host["SecurityOpt"],
        "mounts": sorted(
            [
                {
                    "destination": mount["Destination"],
                    "rw": mount["RW"],
                    "type": mount["Type"],
                }
                for mount in raw["Mounts"]
            ],
            key=lambda item: item["destination"],
        ),
        "networks": sorted(raw["NetworkSettings"]["Networks"]),
    }


def validate_prelaunch(measured: dict[str, Any]) -> None:
    expected = {
        "image": IMAGE_ID,
        "user": "10004:10004",
        "cmd": ["python", "-I", "-S", "-B", "/probe/e14_envelope_probe.py"],
        "working_dir": "/opt/sana",
        "network_mode": "none",
        "readonly_rootfs": True,
        "pids_limit": 1,
        "memory": 536870912,
        "memory_swap": 536870912,
        "nano_cpus": 1000000000,
        "cap_drop": ["ALL"],
        "security_opt": ["no-new-privileges:true"],
        "mounts": [
            {"destination": "/input", "rw": False, "type": "bind"},
            {"destination": "/output", "rw": True, "type": "bind"},
            {"destination": "/probe/e14_envelope_probe.py", "rw": False, "type": "bind"},
            {"destination": "/tool/e14_admission.py", "rw": False, "type": "bind"},
        ],
        "networks": ["none"],
    }
    mismatches = {
        key: {"expected": value, "measured": measured.get(key)}
        for key, value in expected.items()
        if measured.get(key) != value
    }
    if mismatches:
        raise RuntimeError("prelaunch envelope mismatch: " + json.dumps(mismatches, sort_keys=True))
    environment = measured["environment"]
    if "PYTHONPATH=" not in environment:
        raise RuntimeError("prelaunch envelope did not clear PYTHONPATH")


def main() -> int:
    a1 = (ROOT / "e14" / "vendor-acquisition-v2").resolve(strict=True)
    scanner = (ROOT / "src" / "e14_admission.py").resolve(strict=True)
    probe = (ROOT / "tools" / "e14_envelope_probe.py").resolve(strict=True)
    controller = Path(__file__).resolve(strict=True)
    admission_root = ROOT / "e14" / "vendor-admission-v1"
    if admission_root.exists():
        raise RuntimeError("future admission root must be absent")

    temporary_base = Path(tempfile.gettempdir()).resolve(strict=True)
    output = Path(tempfile.mkdtemp(prefix="sana-e14-envelope-", dir=temporary_base)).resolve()
    if output.parent != temporary_base or not output.name.startswith("sana-e14-envelope-"):
        raise RuntimeError("unsafe temporary output path")
    name = "sana-e14-g7-" + uuid.uuid4().hex
    container_created = False
    try:
        create_args = [
            "create",
            "--name",
            name,
            "--network",
            "none",
            "--read-only",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges:true",
            "--pids-limit",
            "1",
            "--memory",
            "536870912",
            "--memory-swap",
            "536870912",
            "--cpus",
            "1",
            "--user",
            "10004:10004",
            "--workdir",
            "/opt/sana",
            "--env",
            "PYTHONPATH=",
            "--mount",
            f"type=bind,src={a1},dst=/input,readonly",
            "--mount",
            f"type=bind,src={scanner},dst=/tool/e14_admission.py,readonly",
            "--mount",
            f"type=bind,src={probe},dst=/probe/e14_envelope_probe.py,readonly",
            "--mount",
            f"type=bind,src={output},dst=/output",
            IMAGE_ID,
            "python",
            "-I",
            "-S",
            "-B",
            "/probe/e14_envelope_probe.py",
        ]
        container_id = docker(*create_args)
        container_created = True
        prelaunch_raw = json.loads(docker("inspect", container_id))[0]
        prelaunch = selected_inspect(prelaunch_raw)
        validate_prelaunch(prelaunch)
        docker("start", container_id)

        ready = output / "probe-ready.json"
        deadline = time.monotonic() + 20
        while not ready.is_file() and time.monotonic() < deadline:
            time.sleep(0.1)
        if not ready.is_file():
            raise RuntimeError("probe did not reach observation point")

        top = docker("top", container_id)
        stats_text = docker(
            "stats",
            "--no-stream",
            "--format",
            "{{json .}}",
            container_id,
        )
        running_raw = json.loads(docker("inspect", container_id))[0]
        exit_code = int(docker("wait", container_id, timeout=30))
        final_raw = json.loads(docker("inspect", container_id))[0]
        logs = docker("logs", container_id)
        probe_report = json.loads(ready.read_text(encoding="utf-8"))
        image_raw = json.loads(docker("image", "inspect", IMAGE_ID))[0]
        docker_version = json.loads(docker("version", "--format", "{{json .}}"))
        docker_info = json.loads(docker("info", "--format", "{{json .}}"))
        docker_path = Path(shutil.which("docker") or "").resolve(strict=True)

        stats = json.loads(stats_text)
        report = {
            "schema": "sana.e14.a2-g6-g7-envelope-evidence.v1",
            "status": "INCONCLUSIVE_PENDING_EXTERNAL_MODULE_OBSERVATION",
            "g6_envelope": "PASS" if exit_code == 0 else "INCONCLUSIVE",
            "g7_boot_network_child": "PARTIAL_BLOCKING_EXTERNAL_MODULE_OBSERVATION"
            if exit_code == 0
            else "INCONCLUSIVE",
            "authority_effect": "NONE",
            "admission_executed": False,
            "external_tcb": {
                "docker_cli_path": str(docker_path),
                "docker_cli_sha256": digest(docker_path),
                "docker_version": docker_version,
                "docker_operating_system": docker_info["OperatingSystem"],
                "docker_os_type": docker_info["OSType"],
                "docker_architecture": docker_info["Architecture"],
                "docker_security_options": docker_info["SecurityOptions"],
            },
            "controller": {
                "path": "tools/run_e14_envelope_probe.py",
                "sha256": digest(controller),
            },
            "probe": {
                "path": "tools/e14_envelope_probe.py",
                "sha256": digest(probe),
            },
            "scanner": {
                "path": "src/e14_admission.py",
                "sha256": digest(scanner),
            },
            "image": {
                "id": image_raw["Id"],
                "repo_digest": IMAGE_REPO_DIGEST,
                "rootfs_layers": image_raw["RootFS"]["Layers"],
            },
            "prelaunch": prelaunch,
            "running_state": {
                "pid": running_raw["State"]["Pid"],
                "running": running_raw["State"]["Running"],
                "networks": sorted(running_raw["NetworkSettings"]["Networks"]),
            },
            "external_process_observation": top.splitlines(),
            "external_resource_observation": stats,
            "exit": {
                "code": exit_code,
                "oom_killed": final_raw["State"]["OOMKilled"],
                "error": final_raw["State"]["Error"],
            },
            "probe_report": probe_report,
            "stdout_sha256": hashlib.sha256(logs.encode("utf-8")).hexdigest().upper(),
            "external_module_observation": {
                "status": "PARTIAL",
                "basis": "image/rootfs identity and exact command are external; loaded module origins are guest-reported",
            },
            "future_admission_root_absent": not admission_root.exists(),
            "temporary_probe_output_removed": True,
            "next_stage": "FRESH_CHIEF_REVIEW_REQUIRED",
        }
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if exit_code == 0 else 3
    finally:
        if container_created:
            subprocess.run(
                ["docker", "rm", "-f", name],
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
        if output.exists() and output.parent == temporary_base and output.name.startswith(
            "sana-e14-envelope-"
        ):
            shutil.rmtree(output)


if __name__ == "__main__":
    raise SystemExit(main())
