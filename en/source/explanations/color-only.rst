.. _exp-color-only:

#############################################
Considerations for Using Color in Expressions
#############################################

Reference: :ref:`exp-grayscale`

Color is often used to convey information.

Common examples of expressions that utilize color include:

*  Displaying labels of required fields in forms in red.
*  Showing error messages in red.
*  Indicating clickable links by changing their color.
*  Changing the color of text to emphasize it.
*  Using different colors in a pie chart to represent the distribution of responses.

Using color in expressions is not problematic in itself, but if the intended meaning is not conveyed through means other than color differences, it will not be accessible to people with color blindness or visual impairments.

For text information, it's advisable to use clever wording in combination with color to ensure the intent is communicated.

Reference: :ref:`exp-text-wording`

In the case of links, it's acceptable to use color along with another visual element like an underline.

For images, one approach is to provide textual descriptions alongside them.
In the example of a pie chart, altering the background pattern could be one strategy.

It is crucial to express intent through means other than just color differences.

Additionally, employing color combinations that consider those with color vision deficiencies—known as Color Universal Design (CUD)—is also effective.
While using expressions that do not rely on color alone can make the information accessible to those who have significant difficulties with color perception, implementing CUD can make the information even more comprehensible for people with color blindness.

The `Color Universal Design Organization (CUDO) <https://cudo.jp/>`_ [#]_ highlights the following three points of CUD:

   a. Choose color schemes that are easily distinguishable by as many people as possible.
   b. Ensure information is clear to both people who have difficulty distinguishing colors and in situations where colors are hard to distinguish.
   c. Facilitate communication using color names.

   -- `「カラーユニバーサルデザイン３つのポイント」とは？ – NPO法人 カラーユニバーサルデザイン機構 CUDO <https://cudo.jp/?page_id=86>`_

When implementing CUD, use color schemes that meet the points above.
Specifically, you can consider using color palettes like the ones published as the `Color Universal Design Recommended Color Set <https://jfly.uni-koeln.de/colorset/>`_. [#]_
However, color choices often need to align with the brand colors of products or services.
Taking such constraints into account, it is advisable to predefine your own color palette.

When verifying whether a design or implementation is accessible to people with color vision deficiencies, it is advisable to use simulators like the ones listed below.

*  `Chromatic Vision Simulator <https://asada.website/cvsimulator/e/>`_

   -  `for iOS <https://apps.apple.com/us/app/chromatic-vision-simulator/id389310222>`_
   -  `for Android <https://play.google.com/store/apps/details?id=asada0.android.cvsimulator>`_
   -  `Web Edition <https://asada.website/webCVS/>`_

.. [#] The Color Universal Design Organization (CUDO) provides `some information in English here <https://cudo.jp/?page_id=1936>`__.

.. [#] The author of the Color Universal Design Recommended Color Set provides `some information in English here <https://jfly.uni-koeln.de/color/index.html>`__.

.. include:: /inc/info2gl/exp-color-only.rst

.. include:: /inc/info2faq/exp-color-only.rst
