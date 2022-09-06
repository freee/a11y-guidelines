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

編集のための環境構築や表記ルールなどについては、ガイドライン本文の[この文書の編集について](https://a11y-guidelines.freee.co.jp/intro/contributing.html)をご覧ください。

## ライセンス

![クリエイティブ・コモンズ・ライセンス](https://i.creativecommons.org/l/by/4.0/88x31.png)
「freeeアクセシビリティー・ガイドライン」は、freee株式会社が作成したもので、[クリエイティブ・コモンズ 表示 4.0 国際 ライセンス](http://creativecommons.org/licenses/by/4.0/)で提供されています。

Copyright © 2020-2021, freee株式会社

## 更新履歴

### [Ver. 202209.0](https://github.com/freee/a11y-guidelines/releases/202209.0/) (2022年9月6日)

参考： [freeeアクセシビリティー・ガイドラインVer. 202209.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202209.0)

* 各ガイドラインに「対象プラットフォーム」欄を追加
* ガイドラインの優先度の記述箇所を変更
* チェック内容の更新情報を分離して[アクセシビリティー・チェック・リスト更新履歴](https://a11y-guidelines.freee.co.jp/checks/checksheet.html#checksheet-history)として掲載するように変更
* テキスト：[テキスト表示のカスタマイズ](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-customize)の記述をWCAGが示す条件と一致するように変更し、関連する参考情報（[ユーザーCSSを適用したチェックの実施方法](https://a11y-guidelines.freee.co.jp/explanations/text-custom-css.html#exp-text-custom-css)）に掲載しているブックマークレットを修正
* モバイル・アプリケーションの観点からガイドラインとチェック内容を全体的に見直し
  - 意図の変更を伴わない文言変更：
    - マークアップと実装：[文書構造を適切に示すマークアップ、実装を行う](https://a11y-guidelines.freee.co.jp/categories/markup.html#gl-markup-semantics)（タイトルのみ）
    - ページ全体：[適切なセクション分けと見出しの付与](https://a11y-guidelines.freee.co.jp/categories/page.html#gl-page-headings)
    - 入力ディバイス：[適切なフォーカス順序](https://a11y-guidelines.freee.co.jp/categories/input_device.html#gl-input-device-focus)
    - 入力ディバイス：[ダウン・イベントをトリガーにしない](https://a11y-guidelines.freee.co.jp/categories/input_device.html#gl-input-device-use-up-event)
    - 入力ディバイス：[特定の入力ディバイスを前提としない](https://a11y-guidelines.freee.co.jp/categories/input_device.html#gl-input-device-independent)
    - アイコン：[十分な大きさのクリック/タッチのターゲット](https://a11y-guidelines.freee.co.jp/categories/icon.html#gl-icon-target-size)
    - フォーム：[十分な大きさのクリック/タッチのターゲット](https://a11y-guidelines.freee.co.jp/categories/form.html#gl-form-target-size)
    - 動的コンテンツ：[ステータス・メッセージの適切な実装](https://a11y-guidelines.freee.co.jp/categories/dynamic_content.html#gl-dynamic-content-status)
  - 追加：
    - 入力ディバイス：[モバイルの支援技術のサポート](https://a11y-guidelines.freee.co.jp/categories/input_device.html#gl-input-device-support-mobile-assistive-tech)
    - テキスト：[テキストを表示するUIコンポーネントの言語の明示](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-component-lang)
    - テキスト：[モバイルOSの文字サイズ変更機能の使用](https://a11y-guidelines.freee.co.jp/categories/text.html#gl-text-mobile-enlarge-settings)
    - アイコン：[十分な大きさのクリック/タッチのターゲット（モバイル）](https://a11y-guidelines.freee.co.jp/categories/icon.html#gl-icon-target-size-mobile)
    - フォーム：[十分な大きさのクリック/タッチのターゲット（モバイル）](https://a11y-guidelines.freee.co.jp/categories/form.html#gl-form-target-size-mobile)
* NVDAの設定に関して加筆：[NVDAを用いたチェックの実施方法](https://a11y-guidelines.freee.co.jp/explanations/screen-reader-check-nvda.html#exp-screen-reader-check-nvda)
* キーボードのみによる操作に関して加筆：[Tab/Shift+Tabキーを用いたチェック](https://a11y-guidelines.freee.co.jp/explanations/tab-order-check.html#exp-tab-order-check)

### [Ver. 202205.0](https://github.com/freee/a11y-guidelines/releases/202205.0/) (2022年5月10日)

* 誤字修正

### [Ver. 202203.0](https://github.com/freee/a11y-guidelines/releases/202203.0/) (2022年3月29日)

* 動的コンテンツ：[[MUST]適切なDOMツリーを維持する](https://a11y-guidelines.freee.co.jp/categories/dynamic_content.html#gl-dynamic-content-maintain-dom-tree)の見直し
  - モバイル・アプリケーションへの適用を前提に、タイトルを「支援技術への適切な情報提供の維持」に変更し、文言を見直し
  - WCAG 2.1の達成基準1.3.2に加えて、達成基準1.3.1との関連付けも追加
* モーダル・ダイアログに関連するチェック内容の見直し
  - [チェックID：1291](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-1291)、[チェックID：1311](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-1311) からモーダル・ダイアログに関する記述を削除
  - 新たに[チェックID：1292](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-1292)、[チェックID：1312](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-1312)、[チェックID：1313](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-1313)を追加
* チェック内容の文言見直し
  - [チェックID：0811](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0811)に例外があることを明示。
  - [チェックID：0081](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0081)の意図が明確になるように文言修正
* チェック内容の確認方法の例の見直し
  - [チェックID：0413](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0413)のiOS VoiceOverとAndroid TalkBackによる確認方法の文言修正と、NVDAによる確認方法の追加
  - [チェックID：0621](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0621)に、axe-DevToolsによる確認方法を追加
* [axe DevToolsのルールと当ガイドラインの対応](https://a11y-guidelines.freee.co.jp/info/axe-rules.html)を最新のaxe-coreのソースに基づいた内容に更新

### [Ver. 202202.0](https://github.com/freee/a11y-guidelines/releases/202202.0/) (2022年2月18日)

参考：[freeeアクセシビリティー・ガイドラインVer. 202202.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202202.0)

* 「マークアップ全般」カテゴリーを「マークアップと実装」に改名し、全体的に見直し
  - [[MUST]文書構造を適切にマークアップする](https://a11y-guidelines.freee.co.jp/categories/markup.html#gl-markup-semantics)について、スタティックなコンテンツを対象としていることが明確になるように文言を変更
  - [[MUST]対話的なUIコンポーネントの実装](https://a11y-guidelines.freee.co.jp/categories/markup.html#gl-markup-component-implementation)と[チェックID：0553](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0553)を追加
  - [[MUST]コンポーネントをアクセシブルにする](https://a11y-guidelines.freee.co.jp/categories/markup.html#gl-markup-component)の文言を変更
  - 関連して参考情報に加筆：[UIコンポーネントのアクセシビリティー](https://a11y-guidelines.freee.co.jp/explanations/markup-component.html#exp-markup-component)
* ガイドラインおよびチェック内容のYAMLのスキーマ定義を、JSON Schemaで記述して追加

### [Ver. 202201.1](https://github.com/freee/a11y-guidelines/releases/202201.1/) (2022年1月20日)

* ARIAランドマークに関するMDNの開設記事へのリンクを追加：[適切なページ構造、マークアップとスクリーン・リーダーを用いた効率的な情報アクセス](https://a11y-guidelines.freee.co.jp/explanations/page-structure.html)
* axe DevToolsを使ったARIAランドマークに関するチェックの実施方法を追加：[チェックID：0682](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0682)

### [Ver. 202201.0](https://github.com/freee/a11y-guidelines/releases/202201.0/) (2022年1月11日)

参考：[freeeアクセシビリティー・ガイドラインVer. 202201.0を公開しました](https://developers.freee.co.jp/entry/a11y-guidelines-202201.0)

* クリック/タッチのターゲット・サイズ関連の変更
  - テキスト中のリンクは対象外であることが明確になるように文言を変更： アイコン：[[SHOULD]十分な大きさのクリック/タッチのターゲット](https://a11y-guidelines.freee.co.jp/categories/icon.html#gl-icon-target-size)
  - ブラウザーのデフォルトから見た目を変更していないフォーム・コントロールは対象外であることが明確になるように文言を変更： フォーム：[[SHOULD]十分な大きさのクリック/タッチのターゲット](https://a11y-guidelines.freee.co.jp/categories/form.html#gl-form-target-size)、[クリックやタッチのターゲット・サイズに関連する問題とターゲット・サイズの確認方法](https://a11y-guidelines.freee.co.jp/explanations/target-size.html#exp-target-size)
  - チェック内容を、アイコンに対するものとフォーム・コントロールに対するものに分離：
    - 修正：[チェックID：0331](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0331)、[チェックID：0351](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0351)
    - 追加：[チェックID：0332](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0332)、[チェックID：0352](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0352)
  - 対象がデザインのチェック内容に、ターゲット領域が明示されている必要があることを明記：[チェックID：0331](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0331)、[チェックID：0332](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0332)
* ARIAランドマーク関連の変更
  - ARIAランドマークに関する確認方法を参考情報に追加：[適切なページ構造、マークアップとスクリーン・リーダーを用いた効率的な情報アクセス](https://a11y-guidelines.freee.co.jp/explanations/page-structure.html)
  - ARIAランドマークに関するチェックを追加：[チェックID：0682](https://a11y-guidelines.freee.co.jp/checks/checklist.html#check-0682)
* 対象がデザインのチェック内容について、全般的に文言を見直し
* Googleスプレッドシートにまとめて公開しているアクセシビリティー・チェック・リストのバージョン番号に関する説明を追加：[アクセシビリティー・チェック・リストのバージョン番号について](https://a11y-guidelines.freee.co.jp/checks/checksheet.html#checksheet-semver)

これより前の更新履歴は、ガイドライン本文の[更新履歴の項](https://a11y-guidelines.freee.co.jp/intro/history.html)でご確認ください。
