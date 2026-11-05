# Dagger skills

Official agent skills for Dagger.

Install the module in a project with an existing skill directory:

```sh
dagger module install github.com/dagger/skills/dagger
dagger generate
```

The module detects `.agents/skills`, `.claude/skills`, `.cursor/skills`,
`.gemini/skills`, `.github/skills`, and `.opencode/skills` at the workspace root.
It skips symbolic links. It does not create agent settings directories.

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

Skill content lives in `dagger/content`. Publish stable semantic version tags
such as `v0.1.0` to release updates. Module and skill content can update separately:
the installed module stays pinned while its content lookup follows the lockfile.
