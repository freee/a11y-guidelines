
.. _check-0001:

チェックID: 0001
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0001

充分なコントラスト比 ([MUST]3:1以上、[SHOULD]4.5:1以上) が確保されている。

*  アイコンと背景色
*  画像化されたテキスト、その他の画像内のテキストや重要な情報と背景色
*  画像および画像化されたテキストとその隣接領域
*  テキストと背景色

.. END_check-0001

対象
   デザイン
関連ガイドライン
   *  アイコン： :ref:`gl-icon-contrast`
   *  画像： :ref:`gl-image-adjacent-contrast`
   *  画像： :ref:`gl-image-text-contrast`
   *  画像化されたテキスト： :ref:`gl-iot-adjacent-contrast`
   *  画像化されたテキスト： :ref:`gl-iot-text-contrast`
   *  テキスト： :ref:`gl-text-contrast`
参考情報
   *  :ref:`exp-check-contrast`
   *  :ref:`exp-contrast`


.. _check-0021:

チェックID: 0021
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0021

充分なコントラスト比 ([MUST]3:1以上、[SHOULD]4.5:1以上) が確保されている。

*  アイコンと背景色
*  画像化されたテキスト、その他の画像内のテキストや重要な情報と背景色
*  画像および画像化されたテキストとその隣接領域
*  テキストと背景色

.. END_check-0021

対象
   プロダクト
関連ガイドライン
   *  アイコン： :ref:`gl-icon-contrast`
   *  画像： :ref:`gl-image-adjacent-contrast`
   *  画像： :ref:`gl-image-text-contrast`
   *  画像化されたテキスト： :ref:`gl-iot-adjacent-contrast`
   *  画像化されたテキスト： :ref:`gl-iot-text-contrast`
   *  テキスト： :ref:`gl-text-contrast`
参考情報
   *  :ref:`exp-check-contrast`
   *  :ref:`exp-contrast`


axeを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/axe.rst
   :start-after: .. BEGIN_axe-0021
   :end-before: .. END_axe-0021

.. _check-0031:

チェックID: 0031
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0031

グレイスケール表示でも利用に支障が出ない:

*  リンク箇所を判別できる
*  画像、テキストの意図が伝わる
*  入力フォームの必須項目、エラーを認知できる

.. END_check-0031

対象
   デザイン
関連ガイドライン
   *  リンク： :ref:`gl-link-color-only`
   *  画像： :ref:`gl-image-color-only`
   *  テキスト： :ref:`gl-text-color-only`
   *  フォーム： :ref:`gl-form-color-only`
参考情報
   *  :ref:`exp-grayscale`


.. _check-0032:

チェックID: 0032
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0032

形状、色、大きさ、視覚的な位置、方向、音などが分からないと理解できないような説明をしていない。

例：

避けるべき表現
   *  赤字の項目は必須項目です
   *  右の表を参照してください
   *  青いボタンを押してください
問題のない表現
   *  赤い※印のついた項目は必須項目です
   *  右の表（表3）を参照してください
   *  青い「保存」ボタンを押してください

.. END_check-0032

対象
   デザイン
関連ガイドライン
   *  テキスト： :ref:`gl-text-multiple-modality`
参考情報
   *  :ref:`exp-color-only`


.. _check-0051:

チェックID: 0051
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0051

グレイスケール表示でも利用に支障が出ない:

*  リンク箇所を判別できる
*  画像、テキストの意図が伝わる
*  入力フォームの必須項目、エラーを認知できる

.. END_check-0051

対象
   プロダクト
関連ガイドライン
   *  リンク： :ref:`gl-link-color-only`
   *  画像： :ref:`gl-image-color-only`
   *  テキスト： :ref:`gl-text-color-only`
   *  フォーム： :ref:`gl-form-color-only`
参考情報
   *  :ref:`exp-grayscale`


.. _check-0071:

チェックID: 0071
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0071

マウス・ボタンのdownイベントをトリガーにしていない。

.. END_check-0071

対象
   コード
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-use-up-event`
参考情報
   *  :ref:`exp-input-device-various`


.. _check-0081:

チェックID: 0081
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0081

マウス・クリックを受け付けるリンクやボタンなどは、マウス・ボタンを押下した状態でマウス・ポインターを外し、マウス・ボタンを放した場合、その機能が実行されない。（ドラッグ&ドロップは対象外）

.. END_check-0081

対象
   プロダクト
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-use-up-event`
参考情報
   *  :ref:`exp-input-device-various`


.. _check-0091:

チェックID: 0091
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0091

ホバーで表示されるすべてのコンテンツは、以下のすべてを満たす設計になっている:

*  ポインターを移動させることなく、ホバーで表示されたコンテンツを非表示にできる。（ESCキーで消える、など）
*  ポインターを、ホバーで表示されたコンテンツ上に移動しても、コンテンツが消えない。
*  ホバー状態ではなくなった場合、ユーザーが非表示にする操作を行った場合、内容が無効になった場合にのみ、ホバーで表示されたコンテンツを非表示にする。

.. END_check-0091

対象
   デザイン
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-hover`
参考情報
   *  :ref:`exp-dynamic-content-hover`


.. _check-0111:

チェックID: 0111
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0111

ホバーで表示されるすべてのコンテンツは、以下のすべてを満たしている:

*  ポインターを移動させることなく、ホバーで表示されたコンテンツを非表示にできる。（ESCキーで消える、など）
*  ポインターを、ホバーで表示されたコンテンツ上に移動しても、コンテンツが消えない。
*  ホバー状態ではなくなった場合、ユーザーが非表示にする操作を行った場合、内容が無効になった場合にのみ、ホバーで表示されたコンテンツを非表示にする。

.. END_check-0111

対象
   プロダクト
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-hover`
参考情報
   *  :ref:`exp-dynamic-content-hover`


.. _check-0141:

チェックID: 0141
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0141

