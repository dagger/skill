# Dagger skill

The official agent skill for Dagger.

Install the module. If the project has no `dagger.toml`, the install creates
one:

```sh
dagger module install dagger.io/skill
dagger generate
```

The module installs the skill into each of `.agents/skills`, `.claude/skills`,
`.cursor/skills`, `.gemini/skills`, `.github/skills`, and `.opencode/skills`
that exists at the workspace root. If none exists, it uses the agent
instructions at the root: `AGENTS.md` creates `.agents/skills`, and `CLAUDE.md`
creates `.claude/skills`. With both files, it creates both directories. It skips
symbolic links to agent directories. If it finds no skill directory and no
instructions, generation fails with an error.

Agents find this module through `dagger module recommend` and
`dagger generate -l`, not this README. The module and generator descriptions
tell an agent to create its own skills directory before generating, and to read
the installed `SKILL.md` afterwards, because an agent may not load a skills
directory created during its session.

Generation returns a changeset for review. An ownership marker identifies
installed skills. Existing skills without that marker cause an error.
Updates replace managed files; review the changeset to keep local edits.

The generator selects the latest stable Git release. `dagger.lock` records
the selected release and commit. Commit that file with the generated skill.
To select a newer release, run:

```sh
dagger lock update
dagger generate
```

Skill content lives in `content`. Publish stable semantic version tags
such as `v0.1.0` to release updates. Module and skill content can update separately:
the installed module stays pinned while its content lookup follows the lockfile.

Run the module checks with `dagger check`. Run `python3 tests/lock-update.py`
to test pinned generation, conflict handling, and release updates. The update
command is tested against a public repository. The generation test uses a
local Git service with two releases and checks both release pins.
