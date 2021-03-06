.. _category-form:

フォーム
----------------------------

これらのガイドラインは、一般的な入力フォームに加え、input要素などフォーム・コントロールを利用している、一見フォームとは思えないようなコンテンツも対象としています。

.. _form-labeling:

適切なラベル付け
~~~~~~~~~~~~~~~~

参考： :ref:`exp-form-labeling`

.. _gl-form-label:

[MUST] 表示されているテキストをラベルとして用いる
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] フォーム・コントロールには、表示されているテキストをラベルとして明示的に関連付ける。
チェック内容
   .. include:: ../checks/inc/gl-form-label.rst

.. raw:: html

   <div><details>

意図
````

視覚障害者が、フォーム・コントロールの目的を容易に判断することができるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.1.1:

   *  |SC 1.1.1|
   *  |SC 1.1.1ja|

*  SC 1.3.1:

   *  |SC 1.3.1|
   *  |SC 1.3.1ja|

*  SC 2.4.6:

   *  |SC 2.4.6|
   *  |SC 2.4.6ja|

*  SC 2.5.3:

   *  |SC 2.5.3|
   *  |SC 2.5.3ja|

*  SC 3.3.2:

   *  |SC 3.3.2|
   *  |SC 3.3.2ja|

.. raw:: html

   </div></details>

.. _gl-form-hidden-label:

[MUST] 表示されているテキストをラベルにできない場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] フォーム・コントロールに対して表示されているテキストを用いたラベル付けができない場合は、非表示のテキストを用いてラベルを付ける。
チェック内容
   .. include:: ../checks/inc/gl-form-hidden-label.rst

.. raw:: html

   <div><details>

意図
````

視覚障害者が、フォーム・コントロールの目的を容易に判断することができるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 1.1.1:

   *  |SC 1.1.1|
   *  |SC 1.1.1ja|

*  SC 1.3.1:

   *  |SC 1.3.1|
   *  |SC 1.3.1ja|

*  SC 2.4.6:

   *  |SC 2.4.6|
   *  |SC 2.4.6ja|

*  SC 3.3.2:

   *  |SC 3.3.2|
   *  |SC 3.3.2ja|

.. raw:: html

   </div></details>

.. _form-color-only:

色のみによる表現を用いない
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _gl-form-color-only:

[MUST] 複数の視覚的要素を用いた表現
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 必須項目やエラー表示に際して、色に加えて他の視覚的要素も用いる。
チェック内容
   .. include:: ../checks/inc/gl-form-color-only.rst

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

*  SC 1.3.3:

   *  |SC 1.3.3|
   *  |SC 1.3.3ja|

*  SC 1.4.1:

   *  |SC 1.4.1|
   *  |SC 1.4.1ja|

.. raw:: html

   </div></details>

.. _form-timing:

制限時間
~~~~~~~~~~~~~~~~~~~~

参考： :ref:`exp-timing`

.. _gl-form-timing:

[MUST] フォームの入力に制限時間を設ける場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] フォーム入力に制限時間を設定する場合は、次に挙げる事項のうち、少なくとも1つを満たす。

   -  解除： 制限時間があるフォームを利用する前に、ユーザーがその制限時間を解除することができる。又は、
   -  調整： 制限時間があるフォームを利用する前に、ユーザーが少なくともデフォルト設定の10倍を超える、大幅な制限時間の調整をすることができる。又は、
   -  延長： 時間切れになる前にユーザーに警告し、かつ少なくとも20秒間の猶予をもって、例えば「スペースキーを押す」などの簡単な操作により、ユーザーが制限時間を10回以上延長することができる。又は、
   -  リアルタイムの例外： リアルタイムのイベント（例えば、オークション）において制限時間が必須の要素で、その制限時間に代わる手段が存在しない。又は、
   -  必要不可欠な例外： 制限時間が必要不可欠なもので、制限時間を延長することがフォームを無効にすることになる。又は、
   -  20時間の例外： 制限時間が20時間よりも長い。

チェック内容
   .. include:: ../checks/inc/gl-form-timing.rst

.. raw:: html

   <div><details>

意図
````

コンテンツの読み取りや理解に時間がかかる場合や、入力操作などに時間がかかる場合にも問題なくフォームを利用できるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 2.2.1:

   *  |SC 2.2.1|
   *  |SC 2.2.1ja|

.. raw:: html

   </div></details>

.. _gl-form-no-timing:

[SHOULD] 制限時間を設けない
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] 入力や操作に制限時間を設けない。
チェック内容
   .. include:: ../checks/inc/gl-form-no-timing.rst

.. raw:: html

   <div><details>

意図
````

コンテンツの読み取りや理解に時間がかかる場合や、入力操作などに時間がかかる場合にも問題なくフォームを利用できるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 2.2.3:

   *  |SC 2.2.3|
   *  |SC 2.2.3ja|

.. raw:: html

   </div></details>

.. _gl-form-continue:

[SHOULD] 制限時間超過後の操作の継続
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] 制限時間を超過した場合も、データを失うことなくユーザーが操作を継続できるようにする。
チェック内容
   .. include:: ../checks/inc/gl-form-continue.rst

.. raw:: html

   <div><details>

