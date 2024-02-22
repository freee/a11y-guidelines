.. _exp-screen-reader-check-macos-vo:

##########################################
macOSのVoiceOverを用いたチェックの実施方法
##########################################

macOS用スクリーン・リーダーのVoiceOverの推奨設定の方法、基本的な使い方と基本的なチェックの実施方法について記します。

なお、iOSにも同名のスクリーン・リーダーが標準搭載されていますが [#]_ 、macOSのVoiceOverとはまったくの別物です。
本稿ではmacOSのVoiceOverについてのみ記し、「VoiceOver」という記述はmacOS VoiceOverを差します。

本稿のキー操作の説明では、 :kbd:`VO + →` のような表記をしていますが、これは :ref:`macos-vo-vokey` の項で説明する「VoiceOverキー」を押しながら :kbd:`→` を押すことを意味します。
また、 :kbd:`F1` ～ :kbd:`F12` は、キーボード上部のファンクション・キーのことですが、設定によっては :kbd:`fn` キーを押しながら押下する必要がある点に注意が必要です。（後述の :ref:`macvo-fnkey` を参照）

.. [#] :ref:`exp-screen-reader-check-ios-voiceover`

*****************************************
macOS VoiceOverを用いたチェックの位置づけ
*****************************************

:ref:`exp-screen-reader-check-nvda` にもあるように、freeeでは、スクリーン・リーダーを用いて行う必要があるチェックについては、Windows上のNVDAとGoogle Chromeのそれぞれ最新版を標準環境としています。
これは、日本においてはスクリーン・リーダーのユーザーの大半がWindowsを利用していて [#]_ 、これらのユーザーが確実に使えるようにすることが重要であると考えているためです。

しかし、すべてのチェックについてNVDAでなければ実施できないというわけではなく、macOSのVoiceOverでも実施可能なチェックもあります。
最終的なチェックにはNVDAを用いることを推奨しますが、開発中に実施するチェックのうち、以下のような場合はmacOS VoiceOverを用いても問題ありません。

*  すでにNVDAでの挙動に問題がないことが確認されている既存のコンポーネントの動作確認
*  静的なHTMLで実装されている箇所の動作確認

一方、新たに実装するコンポーネントについては、開発の早い段階からNVDAによる動作確認を実施することを強く推奨します。

macOS VoiceOverで問題なく動作してもNVDAでは動作に問題がある場合や、反対にmacOS VoiceOverでは動作に問題があってもNVDAでは問題なく動作する場合もあります。
どちらの環境でも問題なく動作するものを実現できることが理想ですが、freeeでは最低限NVDAで問題なく動作することを目指しています。

.. [#] `第3回支援技術利用状況調査報告書 <https://jbict.net/survey/at-survey-03>`_

********
事前準備
********

VoiceOverの起動と終了
=====================

VoiceOverの起動と終了は、以下のいずれかの方法で行うことができます。

1. :kbd:`Command + F5` キーの押下
2. :kbd:`Command` キーを押しながらTouch IDを3回連続で素早く押す
3. Siriに「ボイスオーバーをオンにする」（起動）または「ボイスオーバーをオフにする」（終了）と話しかける

上記1.と2.の操作は、VoiceOverが起動していないときに実行することでVoiceOverを起動し、VoiceOverが起動しているときに実行することでVoiceOverを終了します。

.. _macvo-fnkey:

ファンクション・キーの設定
--------------------------

前述のように 、 :kbd:`Command + F5` キーは、設定によっては :kbd:`fn + Command + F5` となる場合があります。
ファンクション・キーを使うことが多い場合は、 :kbd:`fn` キーの押下を必要としない設定にすることも検討すると良いでしょう。

macOS Venturaでの設定手順を以下に示します。

1. :menuselection:`Appleメニュー --> システム設定` の順に選択
2. サイドバーで「キーボード」を選択
3. 右側で「キーボードショートカット」をクリック

   .. image:: /img/macvo/macvo-settings-keyboard.png
      :alt: スクリーン・ショット：システム設定でキーボードを選択

4. サイドバーで「ファンクションキー」を選択
5. 右側で「F1、F2 などのキーを標準のファンクションキーとして使用」をオンにする

   .. image:: /img/macvo/macvo-settings-fnkey.png
      :alt: スクリーン・ショット：ファンクションキーの設定

参考： `Mac でファンクションキーを使う方法 - Apple サポート (日本) <https://support.apple.com/ja-jp/102439>`_

初回起動時の操作
================

VoiceOverを初めて起動したときは、以下のような「ようこそダイアログ」が表示され、画面の内容を読み上げる音声が再生されます。

.. image:: /img/macvo/macvo-welcome-dialog.png
   :alt: スクリーン・ショット：VoiceOverのようこそダイアログ

このダイアログからVoiceOver Quick Startにアクセスすることができますが、この時点では :kbd:`V` キーを押してこの画面を閉じます。
なお、VoiceOver Quick Startは、初めてVoiceOverを使用する視覚障害者がVoiceOverの使い方を独習できるように提供されているものです。
VoiceOver起動中に :kbd:`VO + Command + F8` を押下することでいつでも起動することができます。
VoiceOverの操作方法についてより深く理解したい場合などには参考になりますので、活用すると良いでしょう。

推奨設定
========

VoiceOver動作中に :kbd:`VO + F8` を押下すると、VoiceOverユーティリティが起動し、VoiceOverの様々な設定を変更することができます。
この画面では、左側に設定のカテゴリーが表示され、右側に現在選択されているカテゴリーの設定項目が表示されます。

この項では、アクセシビリティー・チェックの実施に当たって推奨する設定を、カテゴリーごとに示します。

一般
----

.. image:: /img/macvo/macvo-util-general.png
   :alt: スクリーン・ショット：VoiceOverユーティリティ（「一般」を選択）

「VoiceOver起動時にようこそダイアログを表示」のチェックを外します。
これにより、前述のようこそダイアログの表示を抑制することができます。

ビジュアル
----------

.. image:: /img/macvo/macvo-util-visual.png
   :alt: スクリーン・ショット：VoiceOverユーティリティ（「ビジュアル」を選択）

「パネルとメニュー」タブの「キャプションパネルを表示」にチェックを入れます。
これにより、VoiceOverの読み上げ内容が画面上に表示されるようになります。

コマンダー
----------

.. image:: /img/macvo/macvo-util-commander-trackpad.png
   :alt: スクリーン・ショット：VoiceOverユーティリティ（「コマンダー」の「トラックパッドコマンダー」タブを選択）

「トラックパッドコマンダー」タブの「トラックパッドコマンダーを有効にする」のチェックを外します。
この項目にチェックが入っていると、トラックパッドをVoiceOverの操作に用いることができるようになり、通常のマウス操作ができなくなります。

.. image:: /img/macvo/macvo-util-commander-quicknav.png
   :alt: スクリーン・ショット：VoiceOverユーティリティ（「コマンダー」の「クイックナビ」タブを選択）

「クイックナビ」タブの「クイックナビを有効にする」のチェックを外します。
この項目がチェックされていると、VOキーを使わずにできる操作が増えます。
日常的にVoiceOverを利用しているユーザーにとっては便利な設定ですが、VoiceOverを利用したアクセシビリティー・チェックを実施する場合には、誤ってこのモードを有効にしてしまった場合などに混乱を招くことも考えられますので、この設定を無効にしておくことを推奨します。

************************
最低限知っておきたいこと
************************

.. _macos-vo-vokey:

VoiceOverキー（ :kbd:`VO` キー）と :kbd:`VO` キー・ロック
=========================================================

VoiceOver起動中は、特定のキーを押しながら他のキーを押下することで、VoiceOverの機能を利用することができます。
これを「VoiceOverキー（ :kbd:`VO` キー）」と呼びます。
初期設定では、 :kbd:`Control + Option` キーの組み合わせ、または :kbd:`Caps Lock` キー の両方がVoiceOverキーとして設定されています。

なお、 :kbd:`VO + ;` を押下すると、 :kbd:`VO` キーを押してロックした状態になります。
この状態では、VoiceOverに関する様々なキー操作を :kbd:`VO` キーを押さずに実行できるようになりますが、あらゆるキー操作が普段とは異なる挙動になるため注意が必要です。
例えば、この状態では :kbd:`Command + F5` を押下しても、 :kbd:`VO + Command + F5` を押下したことになり、VoiceOverを終了することはできません。

キー操作が期待通りの挙動にならない場合は、 :kbd:`VO` キーがロックされた状態になっている可能性も考えられます。
この場合は、 :kbd:`VO + ;` を再度押下してロックを解除してください。

VoiceOverカーソルとキーボード・フォーカス
=========================================

VoiceOverが有効になっていると、VoiceOverカーソルと呼ばれる濃い矩形の枠が画面上に表示されます。
VoiceOverカーソルが移動すると、移動した先に表示されているものが読み上げられることに加えて、そこにあるものが操作対象になります。

初期設定では、VoiceOverカーソルとキーボード・フォーカスやカーソルは同期するようになっていて、基本的に同じ場所にあります。
しかし、これらは実際には独立したもので、必ずしも常に同じ場所にあるわけではない点に注意が必要です。

同様に、VoiceOverカーソルとマウス・ポインターも独立したものです。
初期設定ではこれらは独立して動くようになっていますが、これも設定によって挙動が変わります。

VoiceOverカーソルの移動
=======================

VoiceOverカーソルは、 :kbd:`VO` キーを押しながら矢印キーを押下することで移動することができます。
多くの場合、 :kbd:`VO + →` による右方向への移動を用いて、画面上の表示内容を読み進め、 :kbd:`VO + ←` による左方向への移動を用いて少し戻って読み直す、というような使い方をします。

前述のように、VoiceOverカーソルがある場所にあるものは、操作対象になります。
例えば、リンク上にVoiceOverカーソルがある場合、 :kbd:`VO + Spc` を押下することで、そのリンクをクリックしたのと同じ結果を得られます。
VoiceOverカーソルが何らかの操作ができるものの上にある場合、しばらくすると具体的な操作方法が音声で読み上げられます。

なお、 :kbd:`VO` キーを押さずに矢印キーを押したときの挙動は、VoiceOverが起動していない場合と同じで、カーソルが移動します。
このとき、設定によってVoiceOverカーソルが追従する場合と追従しない場合があります。

項目の操作
==========

テキスト・コンテンツ上で :kbd:`VO + →` と :kbd:`VO + ←` でVoiceOverカーソルを移動する場合、センテンス単位など、ある程度まとまったテキストを単位とした移動が行われます。
ところが、場合によってはその移動の単位がウィンドウの構成要素の単位など、もっと大きな単位になる場合があります。

例えば、Google ChromeのツールバーにVoiceOverカーソルがある状態でVoiceOverカーソルを右方向へ移動していくと、表示されているページのコンテンツに差し掛かったところで「Webコンテンツ」とだけ読み上げるような状態になります。
これは、ページを表示している部分をVoiceOverが1つの要素として解釈しているためです。

このような場合、いわばその要素の中にVoiceOverカーソルを入れて、内部を探索するような形で読み上げる必要があります。
これを行うためのキー操作が、 :kbd:`VO + Shift + ↓` です。

上のGoogle Chromeの例の場合、「Webコンテンツ」と言われた所で :kbd:`VO + Shift + ↓` を押下することで、ページのコンテンツを表示している部分にVoiceOverカーソルを入れることができます。
この状態で、 :kbd:`VO + →` と :kbd:`VO + ←` を用いることで、ページの内容を確認することができます。
さらに、ページ中の表や箇条書きなどがひとまとまりの要素として解釈されている場合もあり、こういった場合にも :kbd:`VO + Shift + ↓` を用いることで、その要素の中にVoiceOverカーソルを入れることができます。

VoiceOverカーソルを現在の要素の外に出すときには、 :kbd:`VO + Shift + ↑` を用います。

ローター
========

VoiceOver起動中に :kbd:`VO + U` を押下すると、ローターと呼ばれるメニューが表示されます。
このメニューでは、現在フォーカスされているウィンドウ内にある要素のリストが表示されます。
例えば、Webページを表示したGoogle Chromeがフォーカスされている状態でローター・メニューを開くと、リンク、見出し、フォーム・コントロール、表、ランドマークなどの項目が、そのページに含まれているものに応じて表示されます。

これらの項目のうちどの項目のリストを表示するかは、左右矢印キーで切り替えることができます。
リストを表示したい項目を選んだら、上下矢印キーでその項目のリスト内を移動します。
リスト内の項目上でEnterキーを押すと、その項目にフォーカスが移動します。

知っておきたいキー操作
======================

:kbd:`VO + A`
   現在VoiceOverカーソルがある箇所以降を読み上げる
:kbd:`VO + Shift + F4`
   VoiceOverカーソルをキーボード・フォーカスの位置に移動
:kbd:`VO + Command + F4`
   キーボード・フォーカスをVoiceOverカーソルの位置に移動
:kbd:`VO + Shift + F5`
   VoiceOverカーソルをマウス・ポインターの位置に移動
:kbd:`Ctrl`
   読み上げの一時停止、再度押下で再開
:kbd:`VO + K`
   キーボード・ヘルプ（1度押下するとヘルプ・モードに入り、再度押下するとヘルプ・モードから抜ける。ヘルプ・モードでは、押下したキーの名称や役割が読み上げられる。）

参考情報
========

ここで紹介した内容は、VoiceOverの機能のごく一部です。
より詳しい使い方や、VoiceOverの機能については、以下の情報を参照してください。

*  `Mac用VoiceOverユーザガイド <https://support.apple.com/ja-jp/guide/voiceover/welcome/mac>`_

なお、このガイドには :kbd:`VO + H` の押下で表示されるヘルプ・メニューからもアクセスできます。

***********************
Webコンテンツのチェック
***********************

ここでは、Webコンテンツのチェックを実施する場合の基本的な考え方やよく実行する操作について説明します。

Webコンテンツのチェックをする場合、基本的にはVoiceOverカーソルですべての情報にアクセスできることを確認することが必要です。
:kbd:`VO + →` で読み進め、 :kbd:`VO + ←` で戻って読むというのが基本的な操作です。

これらのキー操作で進む/戻る長さは、概ね段落単位です。
リンクが含まれているテキストの場合は、リンク部分が1つのまとまりとして扱われます。
また、使用されているHTMLの要素によって、読み進む際の単位が変わることがあります。
:kbd:`VO + →` で読み進んだ際に、読み上げがテキストの途中で止まってしまっても、再度 :kbd:`VO + →` の押下で続きが読み上げられれば問題ありません。

:kbd:`VO + F3` を押下すると、直前に読み上げられた内容を再度読み上げさせることができます。
（正確には、この操作はVoiceOverカーソルが現在ある項目を説明させる操作です。）

まとまったコンテンツを読み上げさせる
====================================

:kbd:`VO + A` を押下すると、現在VoiceOverカーソルがある箇所以降を読み上げさせることができます。

設定によっては、マウス・ポインターの位置に自動的にVoiceOverカーソルが移動しますが、そのような設定になっていない場合は、 :kbd:`VO + Shift + F5` キーを押下することで、VoiceOverカーソルをマウス・ポインターの位置に移動することができます。
この方法と、 :kbd:`VO + →` や :kbd:`VO + ←` でVoiceOverカーソルを目的の箇所に移動した上で、 :kbd:`VO + A` を押下することで、特定の箇所の読み上げを確認することができます。

また、 :kbd:`VO + Shift + Home` （ラップトップ機では :kbd:`VO + Shift + FN + ←` ）で、VoiceOverカーソルをページの先頭に移動することができます。
この操作と :kbd:`VO + A` を組み合わせることで、ページ全体を読み上げさせることができます。

途中で読み上げを停止したい場合は、 :kbd:`Ctrl` キーを押下します。
:kbd:`Ctrl` キーを押下して読み上げを一時停止してから、他の操作をなにもしていない状態の場合は、再度 :kbd:`Ctrl` キーを押下することで読み上げを再開することができます。
または、再度 :kbd:`VO + A` を押下して、続きを読み上げさせることもできます。

操作を受け付けるコンポーネント
==============================

開閉できるメニュー、アコーディオンなど、何らかの操作を受け付けるコンポーネントについては、キーボードで操作ができることを確認する必要があります。

具体的には、VoiceOverカーソルとキーボード・フォーカスをそのコンポーネント上に移動し、そのコンポーネント上でキー操作を実行してみます。

初期設定ではVoiceOverカーソルとキーボード・フォーカスは連動するようになっていますが、そのような設定になっていない場合は、以下のいずれかの操作でVoiceOverカーソルとキーボード・フォーカスを目的のコンポーネント上に移動させます。

*  キーボード・フォーカスを目的のコンポーネント上に移動させてから、 :kbd:`VO + Shift + F4` を押下
*  VoiceOverカーソルを目的のコンポーネント上に移動させてから、 :kbd:`VO + Command + F4` を押下

キー操作をする際は、カーソルキーや :kbd:`Enter` キー、 :kbd:`Spc` キー、 :kbd:`Esc` キーなどを :kbd:`VO` キーとは組み合わせずに押下して挙動を確認します。
その結果として新たなコンテンツが表示された場合は、そのコンテンツをVoiceOverカーソルで読み上げ可能なことを確認します。

移動のための様々なキー操作
==========================

VoiceOver起動中は、以下に挙げるようなキー操作でコンテンツ内を移動することができます。

.. list-table:: VoiceOverで使用できるキー操作（抜粋）
   :header-rows: 1

   *  -  キー操作
      -  説明
   *  -  :kbd:`VO + Command + H` 、 :kbd:`Shift + VO + Command + H`
      -  次、前の見出し
   *  -  :kbd:`VO + Command + X` 、 :kbd:`Shift + VO + Command + X`
      -  次、前のリスト （ ``ul`` 、 ``ol`` 、 ``dl`` 要素）
   *  -  :kbd:`VO + Command + G` 、 :kbd:`Shift + VO + Command + G`
      -  次、前の画像
   *  -  :kbd:`VO + Command + J` 、 :kbd:`Shift + VO + Command + J`
      -  次、前のフォーム・コントロール
   *  -  :kbd:`VO + Command + T` 、 :kbd:`Shift + VO + Command + T`
      -  次、前の表