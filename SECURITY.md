# Security

music-skill runs on your own machine. Its scripts read the project, MIDI and audio files they are given and write their results to the folders they are given. Renders, revisions and configurations go to new paths and never overwrite earlier ones; review and analysis reports are rewritten in place.

- **Downloads** happen only during setup, from a fixed list of hosts (GitHub release and raw hosts, FreePats). Every file must match the size and SHA-256 pinned in the skill's lock files, archives are listed before extraction, and members with absolute paths, `..` or links are refused.
- **External programs** are FluidSynth, FFmpeg and, to unpack the .7z banks, tar, all started without a shell. FFmpeg receives only local WAV files and filter settings built from numbers; filter text is never taken from a project.
- **Input files** are data. MIDI is read with size and event limits and never executed; project files are validated against fixed ranges.

## Reporting a vulnerability

If you find a way to make a script do something it should not, such as writing outside the paths it was given, fetching from another host or running code from an input file, please report it privately: on this repository, open **Security**, then **Report a vulnerability**. Please don't open a public issue for it.

A fix goes into the next release, and the changelog says what was fixed.

Ordinary bugs are welcome as [issues](https://github.com/owoevan-dev/music-skill/issues).
