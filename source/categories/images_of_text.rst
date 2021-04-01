.. _category-images-of-text:

画像化されたテキスト
----------------------------------------

これらのガイドラインは、テキストを画像化して利用する場合を対象としています。

たとえば写真に写っている人物の名札にある名前、図中のテキスト・ラベルなど、文字情報以外の視覚的情報が、コンテンツのより重要な要素となっているようなものは、このガイドラインの対象外です。

注： WCAG 2.1では "images of text" という用語が用いられ、WCAG 2.1日本語訳では「文字画像」という訳語が当てられています。

参考： :ref:`exp-iot-usage`

.. _iot-avoid-usage:

使用の回避
~~~~~~~~~~

.. _gl-iot-avoid-usage:

[SHOULD] 画像化されたテキストを使用しない
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] 画像化されたテキストを用いないと実現できない表現が不可欠な場合（例： ロゴ）を除いて、文字情報は画像化せず、テキスト・データで提供する。
チェック内容
   .. include:: ../checks/inc/gl-iot-avoid-usage.rst

.. raw:: html

   <div><details>

意図
````

スクリーン・リーダーのユーザーかアクセスしやすい形で情報を提示する。

テキスト情報の扱いやすさを損ねない。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.5:

   *  |SC 1.4.5|
   *  |SC 1.4.5ja|

*  SC 1.4.9:

   *  |SC 1.4.9|
   *  |SC 1.4.9ja|

.. raw:: html

   </div></details>

.. _iot-usage:

画像化されたテキストを使用する場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _gl-iot-provide-text:

[MUST] テキスト情報の提供
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 画像化されたテキストに含まれる文字情報をテキストでも提供する。
チェック内容
   .. include:: ../checks/inc/gl-iot-provide-text.rst

.. raw:: html

   <div><details>

意図
````

スクリーン・リーダーのユーザーが画像化されたテキストにアクセスできるようにする。

参考
````

*  :ref:`exp-iot-text-alternative`

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.1.1:

   *  |SC 1.1.1|
   *  |SC 1.1.1ja|

.. raw:: html

   </div></details>

.. _gl-iot-adjacent-contrast:

[MUST] 隣接領域とのコントラスト比の確保
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 画像化されたテキストと隣接領域の色とのコントラスト比を3:1以上にする。
チェック内容
   .. include:: ../checks/inc/gl-iot-adjacent-contrast.rst

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

*  SC 1.4.11:

   *  |SC 1.4.11|
   *  |SC 1.4.11ja|

.. raw:: html

   </div></details>

.. _gl-iot-text-contrast:

[MUST] 画像内のテキストのコントラスト比
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 画像化されたテキストの色と背景の色に十分なコントラスト比を確保する。

   -  テキストの文字サイズが30px（22pt）以上の場合： 3:1以上（[SHOULD] 4.5:1以上）
   -  テキストの文字サイズが22px（18pt）以上で太字の場合： 3:1以上（[SHOULD] 4.5:1以上）
   -  その他の場合： 4.5:1以上（[SHOULD] 7:1以上）

チェック内容
   .. include:: ../checks/inc/gl-iot-text-contrast.rst

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
