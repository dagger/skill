#!/usr/bin/env python3
"""Check the generator against a pinned release and a newer upstream release."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(work, *args):
    return subprocess.check_output(
        ["dagger", "--silent", *args], cwd=work, text=True
    ).strip()


with tempfile.TemporaryDirectory(prefix="dagger-skills-") as temp:
    work = Path(temp)
    subprocess.run(["git", "init", "-q", temp], check=True)
    shutil.copytree(ROOT / "dagger", work / "dagger")
    shutil.copytree(ROOT / "tests", work / "tests")
    (work / "dagger.toml").write_text(
        '[modules.dagger-skills]\nsource = "dagger"\n'
        '[modules.dagger-skills.settings]\nrepository = "dag://skills-tests/repository"\n'
        '[modules.skills-tests]\nsource = "tests"\n'
    )
    (work / ".agents/skills").mkdir(parents=True)
    hostname = run(work, "api", "call", "skills-tests", "server", "hostname")
    old_commit = run(work, "api", "call", "skills-tests", "repository", "tag", "--name=v1.0.0", "commit")
    old_ref = "refs/tags/v1.0.0"
    identity = hostname + "/skills"
    entries = [
        [["version", "2"]],
        ["", "git-latest", [identity], old_ref],
        ["", "git-sha", [identity, old_ref], old_commit],
    ]
    lock = work / "dagger.lock"
    lock.write_text("\n".join(json.dumps(row) for row in entries) + "\n")
    run(work, "generate", "-y")
    skill = work / ".agents/skills/dagger/SKILL.md"
    assert skill.read_text() == "released skill\n", "Did not use the old release pin"
    first_lock = lock.read_text()
    run(work, "generate", "-y")
    assert skill.read_text() == "released skill\n", "Generation followed the newer release"
    assert lock.read_text() == first_lock, "Generation changed the lockfile"
    run(work, "lock", "update")
    run(work, "generate", "-y")
    assert skill.read_text() == "released skill two\n", "Lock update did not select the new release"
    run(work, "check", "--generated=true")
    print("Pinned generation, repeat generation, lock update, and stale-file checks passed.")
