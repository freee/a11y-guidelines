.. _exp-target-size:

################################################################################
クリックやタッチのターゲット・サイズに関連する問題とターゲット・サイズの確認方法
################################################################################

上肢が不自由なユーザーは、細かい操作が苦手な場合があります。
また、ロービジョンのユーザーの中にも細かいマウス操作が苦手なユーザーがいます。

アイコンやフォーム・コントロールにおいて、クリックやタッチに反応する領域のサイズ（ターゲット・サイズ）が小さすぎると、このようなユーザーにとって、目的の箇所をクリック/タッチすることが困難になります。

なお、フォーム・コントロールについてWCAGでは、ブラウザーのデフォルト表示から見た目を変更していない場合は、ターゲット・サイズに関する条件を満たす必要はないとしています。
また、フォーム・コントロールについては、フォーム・フィールドのラベルを適切にマークアップすることで、ラベルもクリック/タッチのターゲットの一部になり、ターゲット・サイズを大きくすることができます。

*********************************************
クリック/タッチのターゲット・サイズの確認方法
*********************************************

クリックやタッチを受け取る要素のサイズは、ブラウザーの開発者ツールを用いれば確認することができます。
ただ、この方法の場合、サイズを確認する要素を正確に指定する必要があることに加えて、複雑な方法でサイズが制御されているような場合もあるため、正確に判断することが容易ではない場合もあります。

そこで、1辺が44pxの正方形を画面上に表示し、この正方形とターゲットのサイズを比較するという簡易的な方法を併用すると良いでしょう。

具体的には、以下のブックマークレットを利用することで、1辺が44pxの赤枠の正方形の内側に、1辺が24pxの青枠の正方形をマウスに追従する形で表示することができます。

#. 以下のコードをターゲットとするブックマーク（ブックマークレット）を作成。

   .. raw:: html

      <details><summary>コードを表示</summary>

   .. code-block:: javascript

      javascript:(function(){var d = document,e=d.createElement('div'),g=d.createElement('div'),w=window;d.body.appendChild(e);e.appendChild(g);e.setAttribute('style','position:absolute;top:0;left:0;z-index:2147483647;box-sizing:border-box;width:44px;height:44px;border:1px solid #f00;background:#fff;opacity:0.5;transform: translate(-50%,-50%);pointer-events:none;');g.setAttribute('style','position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);box-sizing:border-box;width:24px;height:24px;border:1px solid #00f;');w.onmousemove=(function(v){e.style.left=w.scrollX+v.clientX+'px';e.style.top=w.scrollY+v.clientY+'px'})})()

   .. raw:: html

      </details>
      <a href="javascript:(function(){var d = document,e=d.createElement('div'),g=d.createElement('div'),w=window;d.body.appendChild(e);e.appendChild(g);e.setAttribute('style','position:absolute;top:0;left:0;z-index:2147483647;box-sizing:border-box;width:44px;height:44px;border:1px solid #f00;background:#fff;opacity:0.5;transform: translate(-50%,-50%);pointer-events:none;');g.setAttribute('style','position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);box-sizing:border-box;width:24px;height:24px;border:1px solid #00f;');w.onmousemove=(function(v){e.style.left=w.scrollX+v.clientX+'px';e.style.top=w.scrollY+v.clientY+'px'})})()">44x44 pxの4角形を表示するブックマークレット</a>

#. チェック対象のページを表示した状態で、このブックマークレットを実行。

.. include:: /inc/info2gl/exp-target-size.rst

.. include:: /inc/info2faq/exp-target-size.rst
