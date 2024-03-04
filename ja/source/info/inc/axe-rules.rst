ここで掲載している情報は、 `axe-coreのGitHubリポジトリー <https://github.com/dequelabs/axe-core/>`_ の以下に示す時点におけるdevelopブランチの内容に基づいて自動的に生成したものです。axe DevToolsの内容とは一致していない場合もあることにご注意ください。

バージョン
   4.8.1
更新日時
   2023-09-12 06:45:57+0900

.. _axe-rule-area-alt:

******************************************************************************************************************
アクティブな<area>要素には代替テキストが存在しなければなりません (Active <area> elements must have alternate text)
******************************************************************************************************************

イメージマップの<area>要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/area-alt>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.4.4

   -  `Link Purpose (In Context) <https://www.w3.org/TR/WCAG21/#link-purpose-in-context>`_
   -  `リンクの目的 (コンテキスト内) <https://waic.jp/translations/WCAG21/#link-purpose-in-context>`_

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  リンク： :ref:`gl-link-text`
*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-allowed-attr:

*******************************************************************************************************************
要素にはサポートされているARIA属性のみを使用しなければなりません (Elements must only use supported ARIA attributes)
*******************************************************************************************************************

要素のロールがARIA属性をサポートしていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-allowed-attr>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-braille-equivalent:

****************************************************************************************************************************
aria-braille属性には、点じ以外の同等のものがなければなりません  (aria-braille attributes must have a non-braille equivalent)
****************************************************************************************************************************

aria-braillelabelとaria-brailleroledescriptionには、点字以外の同等のものが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-braille-equivalent>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-command-name:

***************************************************************************************************
ARIAコマンドにはアクセシブルな名前がなければなりません (ARIA commands must have an accessible name)
***************************************************************************************************

すべてのARIA button、link、menuitemにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-command-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-conditional-attr:

