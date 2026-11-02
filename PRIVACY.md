# Privacy

music-skill is a skill: instructions and Python scripts that your agent runs. It has no server, no account and no telemetry.

- **What it reads**: only the project, MIDI, audio and configuration files you point it at.
- **What it writes**: renders, reviews, analyses and configurations, in the folders you choose. Nothing is written anywhere else.
- **What it sends**: nothing. The only network access is the one-time setup, which downloads FluidSynth, FFmpeg and the sound banks from their publishers (GitHub and FreePats); those requests carry none of your data. Python packages come from PyPI if your agent installs them.
- **What it keeps**: nothing. There is no music-skill service to keep anything.

Where the scripts run depends on your agent: on your computer in Claude Code or Codex, or in the agent's own sandbox in a chat. What you send to the agent is covered by that agent's privacy policy.

Questions: open an issue at https://github.com/owoevan-dev/music-skill/issues.
