ここで掲載している情報は、 `axe-coreのGitHubリポジトリー <https://github.com/dequelabs/axe-core/>`_ の以下に示す時点におけるdevelopブランチの内容に基づいて自動的に生成したものです。axe DevToolsの内容とは一致していない場合もあることにご注意ください。

バージョン
   4.2.3
更新日時
   2021-07-02 18:07:21++0900

.. _axe-rule-area-alt:

アクティブな<area>要素には代替テキストが存在しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

イメージマップの<area>要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/area-alt>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.1.1

   -  |SC 1.1.1|
   -  |SC 1.1.1ja|

*  達成基準 2.4.4

   -  |SC 2.4.4|
   -  |SC 2.4.4ja|

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-visible-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-visible-label.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-description`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-description.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-decorative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-decorative.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-provide-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-provide-text.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-perceivable.rst

   .. raw:: html

      </details>

*  リンク： :ref:`gl-link-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-link-text.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-allowed-attr:

要素には許可されているARIA属性のみを使用しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

要素のロールにARIA属性が許可されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-allowed-attr>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-command-name:

ARIAコマンドにはアクセシブルな名前がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIA button、link、menuitemにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-command-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-hidden-body:

ドキュメント本体にaria-hidden='true'が存在してはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ドキュメント本体にaria-hidden='true'が存在していないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-hidden-body>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-hidden-focus:

ARIA hidden要素にフォーカス可能な要素を含んではなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

aria-hidden要素にフォーカス可能な要素が含まれていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-hidden-focus>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-input-field-name:

ARIA入力欄にアクセシブルな名前があります
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIA入力欄にアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-input-field-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-meter-name:

ARIA meterノードにはアクセシブルな名前がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIA meterノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-meter-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.1.1

   -  |SC 1.1.1|
   -  |SC 1.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-visible-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-visible-label.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-description`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-description.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-decorative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-decorative.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-provide-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-provide-text.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-perceivable.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-progressbar-name:

ARIA progressbarノードにはアクセシブルな名前がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIA progressbarノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-progressbar-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.1.1

   -  |SC 1.1.1|
   -  |SC 1.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-visible-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-visible-label.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-description`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-description.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-decorative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-decorative.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-provide-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-provide-text.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-perceivable.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-required-attr:

必須のARIA属性が提供されていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ARIAロールのある要素にすべての必須ARIA属性が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-required-attr>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-required-children:

特定のARIAロールには特定の子が含まれていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

子ロールを必須とするARIAロールが指定された要素に、それらが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-required-children>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-required-parent:

特定のARIAロールは特定の親に含まれていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

親ロールを必須とするARIAロールが指定された要素に、それらが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-required-parent>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-roledescription:

aria-roledescriptionはセマンティックなロールを持った要素に使用します
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

aria-roledescriptionが暗黙的もしくは明示的なロールを持った要素に使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-roledescription>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-roles:

使用されているARIAロールは有効な値に一致しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのロール属性が指定された要素で、有効な値が使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-roles>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-toggle-field-name:

ARIAトグル欄にアクセシブルな名前があります
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIAトグル欄にアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-toggle-field-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-tooltip-name:

ARIA tooltipノードにはアクセシブルな名前がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIA tooltipノードにはアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-tooltip-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-valid-attr:

ARIA属性は有効な名前に一致しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

aria- で始まる属性が有効なARIA属性であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-valid-attr>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-aria-valid-attr-value:

ARIA属性は有効な値に一致しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIA属性に有効な値が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-valid-attr-value>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-audio-caption:

<audio>要素にはキャプショントラックが存在しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<audio>要素にキャプションが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/audio-caption>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.2.1

   -  |SC 1.2.1|
   -  |SC 1.2.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  音声・映像コンテンツ： :ref:`gl-multimedia-text-alternative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-text-alternative.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-transcript`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-transcript.rst

   .. raw:: html

      </details>


.. _axe-rule-avoid-inline-spacing:

インラインのテキスト間隔設定はカスタムスタイルシートによって調整可能でなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

style属性で指定されたテキストの間隔は、カスタムスタイルシートにより調整可能であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/avoid-inline-spacing>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.4.12

   -  |SC 1.4.12|
   -  |SC 1.4.12ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  テキスト： :ref:`gl-text-customize`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-text-customize.rst

   .. raw:: html

      </details>


.. _axe-rule-blink:

