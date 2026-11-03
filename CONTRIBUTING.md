# Contributing

Thanks for wanting to help. music-skill is maintained by one person and has a fairly fixed direction, so here is how help works best.

## Issues are welcome

- **A render that went wrong.** Paste the command, the error or the `report.json` checks, and say what you expected. Attach the project file if you can share it.
- **Music that sounds wrong.** Say where (bar numbers or seconds) and what you hear: a clash, a part too loud, a stiff phrase. Listening notes like these are the most useful feedback the project gets.
- **A sound bank you would like.** Link the publisher's page and its licence. Only banks with a clear licence that allows redistribution of music made with them can be added.

Write in any language you like.

## Pull requests

Pull requests from outside the project are closed for now. If you have a fix, describe it in an issue or paste the patch there. When an idea or a patch from an issue is used, the changelog says whose it was. By posting a patch you agree that it may be used under the project's MIT licence.

## What the project will not take

- An audio-generation model inside the skill. The notes are written, not generated.
- Sound banks under NC, ND or unclear licences, or samples taken from commercial libraries.
- Reference melodies, grooves or recordings copied from existing music.

## Running the tests

```bash
python3 -m venv .venv && . .venv/bin/activate        # Windows: py -m venv .venv, then .venv\Scripts\activate
python -m pip install -r skills/music-production/requirements.txt pyyaml pytest
python -m pytest -q tests
```

Without a renderer configuration the render checks are skipped. To include them, run the bootstrap from the README and set `MUSIC_SKILL_CONFIG` to the configuration file.
