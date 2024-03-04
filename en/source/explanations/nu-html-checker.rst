.. _exp-nu-html-checker:

###############################################
The Nu Html Checkerを用いたHTMLのバリデーション
###############################################

`The Nu Html Checker <v.nu_>`_ は、 `W3C <w3c_validator_>`_ や `WhatWG <https://whatwg.org/validator/>`_ でも利用されているHTMLのバリデーターです。
上記W3CまたはWhatWGのページにアクセスして、チェック対象のページのURLを入力して、HTMLの仕様に準拠しているかどうかをチェックするというのが一般的な使い方です。

しかし、この方法には以下の問題があります：

#. 開発中のページのように社外からアクセスできないページや、ログインが必要なページのチェックができない
#. 公開前のページなど、社外に出せないページのチェックに向いていない

以下の方法で、これらの問題に対応することができます。

************************
ブックマークレットの利用
************************

以下の手順でブックマークレットを利用することで、ブラウザーに表示中のページのDOMツリーを送信してチェックすることができます。

#. 以下のコードをターゲットとするブックマーク（ブックマークレット）を作成。

   .. raw:: html

      <details><summary>コードを表示</summary>

   .. code-block:: javascript

      javascript:(function(){function c(a,b){var c=document.createElement("textarea");c.name=a;c.value=b;d.appendChild(c)}var e=function(a){for(var b="",a=a.firstChild;a;){switch(a.nodeType){case Node.ELEMENT_NODE:b+=a.outerHTML;break;case Node.TEXT_NODE:b+=a.nodeValue;break;case Node.CDATA_SECTION_NODE:b+="<![CDATA["+a.nodeValue+"]]\>";break;case Node.COMMENT_NODE:b+="<\!--"+a.nodeValue+"--\>";break;case Node.DOCUMENT_TYPE_NODE:b+="<!DOCTYPE "+a.name+">\n"}a=a.nextSibling}return b}(document),d=document.createElement("form");d.method="POST";d.action="https://validator.w3.org/nu/";d.enctype="multipart/form-data";d.target="_blank";d.acceptCharset="utf-8";c("showsource","yes");c("content",e);document.body.appendChild(d);d.submit()})();


   .. raw:: html

      </details>
      <a href='javascript:(function(){function c(a,b){var c=document.createElement("textarea");c.name=a;c.value=b;d.appendChild(c)}var e=function(a){for(var b="",a=a.firstChild;a;){switch(a.nodeType){case Node.ELEMENT_NODE:b+=a.outerHTML;break;case Node.TEXT_NODE:b+=a.nodeValue;break;case Node.CDATA_SECTION_NODE:b+="<![CDATA["+a.nodeValue+"]]\>";break;case Node.COMMENT_NODE:b+="<\!--"+a.nodeValue+"--\>";break;case Node.DOCUMENT_TYPE_NODE:b+="<!DOCTYPE "+a.name+">\n"}a=a.nextSibling}return b}(document),d=document.createElement("form");d.method="POST";d.action="https://validator.w3.org/nu/";d.enctype="multipart/form-data";d.target="_blank";d.acceptCharset="utf-8";c("showsource","yes");c("content",e);document.body.appendChild(d);d.submit()})();'>表示中のページを https://validator.w3.org/nu/ に送信するブックマークレット</a>

#. チェック対象のページを表示した状態で、このブックマークレットを実行。

この方法を使えば、手元の開発環境だけにあるページのように、社外からアクセスできないページのチェックが可能です。
ただし、ページの内容は validator.w3.org に対して送信されますので、社外に一切出したくないページの場合には使えません。

************************
ローカルに実行環境を構築
************************

以下のいずれかの方法で、手元の開発環境や社内ネットワーク上にThe Nu Html Checkerの実行環境を構築することができます：

#. GitHubからパッケージまたはjarファイルを入手して実行。（jarファイルを利用する場合はJREが必要）

   適切に`JAVA_HOME`環境変数を設定したうえで、以下を実行::

   % java -cp vnu.jar nu.validator.servlet.Main 8888

#. dockerで実行::

   % docker run -it --rm -p 8888:8888 validator/validator:latest

この状態で、 http://localhost:8888/ にブラウザーでアクセスすると、Web UIが表示されます。

詳しい方法やこの他の方法については、 `Nu Html CheckerのGitHub <v.nu_>`_ 参照。

実行環境を構築できたら、前述のブックマークレット中の ``https://validator.w3.org/nu/`` を構築した環境のURLに書き替えて利用することで、チェックを実行することができます。

なお、jarファイルを使えばコマンド・ラインからThe Nu Html Checkerを実行することは可能ですが、この場合、ブラウザーにレンダーされる前のソースファイルに対するチェックになります。
そのため、JavaScriptでコンテンツが更新されるようなページのチェックには不向きです。

.. include:: /inc/info2gl/exp-nu-html-checker.rst

.. _v.nu: https://github.com/validator/validator/
.. _w3c_validator: https://validator.w3.org/nu/