<blink>要素は廃止されており、使用するべきではありません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<blink>要素が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/blink>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.2.2

   -  |SC 2.2.2|
   -  |SC 2.2.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  動的コンテンツ： :ref:`gl-dynamic-content-pause-movement`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-dynamic-content-pause-movement.rst

   .. raw:: html

      </details>

*  動的コンテンツ： :ref:`gl-dynamic-content-pause-refresh`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-dynamic-content-pause-refresh.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-pause-movement`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-pause-movement.rst

   .. raw:: html

      </details>


.. _axe-rule-button-name:

ボタンには認識可能なテキストが存在しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ボタンに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/button-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-bypass:

ページには繰り返されるブロックをスキップする手段が存在しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

各ページに少なくとも1つ、ユーザーがナビゲーション部分をスキップして直接本文へ移動できるメカニズムが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/bypass>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.4.1

   -  |SC 2.4.1|
   -  |SC 2.4.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  ページ全体： :ref:`gl-page-markup-main`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-markup-main.rst

   .. raw:: html

      </details>


.. _axe-rule-color-contrast:

要素には十分な色のコントラストがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

前景色と背景色のコントラストがWCAG 2のAAコントラスト比のしきい値を満たすことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/color-contrast>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.4.3

   -  |SC 1.4.3|
   -  |SC 1.4.3ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  画像： :ref:`gl-image-text-contrast`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-text-contrast.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-text-contrast`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-text-contrast.rst

   .. raw:: html

      </details>

*  テキスト： :ref:`gl-text-contrast`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-text-contrast.rst

   .. raw:: html

      </details>


.. _axe-rule-css-orientation-lock:

ディスプレイの向きを固定するためにCSSメディアクエリーは使用されていません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンテンツが特定のディスプレイの向きに固定されていないこと、およびコンテンツがすべてのディスプレイの向きで操作可能なことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/css-orientation-lock>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.4

   -  |SC 1.3.4|
   -  |SC 1.3.4ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  ページ全体： :ref:`gl-page-orientation`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-orientation.rst

   .. raw:: html

      </details>


.. _axe-rule-definition-list:

<dl>要素は、適切な順序で並べられた<dt>および<dd>グループ、<script>要素または<template>要素のみを直接含んでいなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<dl>要素の構造が正しいことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/definition-list>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-dlitem:

<dt>および<dd>要素は<dl>に含まれていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<dt>および<dd>要素が<dl>に含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/dlitem>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-document-title:

ドキュメントにはナビゲーションを補助するために<title>要素がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

各HTMLドキュメントに空ではない<title>要素が含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/document-title>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.4.2

   -  |SC 2.4.2|
   -  |SC 2.4.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  ページ全体： :ref:`gl-page-title`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-title.rst

   .. raw:: html

      </details>


.. _axe-rule-duplicate-id:

id属性値は一意でなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのid属性値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/duplicate-id>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.1

   -  |SC 4.1.1|
   -  |SC 4.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-valid`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-valid.rst

   .. raw:: html

      </details>


.. _axe-rule-duplicate-id-active:

活性要素のIDは一意でなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

活性要素のid属性値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/duplicate-id-active>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.1

   -  |SC 4.1.1|
   -  |SC 4.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-valid`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-valid.rst

   .. raw:: html

      </details>


.. _axe-rule-duplicate-id-aria:

