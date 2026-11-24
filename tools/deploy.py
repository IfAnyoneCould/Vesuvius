# NOTE this file was written by an AI (Claude), not me. it's just a dev helper for copying
# files to the pico and is not part of the game or the code submission
# usage: uv run python tools/deploy.py [--dry-run] [--all]

import fnmatch
import os
import subprocess
import sys

# folders and files that live on the pico
DEVICE = ["main.py", "configs/", "drivers/", "engine/", "fonts/", "game/", "graphics/", "hardware/"]
EXCLUDE = [
    "*__pycache__*",
    "fonts/*/maps/*",
    "fonts/spleen/ezFBfont_spleen_5x8_ascii_08.py",
    "fonts/spleen/ezFBfont_spleen_8x16_ascii_14.py",
]
CHUNK = 15

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def on_device(path):
    if not any(path == d or path.startswith(d) for d in DEVICE):
        return False
    return not any(fnmatch.fnmatch(path, e) for e in EXCLUDE)


def git_files(all_files):
    if all_files:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
        return [l for l in out.splitlines() if l], []
    out = subprocess.run(
        ["git", "status", "--porcelain", "-uall"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    files, deleted = [], []
    for line in out.splitlines():
        status, path = line[:2], line[3:]
        if " -> " in path:
            path = path.split(" -> ")[1]
        path = path.strip('"')
        if "D" in status:
            deleted.append(path)
        else:
            files.append(path)
    return files, deleted


def mpremote(args):
    return subprocess.run(
        [sys.executable, "-m", "mpremote", *args], cwd=ROOT, stdin=subprocess.DEVNULL
    ).returncode


def main():
    all_files = "--all" in sys.argv
    dry = "--dry-run" in sys.argv
    files, deleted = git_files(all_files)
    files = sorted(f for f in files if on_device(f) and os.path.isfile(os.path.join(ROOT, f)))
    deleted = [f for f in deleted if on_device(f)]

    if not files:
        print("nothing to copy")
    for f in files:
        print("copy", f, flush=True)
    for f in deleted:
        print("deleted locally, still on pico:", f, flush=True)
    if dry or not files:
        return

    # mpremote mkdir fails if the dir exists, so make them all in one go and ignore that
    dirs = set()
    for f in files:
        parts = f.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            dirs.add("/".join(parts[:i]))
    if dirs:
        code = "import os\nfor d in %r:\n    try:\n        os.mkdir(d)\n    except OSError:\n        pass\n" % sorted(dirs, key=lambda d: d.count("/"))
        if mpremote(["exec", code]) != 0:
            sys.exit("failed to make dirs, is the pico plugged in?")

    for i in range(0, len(files), CHUNK):
        args = []
        for f in files[i : i + CHUNK]:
            args += ["cp", f, ":" + f, "+"]
        if mpremote(args[:-1]) != 0:
            sys.exit("copy failed")
    print("copied", len(files), "files")


main()
