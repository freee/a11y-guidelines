ここで掲載している情報は、 `axe-coreのGitHubリポジトリー <https://github.com/dequelabs/axe-core/>`_ の以下に示す時点におけるdevelopブランチの内容に基づいて自動的に生成したものです。axe DevToolsの内容とは一致していない場合もあることにご注意ください。

バージョン
   4.6.3
更新日時
   2023-01-27 03:11:18+0900

.. _axe-rule-area-alt:

********************************************************************************************************************
Active <area> elements must have alternate text （アクティブな<area>要素には代替テキストが存在しなければなりません）
********************************************************************************************************************

イメージマップの<area>要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/area-alt>`__

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

***************************************************************************************************************
Elements must only use allowed ARIA attributes （要素には許可されているARIA属性のみを使用しなければなりません）
***************************************************************************************************************

要素のロールにARIA属性が許可されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-allowed-attr>`__

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

*****************************************************************************************************
ARIA commands must have an accessible name （ARIAコマンドにはアクセシブルな名前がなければなりません）
*****************************************************************************************************

すべてのARIA button、link、menuitemにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-command-name>`__

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

**************************************************************************************************************************
aria-hidden='true' must not be present on the document body （ドキュメント本体にaria-hidden='true'が存在してはなりません）
**************************************************************************************************************************

ドキュメント本体にaria-hidden='true'が存在していないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-hidden-body>`__

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

*************************************************************************************************************************************
ARIA hidden element must not be focusable or contain focusable elements （ARIA hidden要素にフォーカス可能な要素を含んではなりません）
*************************************************************************************************************************************

aria-hidden要素にフォーカス可能な要素が含まれていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-hidden-focus>`__

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

*******************************************************************************************
ARIA input fields must have an accessible name （ARIA入力欄にアクセシブルな名前があります）
*******************************************************************************************

すべてのARIA入力欄にアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-input-field-name>`__

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

************************************************************************************************************
ARIA meter nodes must have an accessible name （ARIA meterノードにはアクセシブルな名前がなければなりません）
************************************************************************************************************

すべてのARIA meterノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-meter-name>`__

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

************************************************************************************************************************
ARIA progressbar nodes must have an accessible name （ARIA progressbarノードにはアクセシブルな名前がなければなりません）
************************************************************************************************************************

すべてのARIA progressbarノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-progressbar-name>`__

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

.. _axe-rule-aria-required-attr:

********************************************************************************************
Required ARIA attributes must be provided （必須のARIA属性が提供されていなければなりません）
********************************************************************************************

ARIAロールのある要素にすべての必須ARIA属性が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-required-attr>`__

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

******************************************************************************************************************
Certain ARIA roles must contain particular children （特定のARIAロールには特定の子が含まれていなければなりません）
******************************************************************************************************************

子ロールを必須とするARIAロールが指定された要素に、それらが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-required-children>`__

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

***********************************************************************************************************************
Certain ARIA roles must be contained by particular parents （特定のARIAロールは特定の親に含まれていなければなりません）
***********************************************************************************************************************

親ロールを必須とするARIAロールが指定された要素に、それらが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-required-parent>`__

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

**************************************************************************************************************************************
aria-roledescription must be on elements with a semantic role （aria-roledescriptionはセマンティックなロールを持った要素に使用します）
**************************************************************************************************************************************

aria-roledescriptionが暗黙的もしくは明示的なロールを持った要素に使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-roledescription>`__

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

*************************************************************************************************************
ARIA roles used must conform to valid values （使用されているARIAロールは有効な値に一致しなければなりません）
*************************************************************************************************************

すべてのロール属性が指定された要素で、有効な値が使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-roles>`__

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

**********************************************************************************************
ARIA toggle fields must have an accessible name （ARIAトグル欄にアクセシブルな名前があります）
**********************************************************************************************

すべてのARIAトグル欄にアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-toggle-field-name>`__

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

****************************************************************************************************************
ARIA tooltip nodes must have an accessible name （ARIA tooltipノードにはアクセシブルな名前がなければなりません）
****************************************************************************************************************

