# Agent instructions

- `content/` is the skill that users install. `main.dang` is the module that
  installs it. Keep skill text short, plain, and true for any project.
- Run the module checks with `dagger check`. Run `python3 tests/lock-update.py`
  after changing generation or release pinning.
- `.agents/skills/dagger` is generated from the latest release, not from
  `content/`. Update it with `dagger generate -y`. Do not edit it by hand.
