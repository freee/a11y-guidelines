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

### [Ver. 202209.1](https://github.com/freee/a11y-guidelines/releases/202209.1/) (2022年9月22日)

* NVDAの多言語処理に関する項目の推奨設定を変更：[NVDAを用いたチェックの実施方法](https://a11y-guidelines.freee.co.jp/explanations/screen-reader-check-nvda.html)
* 各ガイドラインの「チェック内容」の項と[アクセシビリティー・チェック全項目一覧](https://a11y-guidelines.freee.co.jp/checks/checklist.html)の表示を変更
* 誤字修正

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

これより前の更新履歴は、ガイドライン本文の[更新履歴の項](https://a11y-guidelines.freee.co.jp/intro/history.html)でご確認ください。