すべてのARIA tooltipノードにはアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-tooltip-name>`__

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

**********************************************************************************************
ARIA attributes must conform to valid names （ARIA属性は有効な名前に一致しなければなりません）
**********************************************************************************************

aria- で始まる属性が有効なARIA属性であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-valid-attr>`__

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

*********************************************************************************************
ARIA attributes must conform to valid values （ARIA属性は有効な値に一致しなければなりません）
*********************************************************************************************

すべてのARIA属性に有効な値が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-valid-attr-value>`__

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

*************************************************************************************************************
<audio> elements must have a captions track （<audio>要素にはキャプショントラックが存在しなければなりません）
*************************************************************************************************************

<audio>要素にキャプションが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/audio-caption>`__

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

***********************************************************************************************************************************************************
Inline text spacing must be adjustable with custom stylesheets （インラインのテキスト間隔設定はカスタムスタイルシートによって調整可能でなければなりません）
***********************************************************************************************************************************************************

style属性で指定されたテキストの間隔は、カスタムスタイルシートにより調整可能であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/avoid-inline-spacing>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.12

   -  `Text Spacing <https://www.w3.org/TR/WCAG21/#text-spacing>`_
   -  `テキストの間隔 <https://waic.jp/translations/WCAG21/#text-spacing>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-customize`

.. _axe-rule-blink:

****************************************************************************************************************
<blink> elements are deprecated and must not be used （<blink>要素は廃止されており、使用するべきではありません）
****************************************************************************************************************

<blink>要素が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/blink>`__

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

*********************************************************************************************
Buttons must have discernible text （ボタンには認識可能なテキストが存在しなければなりません）
*********************************************************************************************

ボタンに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/button-name>`__

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

*****************************************************************************************************************************
Page must have means to bypass repeated blocks （ページには繰り返されるブロックをスキップする手段が存在しなければなりません）
*****************************************************************************************************************************

各ページに少なくとも1つ、ユーザーがナビゲーション部分をスキップして直接本文へ移動できるメカニズムが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/bypass>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.4.1

   -  `Bypass Blocks <https://www.w3.org/TR/WCAG21/#bypass-blocks>`_
   -  `ブロックスキップ <https://waic.jp/translations/WCAG21/#bypass-blocks>`_

関連ガイドライン
================

*  ページ全体： :ref:`gl-page-markup-main`

.. _axe-rule-color-contrast:

***************************************************************************************************
Elements must have sufficient color contrast （要素には十分な色のコントラストがなければなりません）
***************************************************************************************************

前景色と背景色のコントラストがWCAG 2のAAコントラスト比のしきい値を満たすことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/color-contrast>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.3

   -  `Contrast (Minimum) <https://www.w3.org/TR/WCAG21/#contrast-minimum>`_
   -  `コントラスト (最低限) <https://waic.jp/translations/WCAG21/#contrast-minimum>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-contrast`
*  画像化されたテキスト： :ref:`gl-iot-text-contrast`
*  画像： :ref:`gl-image-text-contrast`

.. _axe-rule-color-contrast-enhanced:

***************************************************************************************************
Elements must have sufficient color contrast （要素には十分な色のコントラストがなければなりません）
***************************************************************************************************

前景色と背景色のコントラストがWCAG 2のAAAコントラスト比のしきい値を満たすことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/color-contrast-enhanced>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.6

   -  `Contrast (Enhanced) <https://www.w3.org/TR/WCAG21/#contrast-enhanced>`_
   -  `コントラスト (高度) <https://waic.jp/translations/WCAG21/#contrast-enhanced>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-contrast`
*  画像化されたテキスト： :ref:`gl-iot-text-contrast`
*  画像： :ref:`gl-image-text-contrast`

.. _axe-rule-css-orientation-lock:

*********************************************************************************************************************************
CSS Media queries must not lock display orientation （ディスプレイの向きを固定するためにCSSメディアクエリーは使用されていません）
*********************************************************************************************************************************

コンテンツが特定のディスプレイの向きに固定されていないこと、およびコンテンツがすべてのディスプレイの向きで操作可能なことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/css-orientation-lock>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.4

   -  `Orientation <https://www.w3.org/TR/WCAG21/#orientation>`_
   -  `表示の向き <https://waic.jp/translations/WCAG21/#orientation>`_