ARIAおよびラベルに使用されているIDは一意でなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ARIAおよびラベルに使用されているすべてのid属性値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/duplicate-id-aria>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.1

   -  |SC 4.1.1|
   -  |SC 4.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-valid`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-valid.rst

   .. raw:: html

      </details>


.. _axe-rule-empty-table-header:

テーブルのヘッダーは空にしてはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

テーブルのヘッダーに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/empty-table-header>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-form-field-multiple-labels:

複数のlabel要素をフォームフィールドに付与するべきではありません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

フォームフィールドに複数のlabel要素が存在しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/form-field-multiple-labels>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 3.3.2

   -  |SC 3.3.2|
   -  |SC 3.3.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>


.. _axe-rule-frame-focusable-content:

tabindex=-1が指定されているフレームには、フォーカス可能なコンテンツが含まれていてはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

tabindex=-1が指定されている<frame>と<iframe>要素が、フォーカス可能なコンテンツを含まないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/frame-focusable-content>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.1.1

   -  |SC 2.1.1|
   -  |SC 2.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-input-device-keyboard-operable.rst

   .. raw:: html

      </details>


.. _axe-rule-frame-title:

フレームにはtitle属性がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<iframe>および<frame>要素に空ではないtitle属性が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/frame-title>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.4.1

   -  |SC 2.4.1|
   -  |SC 2.4.1ja|

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  ページ全体： :ref:`gl-page-markup-main`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-markup-main.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-html-has-lang:

<html>要素にはlang属性がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのHTMLドキュメントにlang属性が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/html-has-lang>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 3.1.1

   -  |SC 3.1.1|
   -  |SC 3.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  テキスト： :ref:`gl-text-page-lang`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-text-page-lang.rst

   .. raw:: html

      </details>


.. _axe-rule-html-lang-valid:

<html>要素のlang属性には有効な値がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<html>要素のlang属性に有効な値があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/html-lang-valid>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 3.1.1

   -  |SC 3.1.1|
   -  |SC 3.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  テキスト： :ref:`gl-text-page-lang`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-text-page-lang.rst

   .. raw:: html

      </details>


.. _axe-rule-html-xml-lang-mismatch:

HTML要素に指定されたlangおよびxml:lang属性は同じ基本言語を持たなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTML要素に指定された有効なlangおよびxml:lang属性の両方がページの基本言語と一致することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/html-xml-lang-mismatch>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 3.1.1

   -  |SC 3.1.1|
   -  |SC 3.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  テキスト： :ref:`gl-text-page-lang`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-text-page-lang.rst

   .. raw:: html

      </details>


.. _axe-rule-image-alt:

画像には代替テキストがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<img>要素に代替テキストが存在する、またはnoneまたはpresentationのロールが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/image-alt>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.1.1

   -  |SC 1.1.1|
   -  |SC 1.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-visible-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-visible-label.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-description`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-description.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-decorative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-decorative.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-provide-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-provide-text.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-perceivable.rst

   .. raw:: html

      </details>


.. _axe-rule-input-button-name:

入力ボタンには認識可能なテキストが存在しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

入力ボタンに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/input-button-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-input-image-alt:

画像ボタンには代替テキストがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<input type="image">要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/input-image-alt>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.1.1

   -  |SC 1.1.1|
   -  |SC 1.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-visible-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-visible-label.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-description`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-description.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-decorative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-decorative.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-provide-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-provide-text.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-perceivable.rst

   .. raw:: html

      </details>


.. _axe-rule-label:

フォーム要素にはラベルがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのフォーム要素にラベルが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/label>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-label-content-name-mismatch:

要素の視認できるテキストはそれらのアクセシブルな名前の一部でなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンテンツによってラベル付けされた要素は、それらの視認できるテキストがアクセシブルな名前の一部になっていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/label-content-name-mismatch>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.5.3

   -  |SC 2.5.3|
   -  |SC 2.5.3ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>


.. _axe-rule-link-in-text-block:

リンクは色に依存しない方法で周囲のテキストと区別できなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

色に依存することなくリンクを区別できます

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/link-in-text-block>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.4.1

   -  |SC 1.4.1|
   -  |SC 1.4.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-color-only`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-color-only.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-color-only`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-color-only.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-color-only`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-color-only.rst

   .. raw:: html

      </details>

*  リンク： :ref:`gl-link-color-only`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-link-color-only.rst

   .. raw:: html

      </details>

*  テキスト： :ref:`gl-text-color-only`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-text-color-only.rst

   .. raw:: html

      </details>


.. _axe-rule-link-name:

リンクには認識可能なテキストがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

リンクに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/link-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

*  達成基準 2.4.4

   -  |SC 2.4.4|
   -  |SC 2.4.4ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>

*  リンク： :ref:`gl-link-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-link-text.rst

   .. raw:: html

      </details>


.. _axe-rule-list:

<ul>および<ol>の直下には<li>、<script>または<template>要素のみを含まなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

リストが正しく構造化されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/list>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-listitem:

<li>要素は<ul>または<ol>内に含まれていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<li>要素がセマンティックに使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/listitem>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-marquee:

<marquee>要素は非推奨のため、使用してはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<marquee>要素が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/marquee>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.2.2

   -  |SC 2.2.2|
   -  |SC 2.2.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  動的コンテンツ： :ref:`gl-dynamic-content-pause-movement`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-dynamic-content-pause-movement.rst

   .. raw:: html

      </details>

*  動的コンテンツ： :ref:`gl-dynamic-content-pause-refresh`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-dynamic-content-pause-refresh.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-pause-movement`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-pause-movement.rst

   .. raw:: html

      </details>