ショートカットキーを提供していて、それが画面のどこにフォーカスがあっても作動する仕様である場合、以下のいずれかを満たしている：

*  ユーザーがショートカットキーを無効にできる
*  ユーザーがショートカットキーの割当を変更できる

.. END_check-0141

対象
   プロダクト
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-shortcut-keys`
参考情報
   *  :ref:`exp-input-device-various`


.. _check-0151:

チェックID: 0151
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0151

デフォルトのフォーカス・インジケーターを用いない場合、代替となるフォーカス・インジケーターを設計資料で明示している。

.. END_check-0151

対象
   デザイン
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-focus-indicator`
参考情報
   *  :ref:`exp-tab-order-check`


.. _check-0152:

チェックID: 0152
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0152

Tab/Shift+Tabキーでフォーカスを移動しているときに、以下のような変化を発生させる機能が設計資料にない：

*  フォームの送信
*  レイアウトの変更
*  ページの遷移
*  モーダル・ダイアログの表示
*  表示内容の大幅な変更、など

.. END_check-0152

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-dynamic-content-focus`
   *  動的コンテンツ： :ref:`gl-dynamic-content-focus`
参考情報
   *  :ref:`exp-tab-order-check`
   *  :ref:`exp-form-dynamic-content`


.. _check-0171:

チェックID: 0171
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0171

Tab/Shift+Tabキーによるフォーカス移動時の挙動は以下のすべてを満たしている：

*  フォーカス・インジケーターまたはそれを代替する表示がある
*  自動的に次のような挙動が発生しない：

   -  フォームの送信
   -  レイアウトの変更
   -  ページの遷移
   -  モーダル・ダイアログの表示
   -  表示内容の大幅な変更など

.. END_check-0171

対象
   プロダクト
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-focus-indicator`
   *  フォーム： :ref:`gl-form-dynamic-content-focus`
   *  動的コンテンツ： :ref:`gl-dynamic-content-focus`
参考情報
   *  :ref:`exp-tab-order-check`
   *  :ref:`exp-form-dynamic-content`


.. _check-0172:

チェックID: 0172
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0172

Tab/Shift+Tabキーを使ったフォーカスの移動時、文脈、レイアウト、操作手順に即した自然な順序でフォーカスが移動する。

*  リンクとボタン
*  フォーム・コントロール
*  その他、マウスやキーボードによる操作を受け付けるすべてのもの

.. END_check-0172

対象
   プロダクト
関連ガイドライン
   *  リンク： :ref:`gl-link-tab-order`
   *  入力ディバイス： :ref:`gl-input-device-focus`
   *  入力ディバイス： :ref:`gl-input-device-keyboard-operable`
   *  フォーム： :ref:`gl-form-tab-order`
参考情報
   *  :ref:`exp-tab-order-check`
   *  :ref:`exp-input-device-various`


.. _check-0201:

チェックID: 0201
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0201

動画プレイヤーのような、何らかの機能を提供するためにページ中に埋め込まれているプログラムなどにフォーカスがある状態のとき、Tab, Shift+Tab, 矢印キー、ESCキーのいずれかの操作で、埋め込まれているものの外の領域にあるリンクなどにフォーカスを移動することができ、自動的にフォーカスが元の位置に戻されない。

.. END_check-0201

対象
   プロダクト
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-no-trap`
   *  音声・映像コンテンツ： :ref:`gl-multimedia-no-trap`
参考情報
   *  :ref:`exp-keyboard-notrap`


.. _check-0211:

チェックID: 0211
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0211

クリックやホバーなどのマウス操作を受け付けるものは、キーボードのみでも操作できるように設計されている。

.. END_check-0211

対象
   デザイン
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-keyboard-operable`
参考情報
   *  :ref:`exp-input-device-various`


.. _check-0231:

チェックID: 0231
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0231

クリックやホバーなどのマウス操作を受け付けるものは、キーボードのみでも操作できる。

.. END_check-0231

