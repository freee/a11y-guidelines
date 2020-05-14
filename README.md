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

Copyright © 2020, freee株式会社

## 更新履歴

### 次期リリース

* 誤字修正 ([#3](https://github.com/freee/a11y-guidelines/pull/3), [#5](https://github.com/freee/a11y-guidelines/pull/5), [#6](https://github.com/freee/a11y-guidelines/pull/6))

### [Ver. 202004.0](https://github.com/freee/a11y-guidelines/releases/202004.0/) (2020年4月30日)

* 初版公開
