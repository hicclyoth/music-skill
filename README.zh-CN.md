<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/logo-dark-1200.png">
    <img src="assets/brand/logo-1200.png" alt="music-skill" width="440">
  </picture>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <strong>简体中文</strong> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/owoevan-dev/music-skill/actions/workflows/tests.yml"><img src="https://github.com/owoevan-dev/music-skill/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f1c1a" alt="Licence: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-1f1c1a" alt="Python 3.10 or newer">
</p>

<p align="center"><strong>不是生成，是作曲。</strong></p>

music-skill 是一个 [Agent Skill](https://agentskills.io)，让 AI agent 像作曲家加上一间小录音棚那样，写出原创的器乐曲。每一个音都由 agent 写下，skill 负责检查乐谱、用采样乐器演奏、混音和母带处理。

整个过程没有用到任何音频生成模型。除了 MP3 和 WAV，你还会得到 MIDI、每个声部各自的音轨，以及一份项目文件：其中任何一个音都能修改，改完再重新渲染。

<p align="center">
  <img src="docs/images/daybreak-signal.png" alt="《Daybreak Signal》的每一个音按声部排列：红色是主旋律，下方依次是管弦、吉他、贝斯和鼓，上方标出段落">
</p>

## 试听

《Daybreak Signal》是一首动漫片头风格的器乐曲，TV 尺寸：87 秒、176 BPM，进副歌时上移小三度转调。由 Claude（Opus 5.5）用这个 skill 作曲、编曲和混音，之后又做了修改：减少停顿、让主旋律连贯，并另外做了一版钢琴主旋律。

- [钢琴主旋律](examples/daybreak-signal/piano.mp3)
- [电吉他主旋律](examples/daybreak-signal/guitar.mp3)

两个版本只在主旋律的乐器上不同。[examples/daybreak-signal](examples/daybreak-signal) 里有写出这首曲子的脚本，以及两份项目文件。在 Windows 上用锁定版本的工具重新渲染，会得到相同的母带，差异仅在 24 位的舍入误差。

## 为什么不直接生成？

文字生成音乐的模型交给你的是一段做好的音频。只要有一小节不对，就得重新生成，换来的是另一首歌。你没法打开它挪动一个音，也说不清里面的声音从哪里来。

这里由 agent 写出乐谱，所以音乐是由一个个你看得懂、改得动的决定组成的：第 33 小节的旋律、一个和弦的配置、鼓手敲镲片的力度。只改一个音，就只会重新渲染那个声部。声音来自真实乐器的多重采样录音，许可都查得到，也没有用到任何以他人录音训练的模型。

## 工作原理

1. **写谱**：agent 先规划曲式和主题，再写出项目文件。每个音的音高和时值记在乐谱里；怎么演奏（力度、时间点、松开的时机）另外记录。较长的曲子通常由 agent 写一个简短的 Python 脚本来生成，让和声配置、贝斯线和鼓的乐句都清晰、好改。
2. **检查乐谱**：`review` 会列出声部之间持续的小二度和小九度，以及落在和弦外的旋律音，让每一处都是有意的选择，而不是意外。
3. **演奏**：演奏模型加入真人演奏会有的偏差：每位乐手在时间和音量上缓慢的起伏、略微靠后的贝斯、乐句的起伏弧线，以及和弦中各音不会同时按下、也不会同时松开。采样的主旋律可以连奏，也可以推弦。
4. **渲染**：FluidSynth 用有许可的 SoundFont 音色库，让每个声部用各自的乐器演奏。
5. **混音与母带**：各声部经过鼓、贝斯、节奏、合奏和主旋律总线，以及四种自动生成的混响，最后由母带处理做到 −14 LUFS，真峰值不超过 −1 dBTP。管弦乐和管风琴可以跳过压缩器，保留完整的强弱对比。
6. **测量**：`analyze` 会测出每个段落的响度、频谱和立体声，以及主旋律比伴奏响多少。这些数字能指出问题所在，但不能代替实际聆听。

只改一个音，就只会重新渲染那一个声部；只改混音，则完全不需要重新渲染。

游戏用的项目可以设置循环：渲染时会把混响尾巴折回循环开头，并按 Godot 和 RPG Maker 读取的格式，把循环点写进 WAV 和 Ogg 文件，每个段落也标上提示点。循环还能拆成几层，各层相加就是完整混音，让音乐随着游戏紧张程度逐层加厚。

## 安装

**Claude Code**

```
/plugin marketplace add owoevan-dev/music-skill
/plugin install music-skill@music-skill
```

**Codex 与其他 agent**

```
npx skills add owoevan-dev/music-skill
```

也可以直接把 `skills/music-production` 复制到 agent 的 skills 文件夹。

**渲染工具**：每台电脑设置一次，可以交给 agent 代劳。

Windows x64 会下载锁定版本的 FluidSynth 和 FFmpeg 便携版：

```
python skills/music-production/scripts/bootstrap.py --runtime <folder>/.runtime --config <folder>/local-config.json
```

Linux（Ubuntu 24.04、Debian 13 或更新版本）和 macOS 使用系统软件包：

```
sudo apt install fluidsynth ffmpeg libarchive-tools        # macOS：brew install fluid-synth ffmpeg
python3 skills/music-production/scripts/bootstrap.py --system --runtime <folder>/.runtime --config <folder>/local-config.json
```

然后下载示范曲用到的乐器，约 1 GB：

```
python skills/music-production/scripts/fetch_soundbanks.py --config <folder>/local-config.json --runtime <folder>/.runtime --output <folder>/local-config.studio.json
```

需要 Python 3.10 及以上版本和 NumPy。不需要 GPU、账号或音频模型。所有文件都从发布者自己的页面下载，并用锁定的 SHA-256 校验。

## 使用方法

直接用平常的话告诉 agent：

> 给我的益智游戏标题画面写一首 90 秒的器乐曲，温暖、带点忧伤，用钢琴和弦乐。

> 做一首 TV 尺寸的动漫片头风格曲子，吉他乐队配钢琴主旋律。

> 给我的视觉小说写一段悲伤场景的循环配乐：柔和的钢琴和大提琴，安静到可以边听边读。

> 写两分钟的管弦乐：日出，从安静的圆号独奏到整个乐团。

> 第 33 小节的副歌旋律太满了，简化一下再重新渲染。

> 也把 MIDI 和分轨发给我。

## 音色库

| 乐器 | 音色库 | 许可 |
|---|---|---|
| 三角钢琴 | VCSL 的 Steinway B（Versilian Studios）；Osiris Piano（Karoryfer Samples），分别录了踩与不踩延音踏板的版本；两者都在这里构建 | CC0 |
| 电吉他 | FreePats FSBS：两种失真、一种干净音色 | CC0 |
| 电贝斯 | Bass YR，拨片与指弹，采样由 Andrea Biasior 录制；Black And Blue Basses（Karoryfer Samples）的五弦贝斯，含幽灵音，在这里构建 | CC0 |
| 架子鼓 | Big Rusty Drums（Karoryfer Samples），在这里构建为 GM 键位 | CC0 |
| 弦乐（含震音和拨奏）、独奏小提琴、低音提琴、铜管、小号、圆号、长号、大号、木管、短笛、钟琴 | 由 VSCO 2 Community Edition（Versilian Studios）构建 | CC0 |
| 竖琴、马林巴、颤音琴、木琴、管钟、定音鼓、管弦打击乐（镲与镲的渐强、锣、三角铁、雪橇铃、风铃）、管风琴 | 由 VCSL（Versilian Studios）构建 | CC0 |
| 独奏大提琴 | Karoryfer x bigcat cello（Karoryfer Lecolds 与 bigcat instruments），连同原有的持续音循环点在这里构建 | CC0 |
| 其他乐器 | MuseScore MS Basic | MIT |

录音音色库全部是 CC0，用它们制作的音乐不需要署名。MS Basic 的 MIT 声明只随音色库本身的副本，不涉及用它渲染出来的音乐。来源列在 [THIRD_PARTY.md](THIRD_PARTY.md)。

## 效果如何

`selfcheck.py` 共有 46 项检查，从 MIDI 往返转换、压缩包安全到实际渲染都包含在内。例如：只改一个音时只会重新渲染一个声部；旧的单一混响混音能逐位重现之前的版本；响度测量对 BS.1770 的标准测试音读出 −3.01 LUFS。CI 会跑完所有检查（包括渲染），环境是 Ubuntu（FluidSynth 2.3、FFmpeg 6.1）和 macOS（FluidSynth 2.6、FFmpeg 9.0）。

音乐好不好听是另一回事，只有实际聆听才知道。上面的示范曲是这个仓库最好的证据。

## 局限

- 不会唱歌、不写歌词，也不支持 VST 插件。
- 音色的上限取决于免费音色库：YR 贝斯只有一层力度，弦乐起音偏慢，马林巴、木琴和短笛的采样稀疏，采样吉他的推弦是把整段采样变调，不会有真实琴弦的音色变化。
- agent 听不到声音。`review` 和 `analyze` 只能找出问题，结果必须由人来听；skill 也会要求 agent 不得声称自己听过。
- Linux 和 macOS 使用系统的 FluidSynth 和 FFmpeg，渲染出的采样可能与 Windows 的锁定版本略有差异。

## 文档

| | |
|---|---|
| [SKILL.md](skills/music-production/SKILL.md) | agent 遵循的工作流程，以及所有命令 |
| [schema.md](skills/music-production/references/schema.md) | 项目文件：乐谱、演奏与混音 |
| [arrangement.md](skills/music-production/references/arrangement.md) | 曲式、旋律、和声配置与各声部的职责 |
| [performance-and-mix.md](skills/music-production/references/performance-and-mix.md) | 演奏、总线混音，以及如何解读 `analyze` |
| [soundbanks.md](skills/music-production/references/soundbanks.md) | 各音色库的特性与局限，以及如何加入自己的音色库 |
| [setup.md](skills/music-production/references/setup.md) | 在 Windows、Linux 和 macOS 上安装渲染工具 |
| [sources-and-rights.md](skills/music-production/references/sources-and-rights.md) | 使用外部乐谱、MIDI 与采样的注意事项 |

文档本身以英文撰写。

## 参与贡献

欢迎在 [Issues](https://github.com/owoevan-dev/music-skill/issues) 报告错误、提供试听反馈或推荐音色库。目前不接受项目外部的 Pull Request，原因和替代做法写在 [CONTRIBUTING.md](CONTRIBUTING.md) 里。

## 许可

代码与文档采用 [MIT](LICENSE) 许可。示范录音与乐曲本身以 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) 贡献到公有领域。第三方工具和音色库保留各自的许可，由用户从发布者处下载，不包含在这个仓库中。曲子的那张图是程序直接从钢琴版的项目文件画出来的；logo 的文字是将 Noto Serif TC（SIL Open Font License）转为轮廓。