対象
   プロダクト
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-keyboard-operable`
参考情報
   *  :ref:`exp-input-device-various`


.. _check-0241:

チェックID: 0241
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0241

リンク・テキストは「こちら」などになっておらず、リンク・テキストの文言から遷移先をある程度推測できるようになっている。

.. END_check-0241

対象
   デザイン
関連ガイドライン
   *  リンク： :ref:`gl-link-text`

.. _check-0242:

チェックID: 0242
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0242

同じ文脈において、遷移先が同じリンク、目的が同じボタンには、一貫したテキストやアイコンが使われている。

.. END_check-0242

対象
   デザイン
関連ガイドライン
   *  リンク： :ref:`gl-link-consistent-text`
   *  アイコン： :ref:`gl-icon-consistent`

.. _check-0261:

チェックID: 0261
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0261

*  「○○はこちら」の「こちら」の部分だけがリンクになっていない。（この場合は「○○はこちら」全体をリンクにする。）、または
*  リンク・テキストの意図がマークアップで明確になっている。

.. END_check-0261

対象
   プロダクト
関連ガイドライン
   *  リンク： :ref:`gl-link-text`

.. _check-0262:

チェックID: 0262
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0262

同じ文脈において、遷移先が同じリンク、目的が同じボタンには、一貫したテキストやアイコンが使われている。

.. END_check-0262

対象
   プロダクト
関連ガイドライン
   *  リンク： :ref:`gl-link-consistent-text`
   *  アイコン： :ref:`gl-icon-consistent`

.. _check-0271:

チェックID: 0271
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0271

見出しのテキストは、内容を適切に示す文言になっている。

.. END_check-0271

対象
   デザイン
関連ガイドライン
   *  テキスト： :ref:`gl-text-heading-label`
参考情報
   *  :ref:`exp-text-wording`


.. _check-0311:

チェックID: 0311
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0311

文字サイズの指定において、絶対値指定（例：px）と相対値指定（例：rem）が混在していない。

.. END_check-0311

対象
   コード
関連ガイドライン
   *  テキスト： :ref:`gl-text-enlarge-settings`
参考情報
   *  :ref:`exp-magnification`


.. _check-0321:

チェックID: 0321
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0321

ブラウザーのズーム機能で200パーセントまで拡大しても、テキストの理解を妨げるようなレイアウト崩れが起こらない。

.. END_check-0321

対象
   プロダクト
関連ガイドライン
   *  テキスト： :ref:`gl-text-zoom`
参考情報
   *  :ref:`exp-magnification`


.. _check-0322:

チェックID: 0322
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0322

1280x1024のサイズのウィンドウにおいて400パーセントの拡大表示をしたときに適切にリフローされ

*  縦書きのコンテンツでは縦スクロールが、横書きのコンテンツでは横スクロールが発声しない、かつ
*  読み取れない内容や利用できない機能がない

.. END_check-0322

対象
   プロダクト
関連ガイドライン
   *  テキスト： :ref:`gl-text-zoom-reflow`
参考情報
   *  :ref:`exp-magnification`


.. _check-0323:

チェックID: 0323
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0323

ブラウザーの文字サイズ変更機能で200パーセントの拡大表示をする設定をしても、テキストの理解を妨げるようなレイアウト崩れが起こらない。

.. END_check-0323

対象
   プロダクト
関連ガイドライン
   *  テキスト： :ref:`gl-text-enlarge-settings`
参考情報
   *  :ref:`exp-magnification`


.. _check-0324:

チェックID: 0324
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0324

ブラウザーの文字サイズ変更機能で200パーセントまで拡大することができ、その際テキストの理解を妨げるようなレイアウト崩れが起こらない。

.. END_check-0324

対象
   プロダクト
関連ガイドライン
   *  テキスト： :ref:`gl-text-enable-enlarge`
参考情報
   *  :ref:`exp-magnification`


.. _check-0331:

チェックID: 0331
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0331

ボタンなどのサイズが、デスクトップWebでは少なくとも24 x 24、なるべく44 x 44 CSS px、モバイルでは44 x 44 CSS px以上になっていることを確認している。

.. END_check-0331

対象
   デザイン
関連ガイドライン
   *  アイコン： :ref:`gl-icon-target-size`
   *  フォーム： :ref:`gl-form-target-size`
参考情報
   *  :ref:`exp-target-size`


.. _check-0351:

チェックID: 0351
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0351

ボタンなどのサイズが、デスクトップWebでは少なくとも24 x 24、なるべく44 x 44 CSS px、モバイルでは44 x 44 CSS px以上になっていることを確認している。

.. END_check-0351

対象
   プロダクト
関連ガイドライン
   *  アイコン： :ref:`gl-icon-target-size`
   *  フォーム： :ref:`gl-form-target-size`
参考情報
   *  :ref:`exp-target-size`


.. _check-0361:

チェックID: 0361
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0361

以下のような機能が設計資料に存在しない：

*  特定の入力ディバイスで発生するイベントのみをトリガーにした機能
*  使用できる入力ディバイスを、特定の時点で検出されたものに限定している機能

.. END_check-0361

対象
   デザイン
関連ガイドライン
   *  入力ディバイス： :ref:`gl-input-device-independent`
参考情報
   *  :ref:`exp-input-device-various`


.. _check-0391:

チェックID: 0391
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0391

*  アイコンには、その役割や示している状態を表すテキスト・ラベルが併せて表示されている。または
*  テキスト・ラベルを表示できない場合、色の違いだけでアイコンの意味の違いを表さず、形状（モチーフ）やサイズでも違いを示している。かつ
*  役割や意味がわかる alt 属性の値を設計資料で明示している。

.. END_check-0391

対象
   デザイン
関連ガイドライン
   *  アイコン： :ref:`gl-icon-visible-label`
   *  アイコン： :ref:`gl-icon-color-only`

.. _check-0401:

チェックID: 0401
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0401

*  アイコンの役割や示している状態を表すテキストが表示されていて、 ``aria-labelledby`` 属性で関連付けられている。または
*  ``alt`` 属性または ``aria-label`` 属性で、そのようなテキストが指定されている。
*  開発者ツールで確認すると、Accessible Nameに適切なテキストが設定されている状態になっている。

.. END_check-0401

対象
   コード
関連ガイドライン
   *  アイコン： :ref:`gl-icon-visible-label`

.. _check-0411:

チェックID: 0411
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0411

アイコンの役割や示している状態が分かるテキストが、スクリーン・リーダーで読み上げられる。

.. END_check-0411

対象
   プロダクト
関連ガイドライン
   *  アイコン： :ref:`gl-icon-visible-label`

NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0411
   :end-before: .. END_nvda-0411

.. _check-0412:

チェックID: 0412
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0412

テキストのラベルが併せて表示されていないアイコンで、形状とサイズが同じで色だけが違うものがない。（例：異なる状態を表す複数のアイコンが、色の違いだけで状態の違いを表していない。）

.. END_check-0412

対象
   プロダクト
関連ガイドライン
   *  アイコン： :ref:`gl-icon-color-only`

.. _check-0421:

チェックID: 0421
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0421

*  画像に関する簡潔で過不足ない説明（ ``alt`` 属性値）が、設計資料で明示されている。かつ
*  短いテキストでは充分に説明できない場合には、詳細な説明のテキストが設計資料で明示されている。

.. END_check-0421

対象
   デザイン
関連ガイドライン
   *  画像： :ref:`gl-image-description`
参考情報
   *  :ref:`exp-image-text-alternative`


.. _check-0431:

チェックID: 0431
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0431

*  画像に関する簡潔で過不足ない説明が ``alt`` 属性や ``aria-label`` 属性で付加されている。かつ
*  詳細な説明が必要な場合には、その説明が当該の画像の直前または直後に表示されている、または ``aria-describedby`` 属性で関連付けられている。

.. END_check-0431

対象
   コード
関連ガイドライン
   *  画像： :ref:`gl-image-description`
参考情報
   *  :ref:`exp-image-text-alternative`


.. _check-0441:

チェックID: 0441
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0441

画像の説明が適切に読み上げられる。

.. END_check-0441

対象
   プロダクト
関連ガイドライン
   *  画像： :ref:`gl-image-description`
参考情報
   *  :ref:`exp-image-text-alternative`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0441
   :end-before: .. END_nvda-0441

axeを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/axe.rst
   :start-after: .. BEGIN_axe-0441
   :end-before: .. END_axe-0441

.. _check-0451:

チェックID: 0451
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0451

情報や機能性を一切持たない画像は、説明のテキストを付加してはならないことが設計資料で明示されている。

.. END_check-0451

対象
   デザイン
関連ガイドライン
   *  画像： :ref:`gl-image-decorative`
参考情報
   *  :ref:`exp-image-text-alternative`


.. _check-0461:

チェックID: 0461
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0461

情報や機能性を一切持たない画像には、空の ``alt`` 属性（ ``alt=""`` ）や ``role="presentation"`` が付与されていて、スクリーン・リーダーで読み上げられない。

.. END_check-0461

対象
   コード
関連ガイドライン
   *  画像： :ref:`gl-image-decorative`
参考情報
   *  :ref:`exp-image-text-alternative`


.. _check-0471:

チェックID: 0471
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0471

情報や機能性を一切持たない画像は、スクリーン・リーダーで読み上げられない。

.. END_check-0471

対象
   プロダクト
関連ガイドライン
   *  画像： :ref:`gl-image-decorative`
参考情報
   *  :ref:`exp-image-text-alternative`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0471
   :end-before: .. END_nvda-0471

.. _check-0481:

チェックID: 0481
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0481

画像化されたテキストを用いて実装する対象として、自社および他者のロゴ、バナー、図や写真の中の文字列以外のものが設計資料中に存在しない。

.. END_check-0481

対象
   デザイン
関連ガイドライン
   *  画像化されたテキスト： :ref:`gl-iot-avoid-usage`
参考情報
   *  :ref:`exp-iot-usage`


.. _check-0501:

チェックID: 0501
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0501

自社および他者のロゴ、バナー、図や写真の中の文字列を除いて、画像化されたテキストがない。

.. END_check-0501

対象
   プロダクト
関連ガイドライン
   *  画像化されたテキスト： :ref:`gl-iot-avoid-usage`
参考情報
   *  :ref:`exp-iot-usage`


.. _check-0521:

チェックID: 0521
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0521

画像化されているテキストと同じ内容が ``alt`` 属性または ``aria-label`` 属性で示されていて、スクリーン・リーダーなとで確認できる。

.. END_check-0521

対象
   コード
関連ガイドライン
   *  画像化されたテキスト： :ref:`gl-iot-provide-text`
参考情報
   *  :ref:`exp-iot-usage`


.. _check-0531:

チェックID: 0531
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0531

画像化されているテキストと同じ内容がスクリーン・リーダーなとで確認できる。

.. END_check-0531

対象
   プロダクト
関連ガイドライン
   *  画像化されたテキスト： :ref:`gl-iot-provide-text`
参考情報
   *  :ref:`exp-iot-text-alternative`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0531
   :end-before: .. END_nvda-0531

.. _check-0541:

チェックID: 0541
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0541

見出し（ ``h1`` ～ ``h6`` ）、箇条書き（ ``ul``, ``ol``, ``dl`` ）、表（ ``table`` ）など、HTMLのセマンティクスで表現できるものがそれらで表現されるよう、設計資料で明示されている。

.. END_check-0541

対象
   デザイン
関連ガイドライン
   *  マークアップ全般： :ref:`gl-markup-semantics`

.. _check-0551:

チェックID: 0551
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0551

見出し（ ``h1`` ～ ``h6`` ）、箇条書き（ ``ul``, ``ol``, ``dl`` ）、表（ ``table`` ）などを用いてセマンティクスが適切にマークアップされている。

.. END_check-0551

対象
   コード
関連ガイドライン
   *  マークアップ全般： :ref:`gl-markup-semantics`

.. _check-0571:

チェックID: 0571
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0571

validatorやlinterでチェックが通る。

.. END_check-0571

対象
   コード
関連ガイドライン
   *  マークアップ全般： :ref:`gl-markup-valid`
参考情報
   *  :ref:`exp-check-tools`


.. _check-0591:

チェックID: 0591
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0591

静的なテキストではない部分（例：開閉するメニュー、タブ・パネル、日付選択UI）も、スクリーン・リーダーで問題なく操作できる。

.. END_check-0591

対象
   プロダクト
関連ガイドライン
   *  マークアップ全般： :ref:`gl-markup-component`
参考情報
   *  :ref:`exp-markup-component`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0591
   :end-before: .. END_nvda-0591

.. _check-0611:

チェックID: 0611
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0611

日本語のページには、 ``<html lang="ja">`` の記述がある。

.. END_check-0611

対象
   コード
関連ガイドライン
   *  テキスト： :ref:`gl-text-page-lang`
参考情報
   *  :ref:`exp-text-lang`


.. _check-0621:

チェックID: 0621
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0621

多言語対応している読み上げ環境を用いて読み上げさせたとき、適切な言語の音声エンジンで読み上げられる。

.. END_check-0621

対象
   プロダクト
関連ガイドライン
   *  テキスト： :ref:`gl-text-page-lang`
参考情報
   *  :ref:`exp-text-lang`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0621
   :end-before: .. END_nvda-0621

.. _check-0631:

チェックID: 0631
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0631

そのページの目的を示し、かつ他のページとは異なる ページ・タイトル（ ``title`` 要素）が設計資料で定義されている。

.. END_check-0631

対象
   デザイン
関連ガイドライン
   *  ページ全体： :ref:`gl-page-title`
参考情報
   *  :ref:`exp-page-structure`


.. _check-0651:

チェックID: 0651
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0651

そのページの目的を示し、かつ他のページとは異なるページ・タイトルが付けられている。（ブラウザーのタイトルバー/タブバーに表示されている。）

.. END_check-0651

対象
   プロダクト
関連ガイドライン
   *  ページ全体： :ref:`gl-page-title`
参考情報
   *  :ref:`exp-page-structure`


.. _check-0661:

チェックID: 0661
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0661

ページのどの部分がそれぞれ ``header``, ``nav``, ``main``, ``footer`` 要素でマークアップされるべきかが、複数のページで一貫した形で設計資料に明示されている。

.. END_check-0661

対象
   デザイン
関連ガイドライン
   *  ページ全体： :ref:`gl-page-landmark`
   *  ページ全体： :ref:`gl-page-consistent-navigation`
参考情報
   *  :ref:`exp-page-structure`


.. _check-0671:

チェックID: 0671
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0671

*  ``header``, ``main``, ``nav``, ``footer`` の各要素が適切に用いられている。または
*  これらが ``role`` 属性で明示されている。

.. END_check-0671

対象
   コード
関連ガイドライン
   *  ページ全体： :ref:`gl-page-landmark`
参考情報
   *  :ref:`exp-page-structure`


.. _check-0672:

チェックID: 0672
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0672

*  ``main`` 要素が本文の開始位置を反映している。または
*  本文の先頭部分に ``h1`` 要素や ``h2`` 要素でマークアップされた見出しがある。

.. END_check-0672

対象
   コード
関連ガイドライン
   *  ページ全体： :ref:`gl-page-markup-main`
参考情報
   *  :ref:`exp-page-structure`


.. _check-0681:

チェックID: 0681
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0681

スクリーン・リーダーの見出しジャンプ機能やARIAランドマークで示される領域間ジャンプ機能で本文の開始位置を見つけることができる。

.. END_check-0681

対象
   プロダクト
関連ガイドライン
   *  ページ全体： :ref:`gl-page-markup-main`
参考情報
   *  :ref:`exp-page-structure`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0681
   :end-before: .. END_nvda-0681

.. _check-0711:

チェックID: 0711
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0711

ページの状態が変化したときも含めて、スクリーン・リーダーで読み上げさせた時、内容的、および視覚的に自然な順序で読み上げられる。

.. END_check-0711

対象
   プロダクト
関連ガイドライン
   *  ページ全体： :ref:`gl-page-markup-order`
   *  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`
