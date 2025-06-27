.. _exp-magnification:

##############################
Accessibility in Enlarged View
##############################

Some users with low vision operate their PCs and smartphones with the display enlarged. It is essential to ensure that when the display is enlarged, the layout does not break, making it difficult to access information or operate the device.

*****************************
Enlarged View in Web Browsers
*****************************

There are two ways to enlarge the display in a Web browser: using the browser's zoom function or changing the font size.

Our guidelines require that content does not have issues when enlarged to 200% using either method.
To meet this requirement, content must work without issues when zoomed to 200% using the browser's zoom function at a minimum.

On the other hand, with the font size change function, it is highly desirable for the display to enlarge appropriately when set to 200%.
However, the minimum requirement is that no layout breakages occur that would hinder the understanding or use of the content, regardless of whether the display is actually enlarged.
This helps ensure that users who regularly use the font size change function are not inconvenienced.

When the zoom function is used, issues with enlarged displays are rare.
However, when the font size is changed, issues can arise if absolute values like ``px`` and relative values like ``em`` or ``rem`` are mixed in the font size specifications.

Furthermore, the guidelines require content to reflow appropriately so that both vertical and horizontal scrolling are not needed when enlarged to 400%.
The corresponding WCAG 2.1 Success Criterion (SC 1.4.10) for this guideline requires that content reflows so that horizontal scrolling does not occur in vertically scrolling content (e.g., horizontal text) when the display is equivalent to 320 CSS px in width, and vertical scrolling does not occur in horizontally scrolling content (e.g., vertical text) when the display is equivalent to 256 CSS px in height.
This is intended to prevent a situation where both vertical and horizontal scrolling are necessary when viewing a 1280x1024 screen at 400% zoom.

To check the display on a 1280x1024 screen, it is a good idea to set your browser window to this size and then enlarge the display.
You can easily change the window size to 1280x1024 using the following steps:

#. Create a bookmark (bookmarklet) with the following code.

   .. raw:: html

      <details><summary>Show code</summary>

   .. code-block:: javascript

      javascript:window.open(location.href,'a11ytest_1280x1024','width=1280,height=1024')

   .. raw:: html

      </details>
      <a href="javascript:window.open(location.href,'a11ytest_1280x1024','width=1280,height=1024')">Bookmarklet to change window size to 1280x1024</a>

#. While viewing the page you want to check, run this bookmarklet.

Reference: Zoom vs. Font Size Change
====================================

The zoom function is a standard feature in modern browsers that magnifies or reduces the entire window.
In Google Chrome, you can use it by selecting :menuselection:`Make Text Larger` or :menuselection:`Make Text Smaller` from the Chrome menu.
You can also use the keyboard shortcuts :kbd:`Ctrl++` and :kbd:`Ctrl+-`, respectively.

On the other hand, the font size change function only changes the size of the text.
In Google Chrome, you can set this by clicking "Customize fonts" in the "Appearance" section of the settings page.
You can also access this screen by typing ``chrome://settings/fonts`` into the address bar.

Note that the default value for this setting in Google Chrome is 16 (verified with version 85.0.4183.102).
To return to the standard display after using the font size change function, set this value.

************************************
Enlarged View in Mobile Applications
************************************

Users who need an enlarged view often use the magnification features provided by the operating system when using applications on smartphones. The following steps show how to configure the settings for an enlarged display.

For iOS
=======

You can set the maximum magnification by following these steps. Applications that support iOS's Dynamic Type feature will be displayed appropriately.

#. In the "Settings" app, tap :menuselection:`Accessibility --> Display & Text Size --> Larger Text`.
#. Turn on "Larger Accessibility Sizes".
#. Use the slider at the bottom of the screen to set the maximum size.

For Android
===========

Note: The following descriptions are for Android 16 on a Pixel 8. The steps may differ depending on the device model and Android version.

You can set the font size by following these steps:

#. In the "Settings" app, tap :menuselection:`Accessibility` --> Display size and text`.
#. Use the slider under "Font size" to set the font size.

You can also set the display size, including parts other than text, by following these steps:

#. In the "Settings" app, tap :menuselection:`Accessibility --> Display size and text`.
#. Use the slider under "Display size" to set the display size.

You can also use these two settings in combination.

.. include:: /inc/info2gl/exp-magnification.rst
