.. _exp-markup-semantics:

############################################
セマンティクスを適切にマークアップする重要性
############################################

文書の構造を示すような情報を「セマンティクス（意味情報）」と呼びます。
見出し、段落、箇条書きとそれを構成する項目などを例として挙げることができます。

視覚的にコンテンツを利用する多くの場合において、文字のサイズやフォントの種類、レイアウトなどの視覚的情報からそのセマンティクス（意味情報）を判断します。
例えば、大きめの文字で画面上部中央に表示されているフレーズを、そのページの内容を表す見出しだと判断する、といった具合です。

ところが、スクリーン・リーダーを初めとする支援技術は、少なくとも現時点ではこのようなセマンティクスを視覚的な特徴から正確に推測することができません。
そのため支援技術は、HTMLでどのように記述されているかという情報に基づいてセマンティクスを判断しています。
上記の例の場合、見出しのテキストが ``h1`` 要素になっていれば、支援技術はそれが見出しであることを理解してユーザーに伝えることができますが、``div`` 要素や ``span`` 要素になっていてCSSで文字サイズなどが変更されているだけの場合、支援技術がそれを見出しだと判断することはできません。

支援技術、特にスクリーン・リーダーが正しいセマンティクスをユーザーに伝えられることは、より効率的なコンテンツ利用につながります。
例として、見出しジャンプ機能を用いた斜め読みを挙げることができます。

多くのスクリーン・リーダーには、複数の ``h1`` ～ ``h6`` 要素があるページにおいて、前後の見出しにジャンプして読み上げさせる機能があります。
この機能を使って見出しの拾い読みをしたり、見出しの直後のテキストだけを読んだりして、いわば斜め読みのようなことが可能になります。
スクリーン・リーダーを利用している視覚障害者の多くは、画面全体を一度に見ることができず、アクセスしたページに必要としている情報が掲載されているかどうかの判断を短時間にすることができませんので、このような手法でコンテンツを利用できることは、効率的なコンテンツ利用につながります。

支援技術が適切にコンテンツを解析し、ユーザーに伝えられるようにするために、コンテンツの内容に応じたセマンティクスを表す適切なマークアップを行うことが極めて重要です。

.. include:: /inc/info2gl/exp-markup-semantics.rst