参考情報
   *  :ref:`exp-dynamic-content-maintain-dom-tree`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0711
   :end-before: .. END_nvda-0711

.. _check-0721:

チェックID: 0721
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0721

ページ内の機能や内容の区切り、本分の先頭部分などに適切に見出しが配置されている。

.. END_check-0721

対象
   デザイン
関連ガイドライン
   *  ページ全体： :ref:`gl-page-headings`
参考情報
   *  :ref:`exp-page-structure`


.. _check-0731:

チェックID: 0731
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0731

``h1`` ～ ``h6`` 要素で見出しが適切にマークアップされている。

.. END_check-0731

対象
   コード
関連ガイドライン
   *  ページ全体： :ref:`gl-page-headings`
参考情報
   *  :ref:`exp-page-structure`


.. _check-0741:

チェックID: 0741
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0741

スクリーン・リーダーが見出しを適切に見出しとして認識している。

.. END_check-0741

対象
   プロダクト
関連ガイドライン
   *  ページ全体： :ref:`gl-page-headings`
参考情報
   *  :ref:`exp-page-structure`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0741
   :end-before: .. END_nvda-0741

.. _check-0751:

チェックID: 0751
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0751

特定の画面方向に固定した使用を前提としたデザインになっていない。

.. END_check-0751

