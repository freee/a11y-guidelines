.. _exp-check-contrast:

############################
コントラスト比のチェック方法
############################

Webやモバイル・アプリケーションにおいて、ロービジョン者でもコンテンツを知覚できるよう、テキストやUIコンポーネントにそれぞれコントラスト比の基準を満たす色の組み合わせを用いることが重要です。

Webページで色のコントラスト比が不足している場所を発見するには、 `axe DevTools`_ のようなチェック・ツールを用いると良いでしょう。
モバイル・アプリケーションの画面など、このようなチェック・ツールが利用できない場合は、 `WebAIM: Contrast Checker`_ のような、具体的な色同士のコントラスト比の計算ができるツールと、カラー・ピッカーを組み合わせて使用すると良いでしょう。

****************************************
アクセシビリティー・チェックツールの使用
****************************************

Google Chromeでは、開発者ツールの Lighthouseタブから、色のコントラスト比の問題を含め、アクセシビリティーの問題をチェックすることができます。

また、 `axe DevTools`_ でも、Webページ全体からコントラスト比の問題を含め、アクセシビリティー上の問題のある場所を発見することができます。
axe DevToolsは、`Google Chrome 拡張`_ および `Mozilla Firefoxアドオン`_ として提供されています。

**************************************
コントラスト比の自動判定ができない場合
**************************************

画像の中の文字など、これらのチェック・ツールではコントラスト比を正しく判定できない場合があります。

axe DevToolsのGoogle Chrome拡張の場合、コントラスト比の判定ができない場合も「要素には十分な色のコントラストがなければなりません」のような、コントラスト比が不充分な場合と同じメッセージが表示されます。
しかし自動判定ができない場合は、詳細パネルに「This potential issue needs your review... コントラスト比を判定できません」といったメッセージが表示されます。

また、axe DevToolsが利用できるのはWebページに対するチェックのみで、モバイル・アプリケーションの画面などに対しては利用できません。

このような場合は、当該箇所のカラー・コードを調べ、コントラスト比を確認します。

モバイル・アプリケーションの画面のチェック
==========================================

モバイル・アプリケーションの画面を対象にしたチェックを実施する場合、以下のような方法が考えられます：

*  スクリーン・ショットを撮り、その画像をPC上でチェックする。
*  Google Meetなどのオンライン会議ツールを使って画面を共有し、PC上で共有された画面をチェックする。
   ただし利用するオンライン会議ツールによっては、共有された画面に色補正が加えられることも考えられるので、この方法を用いる場合は注意が必要です。

カラー・コードを調べる
======================

カラー・ピッカーと呼ばれるツールで、コントラスト比のチェックをしたい箇所で用いられている色のカラー・コードを調べることができます。

後述するWebAIM: Contrast Checkerでも、カラー・ピッカーが提供されていますが、WindowsやmacOSで動作するものもあります。
以下では代表的なものを挙げます。

Windows
-------

Microsoft PowerToysの機能の1つとして、Color Pickerが提供されています。

Microsoft PowerToysは、Microsoft StoreまたはGitHubから入手することができます：

*  `Microsoft PowerToys (Microsoft Store)`_
*  `Microsoft PowerToys (GitHub)`_

参考： `Microsoft PowerToys: Windows をカスタマイズするためのユーティリティ`_

macOS
-----

macOSには、Digital Color Meterというカラー・ピッカーが標準で搭載されています。

参考： `Mac用Digital Color Meterユーザガイド`_

macOSでカラー・ピッカーを使用する場合、ディスプレイのカラー・プロファイルの影響を受けることがあります。
これを防ぐためには、macOSのカラープロファイル設定で、「このディスプレイのプロファイルのみを表示」のチェックを外してから「SRGB IEC61966-2.1」を選択します。

参考： `Macのディスプレイのカラープロファイルを変更する`_

Figmaを使用する場合、画面上部、ファイル名の右横のメニュー内、「File color profile」から、各ファイルに適用されているカラー・プロファイルを確認することができます。
「sRGB」または「Same as preferred profile (sRGB)」となっていれば問題ありません。

また、画面左上、Figmaのメニュー・アイコンから、:menuselection:`Preferences --> Color profile...` で 「sRGB」に変更することで、ファイルの新規作成時にsRGBが選択されるようになります。

コントラスト比の計算ツールの使用
================================

コントラスト比の計算式は非常に複雑であるため、 `WebAIM: Contrast Checker`_ のような計算ツールを使用することが一般的です。
`contrast.app`_ のように、インストールして常駐させるタイプのチェッカーも存在します。

なお、コントラスト比の計算ツールによって小数点以下の丸め方に差異があり、計算結果がバラつくことがあります。
計算結果は目安として考え、コントラスト比に余裕のある色を選ぶのが望ましいでしょう。

****
参考
****

*  :ref:`exp-contrast`
*  |Vibes Color Contrast|

.. include:: /inc/info2gl/exp-check-contrast.rst

.. _axe DevTools: https://www.deque.com/axe/
.. _WebAIM\: Contrast Checker: https://webaim.org/resources/contrastchecker/
.. _Google Chrome 拡張: https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd
.. _Mozilla Firefoxアドオン: https://addons.mozilla.org/firefox/addon/axe-devtools/
.. _contrast.app: https://usecontrast.com/
.. _Macのディスプレイのカラープロファイルを変更する: https://support.apple.com/ja-jp/guide/mac-help/mchlf3ddc60d/mac
.. _Mac用Digital Color Meterユーザガイド: https://support.apple.com/ja-jp/guide/digital-color-meter/welcome/mac
.. _Microsoft PowerToys (Microsoft Store): https://apps.microsoft.com/detail/xp89dcgq3k6vld
.. _Microsoft PowerToys (GitHub): https://github.com/microsoft/PowerToys
.. _Microsoft PowerToys\: Windows をカスタマイズするためのユーティリティ: https://learn.microsoft.com/ja-jp/windows/powertoys/

.. translated:: true

