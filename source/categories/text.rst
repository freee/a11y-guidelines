.. _category-text:

テキスト
----------------------------

これらのガイドラインは、テキスト情報に関するものです。テキスト情報とは、大ざっぱにいえば文字情報ですが、文字情報を画像化して表示するものはこれらのガイドラインの対象ではありません。これについては、「画像化されたテキストに関するガイドライン」を参照してください。

.. _text-wording:

文言と表現
~~~~~~~~~~

参考： :ref:`exp-text-wording`

.. _gl-text-multiple-modality:

[MUST] 特定の感覚に依存しない表現
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 特定の感覚だけを前提とした表現を用いない。
チェック内容
   .. include:: ../checks/inc/gl-text-multiple-modality.rst

.. raw:: html

   <div><details>

意図
````

視覚障害者、色弱者がコンテンツを利用できるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.3.3:

   *  |SC 1.3.3|
   *  |SC 1.3.3ja|

例
``

.. include:: ../checks/inc/0032-example.rst

.. raw:: html

   </div></details>

.. _gl-text-color-only:

[MUST] 複数の視覚的要素を用いた表現
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 強調、引用など、何らかの意図を文字色を変えることによって表現している場合、書体など他の視覚的な要素も併せて用い、色が判別できなくてもその意味を理解できるようにする。
チェック内容
   .. include:: ../checks/inc/gl-text-color-only.rst

.. raw:: html

   <div><details>

意図
````

視覚障害者や色弱者がコンテンツを利用できるようにする。

参考
````

*  :ref:`exp-color-only`
*  :ref:`exp-grayscale`

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.1:

   *  |SC 1.4.1|
   *  |SC 1.4.1ja|

.. raw:: html

   </div></details>

.. _gl-text-heading-label:

[MUST] 適切な文言の見出し
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 主題又は目的を説明する見出しを付ける。
チェック内容
   .. include:: ../checks/inc/gl-text-heading-label.rst

.. raw:: html

   <div><details>

意図
````

視覚障害者が、ページ内で目的のコンテンツを見つけやすくする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 2.4.6:

   *  |SC 2.4.6|
   *  |SC 2.4.6ja|

.. raw:: html

   </div></details>

.. _text-lang:

自然言語
~~~~~~~~~~~~

参考： :ref:`exp-text-lang`

.. _gl-text-page-lang:

[MUST] ページの主たる言語の指定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] html要素に適切にlang属性を指定する。
チェック内容
   .. include:: ../checks/inc/gl-text-page-lang.rst

.. raw:: html

   <div><details>

意図
````

音声/点字出力などが適切に行われるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 3.1.1:

   *  |SC 3.1.1|
   *  |SC 3.1.1ja|

.. raw:: html

   </div></details>

.. _gl-text-phrase-lang:

[SHOULD] 部分的に使用される言語の明示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] 段落単位など、比較的長いテキストの言語がhtml要素のlang属性で指定したものと異なる場合は、その部分に対して適切にlang属性を指定する。
チェック内容
   .. include:: ../checks/inc/gl-text-phrase-lang.rst

.. raw:: html

   <div><details>

意図
````

音声/点字出力などが適切に行われるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 3.1.2:

   *  |SC 3.1.2|
   *  |SC 3.1.2ja|

.. raw:: html

   </div></details>

.. _text-magnification:

テキスト表示の拡大
~~~~~~~~~~~~~~~~~~~~

参考： :ref:`exp-magnification`

.. _gl-text-zoom:

[MUST] ズーム機能を用いた200パーセントの拡大表示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] コンテンツや機能を損なうことなく、ブラウザーのズーム機能で200パーセントまで拡大できるようにする。
チェック内容
   .. include:: ../checks/inc/gl-text-zoom.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者が、問題なくコンテンツを利用できるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.4:

   *  |SC 1.4.4|
   *  |SC 1.4.4ja|

.. raw:: html

   </div></details>

.. _gl-text-enlarge-settings:

[MUST] 文字サイズ変更機能の使用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] コンテンツや機能を損なうことなく、ブラウザーの文字サイズ変更機能で200パーセントの拡大表示をする設定ができるようにする。
チェック内容
   .. include:: ../checks/inc/gl-text-enlarge-settings.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者が、ズーム機能ではなく文字サイズ変更機能で拡大表示を行う設定をした際、実際に拡大表示が行われるかどうかにかかわらず、表示が崩れるなど、コンテンツの利用に支障がでることがないようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.4:

   *  |SC 1.4.4|
   *  |SC 1.4.4ja|

.. raw:: html

   </div></details>

.. _gl-text-enable-enlarge:

[SHOULD] 文字サイズ変更機能による200パーセントの拡大表示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] ブラウザーの文字サイズ変更機能で200パーセントの拡大表示をできるようにする。
チェック内容
   .. include:: ../checks/inc/gl-text-enable-enlarge.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者が、ズーム機能ではなく文字サイズ変更機能で拡大表示をできるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.4:

   *  |SC 1.4.4|
   *  |SC 1.4.4ja|

.. raw:: html

   </div></details>

.. _gl-text-zoom-reflow:

[SHOULD] 400パーセントの拡大表示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] 400パーセントの拡大表示をしたときでも、横書きのコンテンツのように縦スクロールを前提としたコンテンツては横スクロールが、縦書きのコンテンツのように横スクロールを前提としたコンテンツでは縦スクロールが必要にならないようにする。
チェック内容
   .. include:: ../checks/inc/gl-text-zoom-reflow.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者が、ズーム機能で拡大表示しても問題なくコンテンツを利用できるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.10:

   *  |SC 1.4.10|
   *  |SC 1.4.10ja|

.. raw:: html

   </div></details>

.. _text-display:

テキストの表示
~~~~~~~~~~~~~~~~

.. _gl-text-customize:

[MUST] テキスト表示のカスタマイズ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] ユーザーがline-heightを1.5em以上、段落間の空白を2em以上、letter-spacingを0.12em以上に変更し、その他のプロパティーを一切変更していない状況において、コンテンツおよび機能に損失が生じないようにする。
チェック内容
   .. include:: ../checks/inc/gl-text-customize.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者が、問題なくコンテンツを利用できるようにする。

参考
````

*  :ref:`exp-text-custom-css`

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.12:

   *  |SC 1.4.12|
   *  |SC 1.4.12ja|

.. raw:: html

   </div></details>

.. _gl-text-contrast:

[MUST] コントラスト比の確保
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 文字色と背景色に十分なコントラストを確保する。

   -  テキストの文字サイズが30px（22pt）以上の場合： 3:1以上（[SHOULD] 4.5:1以上）
   -  テキストの文字サイズが22px（18pt）以上で太字の場合： 3:1以上（[SHOULD] 4.5:1以上）
   -  その他の場合： 4.5:1以上（[SHOULD] 7:1以上）

チェック内容
   .. include:: ../checks/inc/gl-text-contrast.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者が、コンテンツを利用できるようにする。

参考
````

*  :ref:`exp-contrast`
*  :ref:`exp-check-contrast`
*  |Vibes Color Contrast|

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.3:

   *  |SC 1.4.3|
   *  |SC 1.4.3ja|

*  SC 1.4.6:

   *  |SC 1.4.6|
   *  |SC 1.4.6ja|

.. raw:: html

   </div></details>