対象
   デザイン
関連ガイドライン
   *  ページ全体： :ref:`gl-page-orientation`
参考情報
   *  :ref:`exp-page-orientation`


.. _check-0771:

チェックID: 0771
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0771

画面方向を検知できる端末において、端末の方向を変えると適切に画面が回転する。

.. END_check-0771

対象
   プロダクト
関連ガイドライン
   *  ページ全体： :ref:`gl-page-orientation`
参考情報
   *  :ref:`exp-page-orientation`


.. _check-0781:

チェックID: 0781
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0781

*  グローバル・ナビゲーション、ヘッダー、フッター、パンくずリスト、サポートUIなど、複数のページで共通に用いられているページの構成要素は、すべてのページで同じ出現順序になっている。かつ
*  これらの構成要素の中でのリンクやボタンの出現順序はすべてのページで同じになっている。

.. END_check-0781

対象
   デザイン
関連ガイドライン
   *  ページ全体： :ref:`gl-page-consistent-navigation`
参考情報
   *  :ref:`exp-page-navigation`


.. _check-0801:

チェックID: 0801
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0801

*  グローバル・ナビゲーション、ヘッダー、フッター、パンくずリスト、サポートUIなど、複数のページで共通に用いられているページの構成要素は、すべてのページで同じ出現順序になっている。かつ
*  これらの構成要素の中でのリンクやボタンの出現順序はすべてのページで同じになっている。

.. END_check-0801

対象
   プロダクト
関連ガイドライン
   *  ページ全体： :ref:`gl-page-consistent-navigation`
参考情報
   *  :ref:`exp-page-navigation`


.. _check-0811:

チェックID: 0811
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0811

そのページへの到達手段が複数ある。

例：

*  ナビゲーション・メニューといわゆるハブ・ページの両方から遷移できる。
*  特定のページ中のリンクから遷移することに加えて、サイト内検索機能からも遷移できる。
*  ヘルプ・ページ中のリンクからも遷移できる。

.. END_check-0811

