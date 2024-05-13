.. _exp-check-contrast:

##################################
Method for Checking Contrast Ratio
##################################

In both Web and mobile applications, it is crucial to use color combinations that meet the contrast ratio criteria for text and UI components to ensure that content is perceivable by people with low vision.

To identify areas on a Web page where the color contrast ratio is insufficient, it is recommended to use checking tools such as `axe DevTools`_.
If check tools as such are not available, such as when checking mobile application screens, using tools that calculate the contrast ratio between specific colors, such as `WebAIM: Contrast Checker`_, in combination with a color picker, would be beneficial.

*******************************
Using Accessibility Check Tools
*******************************

In Google Chrome, you can check for accessibility issues, including color contrast ratio problems, using the Lighthouse tab in the developer tools.

Additionally, with `axe DevTools`_, you can identify areas with accessibility issues, including contrast ratio problems, across the entire Web page.
axe DevTools is available as a `Google Chrome extension`_ and a `Mozilla Firefox add-on`_.

***********************************************************
When Automatic Contrast Ratio Detection Cannot Be Performed
***********************************************************

These tools may not provide accurate contrast ratio assessments in cases such as for text within images.

For the axe DevTools Chrome extension, if the contrast ratio cannot be determined, the message "Elements must have sufficient color contrast" will be displayed, just as when the contrast ratio is insufficient.
However, if automatic detection fails, the detailed panel will display a message such as "This potential issue needs your review... Cannot determine the contrast ratio."

Additionally, axe DevTools can only be used for checking web pages and cannot be used for checking screens of mobile applications.

In such cases, it is necessary to examine the color codes of the specific areas and manually check the contrast ratio.

Checking Screens of Mobile Applications
=======================================

The followings are a few examples of how you might conduct checks on screens of mobile applications.

*  Take screenshots and check the images on a PC.
*  Share the screen using online meeting tools such as Google Meet and check the shared screen on a PC.
   Exercise caution when using this method, as some online meeting tools may apply color correction to the shared screen.

Examining Color Codes
=====================

Using a tool called a color picker, you can examine the color codes used in specific areas where contrast ratio checks are required.

Although WebAIM: Contrast Checker described below provides a color picker, there are also tools available for Windows and macOS.
Here are some popular ones:

Windows
-------

Color picker is provided as one of the features of Microsoft PowerToys.

Microsoft PowerToys can be obtained from the Microsoft Store or GitHub:

*  `Microsoft PowerToys (Microsoft Store)`_
*  `Microsoft PowerToys (GitHub)`_

Reference: `Microsoft PowerToys: Utilities to customize Windows`_

macOS
-----

macOS comes with a built-in color picker called Digital Color Meter.

Reference: `Digital Color Meter User Guide for Mac`_

When using the color picker on macOS, it may be influenced by the display's color profile.
To prevent this, deselect the "Show profiles for this display only" checkbox in macOS's color profile settings, then choose "SRGB IEC61966-2.1".

Reference: `Change your Mac display’s color profile`_

In Figma, you can check the color profile applied to each file by selecting "File color profile" from the menu located at the top of the screen next to the file name.
If it's set to "sRGB" or "Same as preferred profile (sRGB)," there's no issue.

Additionally, you can ensure that sRGB is selected for new file creation by changing it in Figma's preferences menu under ":menuselection:`Preferences --> Color profile...`" available from the menu icon in the top left corner of the Figma interface.

Contrast Ratio Calculation Tools
================================

Because the formula for calculating contrast ratio is complex, it is common to use calculation tools such as `WebAIM: Contrast Checker`_.
There are also checker tools that can be installed and run persistently, such as `contrast.app`_.

Note that there may be discrepancies in the rounding of decimal places among contrast ratio calculation tools, resulting in varied calculation results.
It's advisable to consider the results as approximate and opt for colors that provide a margin of contrast.

**********
References
**********

*  :ref:`exp-contrast`
*  |Vibes Color Contrast|

.. include:: /inc/info2gl/exp-check-contrast.rst

.. _axe DevTools: https://www.deque.com/axe/
.. _WebAIM\: Contrast Checker: https://webaim.org/resources/contrastchecker/
.. _Google Chrome extension: https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd
.. _Mozilla Firefox add-on: https://addons.mozilla.org/firefox/addon/axe-devtools/
.. _contrast.app: https://usecontrast.com/
.. _Change your Mac display’s color profile: https://support.apple.com/en-us/guide/mac-help/mchlf3ddc60d/mac
.. _Digital Color Meter User Guide for Mac: https://support.apple.com/en-us/guide/digital-color-meter/welcome/mac
.. _Microsoft PowerToys (Microsoft Store): https://apps.microsoft.com/detail/xp89dcgq3k6vld
.. _Microsoft PowerToys (GitHub): https://github.com/microsoft/PowerToys
.. _Microsoft PowerToys\: Utilities to customize Windows: https://learn.microsoft.com/en-us/windows/powertoys/
