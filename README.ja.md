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
  <img src="docs/images/above-the-clouds.png" alt="『Above the Clouds』のすべての音をオーケストラのセクションごとに並べた図。赤がメロディーで、その下に弦、木管、金管、ハープとオルガン、打楽器。上にセクション名">
</p>

## 試聴

**[『Above the Clouds』](examples/above-the-clouds)**：オーケストラとオルガンのための演奏会用序曲です。遠くから響くホルンに始まり、アレグロ、嵐、静かなヴァイオリン独奏を経て、オルガンとともに大きな旋律がフォルティッシッシモで鳴ります。[全曲](examples/above-the-clouds/above_the_clouds.mp3)（4:28）か、[最後の 1:41](examples/above-the-clouds/above_the_clouds_highlight.mp3)をどうぞ。

**[『Signal Fire』](examples/genre-demos/signal_fire.mp3)**：フェスティバル系のハウスです。ピアノのテーマ、ビルドアップ、スーパーソーのドロップを、スキル内蔵のシンセサイザーとドラムマシンで作っています。

ほかのスタイルは [examples/genre-demos](examples/genre-demos) にあります。

- [『Late Set at the Corner』](examples/genre-demos/late_set.mp3)：テナーサックスとピアノトリオのジャズ・ブルース
- [『Midnight Coastline』](examples/genre-demos/midnight_coastline.mp3)：シンセウェイヴ。ストリングマシンのパッドにグライドするリード
- [『Rain on the Tram Line』](examples/genre-demos/tram_line_rain.mp3)：ローファイ・ヒップホップ。くたびれたテープのピアノとアーチトップギター
- [『Paper Satellites』](examples/genre-demos/paper_satellites.mp3)：フューチャーベース。キックに合わせてうねるスーパーソーのコードと 808
- [『Pixel Lantern』](examples/genre-demos/pixel_lantern.mp3)：ファミコン（NES）の制約で書いた、ゲームのフィールド用ループ

どの曲も Claude（Opus 5.5）がこのスキルで作曲・編曲・ミックスしました。各サンプルフォルダには曲を書いたスクリプトとプロジェクトファイルがあり、Windows で固定バージョンのツールを使ってレンダリングし直すと、24 ビットの丸め誤差の範囲で同じマスターになります。[『Daybreak Signal』](examples/daybreak-signal) はピアノがメロディーを弾くアニメのオープニング風の曲で、曲をどう手直ししていくかを示しています。

## クイックスタート

1. スキルを入れます。Claude Code では：

   ```
   /plugin marketplace add owoevan-dev/music-skill
   /plugin install music-skill@music-skill
   ```

   Codex などほかのエージェントでは `npx skills add owoevan-dev/music-skill`。
