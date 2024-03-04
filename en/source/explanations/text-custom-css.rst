.. _exp-text-custom-css:

#######################################
ユーザーCSSを適用したチェックの実施方法
#######################################

ロービジョンのユーザー、ディスレクシアのユーザーのように読みに困難があるユーザーの中には、文字の表示方法をカスタマイズすることで、テキスト情報を理解しやすくなるユーザーがいます。
このようなユーザーは、支援技術を用いて表示をカスタマイズしている場合もありますし、拡張機能などを用いてユーザーCSSを適用している場合もあるでしょう。

以下、ガイドラインが求めるカスタマイズを実現するための方法を示します。

*****************************************
ガイドラインが求める条件を満たすためのCSS
*****************************************

ガイドラインが求める条件は、以下のCSSの通りです：

.. code-block:: css

   * {
     line-height: 1.5em !important;
     letter-spacing: 0.12em !important;
   }
   p + * {
     margin-top: 2em !important;
   }

このCSSをユーザーCSSとしてブラウザーに設定すれば良いわけですが、例えばGoogle ChromeではユーザーCSSを指定する機能は廃止されているようですし、他のブラウザーでもその設定方法があまり分かりやすいとはいえません。
日常的にユーザーCSSを活用しているユーザーは、ブラウザーの拡張機能を活用するなどして、ユーザーCSSを適用しているものと考えられます。

チェックに当たっては、以下に示すブックマークレットを活用する方法が便利でしょう。

************************
ブックマークレットの利用
************************

以下の手順でブックマークレットを利用することで、ガイドラインが求める条件のカスタムCSSをブラウザーに表示中のページに適用した表示を確認することができます。

#. 以下のコードをターゲットとするブックマーク（ブックマークレット）を作成。

   .. raw:: html

      <details><summary>コードを表示</summary>

   .. code-block:: javascript

      javascript:(function(){var d=document,s=d.createElement('style');s.innerHTML='*{line-height:1.5em !important;letter-spacing: 0.12em !important;} p+*{margin-top: 2em !important;}';d.head.appendChild(s)})()

   .. raw:: html

      </details>
      <a href="javascript:(function(){var d=document,s=d.createElement('style');s.innerHTML='*{line-height:1.5em !important;letter-spacing: 0.12em !important;} p+*{margin-top: 2em !important;}';d.head.appendChild(s)})()">表示中のページにカスタムCSSを適用するブックマークレット</a>

#. チェック対象のページを表示した状態で、このブックマークレットを実行。

.. include:: /inc/info2gl/exp-text-custom-css.rst