.. _axe-rule-meta-refresh:

制限時間のある更新が存在してはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<meta http-equiv="refresh">が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/meta-refresh>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.2.1

   -  |SC 2.2.1|
   -  |SC 2.2.1ja|

*  達成基準 2.2.4

   -  |SC 2.2.4|
   -  |SC 2.2.4ja|

*  達成基準 3.2.5

   -  |SC 3.2.5|
   -  |SC 3.2.5ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-timing`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-timing.rst

   .. raw:: html

      </details>

*  ログイン・セッション： :ref:`gl-login-session-timing`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-login-session-timing.rst

   .. raw:: html

      </details>

*  動的コンテンツ： :ref:`gl-dynamic-content-no-interrupt`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-dynamic-content-no-interrupt.rst

   .. raw:: html

      </details>


.. _axe-rule-nested-interactive:

対話的なコントロールがネストされていないことを確認します
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ネストされた対話的なコントロールはスクリーン・リーダーで読み上げられません

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/nested-interactive>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>


.. _axe-rule-no-autoplay-audio:

<video> または <audio> 要素は音声を自動再生しません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<video> または <audio> 要素が音声を停止またはミュートするコントロールなしに音声を3秒より長く自動再生しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/no-autoplay-audio>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.4.2

   -  |SC 1.4.2|
   -  |SC 1.4.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  音声・映像コンテンツ： :ref:`gl-multimedia-operable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-operable.rst

   .. raw:: html

      </details>


.. _axe-rule-object-alt:

<object>要素には代替テキストがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<object>要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/object-alt>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.1.1

   -  |SC 1.1.1|
   -  |SC 1.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-visible-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-visible-label.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-description`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-description.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-decorative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-decorative.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-provide-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-provide-text.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-perceivable.rst

   .. raw:: html

      </details>


.. _axe-rule-p-as-heading:

p要素を見出しとしてスタイル付けするために太字、イタリック体、およびフォントサイズを使用しません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

見出しのスタイル調整のためにp要素が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/p-as-heading>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-role-img-alt:

[role='img'] 要素に代替テキストが必要です
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[role='img'] 要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/role-img-alt>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.1.1

   -  |SC 1.1.1|
   -  |SC 1.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-visible-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-visible-label.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-description`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-description.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-decorative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-decorative.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-provide-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-provide-text.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-perceivable.rst

   .. raw:: html

      </details>


.. _axe-rule-scrollable-region-focusable:

スクロール可能な領域にキーボードでアクセスできるようにします
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スクロール可能なコンテンツを持つ要素はキーボードでアクセスできるようにするべきです

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/scrollable-region-focusable>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.1.1

   -  |SC 2.1.1|
   -  |SC 2.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-input-device-keyboard-operable.rst

   .. raw:: html

      </details>


.. _axe-rule-select-name:

select要素にはアクセシブルな名前がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

select要素にはアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/select-name>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 4.1.2

   -  |SC 4.1.2|
   -  |SC 4.1.2ja|

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  マークアップ全般： :ref:`gl-markup-component`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-component.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-server-side-image-map:

サーバーサイドのイメージマップを使用してはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

サーバーサイドのイメージマップが使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/server-side-image-map>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.1.1

   -  |SC 2.1.1|
   -  |SC 2.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-input-device-keyboard-operable.rst

   .. raw:: html

      </details>


.. _axe-rule-svg-img-alt:

img ロールを持つ svg 要素に代替テキストが存在します
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

img、graphics-document または graphics-symbol ロールを持つ svg 要素にアクセシブルなテキストがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/svg-img-alt>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.1.1

   -  |SC 1.1.1|
   -  |SC 1.1.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  アイコン： :ref:`gl-icon-visible-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-icon-visible-label.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-description`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-description.rst

   .. raw:: html

      </details>

