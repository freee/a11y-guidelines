.. _exp-axe:

########################################
Checking Accessibility With axe DevTools
########################################

axe DevTools is a very commonly used accessibility checking tool.
Its core functionality is implemented as `axe-core <https://github.com/dequelabs/axe-core>`_ which allows it to be used in various ways.
Here, we will introduce how to use it as a browser extension to check the accessibility status of existing Web pages.

For specific instructions on how to conduct checks using axe DevTools, please refer to :ref:`check-example-axe`.
Also refer to :ref:`info-axe-rules` for additional information.

**************************************
How to Install and Launch axe DevTools
**************************************

You can install the Chrome extension from the Chrome Web Store.

`axe DevTools - Web Accessibility Testing - Chrome ウェブストア <https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd>`_

The axe DevTools extension is used within the developer tools.

With the page you want to analyze open, select :menuselection:`More Tools --> Developer Tools` from the button at the right end of the toolbar, or use the shortcut keys (:kbd:`Ctrl+Shift+I` on Windows, :kbd:`Command+Option+I` on macOS).

.. image:: /img/axe/axe-1.png
   :alt: Screenshot: opening the developer tools from the menu

In the developer tools, select the "axe DevTools" tab.

.. image:: /img/axe/axe-6.png
   :alt: Screenshot: axe DevTools at the right end of the developer tools' tab bar

If the display area of the developer tools is narrow, the "axe DevTools" may be hidden under the ">>" icon.

.. image:: /img/axe/axe-2.png
   :alt: Screenshot: axe DevTools is hidden behind the '>>' icon, within the menu that appears when the icon is clicked, there is axe DevTools

***************************
Initial Setup (Recommended)
***************************

To check more items, it is advisable to perform the following initial setup:

1. Click :menuselection:`Options --> Settings`

   .. image:: /img/axe/axe-settings.png
      :alt: Screenshot: opening the Settings from the Options screen

2. Check "Enable" under "Best Practices"

   .. image:: /img/axe/axe-settings-best-practices.png
      :alt: Screenshot: checking Enable under Best Practices

3. 「Click "Save"

********************************************
Analyzing the Current Page with axe DevTools
********************************************

With the page you want to analyze open, open the axe DevTools tab within the developer tools and click the "SCAN ALL OF MY PAGE" button.

.. image:: /img/axe/axe-8.png
   :alt: Screenshot: axe DevTools tab

You can instantly identify issues on the current page.

.. image:: /img/axe/axe-9.png
   :alt: Screenshot: Displaying issues on the page with axe DevTools

**********************
How to Read the Report
**********************

In the axe DevTools interface, there are two main areas: one displays the number of issues found, and the other shows the list of those issues.

The area that displays the number of issues found will show the count of problems on that page.
Here, you can filter the list using User Impact (which is different from definitions like 'severity' within this guide) and "Best Practices" within axe DevTools.

.. image:: /img/axe/axe-3.png
   :alt: Screenshot: the area that displays the number of issues

You can view detailed information about each issue by clicking on it in the list of found problems.

The detailed view shows the location in the HTML where the issue occurs and provides information for fixing it.

.. image:: /img/axe/axe-4.png
   :alt: Screenshot: detail view of an issue

If the same issue is found in multiple places, the count is displayed on the list, and you can check each one using the pager in the detail view.

.. image:: /img/axe/axe-pager.png
   :alt: Screenshot: Pager in the detailed view

**************************************
Considerations When Using axe DevTools
**************************************

*  In areas where modal dialogs or accordions open and close, it is necessary to analyze with axe DevTools several times in both the opened and closed states.
*  While axe DevTools alone cannot detect all issues, it can instantly identify problems that can be programmatically detected. It is also extremely useful for pinpointing areas that may require further investigation.

.. include:: /inc/info2faq/exp-axe.rst

