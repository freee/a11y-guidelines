.. _category-image:

画像
------------------------

これらのガイドラインは、画像に関するものです。
なお、すべてのガイドラインが[MUST]です。

.. _image-text-alternative:

テキスト情報の提供
~~~~~~~~~~~~~~~~~~

参考： :ref:`exp-image-text-alternative`

.. _gl-image-description:

[MUST] 画像の説明の提供
^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 画像に関する過不足のない説明をテキストで提供する。
チェック内容
   .. include:: ../checks/inc/gl-image-description.rst

.. raw:: html

   <div><details>

意図
````

視覚障害者が画像の存在を認知し、内容を理解できるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.1.1:

   *  |SC 1.1.1|
   *  |SC 1.1.1ja|

.. raw:: html

   </div></details>

.. _gl-image-decorative:

[MUST] 装飾目的の画像の無視
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 純粋な装飾目的の画像は、スクリーン・リーダーなどの支援技術が無視するようにする。
チェック内容
   .. include:: ../checks/inc/gl-image-decorative.rst

.. raw:: html

   <div><details>

意図
````

不要な情報が提示されないようにすることで、視覚障害者などの情報取得をスムースにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.1.1:

   *  |SC 1.1.1|
   *  |SC 1.1.1ja|

.. raw:: html

   </div></details>

.. _image-visual:

表示と視覚的要素
~~~~~~~~~~~~~~~~

参考： :ref:`exp-image-visual`

.. _gl-image-color-only:

[MUST] 複数の視覚的要素を用いた表現
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 特定の色に何らかの意味を持たせている場合、形状、模様など他の視覚的な要素も併せて用い、色が判別できなくてもその意味を理解できるようにする。
チェック内容
   .. include:: ../checks/inc/gl-image-color-only.rst

.. raw:: html

   <div><details>

意図
````

視覚障害者や色弱者が、コンテンツを利用できるようにする。

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

.. _gl-image-adjacent-contrast:

[MUST] 隣接領域とのコントラスト比の確保
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 画像の隣接領域の色とのコントラスト比を3:1以上にする。
チェック内容
   .. include:: ../checks/inc/gl-image-adjacent-contrast.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者が、コンテンツを利用できるようにする。

参考
````

*  :ref:`exp-contrast`
*  :ref:`exp-check-contrast`

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.4.11:

   *  |SC 1.4.11|
   *  |SC 1.4.11ja|

.. raw:: html

   </div></details>

.. _gl-image-text-contrast:

[MUST] 画像内のテキストのコントラスト比
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 画像内のテキストや、重要な情報を伝える視覚的要素の色と背景の色に、十分なコントラストを確保する。

   -  テキストの文字サイズが30px（22pt）以上の場合： 3:1以上（[SHOULD] 4.5:1以上）
   -  テキストの文字サイズが22px（18pt）以上で太字の場合： 3:1以上（[SHOULD] 4.5:1以上）
   -  その他の場合： 4.5:1以上（[SHOULD] 7:1以上）

チェック内容
   .. include:: ../checks/inc/gl-image-text-contrast.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者が、コンテンツを利用できるようにする。

参考
````

*  :ref:`exp-contrast`
*  :ref:`exp-check-contrast`

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