意図
````

コンテンツの読み取りや理解に時間がかかる場合や、入力操作などに時間がかかる場合にも問題なくフォームを利用できるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 2.2.5:

   *  |SC 2.2.5|
   *  |SC 2.2.5ja|

.. raw:: html

   </div></details>


.. _form-tab-order:

Tabキーによるフォーカスの移動順序
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _gl-form-tab-order:

[MUST] 適切なフォーカス順序
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] Tab/Shift+Tabキーでフォーカスを移動させたとき、コンテンツの意味に合った適切な順序でフォーカスを移動させる。
チェック内容
   .. include:: ../checks/inc/gl-form-tab-order.rst

.. raw:: html

   <div><details>

意図
````

スクリーン・リーダーなどの支援技術がコンテンツを正しく認識し、ユーザーに適切な形で提示できるようにする。

参考
````

*  :ref:`exp-tab-order-check`

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 2.4.3:

   *  |SC 2.4.3|
   *  |SC 2.4.3ja|

.. raw:: html

   </div></details>


.. _form-dynamic-content:

予期できない動的な変化の抑制
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

参考： :ref:`exp-form-dynamic-content`

.. _gl-form-dynamic-content-focus:

[MUST] フォーカス時の挙動
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] フォーカスを受け取ったときに、コンテンツの意味を変える、またはページ全体に及ぶような動的な変化を引き起こすフォーム・コントロールやコンポーネントを用いない。
チェック内容
   .. include:: ../checks/inc/gl-form-dynamic-content-focus.rst

.. raw:: html

   <div><details>

意図
````

視覚障害、認知障害があるユーザーが予期できない挙動を発生させない。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 3.2.1:

   *  |SC 3.2.1|
   *  |SC 3.2.1ja|

.. raw:: html

   </div></details>

.. _gl-form-dynamic-content-change:

[MUST] フォームの値の変更時の挙動
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 値が変更されたときに、コンテンツの意味の変更、ページ全体に及ぶような変化、他のフォーム・フィールドの値の変更などを引き起こすようなフォーム・フィールドを作らない、またはそのようなフォーム・フィールドの挙動について、事前にユーザーに知らせる。
チェック内容
   .. include:: ../checks/inc/gl-form-dynamic-content-change.rst

.. raw:: html

   <div><details>

意図
````

視覚障害、認知障害があるユーザーが予期できない挙動を発生させない。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 3.2.2:

   *  |SC 3.2.2|
   *  |SC 3.2.2ja|

.. raw:: html

   </div></details>


.. _form-errors:

エラーの扱い
~~~~~~~~~~~~

参考： :ref:`exp-form-errors`

.. _gl-form-errors-identify:

[MUST] テキスト情報によるエラーの特定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [MUST] 入力エラーがある場合、エラー箇所とエラー内容をテキストで知らせる。
チェック内容
   .. include:: ../checks/inc/gl-form-errors-identify.rst

.. raw:: html

   <div><details>

意図
````

視覚障害者、色弱者が、エラー箇所を特定できるようにする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 3.3.1:

   *  |SC 3.3.1|
   *  |SC 3.3.1ja|

.. raw:: html

   </div></details>

.. _gl-form-errors-correction:

[SHOULD] エラーの修正方法の提示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] 入力エラーがある場合に、修正方法を示す。
チェック内容
   .. include:: ../checks/inc/gl-form-errors-correction.rst

.. raw:: html

   <div><details>

意図
````

フォーム入力における認知障害者、学習障害者の困難を軽減する。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 3.3.3:

   *  |SC 3.3.3|
   *  |SC 3.3.3ja|

.. raw:: html

   </div></details>

.. _gl-form-errors-cancel:

[SHOULD] 誤操作の防止
^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] 法的行為、経済的取引、データの変更や削除を生じる機能については、取り消し、送信前の確認・修正、または送信時のエラー・チェックと修正を可能にする。
チェック内容
   .. include:: ../checks/inc/gl-form-errors-cancel.rst

.. raw:: html

   <div><details>

意図
````

誤操作による影響を少なくする。

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 3.3.4:

   *  |SC 3.3.4|
   *  |SC 3.3.4ja|

.. raw:: html

   </div></details>

.. _form-target-size:

クリック/タッチのターゲット・サイズ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _gl-form-target-size:

[SHOULD] 十分な大きさのクリック/タッチのターゲット
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ガイドライン
   [SHOULD] クリック/タッチのターゲット・サイズは充分に大きいものにする。

   -  デスクトップ向けWebでは最低24 x 24 CSS px、可能であれば44 x 44 CSS px以上
   -  モバイル向けは44 x 44 CSS px以上

チェック内容
   .. include:: ../checks/inc/gl-form-target-size.rst

.. raw:: html

   <div><details>

意図
````

ロービジョン者、細かい手の動きが難しい肢体不自由者の、誤ったクリック/タッチ操作を防ぐ。

参考
````

*  :ref:`exp-target-size`

対応するWCAG 2.1の達成基準
````````````````````````````

*  SC 2.5.5:

   *  |SC 2.5.5|
   *  |SC 2.5.5ja|

.. raw:: html

   </div></details>

