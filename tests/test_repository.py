"""Repository tests: packaging, links, privacy, the demo and the skill's own selfcheck.

Run from the repository root: python -m pytest -q tests
Set MUSIC_SKILL_CONFIG to a renderer configuration written by bootstrap.py to include the render checks."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'music-production'
SCRIPTS = SKILL / 'scripts'
EXAMPLE = ROOT / 'examples' / 'daybreak-signal'
OVERTURE = ROOT / 'examples' / 'above-the-clouds'
GENRES = ROOT / 'examples' / 'genre-demos'
GENRE_DEMOS = ('signal_fire', 'late_set', 'midnight_coastline', 'tram_line_rain', 'paper_satellites', 'pixel_lantern')
CONFIG = os.environ.get('MUSIC_SKILL_CONFIG')
DEMOS = {'piano': ['1.1.r3p4', '--arr', 'r3', '--lead', 'piano', '--mix', 'bus']}


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def frontmatter():
    yaml = pytest.importorskip('yaml')
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    assert m, 'SKILL.md starts with a YAML frontmatter'
    # a strict parser, as the agents' skill loaders use: an unquoted value holding ": " does not load
    return text, yaml.safe_load(m.group(1))


def test_skill_frontmatter():
    text, front = frontmatter()
    assert front['name'] == SKILL.name and re.fullmatch(r'[a-z0-9-]{1,64}', front['name'])
    assert 0 < len(front['description']) <= 1024
    assert '<' not in front['description'] and '>' not in front['description']
    assert len(front.get('compatibility', '')) <= 500
    assert all(isinstance(v, str) for v in front['metadata'].values())
    assert len(text.splitlines()) < 500


def test_plugin_manifests_agree():
    _, front = frontmatter()
    claude, codex = load(ROOT / '.claude-plugin' / 'plugin.json'), load(ROOT / '.codex-plugin' / 'plugin.json')
    assert front['metadata']['version'] == claude['version'] == codex['version']
    for path in claude['skills']:
        assert (ROOT / path / 'SKILL.md').is_file()
    for key in ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords'):
        assert codex[key] == claude[key], key
    ui = codex['interface']
    assert len(ui['displayName']) <= 30 and len(ui['shortDescription']) <= 30 and len(ui['longDescription']) <= 4000
    assert len(ui['defaultPrompt']) <= 3 and all(len(p) <= 128 for p in ui['defaultPrompt'])
    assert re.fullmatch(r'#[0-9A-Fa-f]{6}', ui['brandColor'])
    markets = load(ROOT / '.claude-plugin' / 'marketplace.json'), load(ROOT / '.agents' / 'plugins' / 'marketplace.json')
    assert all(m['name'] == claude['name'] and [p['name'] for p in m['plugins']] == [claude['name']] for m in markets)


def image_size(path):
    """(width, height) of a PNG from its header, or of an SVG from its viewBox."""
    if path.suffix == '.svg':
        w, h = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', path.read_text(encoding='utf-8')).groups()
        return float(w), float(h)
    data = path.read_bytes()[:24]
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    return int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')


def test_listing_icons():
    """Every icon a listing names exists, is square and at least 48 px; Claude's directory wants 512 to 2048 px."""
    claude, codex = load(ROOT / '.claude-plugin' / 'plugin.json'), load(ROOT / '.codex-plugin' / 'plugin.json')
    for rel in (claude['icon'], codex['interface']['composerIcon'], codex['interface']['logo']):
        w, h = image_size(ROOT / rel)
        assert w == h >= 48, (rel, w, h)
    w, _ = image_size(ROOT / claude['icon'])
    assert 512 <= w <= 2048 and (ROOT / claude['icon']).stat().st_size < 2_000_000
    assert all((ROOT / rel).is_file() for rel in codex['interface'].get('screenshots', []))


def test_skill_carries_its_codex_icons():
    """The skill's own Codex metadata travels with the folder: its icons are inside it, the brand's own."""
    yaml = pytest.importorskip('yaml')
    ui = yaml.safe_load((SKILL / 'agents' / 'openai.yaml').read_text(encoding='utf-8'))['interface']
    for key, brand in (('icon_small', 'icon-small.svg'), ('icon_large', 'icon-512.png')):
        assert (SKILL / ui[key]).read_bytes() == (ROOT / 'assets' / 'brand' / brand).read_bytes(), key


def test_skill_folder_carries_the_licence():
    """The skill is often copied on its own, without the repository round it: its folder keeps the licence."""
    assert (SKILL / 'LICENSE').read_text(encoding='utf-8') == (ROOT / 'LICENSE').read_text(encoding='utf-8')


def test_markdown_links_resolve():
    """Markdown links and the HTML images and links in the READMEs' headers point at files that exist."""
    bad = []
    for md in [*ROOT.glob('*.md'), *(ROOT / 'examples').rglob('*.md'), *SKILL.rglob('*.md')]:
        text = md.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)#\s]+)', text) + re.findall(r'(?:src|srcset|href)="([^"#]+)"', text):
            if not re.match(r'[a-z]+:', target) and not (md.parent / target).exists():
                bad.append(f'{md.relative_to(ROOT)} -> {target}')
    assert not bad, bad


