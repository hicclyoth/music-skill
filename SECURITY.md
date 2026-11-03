# Security

music-skill runs on your own machine. Its scripts read the project, MIDI and audio files they are given and write their results to the folders they are given. Renders, reviews, analyses, revisions and configurations go to new paths and never overwrite earlier ones.

- **Downloads** happen only during setup, over HTTPS, from a fixed list of hosts: GitHub (releases, raw files, and the API for a source build's file list), the University of Iowa's sample site (only when its banks are built from source) and, for pedalboard, PyPI through pip. Every redirect is checked against that list before it is followed. Every file must match the size and SHA-256 (or git hash) pinned in the skill's lock files, or it is downloaded again and never kept; archives are listed before extraction, and members with absolute paths, `..` or links are refused.
- **External programs** are FluidSynth, FFmpeg, pip (for the pinned pedalboard wheel), tar or 7-Zip (to unpack a FreePats .7z, only when the release cannot be reached) and the skill's own Surge XT host (`scripts/surge_host.py`, which loads pedalboard and the Surge XT plugin), all started without a shell. FFmpeg receives only local WAV files and filter settings built from numbers; filter text is never taken from a project.
- **Input files** are data. MIDI is read with size and event limits and never executed; project files are validated against fixed ranges.

## Reporting a vulnerability

If you find a way to make a script do something it should not, such as writing outside the paths it was given, fetching from another host or running code from an input file, please report it privately: on this repository, open **Security**, then **Report a vulnerability** (or go straight to https://github.com/owoevan-dev/music-skill/security/advisories/new). Please don't open a public issue for it.

A fix goes into the next release, and the changelog says what was fixed.

Ordinary bugs are welcome as [issues](https://github.com/owoevan-dev/music-skill/issues).
