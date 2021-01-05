# freee Accessibility Guidelines

freee株式会社が作成しているアクセシビリティー・ガイドラインの一般公開版のリポジトリーです。現在作成中で、随時更新する予定です。

このガイドラインの作成の経緯などについて詳しくは、[ガイドラインのイントロダクション](https://a11y-guidelines.freee.co.jp/intro/index.html)と、[freee Developers Blogの記事](https://developers.freee.co.jp/entry/a11y-guidelines-202004.0)をご覧ください。

## 最新ファイルの入手

以下のURLで最新のファイルを入手していただけます:

* HTML版: <https://a11y-guidelines.freee.co.jp/>
* HTMLファイルをまとめたzipファイルおよびソースファイル: <https://github.com/freee/a11y-guidelines/releases/latest>

## この文書に関するお問い合わせなど

この文書に関するお問い合わせ、ご意見などは、このリポジトリーでissueを作成してお知らせください。

誤字脱字の修正など、エディトリアルな修正の提案については、issueまたはpull requestを作成してください。

## 日本語の表記ルールについて

このガイドラインは、 原則として[日本翻訳連盟](https://www.jtf.jp/)が公開している[JTF日本語標準スタイルガイド(翻訳用）](https://www.jtf.jp/tips/styleguide)に従って記述しています。

リポジトリーのルート・ディレクトリーの `.textlintrc` に、現在使用しているtextlintのルールが含まれていますが、現時点では不完全な状態です。

## ソースについて

この文書はreStructuredTextで記述し、Sphinxで処理しています。
HTMLファイルの生成には、Python 3.x (開発環境では3.7.xを使っています)、[Sphinx](https://www.sphinx-doc.org/en/master/)と[Read the Docs Sphinx Theme (sphinx_rtd_theme)](https://github.com/readthedocs/sphinx_rtd_theme)が必要です。

このリポジトリーをcloneしたうえで、Pythonが利用できる環境で、以下のように実行するとHTMLを生成することができます:

`````
% pip install --upgrade pip
% pip install -r requirements.txt
% make html
`````

## ライセンス

![クリエイティブ・コモンズ・ライセンス](https://i.creativecommons.org/l/by/4.0/88x31.png)
「freeeアクセシビリティー・ガイドライン」は、freee株式会社が作成したもので、[クリエイティブ・コモンズ 表示 4.0 国際 ライセンス](http://creativecommons.org/licenses/by/4.0/)で提供されています。

Copyright © 2020-2021, freee株式会社

## 更新履歴

### [Ver. 202101.0](https://github.com/freee/a11y-guidelines/releases/202101.0/) (2021年1月5日)

参考： [freeeアクセシビリティー・ガイドラインVer. 202101.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202101.0)

* 参考情報更新
   - [Tab/Shift+Tabキーを用いたチェック](https://a11y-guidelines.freee.co.jp/explanations/tab-order-check.html)に、キーボードのみを用いた操作が可能であることを確認する方法として、マウス・ポインターを非表示にする方法を追加
* 誤字修正

### [Ver. 202011.0](https://github.com/freee/a11y-guidelines/releases/202011.0/) (2020年11月27日)

参考： [freeeアクセシビリティー・ガイドラインVer. 202011.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202011.0)

**注意** ：新たに追加されたガイドラインと、優先度が変更されたガイドラインがあります。

* WCAG 2.1の各達成基準と当ガイドラインの対応表を追加： [WCAG 2.1の各達成基準と当ガイドラインの項目との対応](https://a11y-guidelines.freee.co.jp/info/wcag21-mapping.html)
* WCAG 2.1の各達成基準の適合レベルと、当ガイドラインの優先度の関係に関する情報を追加： [当ガイドラインの優先度とWCAG 2.1の適合レベルについて](https://a11y-guidelines.freee.co.jp/info/priority.html)
* 画像化されたテキストに関するガイドラインの見直し： [[SHOULD] 画像化されたテキストを使用しない](https://a11y-guidelines.freee.co.jp/categories/images_of_text.html#gl-iot-avoid-usage)
    - 変更前：画像化されたテキストを用いていない、または用いられている画像化されたテキストがコントラスト比と代替情報に関するガイドラインを満たしている場合に[MUST]の条件を満たす
    - 変更後：画像化されたテキストが用いられていない場合は[SHOULD]の条件を満たし、用いられている画像化されたテキストがコントラスト比と代替情報に関するガイドラインを満たしている場合は[MUST]の条件を満たす
* テキストの代替の音声・映像コンテンツの音声解説に関するガイドラインを追加： [[SHOULD] 音声解説の提供](https://a11y-guidelines.freee.co.jp/categories/multimedia.html#gl-multimedia-video-description-no-exception)
    - 対応するチェック内容を追加： [チェックID: 1562](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-1562)
* [入力ディバイス： [MUST] ショートカット・キーを提供する場合](https://a11y-guidelines.freee.co.jp/categories/input_device.html#gl-input-device-shortcut-keys)の優先度を[SHOULD]から[MUST]に変更
* ARIAランドマークに関する用語の見直しと統一（内容に変更無し）
* 一部チェック内容について、文言の見直し（内容に変更無し）
* 誤字修正

### [Ver. 202010.0](https://github.com/freee/a11y-guidelines/releases/202010.0/) (2020年10月27日)

参考： [freeeアクセシビリティー・ガイドラインVer. 202010.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202010.0)

**注意** ：以下のチェック実施方法の例の追加に伴い、チェック内容の全項目一覧のURLが変更されています：

旧： `https://a11y-guidelines.freee.co.jp/checks/index.html`  
新： <https://a11y-guidelines.freee.co.jp/checks/checklist.html>

* チェック内容の追加
    - [チェックID: 0621](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0621)
* いくつかのチェック内容について、チェックの実施方法を例として追加
    - [NVDAを用いたチェック実施方法の例](https://a11y-guidelines.freee.co.jp/checks/examples/nvda.html)
    - [axeを用いたチェック実施方法の例](https://a11y-guidelines.freee.co.jp/checks/examples/axe.html)
* 参考情報の追加
    - [axeを使用したアクセシビリティー・チェック](https://a11y-guidelines.freee.co.jp/explanations/axe.html)
   - [リンク先の内容を推測しやすくする](https://a11y-guidelines.freee.co.jp/explanations/link-text.html)
* 参考情報の更新
    - ARIAライブ・リージョンの実装例と実装時の注意点を追加：[ステータス・メッセージとスクリーン・リーダー](https://a11y-guidelines.freee.co.jp/explanations/dynamic_content-status.html)
    - `lang` 属性に関する具体的な説明を追加： [lang 属性と音声読み上げ](https://a11y-guidelines.freee.co.jp/explanations/text-lang.html)
    - ナビゲーションの一貫性について加筆： [使いやすさとアクセシビリティーを改善するナビゲーションの設計と実装](https://a11y-guidelines.freee.co.jp/explanations/page-navigation.html)
* 誤字修正

### [Ver. 202009.0](https://github.com/freee/a11y-guidelines/releases/202009.0/) (2020年9月29日)

参考： [freeeアクセシビリティー・ガイドラインVer. 202009.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202009.0)

* テキストの拡大表示に関連するガイドライン、チェック内容、参考情報を更新
    - 意図をより明確にするために、「200パーセントの拡大表示」を3ガイドラインに分割
        - 変更前\
          200パーセントの拡大表示：[MUST]コンテンツや機能を損なうことなくブラウザーのズーム機能で200パーセントまで拡大できるようにする。
        - 変更後
           * [[MUST] ズーム機能を用いた200パーセントの拡大表示](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-zoom)
           * [[MUST] 文字サイズ変更機能の使用](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-enlarge-settings)
           * [[SHOULD] 文字サイズ変更機能による200パーセントの拡大表示](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-enable-enlarge)
    - 意図を明確にするために[[SHOULD] 400パーセントの拡大表示](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-zoom-reflow)の文言を変更
    - 関連するチェック内容の変更と追加
        - 変更： [チェックID: 0321](https://a11y-guidelines.freee.co.jp/checks/index.html#check-0321)、[チェックID: 0322](https://a11y-guidelines.freee.co.jp/checks/index.html#check-0322)
        - 追加： [チェックID: 0311](https://a11y-guidelines.freee.co.jp/checks/index.html#check-0311)、[チェックID: 0323](https://a11y-guidelines.freee.co.jp/checks/index.html#check-0323)、[チェックID: 0324](https://a11y-guidelines.freee.co.jp/checks/index.html#check-0324)
    - 関連する参考情報の更新： [拡大表示時のアクセシビリティー](https://a11y-guidelines.freee.co.jp/explanations/magnification.html)
* その他参考情報の更新
    - [色を用いた表現に関する注意点](https://a11y-guidelines.freee.co.jp/explanations/color-only.html)にカラー・ユニバーサル・デザインに関する記述を追加
    - [スクリーン・リーダーを用いたチェックの実施方法](https://a11y-guidelines.freee.co.jp/explanations/screen-reader-check.html)にNVDAのスピーチビューアーに関する説明を追加
* 誤字修正

### [Ver. 202008.0](https://github.com/freee/a11y-guidelines/releases/202008.0/) (2020年8月21日)

参考： [freeeアクセシビリティー・ガイドラインVer. 202008.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202008.0)

* チェック内容の見直し
    - チェック対象を「デザイン」、「コード」、「プロダクト」に変更
    - 全ガイドラインに対するチェック内容の見直しと整理
    - すべてのチェック内容をまとめた章を追加： [アクセシビリティー・チェック・リスト](https://a11y-guidelines.freee.co.jp/checks/index.html)
* 参考情報更新
    - クリック/タッチ・ターゲットのサイズの確認方法についての記述を追加： [クリックやタッチのターゲット・サイズに関連する問題とターゲット・サイズの確認方法](https://a11y-guidelines.freee.co.jp/explanations/target-size.html)
* 誤字修正 ([#10](https://github.com/freee/a11y-guidelines/pull/10), [#11](https://github.com/freee/a11y-guidelines/pull/11)、他)

### [Ver. 202007.0](https://github.com/freee/a11y-guidelines/releases/202007.0/) (2020年7月10日)

参考： [freeeアクセシビリティー・ガイドラインVer. 202007.0を公開しました](https://developers.freee.co.jp/entry//a11y-guidelines-202007.0)

* 参考情報追加：[スクリーン・リーダーを用いたチェックの実施方法](https://a11y-guidelines.freee.co.jp/explanations/screen-reader-check.html#exp-screen-reader-check)
* 参考情報更新
  - [様々なユーザーの入力手段の特徴とそのサポート](https://a11y-guidelines.freee.co.jp/explanations/input_device-various.html#exp-input-device-various)：[[MUST] ダウン・イベントをトリガーにしない](https://a11y-guidelines.freee.co.jp/categories/input_device.html#gl-input-device-use-up-event)に関する説明で、クリック・イベントについての記述を追加
* 動的コンテンツの[[MUST] 点滅、スクロールを伴うコンテンツ](https://a11y-guidelines.freee.co.jp/categories/dynamic_content.html#gl-dynamic-content-pause-movement)から「動きを伴うコンテンツ」の記述を削除し、音声・映像コンテンツにアニメーションや動画を対象とした新ガイドラインを追加：[[MUST] 動きを伴うコンテンツ](https://a11y-guidelines.freee.co.jp/categories/multimedia.html#gl-multimedia-pause-movement)
* リンクのターゲット・サイズに関するガイドラインについて、テキスト・リンクについてはWCAGで例外とされているので、アイコンの場合の基準のみ記し、アイコンのカテゴリーに移動：[[SHOULD] 十分な大きさのクリック/タッチのターゲット](https://a11y-guidelines.freee.co.jp/categories/icon.html#gl-icon-target-size)
* フォームのターゲット・サイズに関するガイドラインについて、アイコンと同じ基準を明記：[[SHOULD] 十分な大きさのクリック/タッチのターゲット](https://a11y-guidelines.freee.co.jp/categories/form.html#gl-form-target-size)
* 入力ディバイスのガイドライン2項目をマージ：[[MUST] 特定の入力ディバイスを前提としない](https://a11y-guidelines.freee.co.jp/categories/input_device.html#gl-input-device-independent)
  マージ対象ガイドライン：
  - [MUST] 入力ディバイスのサポート：OSがサポートしている入力ディバイスの使用を妨げない。
  - [MUST] ユーザーの動きだけをトリガーにしない：加速度センサー、モーション・キャプチャーなどを活用した、ユーザーの動きをトリガーにする機能は、他のインターフェースによっても実行できるようにする。
* ガイドラインの文言を一部変更（下表参照）

#### Ver. 202007.0でのガイドライン文言変更箇所

| 該当箇所 | 変更前 | 変更後 | 補足 |
|---|---|---|---|
| ページ全体：[[SHOULD] 適切なセクション分けと見出しの付与](https://a11y-guidelines.freee.co.jp/categories/page.html#gl-page-headings) |  `h?` 要素を使って適切に見出しを付ける。 |  コンテンツを適切にセクション分けし、 `h?` 要素を使って見出しを付ける。 |  意図が明確になるように同ガイドラインの見出しも変更しています。 |
| 入力ディバイス：[[MUST] ダウン・イベントをトリガーにしない](https://a11y-guidelines.freee.co.jp/categories/input_device.html#gl-input-device-use-up-event) |  操作の実行、完了のトリガーにはダウン・イベントを使わず、アップ・イベントを使う。 |  クリックやタップで実行される機能の実行、完了のトリガーには、ダウン・イベントを使わず、アップ・イベントやクリック・イベントを使い、誤った操作を中断できるようにする。 |  意図の項にも追記して、ドラッグ&amp;ドロップがこのガイドラインに抵触しないことを明示しています。 |
| テキスト：[[MUST] 適切な文言の見出し](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-heading-label) |  主題又は目的を説明する見出しおよびラベルを付ける。 |  主題又は目的を説明する見出しを付ける。 |  「ラベル」はフォーム・コントロールと画像の説明を意図したものでしたが、これらはそれぞれ別カテゴリーでカバーされているため削除しました。併せて見出しも変更しています。 |
| テキスト：[[MUST] 複数の視覚的要素を用いた表現](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-color-only) |  文字色に何らかの意味を持たせている場合、書体など他の視覚的な要素も併せて用い、色が判別できなくてもその意味を理解できるようにする。 |  強調、引用など、何らかの意図を文字色を変えることによって表現している場合、書体など他の視覚的な要素も併せて用い、色が判別できなくてもその意味を理解できるようにする。 |  ガイドラインの意図を考慮して、掲載セクションを変更しています。 |
| 音声・映像コンテンツ：[[MUST] 書き起こしテキストの提供](https://a11y-guidelines.freee.co.jp/categories/multimedia.html#gl-multimedia-transcript) |  テキストの代替情報ではない音声・映像コンテンツにおいて、映像がなく音声のみの収録済みコンテンツの場合は、書き起こしテキストを提供する。 |  テキストの代替情報ではない、映像がなく音声のみの収録済みコンテンツの場合は、書き起こしテキストを提供する。 | |
| 動的コンテンツ：[[MUST] 点滅、スクロールを伴うコンテンツ](https://a11y-guidelines.freee.co.jp/categories/dynamic_content.html#gl-dynamic-content-pause-movement) |  自動的に開始し5秒以上継続する、点滅、スクロールまたは動きを伴うコンテンツを作らない。そのようなコンテンツを作る場合は、ユーザーが一時停止、停止、非表示にすることができるようにする。 |  同じページ上に、自動的に開始し5秒以上継続する、点滅やスクロールを伴うコンテンツと、他のコンテンツを一緒に配置しない。そのようなコンテンツを作る場合は、ユーザーが一時停止、停止、または非表示にすることができるようにする。 | |
| 動的コンテンツ：[[MUST] 自動更新されるコンテンツ](https://a11y-guidelines.freee.co.jp/categories/dynamic_content.html#gl-dynamic-content-pause-refresh) |  自動的に内容が更新されるコンテンツを作らない。そのようなコンテンツを作る場合は、ユーザーが一時停止、停止、非表示にすることができるか、更新頻度を調整できるようにする。 |  予め設定された間隔で自動的に内容が更新されたり非表示になったりするコンテンツを作らない。そのようなコンテンツを作る場合は、ユーザーが一時停止、停止、非表示にすることができるか、更新頻度を調整できるようにする。 | |
| フォーム：[[SHOULD] 誤操作の防止](https://a11y-guidelines.freee.co.jp/categories/form.html#gl-form-errors-cancel) |  誤った操作が確定することでユーザーに不利益が生じる可能性がある機能については、取り消し、送信前の確認・修正、または送信時のエラー・チェックと修正を可能にする。 |  法的行為、経済的取引、データの変更や削除を生じる機能については、取り消し、送信前の確認・修正、または送信時のエラー・チェックと修正を可能にする。 | |


### [Ver. 202006.0](https://github.com/freee/a11y-guidelines/releases/202006.0/) (2020年6月18日)

参考： [freeeアクセシビリティー・ガイドラインVer. 202006.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202007.0)

* ガイドライン部分の文書構造を見直し
* [入力ディバイス](http://a11y-guidelines.freee.co.jp/categories/input_device.html)に関するガイドラインの構成を一部変更（内容に変更無し）
* コントラスト関連のガイドラインで、文字サイズの表記をpxとptを併記するように変更
* [動的コンテンツ](http://a11y-guidelines.freee.co.jp/categories/dynamic_content.html)に関するガイドラインにガイドラインを1項目追加： [[MUST] 適切なDOMツリーを維持する](http://a11y-guidelines.freee.co.jp/categories/dynamic_content.html#gl-dynamic-content-maintain-dom-tree)
* その他内容の変更を伴わないガイドライン文言の変更
* 「チェック内容」と「チェック対象」を対にして表記するように変更
* チェック内容の追加と文言変更
* 「意図」について、一部内容の変更を伴わない文言変更と追記

### [Ver. 202005.1](https://github.com/freee/a11y-guidelines/releases/202005.1/) (2020年5月26日)

* [日本翻訳連盟](https://www.jtf.jp/)が公開している[JTF日本語標準スタイルガイド(翻訳用）](https://www.jtf.jp/tips/styleguide)に基づき表記揺れなど修正 ([#7](https://github.com/freee/a11y-guidelines/issues/7))
* 誤字修正

### [Ver. 202005.0](https://github.com/freee/a11y-guidelines/releases/202005.0/) (2020年5月21日、Global Accessibility Awareness Day)

参考： [freeeアクセシビリティー・ガイドラインVer. 202005.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202005.0)

* 一部文言を修正
* 色に関するガイドラインについて、色弱者に加えて視覚障害者のアクセスに影響することを「意図」に明記
* 参考情報の追加:
    - [自動的に変化するコンテンツの問題点](https://a11y-guidelines.freee.co.jp/explanations/dynamic_content-auto-updated.html)
    - [フォーム・コントロールのラベル付けの必要性](https://a11y-guidelines.freee.co.jp/explanations/form-labeling.html)
    - [色を用いた表現に関する注意点](https://a11y-guidelines.freee.co.jp/explanations/color-only.html)
    - [フォーム操作で発生する動的な変化が及ぼす影響](https://a11y-guidelines.freee.co.jp/explanations/form-dynamic-content.html)
    - [入力エラーの扱い](https://a11y-guidelines.freee.co.jp/explanations/form-errors.html)
    - [小さすぎるクリックやタッチのターゲット・サイズの問題点](https://a11y-guidelines.freee.co.jp/explanations/target-size.html#exp-target-size)
    - [画像化されたテキストの問題点](https://a11y-guidelines.freee.co.jp/explanations/images_of_text-usage.html)
    - [画像化されたテキストを使用する場合の代替情報の提供](https://a11y-guidelines.freee.co.jp/explanations/images_of_text-text-alternative.html)
    - [コントラスト比確保の重要性](https://a11y-guidelines.freee.co.jp/explanations/contrast.html)
    - [ユーザーCSSを適用したチェックの実施方法](https://a11y-guidelines.freee.co.jp/explanations/text-custom-css.html)
    - [キーボード・トラップが引き起こす問題](https://a11y-guidelines.freee.co.jp/explanations/keyboard-notrap.html)
    - [様々なユーザーの入力手段の特徴とそのサポート](https://a11y-guidelines.freee.co.jp/explanations/input_device-various.html)
    - [音声・映像コンテンツの存在を認知可能にする](https://a11y-guidelines.freee.co.jp/explanations/multimedia-perceivable.html)
    - [音声の自動再生とアクセシビリティー](https://a11y-guidelines.freee.co.jp/explanations/multimedia-autoplay.html)
    - [音声・映像コンテンツのアクセシビリティーを確保する](https://a11y-guidelines.freee.co.jp/explanations/multimedia-content-access.html)
    - [Tab/Shift+Tabキーを用いたチェック](https://a11y-guidelines.freee.co.jp/explanations/tab-order-check.html)
* 参考情報の更新:
    - [Reactコンポーネントなどのアクセシビリティー](https://a11y-guidelines.freee.co.jp/explanations/markup-component.html): AccessibleNameとroleについて加筆
* 誤字修正 ([#3](https://github.com/freee/a11y-guidelines/pull/3), [#5](https://github.com/freee/a11y-guidelines/pull/5), [#6](https://github.com/freee/a11y-guidelines/pull/6), 他)
* CSSなど修正

### [Ver. 202004.0](https://github.com/freee/a11y-guidelines/releases/202004.0/) (2020年4月30日)

参考： [freeeアクセシビリティー・ガイドラインを一般公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202004.0)

* 初版公開
