<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/logo-dark-1200.png">
    <img src="assets/brand/logo-1200.png" alt="music-skill" width="440">
  </picture>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <strong>한국어</strong>
</p>

<p align="center">
  <a href="https://github.com/owoevan-dev/music-skill/actions/workflows/tests.yml"><img src="https://github.com/owoevan-dev/music-skill/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f1c1a" alt="Licence: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-1f1c1a" alt="Python 3.10 or newer">
</p>

<p align="center"><strong>생성하지 말고, 작곡하세요.</strong></p>

music-skill은 작곡가와 작은 스튜디오가 일하는 방식으로 오리지널 기악곡을 만드는 [Agent Skill](https://agentskills.io)입니다. 음 하나하나를 모두 에이전트가 직접 씁니다. 스킬은 그 악보를 검토하고, 샘플링 악기로 연주하고, 믹싱과 마스터링까지 마칩니다.

오디오 생성 모델은 전혀 쓰지 않습니다. MP3와 WAV뿐 아니라 MIDI, 파트별 스템, 그리고 어떤 음이든 고쳐서 다시 렌더링할 수 있는 프로젝트 파일까지 받게 됩니다.

<p align="center">
  <img src="docs/images/daybreak-signal.png" alt="《Daybreak Signal》의 모든 음을 파트별로 나열한 그림. 빨간색이 멜로디이고 그 아래로 오케스트라, 기타, 베이스, 드럼, 위에는 구간 이름">
</p>

## 들어 보기

《Daybreak Signal》은 애니메이션 오프닝 풍의 연주곡입니다. TV 사이즈로 87초, 176 BPM이며, 후렴에 들어갈 때 단3도 위로 전조합니다. Claude(Opus 5.5)가 이 스킬로 작곡·편곡·믹싱을 하고, 그 뒤에 다듬었습니다. 끊기는 곳을 줄이고, 멜로디를 레가토로 잇고, 피아노가 멜로디를 맡는 버전도 따로 만들었습니다.

- [피아노 버전](examples/daybreak-signal/piano.mp3)
- [일렉트릭 기타 버전](examples/daybreak-signal/guitar.mp3)

두 버전은 멜로디를 연주하는 악기만 다릅니다. [examples/daybreak-signal](examples/daybreak-signal)에 이 곡을 쓴 스크립트와 두 프로젝트 파일이 있습니다. Windows에서 고정된 버전의 도구로 다시 렌더링하면, 24비트 반올림 오차 범위 안에서 같은 마스터가 나옵니다.

## 그냥 생성하면 안 되나요?

텍스트로 음악을 만드는 모델이 건네주는 것은 완성된 오디오입니다. 한 마디만 어긋나도 다시 생성하면 다른 곡이 나옵니다. 파일을 열어 음 하나를 옮길 수도 없고, 그 소리가 어디서 왔는지도 설명할 수 없습니다.

여기서는 에이전트가 악보를 쓰기 때문에, 음악은 읽고 고칠 수 있는 결정들로 이루어집니다. 33마디의 멜로디, 화음의 보이싱, 드러머가 크래시를 치는 세기 같은 것들입니다. 음 하나를 바꾸면 그 파트만 다시 렌더링됩니다. 소리는 실제 악기를 멀티샘플링한 녹음이고, 라이선스는 모두 확인할 수 있습니다. 다른 사람의 녹음으로 학습한 모델도 쓰지 않습니다.

## 작동 방식

1. **쓰기**: 에이전트가 곡의 구성과 주제를 정한 뒤 프로젝트 파일을 씁니다. 각 음의 음높이와 길이는 악보에, 연주 방식(벨로시티, 타이밍, 떼는 시점)은 따로 기록합니다. 긴 곡은 보통 에이전트가 짧은 Python 스크립트를 써서 만들기 때문에, 보이싱과 베이스 라인, 드럼 패턴을 읽기도 고치기도 쉽습니다.
2. **악보 검토**: `review`는 파트끼리 계속 울리는 단2도·단9도와, 적힌 코드에서 벗어난 멜로디 음을 목록으로 보여 줍니다. 그래서 하나하나가 우연이 아니라 의도한 선택이 됩니다.
3. **연주**: 연주 모델이 사람이 연주할 때 생기는 어긋남을 더합니다. 연주자마다 타이밍과 음량이 천천히 흔들리고, 베이스는 살짝 뒤에 붙고, 프레이즈에는 둥근 억양이 생기며, 화음의 음들은 동시에 눌리지도 동시에 떼어지지도 않습니다. 샘플링한 멜로디는 레가토로 잇거나 벤딩할 수 있습니다.
4. **렌더링**: FluidSynth가 라이선스가 분명한 SoundFont 음원으로 파트마다 각자의 악기를 연주합니다.
5. **믹싱과 마스터링**: 각 파트는 드럼, 베이스, 리듬, 앙상블, 멜로디 버스와 자동으로 만든 네 가지 리버브를 거쳐, 마스터 처리로 −14 LUFS, 트루 피크 −1 dBTP 이하로 마무리됩니다. 관현악과 오르간 음악은 컴프레서를 거치지 않고 셈여림의 폭을 그대로 살릴 수 있습니다.
6. **측정**: `analyze`는 구간마다 음량, 스펙트럼, 스테레오 이미지, 그리고 멜로디가 반주보다 얼마나 앞에 있는지를 잽니다. 숫자는 문제가 있는 곳을 가리킬 뿐, 듣는 일을 대신하지는 못합니다.

음 하나를 바꾸면 그 파트만 다시 렌더링합니다. 믹스만 바꾸면 다시 렌더링할 것이 없습니다.

게임용 프로젝트는 루프로 만들 수 있습니다. 렌더링할 때 잔향 꼬리를 루프 시작 부분에 겹쳐 넣고, Godot와 RPG Maker가 읽는 형식으로 루프 지점을 WAV와 Ogg 파일에 기록하고, 섹션마다 큐 포인트를 붙입니다. 루프를 여러 레이어로 나눌 수도 있으며, 모든 레이어를 더하면 원래 믹스가 되므로 게임의 긴장감에 따라 소리를 겹쳐 쌓을 수 있습니다.

## 설치

**Claude Code**

```
/plugin marketplace add owoevan-dev/music-skill
/plugin install music-skill@music-skill
```

**Codex와 그 밖의 에이전트**

```
npx skills add owoevan-dev/music-skill
```

`skills/music-production` 폴더를 에이전트의 스킬 폴더에 복사해도 됩니다.

**렌더링 도구**(컴퓨터마다 한 번만, 에이전트에게 맡겨도 됩니다)

Windows x64에서는 고정된 버전의 FluidSynth와 FFmpeg 포터블 빌드를 내려받습니다.

```
python skills/music-production/scripts/bootstrap.py --runtime <folder>/.runtime --config <folder>/local-config.json
```

Linux(Ubuntu 24.04, Debian 13 이상)와 macOS에서는 시스템 패키지를 씁니다.

```
sudo apt install fluidsynth ffmpeg libarchive-tools        # macOS: brew install fluid-synth ffmpeg
python3 skills/music-production/scripts/bootstrap.py --system --runtime <folder>/.runtime --config <folder>/local-config.json
```

이어서 데모에 쓴 악기를 받습니다(약 1 GB).

```
python skills/music-production/scripts/fetch_soundbanks.py --config <folder>/local-config.json --runtime <folder>/.runtime --output <folder>/local-config.studio.json
```

필요한 것은 Python 3.10 이상과 NumPy뿐입니다. GPU도, 계정도, 오디오 모델도 필요 없습니다. 모든 파일은 배포처의 공식 페이지에서 내려받고, 고정된 SHA-256으로 확인합니다.

## 사용법

에이전트에게 평소 말투로 부탁하면 됩니다.

> 퍼즐 게임 타이틀 화면에 쓸 90초짜리 연주곡을 써 줘. 따뜻하고 조금 아련하게, 피아노와 스트링으로.

> TV 사이즈의 애니메이션 오프닝 풍 곡을 만들어 줘. 기타 밴드에 피아노 멜로디로.

> 비주얼 노벨의 슬픈 장면에 깔 루프 곡을 써 줘. 부드러운 피아노와 첼로로, 글을 읽는 데 방해되지 않게 조용하게.

> 풀 오케스트라로 2분짜리 곡을 써 줘. 해돋이 장면으로, 조용한 호른 솔로에서 오케스트라 전체로.

> 33마디 후렴 멜로디가 너무 바빠. 단순하게 바꿔서 다시 렌더링해 줘.

> MIDI랑 스템도 줘.

## 음원

| 악기 | 음원 | 라이선스 |
|---|---|---|
| 그랜드 피아노 | VCSL의 Steinway B(Versilian Studios); Osiris Piano(Karoryfer Samples, 서스테인 페달을 밟은 녹음과 밟지 않은 녹음); 둘 다 여기서 구성 | CC0 |
| 일렉트릭 기타 | FreePats FSBS: 디스토션 2종, 클린 1종 | CC0 |
| 일렉트릭 베이스 | Bass YR, 피크와 핑거(샘플 녹음: Andrea Biasior); Black And Blue Basses(Karoryfer Samples)의 5현 베이스(고스트 노트 포함), 여기서 구성 | CC0 |
| 드럼 키트 | Big Rusty Drums(Karoryfer Samples), GM 건반 배치로 구성 | CC0 |
| 스트링(트레몰로, 피치카토 포함), 솔로 바이올린, 더블베이스, 브라스, 트럼펫, 호른, 트롬본, 튜바, 목관, 피콜로, 글로켄슈필 | VSCO 2 Community Edition(Versilian Studios)으로 구성 | CC0 |
| 하프, 마림바, 비브라폰, 실로폰, 튜블러 벨, 팀파니, 관현악 타악기(심벌과 심벌 크레센도, 공, 트라이앵글, 슬레이 벨, 윈드 차임), 파이프 오르간 | VCSL(Versilian Studios)로 구성 | CC0 |
| 솔로 첼로 | Karoryfer x bigcat cello(Karoryfer Lecolds, bigcat instruments), 녹음에 있는 루프 포인트와 함께 여기서 구성 | CC0 |
| 그 밖의 악기 | MuseScore MS Basic | MIT |

녹음 음원은 모두 CC0라서, 이 음원으로 만든 음악에는 출처 표기가 필요 없습니다. MS Basic의 MIT 고지는 음원 파일 자체의 사본에 따르며, 렌더링한 음악에는 해당하지 않습니다. 출처는 [THIRD_PARTY.md](THIRD_PARTY.md)에 있습니다.

## 어디까지 되나요

`selfcheck.py`에는 46가지 검사가 있으며, MIDI 왕복 변환과 압축 파일 안전성부터 실제 렌더링까지 포함합니다. 예를 들어 음 하나를 고치면 그 파트만 다시 렌더링되는지, 예전의 단일 리버브 믹스가 이전 릴리스를 비트 단위로 재현하는지, 라우드니스 측정이 BS.1770 기준 음을 −3.01 LUFS로 읽는지 확인합니다. CI에서는 Ubuntu(FluidSynth 2.3, FFmpeg 6.1)와 macOS(FluidSynth 2.6, FFmpeg 9.0)에서 렌더링을 포함한 모든 검사를 실행합니다.

음악으로서 좋은지는 다른 문제이고, 직접 들어 봐야만 알 수 있습니다. 위의 데모가 이 저장소가 보여 줄 수 있는 가장 좋은 증거입니다.

## 한계

- 노래를 부르거나 가사를 쓰지 못하고, VST 플러그인도 지원하지 않습니다.
- 소리의 수준은 무료 음원에 달려 있습니다. YR 베이스는 벨로시티 레이어가 하나뿐이고, 스트링은 어택이 느린 편이며, 마림바·실로폰·피콜로는 샘플이 듬성듬성합니다. 샘플링한 기타의 벤딩은 샘플 전체의 음정만 바꾸기 때문에 실제 줄처럼 음색이 변하지는 않습니다.
- 에이전트는 소리를 듣지 못합니다. `review`와 `analyze`는 문제가 있는 곳을 찾을 뿐이고, 결과는 사람이 들어야 합니다. 스킬은 듣지 않았으면서 들었다고 말하지 않도록 에이전트에게 요구합니다.
- Linux와 macOS에서는 시스템의 FluidSynth와 FFmpeg를 쓰기 때문에, 고정 버전을 쓰는 Windows와 샘플 단위로 조금 다를 수 있습니다.

## 문서

| | |
|---|---|
| [SKILL.md](skills/music-production/SKILL.md) | 에이전트가 따르는 작업 순서와 모든 명령 |
| [schema.md](skills/music-production/references/schema.md) | 프로젝트 파일: 악보, 연주, 믹스 |
| [arrangement.md](skills/music-production/references/arrangement.md) | 구성, 멜로디, 보이싱, 각 파트의 역할 |
| [performance-and-mix.md](skills/music-production/references/performance-and-mix.md) | 연주, 버스 믹싱, `analyze` 읽는 법 |
| [soundbanks.md](skills/music-production/references/soundbanks.md) | 각 음원의 특징과 버릇, 직접 음원을 추가하는 방법 |
| [setup.md](skills/music-production/references/setup.md) | Windows, Linux, macOS에 렌더링 도구 설치하기 |
| [sources-and-rights.md](skills/music-production/references/sources-and-rights.md) | 외부 악보, MIDI, 샘플을 쓸 때 주의할 점 |

문서 본문은 영어로 쓰여 있습니다.

## 기여

버그 보고, 들어 본 소감, 음원 제안은 [Issues](https://github.com/owoevan-dev/music-skill/issues)에서 환영합니다. 외부의 풀 리퀘스트는 지금은 받지 않습니다. 이유와 대신할 방법은 [CONTRIBUTING.md](CONTRIBUTING.md)에 있습니다.

## 라이선스

코드와 문서는 [MIT](LICENSE)입니다. 데모 녹음과 곡 자체는 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)으로 퍼블릭 도메인에 공개합니다. 서드파티 도구와 음원은 각자의 라이선스를 따르며, 이 저장소에 포함하지 않고 배포처에서 내려받습니다. 곡 그림은 피아노 버전의 프로젝트 파일에서 코드로 그린 것이고, 로고의 글자는 Noto Serif TC(SIL Open Font License)를 아웃라인으로 바꾼 것입니다.