対象
   デザイン
関連ガイドライン
   *  ページ全体： :ref:`gl-page-redundant-navigation`
参考情報
   *  :ref:`exp-page-navigation`


.. _check-0841:

チェックID: 0841
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0841

グローバル・ナビゲーション内の表示やいわゆるパンくずリストで、そのページのサイト内での位置が明示されている。

.. END_check-0841

対象
   デザイン
関連ガイドライン
   *  ページ全体： :ref:`gl-page-location`
参考情報
   *  :ref:`exp-page-navigation`


.. _check-0851:

チェックID: 0851
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0851

``aria-current`` 属性を用いて、グローバル・ナビゲーションやパンくずリスト内でそのページの位置が明示されている。

.. END_check-0851

対象
   コード
関連ガイドライン
   *  ページ全体： :ref:`gl-page-location`
参考情報
   *  :ref:`exp-page-navigation`


.. _check-0861:

チェックID: 0861
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0861

スクリーン・リーダーで、グローバル・ナビゲーションやパンくずリスト内でそのページの位置が分かるような読み上げがされる。

.. END_check-0861

対象
   プロダクト
関連ガイドライン
   *  ページ全体： :ref:`gl-page-location`
参考情報
   *  :ref:`exp-page-navigation`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0861
   :end-before: .. END_nvda-0861

.. _check-0862:

チェックID: 0862
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0862

グローバル・ナビゲーションやパンくずリスト内でそのページの位置が分かるような表示がされている。

.. END_check-0862

対象
   プロダクト
関連ガイドライン
   *  ページ全体： :ref:`gl-page-location`
参考情報
   *  :ref:`exp-page-navigation`


.. _check-0891:

チェックID: 0891
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0891

line-heightを1.5em以上、段落感の空白を2em以上、letter-spacingを0.12em以上に変更するユーザーCSSを適用しても、表示順序が変わる、文章を途中で読めなくなるなど、コンテンツおよび機能に損失が生じない。

.. END_check-0891

対象
   プロダクト
関連ガイドライン
   *  テキスト： :ref:`gl-text-customize`
参考情報
   *  :ref:`exp-text-custom-css`


.. _check-0911:

チェックID: 0911
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0911

複数の言語が含まれているテキストについて、適切に ``lang`` 属性が指定されている。

.. END_check-0911

対象
   コード
関連ガイドライン
   *  テキスト： :ref:`gl-text-phrase-lang`
参考情報
   *  :ref:`exp-text-lang`


.. _check-0921:

チェックID: 0921
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0921

複数の言語が含まれているテキストについて、多言語対応している読み上げ環境を用いて読み上げさせたとき、適切な言語の音声エンジンで読み上げられる。

.. END_check-0921

対象
   プロダクト
関連ガイドライン
   *  テキスト： :ref:`gl-text-phrase-lang`
参考情報
   *  :ref:`exp-text-lang`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-0921
   :end-before: .. END_nvda-0921

.. _check-0931:

チェックID: 0931
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0931

*  フォーム・コントロールについて、役割が分かり、画面上に表示されているテキストまたは代替テキストが付加された画像を、ラベルとして設計資料に定義している。または
*  ``aria-label`` 属性値として指定すべき、フォーム・コントロールの役割を示すテキストを設計資料に定義している。

.. END_check-0931

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-label`
   *  フォーム： :ref:`gl-form-hidden-label`
参考情報
   *  :ref:`exp-form-labeling`


.. _check-0941:

チェックID: 0941
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0941

*  フォーム・コントロールは、ラベルとなるテキストまたは画像と ``label`` 要素または ``aria-labelledby`` 属性で関連付けられている。または
*  ``aria-label`` 属性で適切なラベルが付けられている。
*  開発者ツールで確認するとフォーム・コントロールのaccessible nameに役割が分かるテキストが指定されている状態になっている。

.. END_check-0941

対象
   コード
関連ガイドライン
   *  フォーム： :ref:`gl-form-label`
   *  フォーム： :ref:`gl-form-hidden-label`
参考情報
   *  :ref:`exp-form-labeling`


.. _check-0951:

チェックID: 0951
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0951

*  フォーム・コントロールの役割が分かるテキストまたは代替テキストが付加された画像がラベルとして表示されていて、このテキストをクリックすると当該のフォーム・コントロールにフォーカスが移動する。または
*  スクリーン・リーダーでフォーム・コントロールとラベルの関連付けが分かるような読み上げがされる。

.. END_check-0951

対象
   プロダクト
関連ガイドライン
   *  フォーム： :ref:`gl-form-label`
   *  フォーム： :ref:`gl-form-hidden-label`
参考情報
   *  :ref:`exp-form-labeling`


axeを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/axe.rst
   :start-after: .. BEGIN_axe-0951
   :end-before: .. END_axe-0951

.. _check-0961:

チェックID: 0961
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0961

フォームの入力に制限時間を設ける場合：

*   事前にユーザーがその制限時間を解除することができる。又は、
*  事前にユーザーが少なくともデフォルト設定の10倍を超える、大幅な制限時間の調整をすることができる。又は、
*  時間切れになる前にユーザーに警告し、かつ少なくとも20秒間の猶予をもって、例えば「スペースキーを押す」などの簡単な操作により、ユーザーが制限時間を10回以上延長することができる。又は、
*  リアルタイムのイベント（例えば、オークション）において制限時間が必須の要素で、その制限時間に代わる手段が存在しない。又は、
*  制限時間が必要不可欠なもので、制限時間を延長することがフォームを無効にすることになる。又は、
*  制限時間が20時間よりも長い。

.. END_check-0961

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-timing`
参考情報
   *  :ref:`exp-timing`


.. _check-0991:

チェックID: 0991
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-0991

フォーム入力に制限時間が設けられていない。