関連ガイドライン
================

*  ページ全体： :ref:`gl-page-orientation`

.. _axe-rule-definition-list:

*********************************************************************************************************************************************************************************************************************************************************
<dl> elements must only directly contain properly-ordered <dt> and <dd> groups, <script>, <template> or <div> elements （<dl>要素は、適切な順序で並べられた<dt>および<dd>グループ、<script>要素または<template>要素のみを直接含んでいなければなりません）
*********************************************************************************************************************************************************************************************************************************************************

<dl>要素の構造が正しいことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/definition-list>`__

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

*************************************************************************************************************
<dt> and <dd> elements must be contained by a <dl> （<dt>および<dd>要素は<dl>に含まれていなければなりません）
*************************************************************************************************************

<dt>および<dd>要素が<dl>に含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/dlitem>`__

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

******************************************************************************************************************************************
Documents must have <title> element to aid in navigation （ドキュメントにはナビゲーションを補助するために<title>要素がなければなりません）
******************************************************************************************************************************************

各HTMLドキュメントに空ではない<title>要素が含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/document-title>`__

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
id attribute value must be unique （id属性値は一意でなければなりません）
************************************************************************

すべてのid属性値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/duplicate-id>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.1

   -  `Parsing <https://www.w3.org/TR/WCAG21/#parsing>`_
   -  `構文解析 <https://waic.jp/translations/WCAG21/#parsing>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-valid`

.. _axe-rule-duplicate-id-active:

********************************************************************************
IDs of active elements must be unique （活性要素のIDは一意でなければなりません）
********************************************************************************

活性要素のid属性値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/duplicate-id-active>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.1

   -  `Parsing <https://www.w3.org/TR/WCAG21/#parsing>`_
   -  `構文解析 <https://waic.jp/translations/WCAG21/#parsing>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-valid`

.. _axe-rule-duplicate-id-aria:

***********************************************************************************************************
IDs used in ARIA and labels must be unique （ARIAおよびラベルに使用されているIDは一意でなければなりません）
***********************************************************************************************************

ARIAおよびラベルに使用されているすべてのid属性値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/duplicate-id-aria>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.1

   -  `Parsing <https://www.w3.org/TR/WCAG21/#parsing>`_
   -  `構文解析 <https://waic.jp/translations/WCAG21/#parsing>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-valid`

.. _axe-rule-form-field-multiple-labels:

********************************************************************************************************************
Form field must not have multiple label elements （複数のlabel要素をフォームフィールドに付与するべきではありません）
********************************************************************************************************************

フォームフィールドに複数のlabel要素が存在しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/form-field-multiple-labels>`__

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

*********************************************************************************************************************************************************
Frames with focusable content must not have tabindex=-1 （tabindex=-1が指定されているフレームには、フォーカス可能なコンテンツが含まれていてはなりません）
*********************************************************************************************************************************************************

tabindex=-1が指定されている<frame>と<iframe>要素が、フォーカス可能なコンテンツを含まないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/frame-focusable-content>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.1.1

   -  `Keyboard <https://www.w3.org/TR/WCAG21/#keyboard>`_
   -  `キーボード <https://waic.jp/translations/WCAG21/#keyboard>`_

関連ガイドライン
================

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`

.. _axe-rule-frame-title:

*********************************************************************************
Frames must have an accessible name （フレームにはtitle属性がなければなりません）
*********************************************************************************

<iframe>および<frame>要素に空ではないtitle属性が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/frame-title>`__

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

*********************************************************************************************
Frames must have a unique title attribute （フレームには一意のtitle属性がなければなりません）
*********************************************************************************************

<iframe>および<frame>要素に一意のtitle属性が含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/frame-title-unique>`__

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

****************************************************************************************
<html> element must have a lang attribute （<html>要素にはlang属性がなければなりません）
****************************************************************************************

すべてのHTMLドキュメントにlang属性が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/html-has-lang>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 3.1.1

   -  `Language of Page <https://www.w3.org/TR/WCAG21/#language-of-page>`_
   -  `ページの言語 <https://waic.jp/translations/WCAG21/#language-of-page>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-page-lang`

