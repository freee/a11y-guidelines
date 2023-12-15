.. _exp-text-lang:

###########################
``lang`` 属性と音声読み上げ
###########################

スクリーン・リーダーの中には、 ``html`` 要素やその他の要素に指定された ``lang`` 属性の値に応じて、読み上げに用いる音声合成エンジンを切り替えるものがあります。
freeeで標準環境としているNVDAでも、音声設定を調整することで、多言語の読み上げに対応した状態になります。
（ :ref:`exp-screen-reader-check` の「その他の初期設定」、「音声」の項を参照）

このようなスクリーン・リーダーでは、例えばhtml要素に ``lang="en"`` が指定されているページにアクセスすると、英語用の音声合成エンジンが利用されます。
多くの英語用の音声合成エンジンは日本語を正しく扱えませんので、もしそのページのコンテンツが主に日本語で書かれている場合には正しい読み上げが行われず、半角の英数字のみを読み上げるような状態になってしまいます。

特に ``html`` 要素の ``lang`` 属性はページ全体の処理に影響しますので、適切な値を ``lang`` 属性に指定することは重要ですが、それ以上に誤った値を指定しないことが重要です。

例えば、以下のように ``html`` 要素の ``lang`` 属性に誤った値が指定されているページは、画面表示に問題はありませんが、多言語の読み上げに対応しているスクリーン・リーダーでは適切に読み上げられません。

`lang-incorrect.html <../_static/samples/lang-incorrect.html>`_ ：

.. raw:: html

   <details><summary>コードを表示</summary>

.. include:: ../_static/samples/lang-incorrect.html
    :code: html
    :number-lines:
    :literal:

.. raw:: html

   </details>

   <iframe src="../_static/samples/lang-incorrect.html" width="100%" height="320px"></iframe>

もし主に日本語で書かれていて ``html`` 要素の ``lang`` 属性に ``ja`` が指定されているページ中に英語のテキスト情報がある場合、その部分も含めて日本語用の音声合成エンジンが用いられます。

“freee”や“Web”といった単語単位であったり、“Web Content Accessibility
Guidelines”のように数単語程度のフレーズであれば、このことが問題になることは少ないのですが、例えば1段落以上の長さに渡って ``html`` 要素の ``lang`` 属性に指定されているのとは異なる言語のテキストがあるような場合などにおいては、その言語に対応した音声合成エンジンが用いられる方が望ましいことがあります。

以下のように、引用されている英文の箇所に ``lang="en"`` を指定してある場合（12行目）、この部分と他の日本語で書かれた部分で読み上げに用いられる音声が変わります。

`lang-partial.html <../_static/samples/lang-partial.html>`_ ：

.. raw:: html

   <details><summary>コードを表示</summary>

.. include:: ../_static/samples/lang-partial.html
    :code: html
    :number-lines:
    :literal:

.. raw:: html

   </details>

   <iframe src="../_static/samples/lang-partial.html" width="100%" height="320px"></iframe>

.. include:: /inc/info2gl/exp-text-lang.rst