.. END_check-0991

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-no-timing`
参考情報
   *  :ref:`exp-timing`


.. _check-1021:

チェックID: 1021
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1021

制限時間が設定されているフォームの入力中に制限時間が超過した場合、それまでの入力内容を失うことなく入力を再開できるようになっている。

.. END_check-1021

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-continue`
参考情報
   *  :ref:`exp-timing`


.. _check-1051:

チェックID: 1051
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1051

フォーム中のフィールドの値の変更や、値変更後のフォーカス移動がトリガーとなって、ページ全体に及ぶような大幅な表示内容の変更、ページ遷移、別のフィールドの値の変更が起こるような機能が設計資料に存在しない。

.. END_check-1051

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-dynamic-content-change`
参考情報
   *  :ref:`exp-form-dynamic-content`


.. _check-1071:

チェックID: 1071
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1071

フォーム中のフィールドの値の変更や、値変更後のフォーカス移動がトリガーとなって、ページ全体に及ぶような大幅な表示内容の変更、ページ遷移、別のフィールドの値の変更が起こらない。

.. END_check-1071

対象
   プロダクト
関連ガイドライン
   *  フォーム： :ref:`gl-form-dynamic-content-change`
参考情報
   *  :ref:`exp-form-dynamic-content`


.. _check-1081:

チェックID: 1081
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1081

フォーム入力でエラーが発生したとき、エラー内容が分かる具体的な表示文言が設計資料で定義されている

.. END_check-1081

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-errors-identify`
参考情報
   *  :ref:`exp-form-errors`


.. _check-1101:

チェックID: 1101
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1101

フォーム入力に関するエラー発生時には、エラーの内容が具体的に分かるテキスト情報が表示される。

.. END_check-1101

対象
   プロダクト
関連ガイドライン
   *  フォーム： :ref:`gl-form-errors-identify`
参考情報
   *  :ref:`exp-form-errors`


.. _check-1111:

チェックID: 1111
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1111

フォーム入力に関するエラー・メッセージには、エラーの修正方法が示されている。

.. END_check-1111

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-errors-correction`
参考情報
   *  :ref:`exp-form-errors`


.. _check-1131:

チェックID: 1131
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1131

フォーム入力に関するエラー・メッセージには、エラーの修正方法が示されている。

.. END_check-1131

対象
   プロダクト
関連ガイドライン
   *  フォーム： :ref:`gl-form-errors-correction`
参考情報
   *  :ref:`exp-form-errors`


.. _check-1141:

チェックID: 1141
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1141

法的行為、経済的取引、データの変更や削除を生じる機能については、取り消し、送信前の確認・修正、または送信時のエラー・チェックと修正が可能になっている。

.. END_check-1141

対象
   デザイン
関連ガイドライン
   *  フォーム： :ref:`gl-form-errors-cancel`
参考情報
   *  :ref:`exp-form-errors`


.. _check-1171:

チェックID: 1171
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1171

ステータス・メッセージとして扱われるべきメッセージ、すなわち表示時や変更時に自動的に読み上げられる必要があるメッセージが、設計資料で特定されている。

.. END_check-1171

対象
   デザイン
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-status`
参考情報
   *  :ref:`exp-dynamic-content-status`


.. _check-1181:

チェックID: 1181
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1181

操作の結果などを伝えるステータス・メッセージには適切に ``aria-live`` 属性が付与されている。

.. END_check-1181

対象
   コード
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-status`
参考情報
   *  :ref:`exp-dynamic-content-status`


.. _check-1191:

チェックID: 1191
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1191

操作の結果などを伝えるステータス・メッセージは、スクリーン・リーダーで自動的に読み上げられる。

.. END_check-1191

対象
   プロダクト
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-status`
参考情報
   *  :ref:`exp-dynamic-content-status`


NVDAを用いたチェック実施方法の例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: /checks/examples/nvda.rst
   :start-after: .. BEGIN_nvda-1191
   :end-before: .. END_nvda-1191

.. _check-1201:

チェックID: 1201
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1201

点滅、スクロールを伴うコンテンツがない。

.. END_check-1201

対象
   デザイン
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-pause-movement`
参考情報
   *  :ref:`exp-dynamic-content-auto-updated`


.. _check-1221:

チェックID: 1221
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1221

点滅、スクロールを伴うコンテンツがない。

.. END_check-1221

対象
   プロダクト
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-pause-movement`
参考情報
   *  :ref:`exp-dynamic-content-auto-updated`


.. _check-1231:

チェックID: 1231
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1231

*  自動更新されるコンテンツがない。または
*  ユーザーが自動更新の間隔やタイミングの変更、自動更新の停止をできる。

.. END_check-1231

対象
   デザイン
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-pause-refresh`
参考情報
   *  :ref:`exp-dynamic-content-auto-updated`


.. _check-1251:

チェックID: 1251
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1251

*  自動更新されるコンテンツがない。または
*  ユーザーが自動更新の間隔やタイミングの変更、自動更新の停止をできる。

.. END_check-1251

対象
   プロダクト
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-pause-refresh`
参考情報
   *  :ref:`exp-dynamic-content-auto-updated`


.. _check-1261:

チェックID: 1261
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1261

1秒間に3回以上光るコンテンツがない。

.. END_check-1261

対象
   デザイン
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-no-flashing`
参考情報
   *  :ref:`exp-dynamic-content-auto-updated`


.. _check-1281:

チェックID: 1281
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1281

1秒間に3回以上光るコンテンツがない。

.. END_check-1281

対象
   プロダクト
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-no-flashing`
参考情報
   *  :ref:`exp-dynamic-content-auto-updated`


.. _check-1291:

チェックID: 1291
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1291

ユーザーが予期しない形で発生する、画面の内容を大きく変更するような通知や自動的に表示されるモーダル・ダイアログがない。

.. END_check-1291

