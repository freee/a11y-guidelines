.. _check-example-nvda:

NVDAを用いたチェック実施方法の例
----------------------------------

NVDAのインストール方法や基本的な使い方などについては、 :ref:`exp-screen-reader-check` を参照してください。

.. _check-example-nvda-0411:

:ref:`check-0411`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0411
      :end-before: .. END_check-0411

.. BEGIN_nvda-0411

以下の操作をしたとき、アイコンの示す状態や機能が分かる読み上げがされることを確認する。

-  ブラウズ・モードでカーソルキー操作をして当該箇所を読み上げさせたとき
-  そのアイコンがボタンやリンクなど、フォーカスを受け取るものの場合、Tab/Shift+Tabキーの操作でフォーカスされたとき

.. END_nvda-0411

.. _check-example-nvda-0441:

:ref:`check-0441`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0441
      :end-before: .. END_check-0441

.. BEGIN_nvda-0441

*  以下の操作をしたとき、画像に関する完結な読み上げがされることを確認する。
   -  ブラウズ・モードでカーソルキー操作をして当該箇所を読み上げさせたとき
   -  その画像がリンクなど、フォーカスを受け取るものの場合、Tab/Shift+Tabキーの操作でフォーカスされたとき
*  詳細な説明が必要な画像の場合、以下のいずれかを満たしている
   -  当該画像の直前または直後に詳細な説明があり、ブラウズ・モードでのカーソルキー操作で読み上げさせることができる
   -  ブラウズ・モードで次/前の画像への移動（G/Shift+Gキー）を実行して当該の画像を読み上げさせたときに、詳細な説明が読み上げられる

.. END_nvda-0441

.. _check-example-nvda-0471:

:ref:`check-0471`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0471
      :end-before: .. END_check-0471

.. BEGIN_nvda-0471

ブラウズ・モードでのカーソルキー操作で当該の画像がある箇所を通過したとき、画像の存在が分かるような読み上げがされない

.. END_nvda-0471

.. _check-example-nvda-0531:

:ref:`check-0531`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0531
      :end-before: .. END_check-0531

.. BEGIN_nvda-0531

ブラウズ・モードでのカーソルキー操作で当該の画像を読み上げさせたとき、画像に含まれるテキストと同じ内容が読み上げられる

.. END_nvda-0531

.. _check-example-nvda-0591:

:ref:`check-0591`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0591
      :end-before: .. END_check-0591

.. BEGIN_nvda-0591

以下のすべてを満たしている：

*  ブラウズ・モードでその部分を読み上げさせたとき、何らかの操作を受け付けるものであることが分かる
*  その部分で提供されているすべての機能を、最低限フォーカス・モードにおいてキーボードで操作できる
*  操作の結果表示が変わる場合、そのことが読み上げられる内容から理解できる
*  操作の結果表示が変わる場合、ブラウズ・モードで変更後の表示内容を読み上げさせて確認できる

.. END_nvda-0591

.. _check-example-nvda-0621:

:ref:`check-0621`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0621
      :end-before: .. END_check-0621

.. BEGIN_nvda-0621

1. NVDAの音声設定で、「サポートされている場合自動的に言語を切り替える」と「サポートされている場合自動的に方言を切り替える」がチェックされている状態にする。（ :ref:`exp-screen-reader-check` の「その他の初期設定」、「音声」の項を参照）
2. ブラウズ・モードで上下矢印キーを用いて読み上げさせたとき、表示されているテキストが問題なく読み上げられることを確認する。

.. END_nvda-0621

.. _check-example-nvda-0681:

:ref:`check-0681`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0681
      :end-before: .. END_check-0681

.. BEGIN_nvda-0681

以下のいずれかの方法で、本文やその画面の中心的な機能の開始位置に移動することができる。

*  ブラウズ・モードで、次/前の見出しへの移動（H/Shift+Hキー）を実行して、容易に本文直前の見出しに移動できる
*  ブラウズ・モードで、次のランドマークへの移動（Dキー）でmain要素の先頭部分に容易に移動でき、その直後から本文が始まっている

.. END_nvda-0681

.. _check-example-nvda-0711:

:ref:`check-0711`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0711
      :end-before: .. END_check-0711

.. BEGIN_nvda-0711

ブラウズ・モードでページ先頭からカーソルキー操作で読み上げさせたとき、自然な、意味の理解を阻害しない順序で読み上げられる

.. END_nvda-0711

.. _check-example-nvda-0741:

:ref:`check-0741`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0741
      :end-before: .. END_check-0741

.. BEGIN_nvda-0741

以下の手順で見出しリストを表示して、ページ中の見出しが過不足なく表示されていることを確認する

1. ブラウズ・モードで要素リストを表示（ :kbd:`NVDA+F7` ）
2. 「種別」を「見出し」に設定（ :kbd:`Alt+H` ）

.. END_nvda-0741

.. _check-example-nvda-0861:

:ref:`check-0861`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0861
      :end-before: .. END_check-0861

.. BEGIN_nvda-0861

ブラウズ・モードでのカーソルキー操作による読み上げで、パンくずリストやグローバル・ナビゲーションの中で現在表示中のページを表す箇所を読み上げたとき、「現在のページ」というような発声がある

.. END_nvda-0861

.. _check-example-nvda-0921:

:ref:`check-0921`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-0921
      :end-before: .. END_check-0921

.. BEGIN_nvda-0921

1. NVDAの音声設定で、「サポートされている場合自動的に言語を切り替える」と「サポートされている場合自動的に方言を切り替える」がチェックされている状態にする。（ :ref:`exp-screen-reader-check` の「その他の初期設定」、「音声」の項を参照）
2. ブラウズ・モードで上下矢印キーを用いて読み上げさせたとき、使用されている言語に応じて読み上げに用いられる音声が切り替わることを確認する。

.. END_nvda-0921

.. _check-example-nvda-1191:

:ref:`check-1191`
~~~~~~~~~~~~~~~~~

   .. include:: /checks/inc/allchecks.rst
      :start-after: .. BEGIN_check-1191
      :end-before: .. END_check-1191

.. BEGIN_nvda-1191

設計資料に従ってステータス・メッセージが表示される操作を行い、ステータス・メッセージが自動的に読み上げられることを確認する。

参考： 期待される挙動を確認する場合は、 :ref:`exp-dynamic-content-status` に示した実装例を参照

.. END_nvda-1191