*  画像： :ref:`gl-image-decorative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-image-decorative.rst

   .. raw:: html

      </details>

*  画像化されたテキスト： :ref:`gl-iot-provide-text`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-iot-provide-text.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-perceivable.rst

   .. raw:: html

      </details>


.. _axe-rule-table-fake-caption:

データテーブルにキャプションをつけるためにデータまたはヘッダーセルを用いるべきではありません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

キャプション付きのテーブルが<caption>要素を用いていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/table-fake-caption>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-td-has-header:

3×3より大きいテーブルの空ではないtd要素はテーブルヘッダーと関連づいていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

大きなテーブルの空ではないデータセルに1つかそれ以上のテーブルヘッダーが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/td-has-header>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-td-headers-attr:

table要素内のheaders属性を使用するすべてのセルは同じ表内の他のセルのみを参照しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ヘッダーを使用しているテーブル内の各セルが、そのテーブル内の他のセルを参照していることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/td-headers-attr>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-th-has-data-cells:

すべてのth要素およびrole=columnheader/rowheaderを持つ要素にはそれらが説明するデータセルがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

データテーブルのテーブルヘッダーがデータセルを参照していることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/th-has-data-cells>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.1

   -  |SC 1.3.1|
   -  |SC 1.3.1ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  フォーム： :ref:`gl-form-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-label.rst

   .. raw:: html

      </details>

*  フォーム： :ref:`gl-form-hidden-label`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-form-hidden-label.rst

   .. raw:: html

      </details>

*  マークアップ全般： :ref:`gl-markup-semantics`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-markup-semantics.rst

   .. raw:: html

      </details>

*  ページ全体： :ref:`gl-page-landmark`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-page-landmark.rst

   .. raw:: html

      </details>


.. _axe-rule-valid-lang:

lang属性には有効な値がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lang属性に有効な値が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/valid-lang>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 3.1.2

   -  |SC 3.1.2|
   -  |SC 3.1.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  テキスト： :ref:`gl-text-phrase-lang`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-text-phrase-lang.rst

   .. raw:: html

      </details>


.. _axe-rule-video-caption:

<video>要素にはキャプションがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<video>要素にキャプションが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/video-caption>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.2.2

   -  |SC 1.2.2|
   -  |SC 1.2.2ja|

関連するガイドラインとチェック内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  音声・映像コンテンツ： :ref:`gl-multimedia-text-alternative`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-text-alternative.rst

   .. raw:: html

      </details>

*  音声・映像コンテンツ： :ref:`gl-multimedia-caption`

   .. raw:: html

      <details><summary>チェック内容</summary>

   .. include:: /checks/inc/gl-multimedia-caption.rst

   .. raw:: html

      </details>


.. _axe-rule-autocomplete-valid:

autocomplete属性は正しく使用しなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

autocomplete属性が正しく、かつフォームフィールドに対して適切であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/autocomplete-valid>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 1.3.5

   -  |SC 1.3.5|
   -  |SC 1.3.5ja|


.. _axe-rule-identical-links-same-purpose:

同じ名前を持つ複数のリンクは同様の目的を持っています
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

同じアクセシブルな名前を持つ複数のリンクが同様の目的を果たすことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/identical-links-same-purpose>`__

関連するWCAG 2.1の達成基準
^^^^^^^^^^^^^^^^^^^^^^^^^^

*  達成基準 2.4.9

   -  |SC 2.4.9|
   -  |SC 2.4.9ja|


.. _axe-rule-accesskeys:

accesskey属性値は一意でなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのaccesskey属性値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/accesskeys>`__


.. _axe-rule-aria-allowed-role:

ARIAロールは要素に対して適切でなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

role属性の値が要素に対して適切であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-allowed-role>`__


.. _axe-rule-aria-dialog-name:

ARIA dialogとalertdialogノードにはアクセシブルな名前がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIA dialog、alertdialogノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-dialog-name>`__


.. _axe-rule-aria-text:

"role=text"が指定されている要素には、フォーカス可能な子孫が含まれていてはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

role="text"が指定されている要素にフォーカス可能な子孫がないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-text>`__


.. _axe-rule-aria-treeitem-name:

ARIA treeitemノードにはアクセシブルな名前がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのARIA treeitemノードにはアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/aria-treeitem-name>`__


.. _axe-rule-empty-heading:

見出しは空にしてはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

見出しに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/empty-heading>`__


.. _axe-rule-focus-order-semantics:

フォーカス順序に含まれる要素には、インタラクティブコンテンツに適したロールが必要です
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

フォーカス順序に含まれる要素に適切なロールがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/focus-order-semantics>`__


.. _axe-rule-frame-tested:

フレームはaxe-coreでテストする必要があります
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<iframe>および<frame>要素にaxe-coreスクリプトが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/frame-tested>`__


.. _axe-rule-frame-title-unique:

フレームには一意のtitle属性がなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<iframe>および<frame>要素に一意のtitle属性が含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/frame-title-unique>`__


.. _axe-rule-heading-order:

見出しのレベルは1つずつ増加させなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

見出しの順序が意味的に正しいことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/heading-order>`__


.. _axe-rule-hidden-content:

ページ上の隠れているコンテンツは分析できません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

隠れているコンテンツについてユーザーに通知します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/hidden-content>`__


.. _axe-rule-image-redundant-alt:

画像の代替テキストはテキストとして繰り返されるべきではありません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

画像の代替がテキストとして繰り返されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/image-redundant-alt>`__


.. _axe-rule-label-title-only:

フォーム要素には視認できるラベルがなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのフォーム要素がtitleまたはaria-describedby属性を使用して単独でラベル付けされていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/label-title-only>`__


.. _axe-rule-landmark-banner-is-top-level:

bannerランドマークは他のランドマークに含まれるべきではありません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

bannerランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-banner-is-top-level>`__


.. _axe-rule-landmark-complementary-is-top-level:

他の要素にasideを含んではなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

complementaryランドマークあるいはasideがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-complementary-is-top-level>`__


.. _axe-rule-landmark-contentinfo-is-top-level:

contentinfoランドマークは他のランドマークに含まれるべきではありません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

contentinfoランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-contentinfo-is-top-level>`__


.. _axe-rule-landmark-main-is-top-level:

mainランドマークは他のランドマークに含まれるべきではありません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mainランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-main-is-top-level>`__


.. _axe-rule-landmark-no-duplicate-banner:

ドキュメントに複数のbannerランドマークが存在してはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ドキュメント内のbannerランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-no-duplicate-banner>`__


.. _axe-rule-landmark-no-duplicate-contentinfo:

ドキュメントに複数のcontentinfoランドマークが存在してはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ドキュメント内のcontentinfoランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-no-duplicate-contentinfo>`__


.. _axe-rule-landmark-no-duplicate-main:

ドキュメントに複数のmainランドマークが存在してはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ドキュメント内のmainランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-no-duplicate-main>`__


.. _axe-rule-landmark-one-main:

ドキュメントにはmainランドマークが1つ含まれていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ドキュメントのランドマークが1つのみであること、およびページ内の各iframeのランドマークが最大で1つであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-one-main>`__


.. _axe-rule-landmark-unique:

ランドマークが一意であることを確認します
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ランドマークは一意のロール又はロール／ラベル／タイトル (例: アクセシブルな名前) の組み合わせがなければなりません

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/landmark-unique>`__


.. _axe-rule-meta-viewport:

ズーミングや拡大縮小は無効にしてはなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<meta name="viewport">がテキストの拡大縮小およびズーミングを無効化しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/meta-viewport>`__


.. _axe-rule-meta-viewport-large:

ユーザーがズームをしてテキストを最大500％まで拡大できるようにするべきです
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<meta name="viewport">で大幅に拡大縮小できることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/meta-viewport-large>`__


.. _axe-rule-page-has-heading-one:

ページにはレベル1の見出しが含まれていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ページ、またはそのフレームの少なくとも1つにはレベル1の見出しが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/page-has-heading-one>`__


.. _axe-rule-presentation-role-conflict:

roleがnoneまたはpresentationの要素をマークしなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

roleがnoneまたはpresentationで、roleの競合の解決が必要な要素をマークします

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/presentation-role-conflict>`__


.. _axe-rule-region:

ページのすべてのコンテンツはlandmarkに含まれていなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ページのすべてのコンテンツがlandmarkに含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/region>`__


.. _axe-rule-scope-attr-valid:

scope属性は正しく使用されなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

scope属性がテーブルで正しく使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/scope-attr-valid>`__


.. _axe-rule-skip-link:

スキップリンクのターゲットが存在し、フォーカス可能でなければなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのスキップリンクにフォーカス可能なターゲットがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/skip-link>`__


.. _axe-rule-tabindex:

要素に0より大きいtabindex属性を指定するべきではありません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

tabindex属性値が0より大きくないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/tabindex>`__


.. _axe-rule-table-duplicate-name:

<caption>要素にsummary属性と同じテキストを含んではなりません
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

テーブルのサマリーとキャプションが同一ではないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.2/table-duplicate-name>`__