.. _axe-rule-html-lang-valid:

**********************************************************************************************************************
<html> element must have a valid value for the lang attribute （<html>要素のlang属性には有効な値がなければなりません）
**********************************************************************************************************************

<html>要素のlang属性に有効な値があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/html-lang-valid>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 3.1.1

   -  `Language of Page <https://www.w3.org/TR/WCAG21/#language-of-page>`_
   -  `ページの言語 <https://waic.jp/translations/WCAG21/#language-of-page>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-page-lang`

.. _axe-rule-html-xml-lang-mismatch:

**********************************************************************************************************************************************************
HTML elements with lang and xml:lang must have the same base language （HTML要素に指定されたlangおよびxml:lang属性は同じ基本言語を持たなければなりません）
**********************************************************************************************************************************************************

HTML要素に指定された有効なlangおよびxml:lang属性の両方がページの基本言語と一致することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/html-xml-lang-mismatch>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 3.1.1

   -  `Language of Page <https://www.w3.org/TR/WCAG21/#language-of-page>`_
   -  `ページの言語 <https://waic.jp/translations/WCAG21/#language-of-page>`_

関連ガイドライン
================

*  テキスト： :ref:`gl-text-page-lang`

.. _axe-rule-image-alt:

****************************************************************************
Images must have alternate text （画像には代替テキストがなければなりません）
****************************************************************************

<img>要素に代替テキストが存在する、またはnoneまたはpresentationのロールが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/image-alt>`__

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

*******************************************************************************************************
Input buttons must have discernible text （入力ボタンには認識可能なテキストが存在しなければなりません）
*******************************************************************************************************

入力ボタンに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/input-button-name>`__

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

*****************************************************************************************
Image buttons must have alternate text （画像ボタンには代替テキストがなければなりません）
*****************************************************************************************

<input type="image">要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/input-image-alt>`__

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

*****************************************************************************
Form elements must have labels （フォーム要素にはラベルがなければなりません）
*****************************************************************************

すべてのフォーム要素にラベルが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/label>`__

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

*********************************************************************************************************************************************************
Elements must have their visible text as part of their accessible name （要素の視認できるテキストはそれらのアクセシブルな名前の一部でなければなりません）
*********************************************************************************************************************************************************

コンテンツによってラベル付けされた要素は、それらの視認できるテキストがアクセシブルな名前の一部になっていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/label-content-name-mismatch>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.5.3

   -  `Label in Name <https://www.w3.org/TR/WCAG21/#label-in-name>`_
   -  `名前 (name) のラベル <https://waic.jp/translations/WCAG21/#label-in-name>`_

関連ガイドライン
================

*  フォーム： :ref:`gl-form-label`

.. _axe-rule-link-in-text-block:

*********************************************************************************************************************************
Links must be distinguishable without relying on color （リンクは色に依存しない方法で周囲のテキストと区別できなければなりません）
*********************************************************************************************************************************

色に依存することなくリンクを区別できます

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/link-in-text-block>`__

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

*************************************************************************************
Links must have discernible text （リンクには認識可能なテキストがなければなりません）
*************************************************************************************

リンクに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/link-name>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 4.1.2

   -  `Name, Role, Value <https://www.w3.org/TR/WCAG21/#name-role-value>`_
   -  `名前 (name) ・役割 (role) 及び値 (value) <https://waic.jp/translations/WCAG21/#name-role-value>`_

*  達成基準 2.4.4

   -  `Link Purpose (In Context) <https://www.w3.org/TR/WCAG21/#link-purpose-in-context>`_
   -  `リンクの目的 (コンテキスト内) <https://waic.jp/translations/WCAG21/#link-purpose-in-context>`_

関連ガイドライン
================

*  マークアップと実装： :ref:`gl-markup-component`
*  入力ディバイス： :ref:`gl-input-device-support-mobile-assistive-tech`
*  リンク： :ref:`gl-link-text`

.. _axe-rule-list:

