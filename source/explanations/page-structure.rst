.. _exp-page-structure:

################################################################################
適切なページ構造、マークアップとスクリーン・リーダーを用いた効率的な情報アクセス
################################################################################

ページを開いたり新たなページに遷移した直後、多くのスクリーン・リーダーでは自動的に ``title`` 要素の内用を読み上げます。
また、複数のウィンドウやタブを切り替えながら利用している場合、 ``title`` 要素の中身で目的のウィンドウ/タブかを判断します。
したがって、 ``title`` 要素の内用をそのページを特定できるものにすることが求められます。

目的のページにたどり着いたら、ユーザーはまずそのページに自分が求めている情報や機能があるかどうかを判断する場合が多いでしょう。
画面全体を一度に見ることができる場合、この判断は容易ですが、スクリーン・リーダーを使っているユーザーの多くは、ある程度ページの中身を読まないと判断することが困難です。

多くのスクリーン・リーダーには、ARIAランドマークで示される複数の領域の間を移動する機能があります。

ARIAランドマークで示される領域とは、 ``header`` 要素、 ``nav`` 要素、 ``main`` 要素、 ``footer`` 要素、 ``aside`` 要素などで、ページを構成する領域を示したものです。
これらの要素の代わりに、 ``div`` 要素などに対して ``role`` 属性を用いて明示する方法もあります。

ページ上に存在する領域を確認するには、ページのソースを確認するか、Chrome拡張、Firefoxアドオン、Opera拡張、Edgeアドオンとして提供されている `Landmark Navigation via Keyboard or Pop-up <https://matatk.agrip.org.uk/landmarks/>`_ のようなツールを活用すると良いでしょう。

ページを構成するすべての要素が適切な領域に含まれていれば、ユーザーは斜め読みのような形でページ全体の構成を把握することができ、また目的の情報が掲載されているかどうかの判断や目的の情報を迅速に見つけることに役立てることができます。

ARIAランドマークについて詳しくは、以下のMDNの記事を参考にしてください：

*  `ARIA: banner ロール <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles/Banner_role>`_
*  `ARIA: complementary ロール <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles/Complementary_role>`_
*  `ARIA: contentinfo ロール <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles/Contentinfo_role>`_
*  `ARIA: form ロール <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles/Form_Role>`_
*  `ARIA: main ロール <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles/Main_role>`_
*  `ARIA: navigation ロール <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles/Navigation_Role>`_
*  `ARIA: region ロール <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles/Region_role>`_
*  `ARIA: search ロール <https://developer.mozilla.org/ja/docs/Web/Accessibility/ARIA/Roles/Search_role>`_

さらに、特に長いページにおいてより効率的な斜め読みを可能にするためには、 ``h?`` 要素を用いてページ内に複数の見出しを配置することが有効です。
ただ、コンテンツの量や性質によっては、複数の見出しを配置することが必ずしも適当ではない場合もありますので注意が必要です。

複数の見出しがあるページの場合、ページ内の情報の構造に合わせて適切な見出しレベルを用いることが重要です。
たとえば、記事のタイトルは ``h1`` 要素、記事中の小見出しは ``h2`` 要素、さらに仮想の見出しは ``h3`` 要素を用いる、といった具合です。

実際にコンテンツを読み始めるとき、ナビゲーションのリンクなどを飛ばして本文の先頭に移動することになります。
本文部分が ``main`` 要素でマークアップされていたり、本文の先頭の見出しが ``h1`` でマークアップされていれば、スクリーン・リーダーの機能を活用して本文の先頭に容易に移動することが可能です。

そしてさらに読み進めていくに当たっては、スクリーン・リーダーはDOM treeに出現する順序（≒HTMLソースの記述順序）に従って読み上げます。
そのため、画面上ではCSSによって隣接した位置に表示されている要素であっても、DOM tree上で離れた位置にあれば、画面表示と読み上げの順序が異なることになります。
当該要素が隣接していることで、その意味が伝わりやすいような場合は特に、DOM tree上の順序が適切になっていることが重要です。

なお、ユーザーの操作によって表示されるコンテンツが変化するようなページについては、さらに注意が必要です。
:ref:`exp-dynamic-content-maintain-dom-tree` も合わせて参照してください。

.. include:: /inc/info2gl/exp-page-structure.rst
