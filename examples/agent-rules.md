# The rules every agent followed

Each piece in these examples was made by one agent session from one short prompt in Chinese. The prompt named a subject
and a folder, and told the agent to read these rules first. They are translated here from the Chinese, without the
paths of the machine they ran on.

## Skill and environment

- Use only the frozen copy of the music-production skill, version 0.3.0. Do not use any other copy of the skill or
  any other configuration.
- Render, review and audition with the given configuration, in which the sound banks, Surge XT and all 3,008 of its
  patches are set up. Do not download or install anything.
- Other agents may be rendering on the same computer; slowness is normal.

## Scope

- Create and change files only in the piece's own folder. Do not change the skill, the configuration, these rules or
  any other folder.
- Do not use subagents, do not commit, and do not upload or publish anything.

## Music

- Entirely original: do not quote or imitate the melody, chord progression or title of an existing work, nor a
  particular song by a particular singer, band or composer.
- Make it completely, following the steps of `SKILL.md`: write `song.json` with one Python script that writes every
  note. Start synth parts from Surge XT patches, as the skill says, finding them with `studio.py sounds` and comparing
  them on the part with `studio.py audition`.
- Then review (with `--config`), render and analyze (with `--reference` where the style has a reference).
- Revise from what the review and the measurements point out, at least one more round, each render in a new folder.
  Every review question gets a musical decision: a change, or a written reason for keeping it.
- You cannot hear the music. Do not say it sounds good or is professional; measurements are only measurements.

## Delivery

- Leave the script, `song.json`, the final render folder and `NOTES.md` in English in the piece's folder.
- `NOTES.md` gives the title, style, length, tempo and key, the instruments, sound banks and Surge patches, the
  sections, what changed in each round and why, how each review question was handled, the final measurements and any
  warning left by review or analyze.
- Then send the final `preview.mp3` with a few sentences: where to listen closely and what you are unsure of.