*******************************************************************************************************************************
ARIA属性は要素のロールの仕様に従って使用しなければなりません (ARIA attributes must be used as specified for the element's role)
*******************************************************************************************************************************

ARIA属性が要素のロールの仕様に従って使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-conditional-attr>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-deprecated-role:

*********************************************************************************
非推奨のARIAロールを使用してはなりません (Deprecated ARIA roles must not be used)
*********************************************************************************

要素に非推奨のロールが使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-deprecated-role>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-hidden-body:

************************************************************************************************************************
ドキュメント本体にaria-hidden="true"が存在してはなりません (aria-hidden="true" must not be present on the document body)
************************************************************************************************************************

ドキュメント本体にaria-hidden="true"が存在しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-hidden-body>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-hidden-focus:

*****************************************************************************************************************************************************************************************
aria-hiddenが指定されている要素は、フォーカス可能であったり、フォーカス可能な要素を含んでいたりしてはなりません (ARIA hidden element must not be focusable or contain focusable elements)
*****************************************************************************************************************************************************************************************

aria-hiddenが指定されている要素にフォーカスできないこと、その要素にフォーカス可能な要素が含まれていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-hidden-focus>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-input-field-name:

*****************************************************************************************************
ARIA入力欄にはアクセシブルな名前がなければなりません (ARIA input fields must have an accessible name)
*****************************************************************************************************

すべてのARIA入力欄にアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-input-field-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-meter-name:

**********************************************************************************************************
ARIA meterノードにはアクセシブルな名前がなければなりません (ARIA meter nodes must have an accessible name)
**********************************************************************************************************

すべてのARIA meterノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-meter-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.1.1

   -  `Non-text Content <https://www.w3.org/TR/WCAG21/#non-text-content>`_
   -  `非テキストコンテンツ <https://waic.jp/translations/WCAG21/#non-text-content>`_

関連ガイドライン
================

*  画像化されたテキスト： :ref:`gl-iot-provide-text`
*  画像： :ref:`gl-image-description`
*  画像： :ref:`gl-image-decorative`
*  アイコン： :ref:`gl-icon-visible-label`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

.. _axe-rule-aria-progressbar-name:

**********************************************************************************************************************
ARIA progressbarノードにはアクセシブルな名前がなければなりません (ARIA progressbar nodes must have an accessible name)
**********************************************************************************************************************

すべてのARIA progressbarノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-progressbar-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.1.1

   -  `Non-text Content <https://www.w3.org/TR/WCAG21/#non-text-content>`_
   -  `非テキストコンテンツ <https://waic.jp/translations/WCAG21/#non-text-content>`_

関連ガイドライン
================

*  画像化されたテキスト： :ref:`gl-iot-provide-text`
*  画像： :ref:`gl-image-description`
*  画像： :ref:`gl-image-decorative`
*  アイコン： :ref:`gl-icon-visible-label`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

.. _axe-rule-aria-prohibited-attr:

*******************************************************************************************************
要素には禁止されているARIA属性を使用してはなりません (Elements must only use permitted ARIA attributes)
*******************************************************************************************************

要素のロールでARIA属性が禁止されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-prohibited-attr>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-required-attr:

******************************************************************************************
必須のARIA属性が提供されていなければなりません (Required ARIA attributes must be provided)
******************************************************************************************

ARIAロールのある要素にすべての必須ARIA属性が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-required-attr>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-required-children:

****************************************************************************************************************
特定のARIAロールには特定の子が含まれていなければなりません (Certain ARIA roles must contain particular children)
****************************************************************************************************************

子ロールを必須とするARIAロールが指定された要素に、それらが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-required-children>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-aria-required-parent:

*********************************************************************************************************************
特定のARIAロールは特定の親に含まれていなければなりません (Certain ARIA roles must be contained by particular parents)
*********************************************************************************************************************

親ロールを必須とするARIAロールが指定された要素に、それらが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-required-parent>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-aria-roledescription:

**************************************************************************************************************************************************
aria-roledescriptionはセマンティックなロールを持った要素に使用しなければなりません (aria-roledescription must be on elements with a semantic role)
**************************************************************************************************************************************************

aria-roledescriptionが暗黙的もしくは明示的なロールを持った要素に使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-roledescription>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-roles:

***********************************************************************************************************
使用されているARIAロールは有効な値に一致しなければなりません (ARIA roles used must conform to valid values)
***********************************************************************************************************

すべてのrole属性が指定された要素で、有効な値が使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-roles>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-toggle-field-name:

********************************************************************************************************
ARIAトグル欄にはアクセシブルな名前がなければなりません (ARIA toggle fields must have an accessible name)
********************************************************************************************************

すべてのARIAトグル欄にアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-toggle-field-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-tooltip-name:

**************************************************************************************************************
ARIA tooltipノードにはアクセシブルな名前がなければなりません (ARIA tooltip nodes must have an accessible name)
**************************************************************************************************************

すべてのARIA tooltipノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-tooltip-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-valid-attr:

********************************************************************************************
ARIA属性は有効な名前に一致しなければなりません (ARIA attributes must conform to valid names)
********************************************************************************************

aria- で始まる属性が有効なARIA属性であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-valid-attr>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-aria-valid-attr-value:

*******************************************************************************************
ARIA属性は有効な値に一致しなければなりません (ARIA attributes must conform to valid values)
*******************************************************************************************

すべてのARIA属性に有効な値が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-valid-attr-value>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-audio-caption:

***********************************************************************************************************
<audio>要素にはキャプショントラックが存在しなければなりません (<audio> elements must have a captions track)
***********************************************************************************************************

<audio>要素にキャプションが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/audio-caption>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.2.1

   -  `Audio-only and Video-only (Prerecorded) <https://www.w3.org/TR/WCAG21/#audio-only-and-video-only-prerecorded>`_
   -  `音声のみ及び映像のみ (収録済) <https://waic.jp/translations/WCAG21/#audio-only-and-video-only-prerecorded>`_

関連ガイドライン
================

*  音声・映像コンテンツ： :ref:`gl-multimedia-text-alternative`
*  音声・映像コンテンツ： :ref:`gl-multimedia-transcript`

.. _axe-rule-avoid-inline-spacing:

*********************************************************************************************************************************************************
インラインのテキスト間隔設定はカスタムスタイルシートによって調整可能でなければなりません (Inline text spacing must be adjustable with custom stylesheets)
*********************************************************************************************************************************************************

style属性で指定されたテキストの間隔は、カスタムスタイルシートにより調整可能であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/avoid-inline-spacing>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.12

   -  `Text Spacing <https://www.w3.org/TR/WCAG21/#text-spacing>`_
   -  `テキストの間隔 <https://waic.jp/translations/WCAG21/#text-spacing>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-customize`

.. _axe-rule-blink:

**************************************************************************************************************
<blink>要素の使用は非推奨で、使用するべきではありません (<blink> elements are deprecated and must not be used)
**************************************************************************************************************

<blink>要素が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/blink>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.2.2

   -  `Pause, Stop, Hide <https://www.w3.org/TR/WCAG21/#pause-stop-hide>`_
   -  `一時停止、停止、非表示 <https://waic.jp/translations/WCAG21/#pause-stop-hide>`_

関連ガイドライン
================

*  動的コンテンツ： :ref:`gl-dynamic-content-pause-movement`
*  動的コンテンツ： :ref:`gl-dynamic-content-pause-refresh`
*  音声・映像コンテンツ： :ref:`gl-multimedia-pause-movement`

.. _axe-rule-button-name:

*******************************************************************************************
ボタンには認識可能なテキストが存在しなければなりません (Buttons must have discernible text)
*******************************************************************************************

ボタンに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/button-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-bypass:

***************************************************************************************************************************
ページには繰り返されるブロックをスキップする手段が存在しなければなりません (Page must have means to bypass repeated blocks)
***************************************************************************************************************************

各ページに少なくとも1つ、ユーザーがナビゲーション部分をスキップして直接本文へ移動できるメカニズムが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/bypass>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.4.1

   -  `Bypass Blocks <https://www.w3.org/TR/WCAG21/#bypass-blocks>`_
   -  `ブロックスキップ <https://waic.jp/translations/WCAG21/#bypass-blocks>`_

関連ガイドライン
================

*  ページ全体： :ref:`gl-page-markup-main`

.. _axe-rule-color-contrast:

***********************************************************************************************************************************
要素は色のコントラスト比（最低限）の閾値を満たしていなければなりません (Elements must meet minimum color contrast ratio thresholds)
***********************************************************************************************************************************

前景色と背景色のコントラストがWCAG 2のAAコントラスト比（最低限）のしきい値を満たすことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/color-contrast>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.3

   -  `Contrast (Minimum) <https://www.w3.org/TR/WCAG21/#contrast-minimum>`_
   -  `コントラスト (最低限) <https://waic.jp/translations/WCAG21/#contrast-minimum>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-contrast`
*  テキスト： :ref:`gl-text-mobile-contrast`
*  画像化されたテキスト： :ref:`gl-iot-text-contrast`
*  画像化されたテキスト： :ref:`gl-iot-mobile-text-contrast`
*  画像： :ref:`gl-image-text-contrast`
*  画像： :ref:`gl-image-mobile-text-contrast`

.. _axe-rule-color-contrast-enhanced:

**********************************************************************************************************************************
要素は色のコントラスト比（高度）の閾値を満たしていなければなりません (Elements must meet enhanced color contrast ratio thresholds)
**********************************************************************************************************************************

前景色と背景色のコントラストがWCAG 2のAAAコントラスト比（高度）のしきい値を満たすことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/color-contrast-enhanced>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.6

   -  `Contrast (Enhanced) <https://www.w3.org/TR/WCAG21/#contrast-enhanced>`_
   -  `コントラスト (高度) <https://waic.jp/translations/WCAG21/#contrast-enhanced>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-contrast`
*  テキスト： :ref:`gl-text-mobile-contrast`
*  画像化されたテキスト： :ref:`gl-iot-text-contrast`
*  画像化されたテキスト： :ref:`gl-iot-mobile-text-contrast`
*  画像： :ref:`gl-image-text-contrast`
*  画像： :ref:`gl-image-mobile-text-contrast`

.. _axe-rule-css-orientation-lock:

*********************************************************************************************************************************
CSSメディアクエリーはディスプレイの向きを固定するために使用してはなりません (CSS Media queries must not lock display orientation)
*********************************************************************************************************************************

コンテンツが特定のディスプレイの向きに固定されていないこと、およびコンテンツがすべてのディスプレイの向きで操作可能なことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/css-orientation-lock>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.4

   -  `Orientation <https://www.w3.org/TR/WCAG21/#orientation>`_
   -  `表示の向き <https://waic.jp/translations/WCAG21/#orientation>`_

関連ガイドライン
================

*  ページ全体： :ref:`gl-page-orientation`

.. _axe-rule-definition-list:

******************************************************************************************************************************************************************************************************************************************************************
<dl>要素は、適切な順序で並べられた<dt>および<dd>のグループ、<script>要素、<template>要素またはdiv要素のみを直接含んでいなければなりません (<dl> elements must only directly contain properly-ordered <dt> and <dd> groups, <script>, <template> or <div> elements)
******************************************************************************************************************************************************************************************************************************************************************

<dl>要素の構造が正しいことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/definition-list>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-dlitem:

***********************************************************************************************************
<dt>および<dd>要素は<dl>に含まれていなければなりません (<dt> and <dd> elements must be contained by a <dl>)
***********************************************************************************************************

<dt>および<dd>要素が<dl>に含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/dlitem>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-document-title:

****************************************************************************************************************************************
ドキュメントにはナビゲーションを補助するために<title>要素がなければなりません (Documents must have <title> element to aid in navigation)
****************************************************************************************************************************************

各HTMLドキュメントに空ではない<title>要素が含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/document-title>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.4.2

   -  `Page Titled <https://www.w3.org/TR/WCAG21/#page-titled>`_
   -  `ページタイトル <https://waic.jp/translations/WCAG21/#page-titled>`_

関連ガイドライン
================

*  ページ全体： :ref:`gl-page-title`

.. _axe-rule-duplicate-id:

************************************************************************
id属性の値は一意でなければなりません (id attribute value must be unique)
************************************************************************

すべてのid属性の値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/duplicate-id>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.1

   -  `Parsing <https://www.w3.org/TR/WCAG21/#parsing>`_
   -  `構文解析 <https://waic.jp/translations/WCAG21/#parsing>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-valid`

.. _axe-rule-duplicate-id-active:

**************************************************************************************
アクティブな要素のIDは一意でなければなりません (IDs of active elements must be unique)
**************************************************************************************

アクティブな要素のid属性の値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/duplicate-id-active>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.1

   -  `Parsing <https://www.w3.org/TR/WCAG21/#parsing>`_
   -  `構文解析 <https://waic.jp/translations/WCAG21/#parsing>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-valid`

.. _axe-rule-duplicate-id-aria:

*********************************************************************************************************
ARIAおよびラベルに使用されているIDは一意でなければなりません (IDs used in ARIA and labels must be unique)
*********************************************************************************************************

ARIAおよびラベルに使用されているすべてのid属性の値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/duplicate-id-aria>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-form-field-multiple-labels:

**************************************************************************************************************
フォームフィールドに複数のlabel要素を付与してはなりりません (Form field must not have multiple label elements)
**************************************************************************************************************

フォームフィールドに複数のlabel要素が存在しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/form-field-multiple-labels>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 3.3.2

   -  `Labels or Instructions <https://www.w3.org/TR/WCAG21/#labels-or-instructions>`_
   -  `ラベル又は説明 <https://waic.jp/translations/WCAG21/#labels-or-instructions>`_

関連ガイドライン
================

*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`

.. _axe-rule-frame-focusable-content:

***********************************************************************************************************************************************
フォーカス可能なコンテンツを含むフレームには、tabindex=-1が指定されていてはなりません (Frames with focusable content must not have tabindex=-1)
***********************************************************************************************************************************************

フォーカス可能な<frame>と<iframe>要素に、tabindex=-1が指定されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/frame-focusable-content>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.1.1

   -  `Keyboard <https://www.w3.org/TR/WCAG21/#keyboard>`_
   -  `キーボード <https://waic.jp/translations/WCAG21/#keyboard>`_

関連ガイドライン
================

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`
*  フォーム： :ref:`gl-form-keyboard-operable`

.. _axe-rule-frame-title:

****************************************************************************************
フレームにはアクセシブルな名前がなければなりません (Frames must have an accessible name)
****************************************************************************************

<iframe>および<frame>要素にアクセシブルな名前が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/frame-title>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-frame-title-unique:

*******************************************************************************************
フレームには一意のtitle属性がなければなりません (Frames must have a unique title attribute)
*******************************************************************************************

<iframe>および<frame>要素に一意のtitle属性が含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/frame-title-unique>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-html-has-lang:

**************************************************************************************
<html>要素にはlang属性がなければなりません (<html> element must have a lang attribute)
**************************************************************************************

すべてのHTMLドキュメントにlang属性が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/html-has-lang>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 3.1.1

   -  `Language of Page <https://www.w3.org/TR/WCAG21/#language-of-page>`_
   -  `ページの言語 <https://waic.jp/translations/WCAG21/#language-of-page>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-page-lang`

.. _axe-rule-html-lang-valid:

********************************************************************************************************************
<html>要素のlang属性には有効な値がなければなりません (<html> element must have a valid value for the lang attribute)
********************************************************************************************************************

<html>要素のlang属性に有効な値があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/html-lang-valid>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 3.1.1

   -  `Language of Page <https://www.w3.org/TR/WCAG21/#language-of-page>`_
   -  `ページの言語 <https://waic.jp/translations/WCAG21/#language-of-page>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-page-lang`

.. _axe-rule-html-xml-lang-mismatch:

********************************************************************************************************************************************************
HTML要素に指定されたlangおよびxml:lang属性は同じ基本言語を持たなければなりません (HTML elements with lang and xml:lang must have the same base language)
********************************************************************************************************************************************************

HTML要素に指定された有効なlangおよびxml:lang属性の両方がページの基本言語と一致することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/html-xml-lang-mismatch>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 3.1.1

   -  `Language of Page <https://www.w3.org/TR/WCAG21/#language-of-page>`_
   -  `ページの言語 <https://waic.jp/translations/WCAG21/#language-of-page>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-page-lang`

.. _axe-rule-image-alt:

**************************************************************************
画像には代替テキストがなければなりません (Images must have alternate text)
**************************************************************************

<img>要素に代替テキストが存在する、またはnoneまたはpresentationのロールが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/image-alt>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.1.1

   -  `Non-text Content <https://www.w3.org/TR/WCAG21/#non-text-content>`_
   -  `非テキストコンテンツ <https://waic.jp/translations/WCAG21/#non-text-content>`_

関連ガイドライン
================

*  画像化されたテキスト： :ref:`gl-iot-provide-text`
*  画像： :ref:`gl-image-description`
*  画像： :ref:`gl-image-decorative`
*  アイコン： :ref:`gl-icon-visible-label`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

.. _axe-rule-input-button-name:

*****************************************************************************************************
入力ボタンには認識可能なテキストが存在しなければなりません (Input buttons must have discernible text)
*****************************************************************************************************

入力ボタンに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/input-button-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-input-image-alt:

***************************************************************************************
画像ボタンには代替テキストがなければなりません (Image buttons must have alternate text)
***************************************************************************************

<input type="image">要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/input-image-alt>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.1.1

   -  `Non-text Content <https://www.w3.org/TR/WCAG21/#non-text-content>`_
   -  `非テキストコンテンツ <https://waic.jp/translations/WCAG21/#non-text-content>`_

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  画像化されたテキスト： :ref:`gl-iot-provide-text`
*  画像： :ref:`gl-image-description`
*  画像： :ref:`gl-image-decorative`
*  アイコン： :ref:`gl-icon-visible-label`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`
*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-label:

***************************************************************************
フォーム要素にはラベルがなければなりません (Form elements must have labels)
***************************************************************************

すべてのフォーム要素にラベルが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/label>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-label-content-name-mismatch:

*******************************************************************************************************************************************************
要素の視認できるテキストはそれらのアクセシブルな名前の一部でなければなりません (Elements must have their visible text as part of their accessible name)
*******************************************************************************************************************************************************

コンテンツによってラベル付けされた要素は、それらの視認できるテキストがアクセシブルな名前の一部になっていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/label-content-name-mismatch>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.5.3

   -  `Label in Name <https://www.w3.org/TR/WCAG21/#label-in-name>`_
   -  `名前 (name) のラベル <https://waic.jp/translations/WCAG21/#label-in-name>`_

関連ガイドライン
================

*  フォーム： :ref:`gl-form-label`

.. _axe-rule-link-in-text-block:

*************************************************************************************************************
リンクは色に依存しない形で区別できなければなりません (Links must be distinguishable without relying on color)
*************************************************************************************************************

リンクが色に依存しない形で周囲のテキストと区別できることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/link-in-text-block>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.1

   -  `Use of Color <https://www.w3.org/TR/WCAG21/#use-of-color>`_
   -  `色の使用 <https://waic.jp/translations/WCAG21/#use-of-color>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-color-only`
*  画像： :ref:`gl-image-color-only`
*  アイコン： :ref:`gl-icon-color-only`
*  リンク： :ref:`gl-link-color-only`
*  フォーム： :ref:`gl-form-color-only`

.. _axe-rule-link-name:

***********************************************************************************
リンクには認識可能なテキストがなければなりません (Links must have discernible text)
***********************************************************************************

リンクに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/link-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.4.4

   -  `Link Purpose (In Context) <https://www.w3.org/TR/WCAG21/#link-purpose-in-context>`_
   -  `リンクの目的 (コンテキスト内) <https://waic.jp/translations/WCAG21/#link-purpose-in-context>`_

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  リンク： :ref:`gl-link-text`
*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-list:

***********************************************************************************************************************************************************************
<ul>および<ol>の直下には<li>、<script>または<template>要素のみを含まなければなりません (<ul> and <ol> must only directly contain <li>, <script> or <template> elements)
***********************************************************************************************************************************************************************

リストが正しく構造化されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/list>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-listitem:

************************************************************************************************************
<li>要素は<ul>または<ol>内に含まれていなければなりません (<li> elements must be contained in a <ul> or <ol>)
************************************************************************************************************

<li>要素がセマンティックに使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/listitem>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-marquee:

**********************************************************************************************************
<marquee>要素は非推奨のため、使用してはなりません (<marquee> elements are deprecated and must not be used)
**********************************************************************************************************

<marquee>要素が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/marquee>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.2.2

   -  `Pause, Stop, Hide <https://www.w3.org/TR/WCAG21/#pause-stop-hide>`_
   -  `一時停止、停止、非表示 <https://waic.jp/translations/WCAG21/#pause-stop-hide>`_

関連ガイドライン
================

*  動的コンテンツ： :ref:`gl-dynamic-content-pause-movement`
*  動的コンテンツ： :ref:`gl-dynamic-content-pause-refresh`
*  音声・映像コンテンツ： :ref:`gl-multimedia-pause-movement`

.. _axe-rule-meta-refresh:

**********************************************************************************************************************
20時間より短い時間経過後のページの自動リロードを使用してはなりません (Delayed refresh under 20 hours must not be used)
**********************************************************************************************************************

一定時間経過後のページの自動リロードのために<meta http-equiv="refresh">が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/meta-refresh>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.2.1

   -  `Timing Adjustable <https://www.w3.org/TR/WCAG21/#timing-adjustable>`_
   -  `タイミング調整可能 <https://waic.jp/translations/WCAG21/#timing-adjustable>`_

関連ガイドライン
================

*  ログイン・セッション： :ref:`gl-login-session-timing`
*  フォーム： :ref:`gl-form-timing`

.. _axe-rule-meta-refresh-no-exceptions:

*********************************************************************************************
一定時間経過後のページの自動リロードを使用してはなりません (Delayed refresh must not be used)
*********************************************************************************************

一定時間経過後のページの自動リロードのために<meta http-equiv="refresh">が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/meta-refresh-no-exceptions>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.2.4

   -  `Interruptions <https://www.w3.org/TR/WCAG21/#interruptions>`_
   -  `割り込み <https://waic.jp/translations/WCAG21/#interruptions>`_

*  達成基準 3.2.5

   -  `Change on Request <https://www.w3.org/TR/WCAG21/#change-on-request>`_
   -  `要求による変化 <https://waic.jp/translations/WCAG21/#change-on-request>`_

関連ガイドライン
================

*  動的コンテンツ： :ref:`gl-dynamic-content-no-interrupt`

.. _axe-rule-meta-viewport:

***************************************************************************************************
ズーム機能やテキストのサイズ変更は無効にしてはなりません (Zooming and scaling must not be disabled)
***************************************************************************************************

<meta name="viewport">がテキストのサイズ変更やズームを無効化しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/meta-viewport>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.4

   -  `Resize text <https://www.w3.org/TR/WCAG21/#resize-text>`_
   -  `テキストのサイズ変更 <https://waic.jp/translations/WCAG21/#resize-text>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-zoom`
*  テキスト： :ref:`gl-text-enlarge-settings`
*  テキスト： :ref:`gl-text-mobile-enlarge-settings`

.. _axe-rule-nested-interactive:

********************************************************************************************
対話的なコントロールはネストされていてはなりません (Interactive controls must not be nested)
********************************************************************************************

スクリーン・リーダーで必ずしもよみあげられなかったり支援技術のフォーカスに関する問題を引き起こす可能性があったりするため、対話的なコントロールがネストされていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/nested-interactive>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-no-autoplay-audio:

*********************************************************************************************************************
<video> または <audio> 要素は音声を自動再生してはなりません (<video> or <audio> elements must not play automatically)
*********************************************************************************************************************

<video> または <audio> 要素が音声を停止またはミュートするコントロールなしに音声を3秒より長く自動再生しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/no-autoplay-audio>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.2

   -  `Audio Control <https://www.w3.org/TR/WCAG21/#audio-control>`_
   -  `音声の制御 <https://waic.jp/translations/WCAG21/#audio-control>`_

関連ガイドライン
================

*  音声・映像コンテンツ： :ref:`gl-multimedia-operable`

.. _axe-rule-object-alt:

*********************************************************************************************
<object>要素には代替テキストがなければなりません (<object> elements must have alternate text)
*********************************************************************************************

<object>要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/object-alt>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.1.1

   -  `Non-text Content <https://www.w3.org/TR/WCAG21/#non-text-content>`_
   -  `非テキストコンテンツ <https://waic.jp/translations/WCAG21/#non-text-content>`_

関連ガイドライン
================

*  画像化されたテキスト： :ref:`gl-iot-provide-text`
*  画像： :ref:`gl-image-description`
*  画像： :ref:`gl-image-decorative`
*  アイコン： :ref:`gl-icon-visible-label`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

.. _axe-rule-p-as-heading:

************************************************************************************************************
スタイル付けした<p>要素を見出しとして使用してはなりません (Styled <p> elements must not be used as headings)
************************************************************************************************************

<p>要素を見出しとしてスタイル付けするために太字、イタリック体、およびフォントサイズが使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/p-as-heading>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-role-img-alt:

*************************************************************************************************************
[role="img"] の要素には代替テキストがなければなりません ([role="img"] elements must have an alternative text)
*************************************************************************************************************

[role="img"] の要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/role-img-alt>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.1.1

   -  `Non-text Content <https://www.w3.org/TR/WCAG21/#non-text-content>`_
   -  `非テキストコンテンツ <https://waic.jp/translations/WCAG21/#non-text-content>`_

関連ガイドライン
================

*  画像化されたテキスト： :ref:`gl-iot-provide-text`
*  画像： :ref:`gl-image-description`
*  画像： :ref:`gl-image-decorative`
*  アイコン： :ref:`gl-icon-visible-label`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

.. _axe-rule-scrollable-region-focusable:

**************************************************************************************************************
スクロール可能な領域はキーボードでアクセスできなければなりません (Scrollable region must have keyboard access)
**************************************************************************************************************

スクロール可能なコンテンツを持つ要素がキーボードでアクセスできることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/scrollable-region-focusable>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.1.1

   -  `Keyboard <https://www.w3.org/TR/WCAG21/#keyboard>`_
   -  `キーボード <https://waic.jp/translations/WCAG21/#keyboard>`_

関連ガイドライン
================

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`
*  フォーム： :ref:`gl-form-keyboard-operable`

.. _axe-rule-select-name:

**************************************************************************************************
select要素にはアクセシブルな名前がなければなりません (Select element must have an accessible name)
**************************************************************************************************

select要素にはアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/select-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`

.. _axe-rule-server-side-image-map:

**********************************************************************************************
サーバーサイドのイメージマップを使用してはなりません (Server-side image maps must not be used)
**********************************************************************************************

サーバーサイドのイメージマップが使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/server-side-image-map>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.1.1

   -  `Keyboard <https://www.w3.org/TR/WCAG21/#keyboard>`_
   -  `キーボード <https://waic.jp/translations/WCAG21/#keyboard>`_

関連ガイドライン
================

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`
*  フォーム： :ref:`gl-form-keyboard-operable`

.. _axe-rule-svg-img-alt:

**********************************************************************************************************************************
imgロールを持つ<svg>要素には代替テキストが存在しなければなりません (<svg> elements with an img role must have an alternative text)
**********************************************************************************************************************************

img、graphics-documentまたはgraphics-symbolロールを持つsvg要素にアクセシブルなテキストがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/svg-img-alt>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.1.1

   -  `Non-text Content <https://www.w3.org/TR/WCAG21/#non-text-content>`_
   -  `非テキストコンテンツ <https://waic.jp/translations/WCAG21/#non-text-content>`_

関連ガイドライン
================

*  画像化されたテキスト： :ref:`gl-iot-provide-text`
*  画像： :ref:`gl-image-description`
*  画像： :ref:`gl-image-decorative`
*  アイコン： :ref:`gl-icon-visible-label`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  音声・映像コンテンツ： :ref:`gl-multimedia-perceivable`

.. _axe-rule-table-fake-caption:

***************************************************************************************************************************************************************
データテーブルにキャプションをつけるためにデータまたはヘッダーセルを用いてはなりません (Data or header cells must not be used to give caption to a data table.)
***************************************************************************************************************************************************************

キャプション付きのテーブルが<caption>要素を用いていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/table-fake-caption>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-td-has-header:

********************************************************************************************************************************************************************************
大きい<table>の空ではない<td>要素は対応するテーブルヘッダーと関連づけられていなければなりません (Non-empty <td> elements in larger <table> must have an associated table header)
********************************************************************************************************************************************************************************

3×3より大きい<table>の空ではないデータセルにはそれぞれ1つ以上のテーブルヘッダーが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/td-has-header>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-td-headers-attr:

*************************************************************************************************************************************************************************************
テーブルのheaders属性を使用するすべてのセルは同じ表内の他のセルのみを参照しなければなりません (Table cells that use the headers attribute must only refer to cells in the same table)
*************************************************************************************************************************************************************************************

テーブルでheaders属性を使用している各セルの参照先が同じテーブル内の他のセルであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/td-headers-attr>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-th-has-data-cells:

***********************************************************************************************************************************
データテーブルのテーブルヘッダーはデータセルを参照していなければなりません (Table headers in a data table must refer to data cells)
***********************************************************************************************************************************

すべての<th>要素およびrole=columnheader/rowheaderを持つ要素にはそれらが説明するデータセルがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/th-has-data-cells>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.1

   -  `Info and Relationships <https://www.w3.org/TR/WCAG21/#info-and-relationships>`_
   -  `情報及び関係性 <https://waic.jp/translations/WCAG21/#info-and-relationships>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-semantics`
*  マークアップと実装： :ref:`gl-markup-component-implementation`
*  ページ全体： :ref:`gl-page-landmark`
*  フォーム： :ref:`gl-form-label`
*  フォーム： :ref:`gl-form-hidden-label`
*  動的コンテンツ： :ref:`gl-dynamic-content-maintain-dom-tree`

.. _axe-rule-valid-lang:

*********************************************************************************
lang属性には有効な値がなければなりません (lang attribute must have a valid value)
*********************************************************************************

lang属性に有効な値が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/valid-lang>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 3.1.2

   -  `Language of Parts <https://www.w3.org/TR/WCAG21/#language-of-parts>`_
   -  `一部分の言語 <https://waic.jp/translations/WCAG21/#language-of-parts>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-phrase-lang`
*  テキスト： :ref:`gl-text-component-lang`

.. _axe-rule-video-caption:

*************************************************************************************
<video>要素にはキャプションがなければなりません (<video> elements must have captions)
*************************************************************************************

<video>要素にキャプションが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/video-caption>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.2.2

   -  `Captions (Prerecorded) <https://www.w3.org/TR/WCAG21/#captions-prerecorded>`_
   -  `キャプション (収録済) <https://waic.jp/translations/WCAG21/#captions-prerecorded>`_

関連ガイドライン
================

*  音声・映像コンテンツ： :ref:`gl-multimedia-text-alternative`
*  音声・映像コンテンツ： :ref:`gl-multimedia-caption`

.. _axe-rule-autocomplete-valid:

************************************************************************************************
autocomplete属性は正しく使用しなければなりません (autocomplete attribute must be used correctly)
************************************************************************************************

autocomplete属性が正しく、かつフォームフィールドに対して適切であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/autocomplete-valid>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.5

   -  `Identify Input Purpose <https://www.w3.org/TR/WCAG21/#identify-input-purpose>`_
   -  `入力目的の特定 <https://waic.jp/translations/WCAG21/#identify-input-purpose>`_


.. _axe-rule-identical-links-same-purpose:

***************************************************************************************************************************
同じ名前を持つ複数のリンクは類似した目的を持っていなければなりません (Links with the same name must have a similar purpose)
***************************************************************************************************************************

同じアクセシブルな名前を持つ複数のリンクが類似した目的を果たすことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/identical-links-same-purpose>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.4.9

   -  `Link Purpose (Link Only) <https://www.w3.org/TR/WCAG21/#link-purpose-link-only>`_
   -  `リンクの目的 (リンクのみ) <https://waic.jp/translations/WCAG21/#link-purpose-link-only>`_


.. _axe-rule-accesskeys:

****************************************************************************************
accesskey属性の値は一意でなければなりません (accesskey attribute value should be unique)
****************************************************************************************

すべてのaccesskey属性の値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/accesskeys>`__


.. _axe-rule-aria-allowed-role:

**************************************************************************************************
ARIAロールは要素に対して適切でなければなりません (ARIA role should be appropriate for the element)
**************************************************************************************************

role属性の値が要素に対して適切であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-allowed-role>`__


.. _axe-rule-aria-dialog-name:

*******************************************************************************************************************************************
ARIA dialogとalertdialogノードにはアクセシブルな名前がなければなりません (ARIA dialog and alertdialog nodes should have an accessible name)
*******************************************************************************************************************************************

すべてのARIA dialog、alertdialogノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-dialog-name>`__


.. _axe-rule-aria-text:

**************************************************************************************************************************************
"role=text"が指定されている要素には、フォーカス可能な子孫が含まれていてはなりません ("role=text" should have no focusable descendants)
**************************************************************************************************************************************

role="text"が指定されている要素にフォーカス可能な子孫がないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-text>`__


.. _axe-rule-aria-treeitem-name:

******************************************************************************************************************
ARIA treeitemノードにはアクセシブルな名前がなければなりません (ARIA treeitem nodes should have an accessible name)
******************************************************************************************************************

すべてのARIA treeitemノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/aria-treeitem-name>`__


.. _axe-rule-empty-heading:

***********************************************************
見出しは空にしてはなりません (Headings should not be empty)
***********************************************************

見出しに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/empty-heading>`__


.. _axe-rule-empty-table-header:

********************************************************************************
テーブルのヘッダーは空にしてはなりません (Table header text should not be empty)
********************************************************************************

テーブルのヘッダーに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/empty-table-header>`__


.. _axe-rule-focus-order-semantics:

********************************************************************************************************************************
フォーカス順序に含まれる要素には、適切なロールがなければなりません (Elements in the focus order should have an appropriate role)
********************************************************************************************************************************

フォーカス順序に含まれる要素にインタラクティブコンテンツに適したロールがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/focus-order-semantics>`__


.. _axe-rule-frame-tested:

**************************************************************************************
フレームはaxe-coreでテストしなければなりません (Frames should be tested with axe-core)
**************************************************************************************

<iframe>および<frame>要素にaxe-coreスクリプトが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/frame-tested>`__


.. _axe-rule-heading-order:

**********************************************************************************************
見出しのレベルは1つずつ増加させなければなりません (Heading levels should only increase by one)
**********************************************************************************************

見出しの順序が意味的に正しいことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/heading-order>`__


.. _axe-rule-hidden-content:

**********************************************************************************************************
ページ上の隠れているコンテンツは分析されなければなりません (Hidden content on the page should be analyzed)
**********************************************************************************************************

隠れているコンテンツについてユーザーに通知します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/hidden-content>`__


.. _axe-rule-image-redundant-alt:

****************************************************************************************************************************
画像の代替テキストはテキストとして繰り返されるべきではありません (Alternative text of images should not be repeated as text)
****************************************************************************************************************************

画像の代替がテキストとして繰り返されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/image-redundant-alt>`__


.. _axe-rule-label-title-only:

************************************************************************************************
フォーム要素には視認できるラベルがなければなりません (Form elements should have a visible label)
************************************************************************************************

すべてのフォーム要素に視認できるラベルがあり、非表示のラベル、titleまたはaria-describedby属性のみを使用してラベル付けされていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/label-title-only>`__


.. _axe-rule-landmark-banner-is-top-level:

******************************************************************************************************************************
bannerランドマークは他のランドマークに含まれるべきではありません (Banner landmark should not be contained in another landmark)
******************************************************************************************************************************

bannerランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-banner-is-top-level>`__


.. _axe-rule-landmark-complementary-is-top-level:

***********************************************************************************************
asideは他の要素に含まれるべきではありません (Aside should not be contained in another landmark)
***********************************************************************************************

complementaryランドマークあるいはasideがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-complementary-is-top-level>`__


.. _axe-rule-landmark-contentinfo-is-top-level:

****************************************************************************************************************************************
contentinfoランドマークは他のランドマークに含まれるべきではありません (Contentinfo landmark should not be contained in another landmark)
****************************************************************************************************************************************

contentinfoランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-contentinfo-is-top-level>`__


.. _axe-rule-landmark-main-is-top-level:

**************************************************************************************************************************
mainランドマークは他のランドマークに含まれるべきではありません (Main landmark should not be contained in another landmark)
**************************************************************************************************************************

mainランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-main-is-top-level>`__


.. _axe-rule-landmark-no-duplicate-banner:

*********************************************************************************************************************
ドキュメントに複数のbannerランドマークが存在してはなりません (Document should not have more than one banner landmark)
*********************************************************************************************************************

ドキュメント内のbannerランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-no-duplicate-banner>`__


.. _axe-rule-landmark-no-duplicate-contentinfo:

*******************************************************************************************************************************
ドキュメントに複数のcontentinfoランドマークが存在してはなりません (Document should not have more than one contentinfo landmark)
*******************************************************************************************************************************

ドキュメント内のcontentinfoランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-no-duplicate-contentinfo>`__


.. _axe-rule-landmark-no-duplicate-main:

*****************************************************************************************************************
ドキュメントに複数のmainランドマークが存在してはなりません (Document should not have more than one main landmark)
*****************************************************************************************************************

ドキュメント内のmainランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-no-duplicate-main>`__


.. _axe-rule-landmark-one-main:

**********************************************************************************************************
ドキュメントにはmainランドマークが1つ含まれていなければなりません (Document should have one main landmark)
**********************************************************************************************************

ドキュメントにmainランドマークが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-one-main>`__


.. _axe-rule-landmark-unique:

***********************************************************************
ランドマークが一意であることを確認します (Ensures landmarks are unique)
***********************************************************************

ランドマークには一意のロール又はロール／ラベル／タイトル (すなわちアクセシブルな名前) の組み合わせがなければなりません

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/landmark-unique>`__


.. _axe-rule-meta-viewport-large:

************************************************************************************************************************************
ユーザーがズームをしてテキストを最大500％まで拡大できなければなりません (Users should be able to zoom and scale the text up to 500%)
************************************************************************************************************************************

<meta name="viewport">で大幅に拡大縮小できることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/meta-viewport-large>`__


.. _axe-rule-page-has-heading-one:

*************************************************************************************************
ページにはレベル1の見出しが含まれていなければなりません (Page should contain a level-one heading)
*************************************************************************************************

ページ、またはそのページ中のフレームの少なくとも1つにはレベル1の見出しが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/page-has-heading-one>`__


.. _axe-rule-presentation-role-conflict:

**********************************************************************************************************************************************
プレゼンテーション目的とされている要素が一貫して無視されることを確認します (Ensure elements marked as presentational are consistently ignored)
**********************************************************************************************************************************************

すべてのスクリーン・リーダーに確実に無視させるために、プレゼンテーション目的とされている要素にはグローバルなARIAまたはtabindexが指定されていてはなりません

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/presentation-role-conflict>`__


.. _axe-rule-region:

**********************************************************************************************************************
ページのすべてのコンテンツはlandmarkに含まれていなければなりません (All page content should be contained by landmarks)
**********************************************************************************************************************

ページのすべてのコンテンツがlandmarkに含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/region>`__


.. _axe-rule-scope-attr-valid:

**************************************************************************************
scope属性は正しく使用されなければなりません (scope attribute should be used correctly)
**************************************************************************************

scope属性がテーブルで正しく使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/scope-attr-valid>`__


.. _axe-rule-skip-link:

***************************************************************************************************************************
スキップリンクのターゲットが存在し、フォーカス可能でなければなりません (The skip-link target should exist and be focusable)
***************************************************************************************************************************

すべてのスキップリンクにフォーカス可能なターゲットがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/skip-link>`__


.. _axe-rule-tabindex:

***************************************************************************************************************
要素に指定するtabindexは0より大きい値であってはなりません (Elements should not have tabindex greater than zero)
***************************************************************************************************************

tabindex属性値が0より大きくないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/tabindex>`__


.. _axe-rule-table-duplicate-name:

****************************************************************************************************************
テーブルのキャプションとサマリーは同一であってはなりません (tables should not have the same summary and caption)
****************************************************************************************************************

<caption>要素の内用がsummary属性のテキストと同一ではないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/table-duplicate-name>`__


.. _axe-rule-target-size:

**********************************************************************************************************************************************
すべてのタッチターゲットは24pxの大きさか、十分なスペースがなければなりません (All touch targets must be 24px large, or leave sufficient space)
**********************************************************************************************************************************************

タッチターゲットのサイズとスペースが十分にあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.8/target-size>`__


