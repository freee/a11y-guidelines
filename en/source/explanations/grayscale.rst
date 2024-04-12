.. _exp-grayscale:

##################################
How to Switch to Grayscale Display
##################################

Reference: :ref:`exp-color-only`

To check how things look in grayscale display, you generally use the display switching function provided by the operating system.
Below, we will show you how to use the display switching functions for each operating system.

*************************
Windows 10 And Windows 11
*************************

1. Open the "Settings" screen and click on "Accessibility" (in Windows 10, it's called "Ease of Access") (the :kbd:`Win + U` keyboard shortcut can be used).
2. Click on "Color filters."
3. Turn on the "Color filters" switch on the right side of the window, then click the dropdown below it to show the related options.
4. Select "Grayscale."

   .. image:: /img/grayscale/win-settings-1.png
      :alt: Screenshot of the Color Filters settings screen

If you frequently use this feature, it would be useful to enable "Color Filter Keyboard Shortcut" on the same screen.
Enabling this setting allows you to toggle the color filters on and off at any time by pressing :kbd:`Win + Ctrl + C`.

.. image:: /img/grayscale/win-settings-2.png
   :alt: Screenshot of the Color Filters settings screen with Keyboard Shortcut enabled

*****
macOS
*****

The following instructions and screenshots are for macOS Ventura.

1. Select :menuselection:`Apple menu --> System Settings`.
2. In the sidebar, choose "Accessibility."
3. Click on "Display" on the right side.

   .. image:: /img/grayscale/mac-settings-1.png
      :alt: Screenshot of the Accessibility, Display settings screen

4. In the "Color Filters" section at the bottom of the screen, turn on the "Color Filters" switch.
5. Select "Grayscale" for the "Filter Type."

   .. image:: /img/grayscale/mac-settings-2.png
      :alt: Screenshot of the Color Filters settings

Reference: `Change accessibility display preferences on Mac - Apple Support <https://support.apple.com/ja-jp/guide/mac-help/unac089/mac>`_

***
iOS
***

1. Tap on the "Settings" app, then select :menuselection:`Accessibility --> Color & Text Size --> Color Filters`.
2. Turn on "Color Filters."
3. Select "Grayscale."

*******
Android
*******

For Android 12
==============

Note: The following steps are based on Android 12 on a Pixel 6. The procedure may vary depending on the device.

1. Tap on the "Settings" app, then select :menuselection:`Accessibility --> Text and display --> Color correction`.
2. Check "Use color correction."
3. Select "Grayscale" for "Correction mode."

For Android 11 And Earlier
==========================

Note: The following steps are based on Android 11 on a Pixel 3A.
The procedure may vary depending on the device model and the version of Android.

1. Tap on the "Settings" app, then go to :menuselection:`System --> Advanced`.
2. Tap on :menuselection:`Developer options` (If "Developer options" is not visible, follow the steps mentioned later to enable "Developer options").
3. Tap on :menuselection:`Simulate color space`.
4. Select "Monochromacy."

You can revert to the standard display mode by selecting "Disabled" in "Simulate color space" or by disabling "Color correction" in the "Settings" app under :menuselection:`Accessibility --> Color correction`.

Reference: Enabling Developer Options
=====================================

If "Developer Options" is not visible, follow these steps to enable it:

1. Tap on the "Settings" app, then select :menuselection:`About phone`.
2. Tap on "Build number" seven times in succession.
3. Enter the PIN set for the device.

****************************
Reference: Using Bookmarklet
****************************

As a simple method for checking, you can use a bookmarklet that turns the display of the page currently viewed in your browser into grayscale.
You can create a bookmarklet by following the steps below.

Please note that there have been reports that this bookmarklet may not function properly and can cause the display to distort when executed.
In such cases, or if you are using a browser where the bookmarklet does not function correctly, or if your are checking the display of non-web page items like mobile applications, use the display switching features of the operating system.

1. Create a bookmark (bookmarklet) with the following code.

   .. raw:: html

      <details><summary>display the code</summary>

   .. code-block:: javascript

      javascript:(function(){var d=document;s=d.createElement("style");s.innerHTML="*{filter:grayscale(100%) !important}";d.body.appendChild(s)})()

   .. raw:: html

      </details>
      <a href='javascript:(function(){var d=document;s=d.createElement("style");s.innerHTML="*{filter:grayscale(100%) !important}";d.body.appendChild(s)})();'>A Bookmarklet to Turn the Displayed Page Into Grayscale</a>

2. With the target page displayed, execute this bookmarklet.

.. include:: /inc/info2gl/exp-grayscale.rst

.. include:: /inc/info2faq/exp-grayscale.rst