*************************************************************************************************************************************************************************
<ul> and <ol> must only directly contain <li>, <script> or <template> elements （<ul>および<ol>の直下には<li>、<script>または<template>要素のみを含まなければなりません）
*************************************************************************************************************************************************************************

リストが正しく構造化されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/list>`__

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

**************************************************************************************************************
<li> elements must be contained in a <ul> or <ol> （<li>要素は<ul>または<ol>内に含まれていなければなりません）
**************************************************************************************************************

<li>要素がセマンティックに使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/listitem>`__

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

************************************************************************************************************
<marquee> elements are deprecated and must not be used （<marquee>要素は非推奨のため、使用してはなりません）
************************************************************************************************************

<marquee>要素が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/marquee>`__

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

********************************************************************************************
Delayed refresh under 20 hours must not be used （制限時間のある更新が存在してはなりません）
********************************************************************************************

<meta http-equiv="refresh">が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/meta-refresh>`__

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

*********************************************************************
Delayed refresh must not be used （Delayed refresh must not be used）
*********************************************************************

Ensures <meta http-equiv="refresh"> is not used for delayed refresh

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/meta-refresh-no-exceptions>`__

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

*****************************************************************************************
Zooming and scaling must not be disabled （ズーミングや拡大縮小は無効にしてはなりません）
*****************************************************************************************

<meta name="viewport">がテキストの拡大縮小およびズーミングを無効化しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/meta-viewport>`__

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
*  テキスト： :ref:`gl-text-enable-enlarge`

.. _axe-rule-nested-interactive:

****************************************************************************************************
Interactive controls must not be nested （対話的なコントロールがネストされていないことを確認します）
****************************************************************************************************

ネストされた対話的なコントロールはスクリーン・リーダーで読み上げられません

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/nested-interactive>`__

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

***************************************************************************************************************
<video> or <audio> elements must not play automatically （<video> または <audio> 要素は音声を自動再生しません）
***************************************************************************************************************

<video> または <audio> 要素が音声を停止またはミュートするコントロールなしに音声を3秒より長く自動再生しないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/no-autoplay-audio>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.4.2

   -  `Audio Control <https://www.w3.org/TR/WCAG21/#audio-control>`_
   -  `音声の制御 <https://waic.jp/translations/WCAG21/#audio-control>`_

関連ガイドライン
================

*  音声・映像コンテンツ： :ref:`gl-multimedia-operable`

.. _axe-rule-object-alt:

***********************************************************************************************
<object> elements must have alternate text （<object>要素には代替テキストがなければなりません）
***********************************************************************************************

<object>要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/object-alt>`__

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

****************************************************************************************************************************************************
Styled <p> elements must not be used as headings （p要素を見出しとしてスタイル付けするために太字、イタリック体、およびフォントサイズを使用しません）
****************************************************************************************************************************************************

見出しのスタイル調整のためにp要素が使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/p-as-heading>`__

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

*************************************************************************************************
[role='img'] elements must have an alternative text （[role='img'] 要素に代替テキストが必要です）
*************************************************************************************************

[role='img'] 要素に代替テキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/role-img-alt>`__

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

************************************************************************************************************
Scrollable region must have keyboard access （スクロール可能な領域にキーボードでアクセスできるようにします）
************************************************************************************************************

スクロール可能なコンテンツを持つ要素はキーボードでアクセスできるようにするべきです

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/scrollable-region-focusable>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.1.1

   -  `Keyboard <https://www.w3.org/TR/WCAG21/#keyboard>`_
   -  `キーボード <https://waic.jp/translations/WCAG21/#keyboard>`_

関連ガイドライン
================

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`

.. _axe-rule-select-name:

****************************************************************************************************
Select element must have an accessible name （select要素にはアクセシブルな名前がなければなりません）
****************************************************************************************************

select要素にはアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/select-name>`__

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

************************************************************************************************
Server-side image maps must not be used （サーバーサイドのイメージマップを使用してはなりません）
************************************************************************************************

サーバーサイドのイメージマップが使用されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/server-side-image-map>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.1.1

   -  `Keyboard <https://www.w3.org/TR/WCAG21/#keyboard>`_
   -  `キーボード <https://waic.jp/translations/WCAG21/#keyboard>`_

