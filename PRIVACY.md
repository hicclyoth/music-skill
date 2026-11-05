# Privacy

music-skill is a skill: instructions and Python scripts that your agent runs. It has no server, no account and no telemetry.

- **What it reads**: only the project, MIDI, audio and configuration files you point it at.
- **What it writes**: renders, reviews, analyses, configurations and the downloaded tools and banks, in the folders you choose (pip runs without its own cache). Python also keeps its bytecode cache next to the scripts. Nothing is written anywhere else.
- **What it sends**: nothing. The only network access is the one-time setup, which downloads FluidSynth, FFmpeg and Surge XT from their publishers, the sound banks from this project's GitHub release (from their publishers if it cannot be reached), and pedalboard through pip. The tools and banks come from GitHub, plus the University of Iowa's sample site when its banks are built from source; pip takes Python packages from PyPI unless you have set it to use another package index, and the pedalboard wheel is checked against its pinned SHA-256. Those requests carry none of your data. NumPy comes through pip when you or your agent install it.
- **What it keeps**: nothing. There is no music-skill service to keep anything.

Where the scripts run depends on your agent: on your computer in Claude Code or Codex, or in the agent's own sandbox in a chat. What you send to the agent is covered by that agent's privacy policy.

Questions: open an issue at https://github.com/owoevan-dev/music-skill/issues.
