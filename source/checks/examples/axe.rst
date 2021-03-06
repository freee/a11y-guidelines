.. _check-example-axe:

axe DevToolsを用いたチェック実施方法の例
------------------------------------------

axe DevToolsのインストールや基本的な使用方法については、 :ref:`exp-axe` を参照してください。
また、 :ref:`info-axe-rules` も合わせて参照してください。

.. _check-example-axe-0021:

:ref:`check-0021`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0021
      :end-before: .. END_check-0021

.. BEGIN_axe-0021

「 :ref:`axe-rule-color-contrast` 」という問題が出ないことを確認する。

ただし、ガイドラインを満たしていない状態であっても、以下の場合は問題として表示されませんので注意が必要です。

*  マウスホバーなどで背景色やテキスト色が変化する場合の、変化後のコントラスト比が不足する場合
*  大きいテキストのコントラスト比が3:1以上4.5:1未満の場合

   -  freeeの場合日本語テキストを想定しているため、「大きいテキスト」を30px（22pt）以上または22px（18pt）以上の太字としているが、WCAGでは欧文テキストを想定して18pt以上または14pt以上の太字としているため、その間のサイズではコントラスト不足を検知できない

*  テキスト以外のコントラスト比が不足している場合

   -  アイコン、画像、画像化されたテキスト、ボタンやフィールドの枠線など

*  半透明な要素などが重なって違う色に見えている場合の、実際に見えている色のコントラスト比が不足する場合
*  要素が重なっていて背景色と前景色の特定が難しい場合

.. END_axe-0021

.. _check-example-axe-0441:

:ref:`check-0441`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0441
      :end-before: .. END_check-0441

.. BEGIN_axe-0441

「 :ref:`axe-rule-image-alt` 」という問題が出ないことを確認する。

ただし、画像に何かしらの代替テキストが入っていれば問題として検知されないため、適切ではない代替テキストの検出をすることはできません。

.. END_axe-0441

.. _check-example-axe-0561:

:ref:`check-0561`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0561
      :end-before: .. END_check-0561

.. BEGIN_axe-0561

以下のいずれの問題も出ないことを確認する。

*  :ref:`axe-rule-empty-heading`
*  :ref:`axe-rule-heading-order`
*  :ref:`axe-rule-page-has-heading-one`

.. END_axe-0561

.. _check-example-axe-0951:

:ref:`check-0951`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0951
      :end-before: .. END_check-0951

.. BEGIN_axe-0951

「 :ref:`axe-rule-label` 」という問題が出ないことを確認する。

.. END_axe-0951