関連ガイドライン
================

*  入力ディバイス： :ref:`gl-input-device-keyboard-operable`

.. _axe-rule-svg-img-alt:

*********************************************************************************************************************
<svg> elements with an img role must have an alternative text （img ロールを持つ svg 要素に代替テキストが存在します）
*********************************************************************************************************************

img、graphics-document または graphics-symbol ロールを持つ svg 要素にアクセシブルなテキストがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/svg-img-alt>`__

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

***********************************************************************************************************************************************************************
Data or header cells must not be used to give caption to a data table. （データテーブルにキャプションをつけるためにデータまたはヘッダーセルを用いるべきではありません）
***********************************************************************************************************************************************************************

キャプション付きのテーブルが<caption>要素を用いていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/table-fake-caption>`__

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

*****************************************************************************************************************************************************************************
Non-empty <td> elements in larger <table> must have an associated table header （3×3より大きいテーブルの空ではないtd要素はテーブルヘッダーと関連づいていなければなりません）
*****************************************************************************************************************************************************************************

大きなテーブルの空ではないデータセルに1つかそれ以上のテーブルヘッダーが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/td-has-header>`__

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

******************************************************************************************************************************************************************************************
Table cells that use the headers attribute must only refer to cells in the same table （table要素内のheaders属性を使用するすべてのセルは同じ表内の他のセルのみを参照しなければなりません）
******************************************************************************************************************************************************************************************

ヘッダーを使用しているテーブル内の各セルが、そのテーブル内の他のセルを参照していることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/td-headers-attr>`__

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

**********************************************************************************************************************************************************************
Table headers in a data table must refer to data cells （すべてのth要素およびrole=columnheader/rowheaderを持つ要素にはそれらが説明するデータセルがなければなりません）
**********************************************************************************************************************************************************************

データテーブルのテーブルヘッダーがデータセルを参照していることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/th-has-data-cells>`__

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

***********************************************************************************
lang attribute must have a valid value （lang属性には有効な値がなければなりません）
***********************************************************************************

lang属性に有効な値が存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/valid-lang>`__

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

***************************************************************************************
<video> elements must have captions （<video>要素にはキャプションがなければなりません）
***************************************************************************************

<video>要素にキャプションが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/video-caption>`__

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

**************************************************************************************************
autocomplete attribute must be used correctly （autocomplete属性は正しく使用しなければなりません）
**************************************************************************************************

autocomplete属性が正しく、かつフォームフィールドに対して適切であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/autocomplete-valid>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 1.3.5

   -  `Identify Input Purpose <https://www.w3.org/TR/WCAG21/#identify-input-purpose>`_
   -  `入力目的の特定 <https://waic.jp/translations/WCAG21/#identify-input-purpose>`_


.. _axe-rule-identical-links-same-purpose:

*************************************************************************************************************
Links with the same name must have a similar purpose （同じ名前を持つ複数のリンクは同様の目的を持っています）
*************************************************************************************************************

同じアクセシブルな名前を持つ複数のリンクが同様の目的を果たすことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/identical-links-same-purpose>`__

関連するWCAG 2.1の達成基準
==========================

*  達成基準 2.4.9

   -  `Link Purpose (Link Only) <https://www.w3.org/TR/WCAG21/#link-purpose-link-only>`_
   -  `リンクの目的 (リンクのみ) <https://waic.jp/translations/WCAG21/#link-purpose-link-only>`_


.. _axe-rule-accesskeys:

****************************************************************************************
accesskey attribute value should be unique （accesskey属性値は一意でなければなりません）
****************************************************************************************

すべてのaccesskey属性値が一意であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/accesskeys>`__


.. _axe-rule-aria-allowed-role:

****************************************************************************************************
ARIA role should be appropriate for the element （ARIAロールは要素に対して適切でなければなりません）
****************************************************************************************************

role属性の値が要素に対して適切であることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-allowed-role>`__


.. _axe-rule-aria-dialog-name:

*********************************************************************************************************************************************
ARIA dialog and alertdialog nodes should have an accessible name （ARIA dialogとalertdialogノードにはアクセシブルな名前がなければなりません）
*********************************************************************************************************************************************