対象
   デザイン
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-no-interrupt`
参考情報
   *  :ref:`exp-dynamic-content-auto-updated`


.. _check-1311:

チェックID: 1311
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1311

ユーザーが予期しない形で発生する、画面の内容を大きく変更するような通知や自動的に表示されるモーダル・ダイアログがない。

.. END_check-1311

対象
   プロダクト
関連ガイドライン
   *  動的コンテンツ： :ref:`gl-dynamic-content-no-interrupt`
参考情報
   *  :ref:`exp-dynamic-content-auto-updated`


.. _check-1321:

チェックID: 1321
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1321

ログイン・セッションにタイムアウトを設ける場合：

*  ログイン時などに、ユーザーがセッション・タイムアウトの設定を解除することができる。又は、
*  ログイン時などに、ユーザーが少なくともデフォルト設定の10倍を超える、大幅なタイムアウト設定値の調整をすることができる。又は、
*  時間切れになる前にユーザーに警告し、かつ少なくとも20秒間の猶予をもって、例えば「スペースキーを押す」などの簡単な操作により、ユーザーがタイムアウトを10回以上延長することができる。又は、
*  タイムアウトが必要不可欠なもので、タイムアウトを延長することがコンテンツの動作を無効にすることになる。又は、
*  タイムアウトが20時間よりも長い。

.. END_check-1321

対象
   デザイン
関連ガイドライン
   *  ログイン・セッション： :ref:`gl-login-session-timing`
参考情報
   *  :ref:`exp-timing`


.. _check-1351:

チェックID: 1351
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1351

ログイン・セッションに有効期限が設定されていない。

.. END_check-1351

対象
   デザイン
関連ガイドライン
   *  ログイン・セッション： :ref:`gl-login-session-no-timing`
参考情報
   *  :ref:`exp-timing`


.. _check-1381:

チェックID: 1381
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1381

ログイン・セッションがタイムアウトした場合、再認証後にデータを失うことなくユーザーが操作を継続できるようになっている。

.. END_check-1381

対象
   デザイン
関連ガイドライン
   *  ログイン・セッション： :ref:`gl-login-session-continue`
参考情報
   *  :ref:`exp-timing`


.. _check-1411:

チェックID: 1411
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1411

*  ページ内に埋め込まれる音声/動画プレイヤーについて、適切なラベル付けがされていてそこにプレイヤーがあることが容易に認知できるようになっている。または
*  前後のテキストから、そこにプレイヤーがあることが推測できる。

.. END_check-1411

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`
参考情報
   *  :ref:`exp-multimedia-perceivable`


.. _check-1421:

チェックID: 1421
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1421

3秒以上の長さの自動再生される音声コンテンツがない。

.. END_check-1421

対象
   デザイン
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-operable`
参考情報
   *  :ref:`exp-multimedia-autoplay`


.. _check-1441:

チェックID: 1441
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1441

3秒以上の長さの自動再生される音声コンテンツがない。

.. END_check-1441

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-operable`
参考情報
   *  :ref:`exp-multimedia-autoplay`


.. _check-1451:

チェックID: 1451
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1451

*  自動的に開始し5秒以上続く動画、アニメーションがない。または
*  動画やアニメーションを呈し、一時停止、または非表示にすることができる。

.. END_check-1451

対象
   デザイン
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-pause-movement`

.. _check-1471:

チェックID: 1471
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1471

*  自動的に開始し5秒以上続く動画、アニメーションがない。または
*  動画やアニメーションを呈し、一時停止、または非表示にすることができる。

.. END_check-1471

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-pause-movement`

.. _check-1481:

チェックID: 1481
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1481

音声・映像コンテンツは、そのコンテンツがなくても不足なく情報が伝わるような内容で、そのコンテンツがテキスト情報の代替もしくは補助的な位置づけであることが明示されている。

.. END_check-1481

対象
   デザイン
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-text-alternative`
参考情報
   *  :ref:`exp-multimedia-content-access`


.. _check-1501:

チェックID: 1501
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1501

音声・映像コンテンツは、そのコンテンツがなくても不足なく情報が伝わるような内容で、そのコンテンツがテキスト情報の代替もしくは補助的な位置づけであることが明示されている。

.. END_check-1501

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-text-alternative`
参考情報
   *  :ref:`exp-multimedia-content-access`


.. _check-1531:

チェックID: 1531
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1531

音声を含むコンテンツには、同期したキャプションが提供されている。

.. END_check-1531

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-caption`
参考情報
   *  :ref:`exp-multimedia-content-access`


.. _check-1561:

チェックID: 1561
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1561

*  動画は、元々収録されている音声トラックの内容から容易に映像を推測できる。または
*  動画には音声解説が含まれている。または
*  映像に関するテキストによる説明が提供されている。

.. END_check-1561

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-video-description`
参考情報
   *  :ref:`exp-multimedia-content-access`


.. _check-1562:

チェックID: 1562
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1562

*  動画は、元々収録されている音声トラックの内容から容易に映像を推測できる。または
*  動画には音声解説が含まれている。

.. END_check-1562

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-video-description-no-exception`
参考情報
   *  :ref:`exp-multimedia-content-access`


.. _check-1591:

チェックID: 1591
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1591

映像がない音声のみのコンテンツについて、音声を書き起こしたテキストが提供されている。

.. END_check-1591

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-transcript`
参考情報
   *  :ref:`exp-multimedia-content-access`


.. _check-1621:

チェックID: 1621
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1621

動画の音声情報には同期した手話通訳が提供されている。

.. END_check-1621

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-sign-language`
参考情報
   *  :ref:`exp-multimedia-content-access`


.. _check-1651:

チェックID: 1651
~~~~~~~~~~~~~~~~~~

.. BEGIN_check-1651

音声コンテンツについて、充分に聴き取りやすい。

.. END_check-1651

対象
   プロダクト
関連ガイドライン
   *  音声・映像コンテンツ： :ref:`gl-multimedia-background-sound`
参考情報
   *  :ref:`exp-multimedia-content-access`