def test_readmes_offer_every_language():
    """Each README links to every other one, so a reader can switch from any of them."""
    readmes = sorted(p.name for p in ROOT.glob('README*.md'))
    assert len(readmes) == 5, readmes
    for name in readmes:
        text = (ROOT / name).read_text(encoding='utf-8')
        assert all(other in text for other in readmes if other != name), name


# FreePats credits its SF2 assembly with this address; the selfcheck tests that an absolute archive member is refused.
ALLOWED = ("'C:/x.sf2'",)
PERSONAL = [re.compile(p) for p in (
    r'(?<![A-Za-z])[A-Za-z]:[\\/](?!/)', r'[\\/]Users[\\/]', r'[\\/]home[\\/]\w', r'\bsk-[A-Za-z0-9_-]{16,}',
    r'[\w.+-]+@[\w-]+\.[\w.]+', r'(?i)api[_-]?key\s*[:=]\s*[\'"]?\w{12,}')]


def repository_files():
    """The repository's own files: git's list in a checkout (a local .venv or render is not part of it), every file in
    an unpacked archive."""
    try:
        listed = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8')
        return [ROOT / f for f in listed.split('\0') if f]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob('*') if p.is_file()]


def test_no_personal_data():
    """Nothing of the people who made it: no paths on their machines, no keys, no addresses."""
    hits = []
    for p in repository_files():
        if not p.is_file() or {'.git', '__pycache__', '.pytest_cache'} & set(p.parts) or p.resolve() == Path(__file__).resolve():
            continue
        if p.suffix == '.mp3':
            data = p.read_bytes()
            size = (data[6] << 21 | data[7] << 14 | data[8] << 7 | data[9]) if data[:3] == b'ID3' else 0
            if re.search(rb'[A-Za-z]:\\|/Users/|/home/|@', data[10:10 + size]):  # the ID3 tags, not the audio
                hits.append(f'{p.relative_to(ROOT)}: a path or address in the tags')
            continue
        if p.suffix not in ('.py', '.md', '.json', '.txt', '.yaml', '.yml', '.toml', '.cfg', '.svg', ''):
            continue
        for i, line in enumerate(p.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
            for allowed in ALLOWED:
                line = line.replace(allowed, '')
            if any(b.search(line) for b in PERSONAL):
                hits.append(f'{p.relative_to(ROOT)}:{i}: {line.strip()[:100]}')
    assert not hits, '\n'.join(hits)


def test_demo_projects_and_recordings():
    sys.path.insert(0, str(SCRIPTS))
    from musiclib.model import validate
    for name in DEMOS:
        p = load(EXAMPLE / f'{name}.json')
        assert p['mix']['chain'] == 'bus' and 85 < validate(p)['seconds'] < 95
        audio = (EXAMPLE / f'{name}.mp3').read_bytes()
        assert len(audio) > 1_000_000 and (audio[:3] == b'ID3' or audio[0] == 0xFF)


@pytest.mark.parametrize('name', DEMOS)
def test_demo_script_writes_the_published_project(tmp_path, name):
    out = tmp_path / f'{name}.json'
    r = subprocess.run([sys.executable, str(EXAMPLE / 'daybreak_signal.py'), str(out), *DEMOS[name]],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    assert r.returncode == 0, r.stderr[-2000:]
    assert load(out) == load(EXAMPLE / f'{name}.json')


def test_example_projects_and_recordings():
    sys.path.insert(0, str(SCRIPTS))
    from musiclib.model import validate
    for folder, name in [(OVERTURE, 'above_the_clouds')] + [(GENRES, n) for n in GENRE_DEMOS]:
        assert validate(load(folder / f'{name}.json'))['seconds'] > 30, name
        audio = (folder / f'{name}.mp3').read_bytes()
        assert len(audio) > 500_000 and (audio[:3] == b'ID3' or audio[0] == 0xFF), name


def test_overture_script_writes_the_published_project(tmp_path):
    out = tmp_path / 'above_the_clouds.json'
    r = subprocess.run([sys.executable, str(OVERTURE / 'above_the_clouds.py'), str(out), '1.0.r7', '--engine-r7'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    assert r.returncode == 0, r.stderr[-2000:]
    assert load(out) == load(OVERTURE / 'above_the_clouds.json')


@pytest.mark.parametrize('name', GENRE_DEMOS)
def test_genre_demo_script_writes_the_published_project(tmp_path, name):
    r = subprocess.run([sys.executable, str(GENRES / f'{name}.py'), str(tmp_path / name)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    assert r.returncode == 0, r.stderr[-2000:]
    assert load(tmp_path / name / 'song.json') == load(GENRES / f'{name}.json')


def test_selfcheck(tmp_path):
    work = tmp_path / 'selfcheck'
    cmd = [sys.executable, str(SCRIPTS / 'selfcheck.py'), '--work', str(work)] + (['--config', CONFIG] if CONFIG else [])
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-3000:]
    report = load(work / 'selfcheck_report.json')
    assert report['status'] == 'PASS' and all(c['passed'] for c in report['checks'])
    assert len(report['checks']) == (86 if CONFIG else 70), [c['name'] for c in report['checks']]
