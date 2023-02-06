.. _intro-contributing:

######################
この文書の編集について
######################

この文書は、GitHub上の以下のリポジトリーで管理しています：

https://github.com/freee/a11y-guidelines

内容の修正、追加、誤字脱字の修正などは、上記リポジトリーのIssuesまたはPull Requestsでお知らせください。
Pull Requestは、developブランチに対して作成してください。

ここでは、この文書の編集に関する情報をまとめて記します。

********
環境構築
********

この文書のソースを処理してHTMLファイルを生成するためには、Pythonが動作する環境が必要です。

以下の手順で、gitリポジトリーをcloneし、必要なモジュールをインストールします：

1. `git clone https://github.com/freee/a11y-guidelines`
2. `pip install --upgrade -r requirements.txt`

**********
表記ルール
**********

この文書は、原則として `日本翻訳連盟`_ が公開している `JTF日本語標準スタイルガイド(翻訳用）`_ に従って記述しています。
リポジトリーのルート・ディレクトリーの .textlintrc に、現在使用しているtextlintのルールが含まれていますが、現時点では不完全な状態です。

**************
ソース・コード
**************

この文書は、 `Sphinx`_ で処理することを前提に作成しています。

全体としてはreStructuredTextで記述していますが、ガイドラインとチェック内容についてはYAMLで記述したファイルをreStructuredTextに変換して処理しています。
`source` ディレクトリー以下のファイルはreStructuredText、 `data/yaml` ディレクトリー以下のファイルはYAMLで記述しています。

`data/json/schemas` ディレクトリー以下のファイルが、YAMLファイルのスキーマ定義です。

`tools/yaml2rst/yaml2rst.py` スクリプトを実行すると、YAMLファイルをreStructuredTextに変換し、 `source/inc` ディレクトリーに出力します。
この状態で `sphinx-build` を実行することで、文書全体を処理することができます。
なお、ルート・ディレクトリーで `make html` を実行すると、このスクリプトの実行も含めて必要な処理が実行されます。

.. _日本翻訳連盟: https://www.jtf.jp/
.. _JTF日本語標準スタイルガイド(翻訳用）: https://www.jtf.jp/tips/styleguide
.. _Sphinx: https://www.sphinx-doc.org/en/master/
