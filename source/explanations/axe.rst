.. _exp-axe:

##################################################
axe DevToolsを使用したアクセシビリティー・チェック
##################################################

axe DevToolsは非常によく使われているアクセシビリティー・チェック・ツールです。
基本機能が `axe-core <https://github.com/dequelabs/axe-core>`_ として実装されているため様々な方法で使用することができますが、ここではブラウザー拡張機能として利用して、出来上がっているWebページのアクセシビリティーの対応状況をチェックする方法を紹介します。

なお、axe DevToolsを用いた具体的なチェックの実施方法については、 :ref:`check-example-axe` を参照してください。
また、 :ref:`info-axe-rules` も合わせて参照してください。

**************************************
axe DevToolsのインストールと起動の仕方
**************************************

ChromeウェブストアからChrome拡張をインストールできます。

`axe DevTools - Web Accessibility Testing - Chrome ウェブストア <https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd>`_

axe DevTools拡張機能はデベロッパーツール内で使用します。

分析対象のページを開いた状態で、ツールバー右端のボタンから :menuselection:`その他のツール --> デベロッパーツール` を選択するか、ショートカットキー（Windowsでは :kbd:`Ctrl+Shift+I` 、macOSでは :kbd:`Command+Option+I` ）を使用してください。

.. image:: /img/axe/axe-1.png
   :alt: スクリーン・ショット：メニューからデベロッパーツールを開こうとしている

デベロッパーツールのタブから「axe DevTools」を選択します。

.. image:: /img/axe/axe-6.png
   :alt: スクリーン・ショット：デベロッパーツールのタブバー、右端に「axe DevTools」がある

デベロッパーツールの表示領域が狭い場合は 「>>」アイコンに隠されていることがあります。

.. image:: /img/axe/axe-2.png
   :alt: スクリーン・ショット：axe DevToolsが「>>」アイコンに隠されている、アイコンをクリックしたメニュー内に「axe DevTools」がある

****************
初期設定（推奨）
****************

より多くの項目をチェックするために、以下の初期設定を行うと良いでしょう。

1. :menuselection:`Options --> Settings` の順にクリック

   .. image:: /img/axe/axe-settings.png
      :alt: スクリーン・ショット：OptionsからSettingsを開こうとしている

2. "Best Practices" で "Enable" をチェック

   .. image:: /img/axe/axe-settings-best-practices.png
      :alt: スクリーン・ショット：Best Practicesの項目のEnableをチェックしている

3. 「保存」をクリック

****************************************
axe DevToolsで今見ているページを分析する
****************************************

分析対象のページを開いた状態でデベロッパーツール内のaxe DevToolsのタブを開き、「SCAN ALL OF MY PAGE」ボタンをクリックします。

.. image:: /img/axe/axe-8.png
   :alt: スクリーン・ショット：axe DevToolsタブ

今見ているページの問題を瞬時に発見することができます。

.. image:: /img/axe/axe-9.png
   :alt: スクリーン・ショット：表示されているページの問題をaxe DevToolsで表示している

**************
レポートの見方
**************

axe DevToolsの画面には発見された問題の件数が表示されるエリアと、その問題のリストが表示されるエリアがあります。

発見された問題の件数が表示されるエリアには、そのページにある問題の件数が表示されます。
ここで、axe DevTools内のUser Impact（当ガイドライン内での「重篤度」などの定義とは別のものです）や、「Best Practices」などを使ってリストをフィルターすることができます。

.. image:: /img/axe/axe-3.png
   :alt: スクリーン・ショット：発見された問題の件数が表示されるエリア

発見された問題のリストは、クリックで開くことでその問題の詳細ビューを見ることができます。

詳細ビューにはその問題が起きているHTML上の場所や、修正するための情報が表示されています。

.. image:: /img/axe/axe-4.png
   :alt: スクリーン・ショット：問題の詳細部分

同じ問題が複数箇所で見つかっている場合は、リスト上にその件数が表示され、詳細ビューのページャーで1つ1つ確認していくことができます。

.. image:: /img/axe/axe-pager.png
   :alt: スクリーン・ショット：詳細ビューにあるページャー

**********************************
axe DevToolsを使用する上での注意点
**********************************

*  モーダルやアコーディオンが開閉するような場所では、開いた状態や閉じた状態で何度かaxe DevToolsで分析してみる必要があります
*  axe DevToolsだけではすべての問題を発見することはできませんが、機械的に発見できる問題を瞬時に発見することができます。また、調査の必要そうな場所を発見するために非常に有用です。

.. include:: /inc/info2faq/exp-axe.rst

