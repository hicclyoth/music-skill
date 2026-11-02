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
  <strong>日本語</strong> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/owoevan-dev/music-skill/actions/workflows/tests.yml"><img src="https://github.com/owoevan-dev/music-skill/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f1c1a" alt="Licence: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-1f1c1a" alt="Python 3.10 or newer">
</p>

<p align="center"><strong>生成せず、作曲する。</strong></p>

music-skill は、作曲家と小さなスタジオのやり方でオリジナルの器楽曲を作るための [Agent Skill](https://agentskills.io) です。音はすべてエージェントが一つずつ書きます。スキルはその譜面をチェックし、サンプリング音源で演奏し、ミックスとマスタリングまで仕上げます。

音声生成モデルは一切使いません。MP3 と WAV に加えて、MIDI、パートごとのステム、そしてどの音でも書き換えて作り直せるプロジェクトファイルが手に入ります。

<p align="center">
  <img src="docs/images/daybreak-signal.png" alt="『Daybreak Signal』のすべての音をパートごとに並べた図。赤がメロディーで、その下にオーケストラ、ギター、ベース、ドラム。上にセクション名">
</p>

## 試聴

『Daybreak Signal』は、アニメのオープニング風のインストゥルメンタルです。TV サイズの 87 秒、176 BPM で、サビに入るところで短三度上に転調します。Claude（Opus 5.5）がこのスキルで作曲・編曲・ミックスを行い、その後手直ししました。止まる箇所を減らし、メロディーをレガートでつなぎ、ピアノがメロディーを弾く版も作っています。

- [ピアノ版](examples/daybreak-signal/piano.mp3)
- [エレキギター版](examples/daybreak-signal/guitar.mp3)

二つの版の違いは、メロディーを弾く楽器だけです。[examples/daybreak-signal](examples/daybreak-signal) に、この曲を書いたスクリプトと両方のプロジェクトファイルがあります。Windows で固定バージョンのツールを使ってレンダリングし直すと、24 ビットの丸め誤差の範囲で同じマスターになります。

## 生成すればいいのでは？

テキストから音楽を作るモデルが返すのは、完成した音声ファイルです。一小節だけおかしくても、作り直せば別の曲になってしまいます。開いて音を一つ動かすことはできませんし、その音がどこから来たのかも説明できません。

ここではエージェントが譜面を書くので、音楽は読んで変えられる判断の積み重ねになります。33 小節目のメロディー、和音のボイシング、ドラマーがクラッシュを叩く強さ。音を一つ変えれば、そのパートだけが作り直されます。音色は実在の楽器をマルチサンプリングした録音で、ライセンスはすべて確認できます。他人の録音で学習したモデルも使っていません。

## しくみ

1. **書く**：エージェントが曲の構成とテーマを決め、プロジェクトファイルを書きます。各音の音高と長さは譜面に、弾き方（ベロシティ、タイミング、離すタイミング）は別に記録します。長めの曲は、エージェントが書く短い Python スクリプトで生成するのが普通です。ボイシングやベースライン、ドラムのパターンが読みやすく、直しやすくなります。
2. **譜面をチェックする**：`review` は、パート同士で鳴り続ける短二度・短九度と、書かれたコードから外れたメロディー音を一覧にします。どれも偶然ではなく、意図した選択になります。
3. **演奏する**：演奏モデルが、人が弾くときに生まれるずれを加えます。奏者ごとのタイミングと音量のゆるやかな揺れ、少し後ろに置いたベース、フレーズの山なりの抑揚、そして同時には押されず同時には離されない和音。サンプリングのメロディーはレガートでつなぐことも、ベンドさせることもできます。
4. **レンダリングする**：FluidSynth が、ライセンスの明確な SoundFont 音源で、パートごとにそれぞれの楽器を鳴らします。
5. **ミックスとマスタリング**：各パートはドラム、ベース、リズム、アンサンブル、メロディーのバスと、自動生成した四種類のリバーブを通り、マスター処理で −14 LUFS、トゥルーピーク −1 dBTP 以下に仕上がります。オーケストラやオルガンの曲は、コンプレッサーを通さずに強弱の幅をそのまま残せます。
6. **計測する**：`analyze` は、セクションごとの音量、スペクトル、ステレオ感、そしてメロディーが伴奏よりどれだけ前に出ているかを測ります。数字は問題の場所を示すだけで、聴くことの代わりにはなりません。

音を一つ変えれば、そのパートだけを作り直します。ミックスを変えるだけなら、作り直しは一切ありません。

ゲーム用のプロジェクトはループにできます。レンダリング時に残響の尾をループの頭へ折り返し、Godot や RPG Maker が読む形式でループ位置を WAV と Ogg に書き込み、各セクションの頭にはキューポイントを付けます。ループをいくつかのレイヤーに分けることもでき、すべてを重ねると元のミックスになるので、ゲームの盛り上がりに合わせて音を重ねていけます。

## インストール

**Claude Code**

```
/plugin marketplace add owoevan-dev/music-skill
/plugin install music-skill@music-skill
```

**Codex やその他のエージェント**

```
npx skills add owoevan-dev/music-skill
```

`skills/music-production` をエージェントのスキルフォルダーにコピーしても使えます。

**レンダリング用ツール**（マシンごとに一度だけ。エージェントに任せられます）

Windows x64 では、固定バージョンの FluidSynth と FFmpeg のポータブル版をダウンロードします。

```
python skills/music-production/scripts/bootstrap.py --runtime <folder>/.runtime --config <folder>/local-config.json
```

Linux（Ubuntu 24.04、Debian 13 以降）と macOS では、システムのパッケージを使います。

```
sudo apt install fluidsynth ffmpeg libarchive-tools        # macOS: brew install fluid-synth ffmpeg
python3 skills/music-production/scripts/bootstrap.py --system --runtime <folder>/.runtime --config <folder>/local-config.json
```

続いて、デモで使った楽器を入れます（ダウンロードは約 1 GB）。

```
python skills/music-production/scripts/fetch_soundbanks.py --config <folder>/local-config.json --runtime <folder>/.runtime --output <folder>/local-config.studio.json
```

必要なのは Python 3.10 以降と NumPy だけです。GPU もアカウントも音声モデルも要りません。ダウンロードはすべて配布元の公式ページから行い、固定した SHA-256 で照合します。

## 使い方

エージェントに普段の言葉で頼んでください。

> パズルゲームのタイトル画面用に、90 秒のインストを書いて。あたたかくて少し切ない感じで、ピアノとストリングス。

> TV サイズのアニメ OP 風の曲を作って。ギターバンドにピアノのメロディーで。

> ビジュアルノベルの悲しい場面に流すループ曲を書いて。柔らかいピアノとチェロで、文章を読む邪魔にならない静かさで。

> フルオーケストラで 2 分の曲を書いて。日の出の情景で、静かなホルンのソロからオーケストラ全体まで。

> 33 小節目のサビのメロディーが忙しすぎる。シンプルにして作り直して。

> MIDI とステムもちょうだい。

## 音源

| 楽器 | 音源 | ライセンス |
|---|---|---|
| グランドピアノ | VCSL の Steinway B（Versilian Studios）、Osiris Piano（Karoryfer Samples。サステインペダルを踏んだ録音と踏まない録音）、どちらもここで構築 | CC0 |
| エレキギター | FreePats FSBS：ディストーション 2 種、クリーン 1 種 | CC0 |
| エレキベース | Bass YR、ピック弾きと指弾き（サンプル収録：Andrea Biasior）、Black And Blue Basses（Karoryfer Samples）の5 弦ベース（ゴーストノート付き）をここで構築 | CC0 |
| ドラムキット | Big Rusty Drums（Karoryfer Samples）を GM の鍵盤配置で構築 | CC0 |
| ストリングス（トレモロ、ピチカートを含む）、ソロ・ヴァイオリン、コントラバス、ブラス、トランペット、ホルン、トロンボーン、テューバ、木管、ピッコロ、グロッケンシュピール | VSCO 2 Community Edition（Versilian Studios）から構築 | CC0 |
| ハープ、マリンバ、ヴィブラフォン、シロフォン、チューブラーベル、ティンパニ、オーケストラ打楽器（シンバルとそのクレッシェンド、ゴング、トライアングル、スレイベル、ウィンドチャイム）、パイプオルガン | VCSL（Versilian Studios）から構築 | CC0 |
| ソロ・チェロ | Karoryfer x bigcat cello（Karoryfer Lecolds、bigcat instruments）を、録音にあるループポイントごとここで構築 | CC0 |
| その他の楽器 | MuseScore MS Basic | MIT |

収録音源はすべて CC0 なので、それで作った音楽にクレジットは要りません。MS Basic の MIT 表示は音源ファイルそのものの複製に付くもので、レンダリングした音楽には及びません。出典は [THIRD_PARTY.md](THIRD_PARTY.md) にあります。

## どこまでできるか

`selfcheck.py` には 46 項目のチェックがあり、MIDI の往復変換やアーカイブの安全性から、実際のレンダリングまで含みます。たとえば、音を一つ直したときに作り直されるのはそのパートだけであること、旧来の単一リバーブのミックスが以前のリリースをビット単位で再現すること、ラウドネス計測が BS.1770 の基準音を −3.01 LUFS と読むこと。CI では、Ubuntu（FluidSynth 2.3、FFmpeg 6.1）と macOS（FluidSynth 2.6、FFmpeg 9.0）で、レンダリングも含めた全チェックを実行しています。

音楽として良いかどうかは別の話で、聴いてみるしかありません。上のデモが、このリポジトリで示せるいちばんの証拠です。

## できないこと

- 歌うことや作詞はできません。VST プラグインにも対応していません。
- 音の質は無料の音源で決まります。YR ベースのベロシティレイヤーは一層だけ、ストリングスは立ち上がりが遅めで、マリンバ、シロフォン、ピッコロはサンプルがまばらです。サンプリングしたギターのベンドはサンプル全体の音程を変えるだけなので、本物の弦のような音色の変化はありません。
- エージェントには音が聞こえません。`review` と `analyze` は問題の場所を見つけるだけで、結果は人が聴く必要があります。スキルは、聴いていないのに聴いたと言わないようエージェントに求めています。
- Linux と macOS ではシステムの FluidSynth と FFmpeg を使うため、固定バージョンの Windows 版とはサンプル単位でわずかに違う場合があります。

## ドキュメント

| | |
|---|---|
| [SKILL.md](skills/music-production/SKILL.md) | エージェントがたどる手順と、すべてのコマンド |
| [schema.md](skills/music-production/references/schema.md) | プロジェクトファイル：譜面、演奏、ミックス |
| [arrangement.md](skills/music-production/references/arrangement.md) | 構成、メロディー、ボイシング、各パートの役割 |
| [performance-and-mix.md](skills/music-production/references/performance-and-mix.md) | 演奏、バスによるミックス、`analyze` の読み方 |
| [soundbanks.md](skills/music-production/references/soundbanks.md) | 各音源の特徴とくせ、自分の音源の追加方法 |
| [setup.md](skills/music-production/references/setup.md) | Windows、Linux、macOS でのレンダリング用ツールの導入 |
| [sources-and-rights.md](skills/music-production/references/sources-and-rights.md) | 外部の譜面、MIDI、サンプルを使うときの注意 |

ドキュメント本体は英語で書かれています。

## コントリビュート

不具合の報告、試聴しての感想、音源の提案は [Issues](https://github.com/owoevan-dev/music-skill/issues) で歓迎しています。外部からのプルリクエストは現在受け付けていません。理由と代わりの方法は [CONTRIBUTING.md](CONTRIBUTING.md) にあります。

## ライセンス

コードとドキュメントは [MIT](LICENSE) です。デモの録音と楽曲は [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) でパブリックドメインに提供しています。サードパーティのツールと音源はそれぞれのライセンスのままで、このリポジトリには含めず、配布元からダウンロードします。曲の図はピアノ版のプロジェクトファイルからコードで描いたもので、ロゴの文字は Noto Serif TC（SIL Open Font License）をアウトライン化したものです。