2. レンダリング用のツールと音源のセットアップをエージェントに頼みます。[インストール](#インストール)のコマンドを実行し、ダウンロードは約 3.6 GB、私たちのテスト環境ではそのあと約 5 分かかりました。
3. ふだんの言葉で曲を頼みます。

   > RPG の町のテーマを 1 分のループで書いて。リコーダーとハープに、やわらかい弦を添えて。

MP3 と WAV、MIDI、パートごとのステム、プロジェクトファイルが手に入ります。24 スレッドのノート PC では、上のサンプル曲のレンダリングは 30 秒（ジャズトリオ、チップチューンのループ）から 5 分（内蔵シンセで作ったハウス）で、4 分半の序曲は 3 分でした。

## 生成すればいいのでは？

テキストから音楽を作るモデルが返すのは、完成した音声ファイルです。一小節だけおかしくても、作り直せば別の曲になってしまいます。開いて音を一つ動かすことはできませんし、その音がどこから来たのかも説明できません。

ここではエージェントが譜面を書くので、音楽は読んで変えられる判断の積み重ねになります。33 小節目のメロディー、和音のボイシング、ドラマーがクラッシュを叩く強さ。音を一つ変えれば、そのパートだけが作り直されます。音色は実在の楽器をマルチサンプリングした録音（ライセンスはすべて確認できます）か、スキル内蔵のシンセサイザーです。他人の録音で学習したモデルも使っていません。

## しくみ

1. **書く**：エージェントが曲の構成とテーマを決め、プロジェクトファイルを書きます。各音の音高と長さは譜面に、弾き方（ベロシティ、タイミング、離すタイミング）は別に記録します。長めの曲は、エージェントが書く短い Python スクリプトで生成するのが普通です。ボイシングやベースライン、ドラムのパターンが読みやすく、直しやすくなります。
2. **譜面をチェックする**：`review` は、パート同士で鳴り続ける短二度・短九度と、書かれたコードから外れたメロディー音を一覧にします。どれも偶然ではなく、意図した選択になります。
3. **演奏する**：演奏モデルが、人が弾くときに生まれるずれを加えます。奏者ごとのタイミングと音量のゆるやかな揺れ、少し後ろに置いたベース、フレーズの山なりの抑揚、そして同時には押されず同時には離されない和音。サンプリングのメロディーはレガートでつなぐことも、ベンドさせることもできます。
4. **レンダリングする**：FluidSynth が、ライセンスの明確な SoundFont 音源で、サンプル音源のパートをそれぞれの楽器で鳴らします。エレクトロニックのパートは、内蔵のシンセサイザーとドラムマシン、または Surge XT シンセサイザーのプリセットで鳴らします。
5. **ミックスとマスタリング**：各パートはドラム、ベース、リズム、アンサンブル、メロディーのバスと、自動生成した四種類のリバーブを通り、マスター処理で −14 LUFS、トゥルーピーク −1 dBTP 以下に仕上がります。オーケストラやオルガンの曲は、コンプレッサーを通さずに強弱の幅をそのまま残せます。エレクトロニックな曲には、サイドチェインのダッキング、テンポに合わせたディレイ、フィルタースイープ、クラブ向けの大音量マスターを加えられます。
6. **計測する**：`analyze` は、セクションごとの音量、スペクトル、ステレオ感、メロディーが伴奏よりどれだけ前に出ているかを測り、マスターの音のバランスを、市販の録音について公表された測定値や同じジャンルのリファレンスと比べます。数字は問題の場所を示すだけで、聴くことの代わりにはなりません。

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

Windows x64 では、固定バージョンの FluidSynth と FFmpeg のポータブル版に加え、Surge XT シンセサイザーとそれを動かすプラグインホストをダウンロードします（約 55 MB。`--no-surge` で省けます）。

```
python skills/music-production/scripts/bootstrap.py --runtime <folder>/.runtime --config <folder>/local-config.json
```

Linux（Ubuntu 24.04、Debian 13 以降）と macOS では、システムのパッケージと、ご自身で入れた Surge XT（あれば）を使います。

```
sudo apt install fluidsynth ffmpeg libarchive-tools        # macOS: brew install fluid-synth ffmpeg
python3 skills/music-production/scripts/bootstrap.py --system --runtime <folder>/.runtime --config <folder>/local-config.json
```

続いて音源を入れます（このプロジェクトで構築したもの）。29 種すべてでダウンロードは約 3.4 GB、インストール後は約 8 GB です。`--only orchestra`、`band`、`world`、`examples`（サンプル曲で使う音源）でグループごとに、または音源名（`--only vcsl,rusty`）で個別に入れられます。入っていない音源を使うプロジェクトは、それを入れるコマンドを示して止まります。`--from-source` を付けると、配布元のサンプルから自分で構築します。

```
python skills/music-production/scripts/fetch_soundbanks.py --config <folder>/local-config.json --runtime <folder>/.runtime --output <folder>/local-config.studio.json
```

必要なのは Python 3.10 以降と NumPy だけです。GPU もアカウントも音声モデルも要りません。ダウンロードはすべて配布元か、このプロジェクト自身のリリースから行い、固定した SHA-256 で照合します。

## 使い方

エージェントに普段の言葉で頼んでください。

> パズルゲームのタイトル画面用に、90 秒のインストを書いて。あたたかくて少し切ない感じで、ピアノとストリングス。

> TV サイズのアニメ OP 風の曲を作って。ギターバンドにピアノのメロディーで。

> ビジュアルノベルの悲しい場面に流すループ曲を書いて。柔らかいピアノとチェロで、文章を読む邪魔にならない静かさで。

> フルオーケストラで 2 分の曲を書いて。日の出の情景で、静かなホルンのソロからオーケストラ全体まで。

> レースゲームの夜のドライブに合うシンセウェイヴの曲を作って。100 BPM、ゲートリバーブのスネア、グライドするリード。

> 33 小節目のサビのメロディーが忙しすぎる。シンプルにして作り直して。

> MIDI とステムもちょうだい。

## 音源

| 楽器 | 音源 | ライセンス |
|---|---|---|
| ピアノと鍵盤 | VCSL（Versilian Studios）の Steinway B、Kawai のグランドピアノ、アップライトピアノ、チェンバロ、Yamaha TX81Z の FM 音色、パイプオルガン。Karoryfer Samples の Osiris Piano（サステインペダルを踏んだ録音と踏まない録音） | CC0 |
| オーケストラ | VSCO 2 Community Edition（Versilian Studios）のストリングス（パート別、トレモロ、ピチカートを含む）、ブラス、トロンボーン、テューバ、コントラバス、木管、ピッコロ、グロッケンシュピール。VCSL のハープ、鍵盤打楽器、チューブラーベル、ティンパニ、オーケストラ打楽器。アイオワ大学電子音楽スタジオのホルン、バストロンボーン、クラリネット、フルート、ソロ弦楽器、打楽器 | CC0。アイオワ：用途を問わず制限なく使用可 |
| バンド | FreePats FSBS のエレキギター（ディストーション 2 種、クリーン 1 種）。Bass YR のピック弾きと指弾き（サンプル収録：Andrea Biasior）。Karoryfer Samples の Big Rusty Drums、5 弦ベース、ピチカートのコントラバス、アーチトップギター、バリトンサックス、テューバ。Karoryfer Lecolds と bigcat instruments のソロ・チェロ | CC0 |
| ソロと民族楽器 | VCSL のテナーサックス、サクセロ、リコーダー、オカリナ、ハーモニカ、フォークハープ、ダン・チャン、プサルテリウム、カリンバ、バラフォン、民族打楽器。二胡。テナー・スチールパン。歌声の「アー」 | CC0。スチールパン：Unlicense |
| シンセサイザー | 内蔵のシンセサイザーとドラムマシン。Surge XT と厳選した 50 のファクトリープリセット（任意、標準でインストール） | 内蔵：MIT。Surge XT：GPL-3.0、独立したプログラムとして実行 |
| その他の楽器 | MuseScore MS Basic | MIT |

収録音源はすべて CC0、用途を問わず制限なく使えるもの（アイオワ大学の録音）、またはパブリックドメインに供されたもの（スチールパン）なので、それで作った音楽にクレジットは要りません。Surge XT は GPL-3.0 で、独立したプログラムとして動きます。GPL が及ぶのはプログラム自体で、それが鳴らした音楽ではありません。MS Basic の MIT 表示は音源ファイルそのものの複製に付くもので、レンダリングした音楽には及びません。出典は [THIRD_PARTY.md](THIRD_PARTY.md) にあります。

## どこまでできるか

`selfcheck.py` には 72 項目のチェック（レンダリング用の設定がなければ 56 項目）があり、MIDI の往復変換やアーカイブの安全性から、実際のレンダリングまで含みます。たとえば、音を一つ直したときに作り直されるのはそのパートだけであること、旧来の単一リバーブのミックスが以前のリリースをビット単位で再現すること、ラウドネス計測が BS.1770 の基準音を −3.01 LUFS と読むこと。CI では、Ubuntu（FluidSynth 2.3、FFmpeg 6.1）と macOS（FluidSynth 2.6、FFmpeg 9.0）で、レンダリングも含めた全チェックを実行しています。

音楽として良いかどうかは別の話で、聴いてみるしかありません。上の曲が、このリポジトリで示せるいちばんの証拠です。

## よくある質問

**作った音楽を動画やゲーム、商用作品に使えますか？** ツールの側に妨げはありません。音源は CC0 か用途を問わず使えるもので、クレジットも要りません。GPL のプログラム（FFmpeg、Surge XT）が及ぶのはプログラム自体で、通った音楽ではありません。エージェントが書いた音楽にあなたの著作権が生じるかどうかは、お住まいの国の法律と、あなたがどこまで手を加えたかによります。

**どのエージェントで使えますか？** Agent Skills を読み込めて Python を実行できるエージェントなら使えます。Claude Code（プラグインとして）、Codex、そのほか `npx skills` で入れたもの。

**インターネットや GPU は必要ですか？** インターネットはセットアップのときだけで、レンダリングは CPU でオフラインに動きます。プロジェクトファイルが外に出るのは、エージェントが読んだ内容を自分のモデルに送るときだけです。

**自分の音源は使えますか？** SF2 の音源なら使えます。`studio.py add-soundfont` で設定に加え、パートで指定します（[soundbanks.md](skills/music-production/references/soundbanks.md)）。加えた音源はそれぞれのライセンスに従うので、作品を公開する前に確認してください。

## できないこと

- 歌うことや作詞はできません。プラグインは Surge XT だけに対応し、お手持ちの VST プラグインはまだ使えません。
- 音の質は無料の音源で決まります。YR ベースのベロシティレイヤーは一層だけ、ストリングスは立ち上がりが遅めで、マリンバ、シロフォン、ピッコロはサンプルがまばらです。サンプリングしたギターのベンドはサンプル全体の音程を変えるだけなので、本物の弦のような音色の変化はありません。
- アコースティックギター、合唱、そして二胡とダン・チャン以外の東アジアの楽器の音源はまだありません。こうしたパートは、サンプルの少ない MS Basic の General MIDI 音色になります。
- Surge XT はオシレーターをランダムな位相で鳴らし始めるため、Surge のパートは合成するたびにわずかに違うテイクになります。レンダーキャッシュは、パートを変えるまで一つのテイクを保持します。それ以外は毎回同じ結果になります。
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
| [ジャンル別ガイド](skills/music-production/references) | エレクトロニック、ビート、ジャズとファンク、アニメのオープニング、ゲームと場面の音楽、オーケストラ、オルガン、ピアノと室内楽 |
| [setup.md](skills/music-production/references/setup.md) | Windows、Linux、macOS でのレンダリング用ツールの導入 |
| [sources-and-rights.md](skills/music-production/references/sources-and-rights.md) | 外部の譜面、MIDI、サンプルを使うときの注意 |

ドキュメント本体は英語で書かれています。

## コントリビュート

不具合の報告、試聴しての感想、音源の提案は [Issues](https://github.com/owoevan-dev/music-skill/issues) で歓迎しています。外部からのプルリクエストは現在受け付けていません。理由と代わりの方法は [CONTRIBUTING.md](CONTRIBUTING.md) にあります。

## ライセンス

コードとドキュメントは [MIT](LICENSE) です。サンプル曲の録音と楽曲は [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) でパブリックドメインに提供しています。サードパーティのツールと音源はそれぞれのライセンスのままで、このリポジトリには含めず、配布元からダウンロードします。序曲の図はそのプロジェクトファイルからコードで描いたもので、ロゴの文字は Noto Serif TC（SIL Open Font License）をアウトライン化したものです。
