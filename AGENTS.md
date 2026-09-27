# AGENTS.md

Copr packaging repo for SatDump release tags. The only artifact is `satdump.spec`.

## Release workflow

- Copr auto-builds on push to `master`.
- Track current `SatDump/SatDump` master. The 1.2.2 tag is stale. Pin `%global commit` to the commit being packaged.
- To release: bump `Version:`, reset `Release:` to `1%{?dist}`, prepend a `%changelog` entry, commit, push.
- Entry format:

  ```
  * Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 1.2.2-1
  - Update to 1.2.2
  ```

## Spec constraints

- `Source0` is the GitHub tag archive. `%autosetup -n SatDump-%{version}`.
- GUI and OpenMP stay on. Disable plugins whose `-devel` is not in Fedora (Aaronia, SDRPlay, MiriSDR, RFNM) instead of adding extra Coprs.
- Do not pre-patch GCC 15 / vendored sol2 issues. Add a patch only after a Copr build of this tarball fails.
- Commit style: `Update to <version>` or `fix spec: <description>`.

## Verification

No local test suite. `rpmlint satdump.spec` if available. The real build is Copr.