すべてのARIA dialog、alertdialogノードにアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-dialog-name>`__


.. _axe-rule-aria-text:

****************************************************************************************************************************************
"role=text" should have no focusable descendants （"role=text"が指定されている要素には、フォーカス可能な子孫が含まれていてはなりません）
****************************************************************************************************************************************

role="text"が指定されている要素にフォーカス可能な子孫がないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-text>`__


.. _axe-rule-aria-treeitem-name:

********************************************************************************************************************
ARIA treeitem nodes should have an accessible name （ARIA treeitemノードにはアクセシブルな名前がなければなりません）
********************************************************************************************************************

すべてのARIA treeitemノードにはアクセシブルな名前があることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/aria-treeitem-name>`__


.. _axe-rule-empty-heading:

*************************************************************
Headings should not be empty （見出しは空にしてはなりません）
*************************************************************

見出しに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/empty-heading>`__


.. _axe-rule-empty-table-header:

**********************************************************************************
Table header text should not be empty （テーブルのヘッダーは空にしてはなりません）
**********************************************************************************

テーブルのヘッダーに認識可能なテキストが存在することを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/empty-table-header>`__


.. _axe-rule-focus-order-semantics:

****************************************************************************************************************************************************
Elements in the focus order should have an appropriate role （フォーカス順序に含まれる要素には、インタラクティブコンテンツに適したロールが必要です）
****************************************************************************************************************************************************

フォーカス順序に含まれる要素に適切なロールがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/focus-order-semantics>`__


.. _axe-rule-frame-tested:

**************************************************************************************
Frames should be tested with axe-core （フレームはaxe-coreでテストする必要があります）
**************************************************************************************

<iframe>および<frame>要素にaxe-coreスクリプトが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/frame-tested>`__


.. _axe-rule-heading-order:

************************************************************************************************
Heading levels should only increase by one （見出しのレベルは1つずつ増加させなければなりません）
************************************************************************************************

見出しの順序が意味的に正しいことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/heading-order>`__


.. _axe-rule-hidden-content:

************************************************************************************************
Hidden content on the page should be analyzed （ページ上の隠れているコンテンツは分析できません）
************************************************************************************************

隠れているコンテンツについてユーザーに通知します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/hidden-content>`__


.. _axe-rule-image-redundant-alt:

******************************************************************************************************************************
Alternative text of images should not be repeated as text （画像の代替テキストはテキストとして繰り返されるべきではありません）
******************************************************************************************************************************

画像の代替がテキストとして繰り返されていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/image-redundant-alt>`__


.. _axe-rule-label-title-only:

**************************************************************************************************
Form elements should have a visible label （フォーム要素には視認できるラベルがなければなりません）
**************************************************************************************************

すべてのフォーム要素がtitleまたはaria-describedby属性を使用して単独でラベル付けされていないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/label-title-only>`__


.. _axe-rule-landmark-banner-is-top-level:

********************************************************************************************************************************
Banner landmark should not be contained in another landmark （bannerランドマークは他のランドマークに含まれるべきではありません）
********************************************************************************************************************************

bannerランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-banner-is-top-level>`__


.. _axe-rule-landmark-complementary-is-top-level:

*****************************************************************************************
Aside should not be contained in another landmark （他の要素にasideを含んではなりません）
*****************************************************************************************

complementaryランドマークあるいはasideがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-complementary-is-top-level>`__


.. _axe-rule-landmark-contentinfo-is-top-level:

******************************************************************************************************************************************
Contentinfo landmark should not be contained in another landmark （contentinfoランドマークは他のランドマークに含まれるべきではありません）
******************************************************************************************************************************************

contentinfoランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-contentinfo-is-top-level>`__


.. _axe-rule-landmark-main-is-top-level:

****************************************************************************************************************************
Main landmark should not be contained in another landmark （mainランドマークは他のランドマークに含まれるべきではありません）
****************************************************************************************************************************

mainランドマークがトップレベルにあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-main-is-top-level>`__


.. _axe-rule-landmark-no-duplicate-banner:

***********************************************************************************************************************
Document should not have more than one banner landmark （ドキュメントに複数のbannerランドマークが存在してはなりません）
***********************************************************************************************************************

ドキュメント内のbannerランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-no-duplicate-banner>`__


.. _axe-rule-landmark-no-duplicate-contentinfo:

*********************************************************************************************************************************
Document should not have more than one contentinfo landmark （ドキュメントに複数のcontentinfoランドマークが存在してはなりません）
*********************************************************************************************************************************

ドキュメント内のcontentinfoランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-no-duplicate-contentinfo>`__


.. _axe-rule-landmark-no-duplicate-main:

*******************************************************************************************************************
Document should not have more than one main landmark （ドキュメントに複数のmainランドマークが存在してはなりません）
*******************************************************************************************************************

ドキュメント内のmainランドマークが最大で1つのみであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-no-duplicate-main>`__


.. _axe-rule-landmark-one-main:

************************************************************************************************************
Document should have one main landmark （ドキュメントにはmainランドマークが1つ含まれていなければなりません）
************************************************************************************************************

ドキュメントのランドマークが1つのみであること、およびページ内の各iframeのランドマークが最大で1つであることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-one-main>`__


.. _axe-rule-landmark-unique:

*************************************************************************
Ensures landmarks are unique （ランドマークが一意であることを確認します）
*************************************************************************

ランドマークは一意のロール又はロール／ラベル／タイトル (例: アクセシブルな名前) の組み合わせがなければなりません

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/landmark-unique>`__


.. _axe-rule-meta-viewport-large:

****************************************************************************************************************************************
Users should be able to zoom and scale the text up to 500% （ユーザーがズームをしてテキストを最大500％まで拡大できるようにするべきです）
****************************************************************************************************************************************

<meta name="viewport">で大幅に拡大縮小できることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/meta-viewport-large>`__


.. _axe-rule-page-has-heading-one:

***************************************************************************************************
Page should contain a level-one heading （ページにはレベル1の見出しが含まれていなければなりません）
***************************************************************************************************

ページ、またはそのフレームの少なくとも1つにはレベル1の見出しが含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/page-has-heading-one>`__


.. _axe-rule-presentation-role-conflict:

************************************************************************************************************************************
Ensure elements marked as presentational are consistently ignored （roleがnoneまたはpresentationの要素をマークしなければなりません）
************************************************************************************************************************************

roleがnoneまたはpresentationで、roleの競合の解決が必要な要素をマークします

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/presentation-role-conflict>`__


.. _axe-rule-region:

************************************************************************************************************************
All page content should be contained by landmarks （ページのすべてのコンテンツはlandmarkに含まれていなければなりません）
************************************************************************************************************************

ページのすべてのコンテンツがlandmarkに含まれていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/region>`__


.. _axe-rule-scope-attr-valid:

****************************************************************************************
scope attribute should be used correctly （scope属性は正しく使用されなければなりません）
****************************************************************************************

scope属性がテーブルで正しく使用されていることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/scope-attr-valid>`__


.. _axe-rule-skip-link:

*****************************************************************************************************************************
The skip-link target should exist and be focusable （スキップリンクのターゲットが存在し、フォーカス可能でなければなりません）
*****************************************************************************************************************************

すべてのスキップリンクにフォーカス可能なターゲットがあることを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/skip-link>`__


.. _axe-rule-tabindex:

*****************************************************************************************************************
Elements should not have tabindex greater than zero （要素に0より大きいtabindex属性を指定するべきではありません）
*****************************************************************************************************************

tabindex属性値が0より大きくないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/tabindex>`__


.. _axe-rule-table-duplicate-name:

********************************************************************************************************************
tables should not have the same summary and caption （<caption>要素にsummary属性と同じテキストを含んではなりません）
********************************************************************************************************************

テーブルのサマリーとキャプションが同一ではないことを確認します

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/table-duplicate-name>`__


.. _axe-rule-target-size:

***************************************************************
All touch targets must be 24px large, or leave sufficient space
***************************************************************

Ensure touch target have sufficient size and space

参考： `Deque Universityの解説（英語） <https://dequeuniversity.com/rules/axe/4.6/target-size>`__


