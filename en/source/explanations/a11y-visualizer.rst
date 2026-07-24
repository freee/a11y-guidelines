.. _exp-a11y-visualizer:

########################################################
Checking Accessibility With Accessibility Visualizer
########################################################

`Accessibility Visualizer <https://github.com/ymrl/a11y-visualizer>`__ is a browser extension that overlays information that is important for improving the accessibility of Web pages, but is not visually visible, onto the pages themselves.

It allows you to check information such as alternative text for images, heading levels, labels of form controls, table structures, lists, language attributes, and WAI-ARIA attributes while looking at the page.
It can also visually display changes in the content of ARIA live regions created by ``role="status"``, ``role="alert"``, ``role="log"``, the ``aria-live`` attribute, and the ``output`` element.

Until now, this information could only be verified by reading the accessibility tree in the browser's developer tools, reading the source code, or actually operating the page with a screen reader.
With Accessibility Visualizer, you can check this information while coding or verifying behavior, even without such knowledge or experience.

*******************************************************************
The Role of Accessibility Visualizer in Accessibility Checks
*******************************************************************

The information displayed by Accessibility Visualizer is supplementary.
Although errors and warnings are displayed for clearly problematic parts, the problems that can be detected mechanically are limited, and whether the displayed names (labels), heading levels, and so on are appropriate must be judged by the person looking at the display.

Furthermore, checks using Accessibility Visualizer do not completely eliminate the need for verification with actual assistive technologies such as screen readers.
For checks that need to be performed with a screen reader, conduct verification with NVDA as described in :ref:`exp-screen-reader-check-nvda`.

On the other hand, the advantage of Accessibility Visualizer is that it allows you to easily check things like the presence of alternative text and labels, and the structure of the page, on screen, even if you are not proficient in operating a screen reader.
Incorporating it into checks during development makes it easier to discover problems at an early stage.
It is a good idea to use it in combination with other checking tools such as :ref:`exp-axe`, and with verification using screen readers.

***********
Preparation
***********

Installation
============

Accessibility Visualizer can be installed from the Chrome Web Store for Google Chrome, and from Firefox Add-Ons for Mozilla Firefox.

*  `Accessibility Visualizer - Chrome Web Store <https://chromewebstore.google.com/detail/accessibility-visualizer/idcacekakoknnpbfjcdhnkffgfbddnhk>`__
*  `Accessibility Visualizer – Get this Extension for Firefox <https://addons.mozilla.org/en-US/firefox/addon/accessibility-visualizer/>`__

After installation, an Accessibility Visualizer item will appear in the browser's extension menu.
If you use it frequently, we recommend pinning it to the browser's toolbar.
When pinned to the toolbar, the Accessibility Visualizer icon will always be displayed.

Displaying the Popup
====================

Clicking the Accessibility Visualizer item in the extension menu, or the Accessibility Visualizer icon pinned to the toolbar, opens the Accessibility Visualizer popup.
In this popup, you configure settings such as selecting which information to display.

There is an "Enabled" checkbox in the popup.
If you uncheck it, no information will be displayed on Web pages.

Note that settings are saved per domain, so you can maintain display settings suited to each site.

***********
Basic Usage
***********

Displaying Tips
===============

When you check the "Show tips" checkbox in the popup, various pieces of information will be displayed on the Web page you are viewing as small labels called "tips."

There are several types of tips, distinguished by color and icon. The following three types are particularly important when performing checks:

Name
   Displayed in green with a person icon.
   It shows the element's "accessible name," that is, the content conveyed to assistive technologies such as screen readers as the alternative text of an image, the label of a form control, or the text of a link or button.
Warning
   Displayed in yellow with a warning triangle icon.
   It indicates a part that may have a problem and should be checked carefully.
Error
   Displayed in red with an error triangle icon.
   It indicates a part that definitely has a problem and requires correction.

In addition, there are tips that indicate heading levels, landmark types, table sizes and cell positions, the number of list items, languages, roles, WAI-ARIA attributes, and more.

When you check the "Interactive" checkbox, tips will appear subdued until you mouse over them.
This is useful when many tips are displayed and the page becomes hard to see.

The display positions of tips may sometimes shift.
In such cases, press the "Re-run" button in the popup.

Presets
=======

The targets for which tips are displayed can be selected individually with the checkboxes in the popup, or easily switched using the preset feature.

*  **Basic**: Displays headings, images, form controls, buttons, links, page, language, and WAI-ARIA information
*  **Structure**: Displays headings, sections, page, and language information
*  **Content**: Displays images, links, tables, and lists
*  **Custom**: Freely select which information to display

Live Region Announcements
=========================

When "Announce live regions" is checked in the popup, changes to the content of ARIA live regions will be displayed prominently near the center of the screen.

ARIA live regions are used to convey changes in the state of the screen to users of assistive technologies such as screen readers (see :ref:`exp-dynamic-content-status`).
Using this feature, you can verify that notifications by live regions occur as intended, without using a screen reader.

While announcements are displayed, the following key operations are available:

:kbd:`Shift`
   Toggle pause/resume
:kbd:`Ctrl`
   Clear the displayed announcements

Display Customization
=====================

How tips and live region announcements are displayed can be customized in the popup settings.
You can adjust the opacity and font size of tips, as well as the opacity, font size, and display duration of live region announcements, so it is a good idea to adjust these settings to make them easy to see on the page you are checking.

*******************************
How to Use It for Checks
*******************************

This section explains the points to check in accessibility checks, for each type of information displayed as tips.

Images
======

When "Images" is checked, tips are displayed for ``img`` elements, ``svg`` elements, and elements with the ``role="img"`` attribute.

*  Name tips display the alternative text of images.
   Check that it is a concise description that conveys almost the same information even if displayed in place of the image. (See :ref:`exp-image-text-alternative`)
*  For ``img`` elements with ``alt=""``, an "Empty alt attribute" warning tip is displayed.
   Images in this state cannot be perceived by assistive technologies such as screen readers.
   Unless the image is placed for decorative purposes, alternative text must be provided.
*  If no alternative text is specified and the element is not ``aria-hidden`` and does not have ``alt=""``, a "No alt attribute" or "No accessible name" error tip is displayed.
   In this case, correction is required.

Headings
========

When "Headings" is checked, tips are displayed for ``h1`` through ``h6`` elements and elements with the ``role="heading"`` attribute.

*  "Heading" tips display the level of the heading.
   Check that the level is appropriate for the structure of the page. (See :ref:`exp-page-structure`)
*  For elements with the ``role="heading"`` attribute but without the ``aria-level`` attribute, a warning tip "No heading level" is displayed.
   Explicitly specifying the ``aria-level`` attribute is recommended.
*  If no name is given to a heading, a "No accessible name" error tip is displayed.
   In this case, correction is required.

Form Controls
=============

When "Form Controls" is checked, tips are displayed for ``input`` elements (excluding those whose ``type`` attribute is ``hidden``, ``button``, ``submit``, ``reset``, or ``image``), ``textarea`` elements, ``select`` elements, ``label`` elements, ``fieldset`` elements, and elements whose ``role`` attribute is one of ``textbox``, ``combobox``, ``checkbox``, ``radio``, ``switch``, ``menuitemcheckbox``, or ``menuitemradio``.

*  Name tips display the labels of form controls.
   Check for omissions and that the labels are appropriate. (See :ref:`exp-form-labeling`)
*  If no name is given, a "No accessible name" error tip is displayed.
   In this case, correction is required.
*  For elements that are not focusable by default and have no ``tabindex`` attribute specified, a "Not focusable" error tip is displayed.
   In this state, keyboard operation is not possible, so correction is required.
*  If there is a problem with the grouping of radio buttons, error tips such as "No name attribute" or "Ungrouped radio button" are displayed.
   In this state, selection with the keyboard does not work correctly, so correction is required.
*  For ``label`` elements whose associated form control does not exist or is hidden, a "Not associated with any control" warning tip is displayed.
   Especially when the control is hidden with ``display:none`` or similar techniques in order to style checkboxes or radio buttons, there is a high possibility that it cannot be operated with the keyboard, so verification is required.

Buttons and Links
=================

When "Buttons" is checked, tips are displayed for ``button`` elements, ``input`` elements whose ``type`` attribute is one of ``button``, ``submit``, ``reset``, or ``image``, and elements with the ``role="button"`` attribute.
When "Links" is checked, tips are displayed for ``a`` elements, ``area`` elements, and elements with the ``role="link"`` attribute.

*  Name tips display the labels of buttons and the text of links.
   Check that the content allows users to predict the behavior or the link destination just by reading it. (See :ref:`exp-link-text`)
*  If no name is given, a "No accessible name" error tip is displayed.
   In this case, correction is required.
*  For elements with the ``role="button"`` attribute that are not focusable by default and have no ``tabindex`` attribute specified, a "Not focusable" error tip is displayed.
   In this state, keyboard operation is not possible, so correction is required.
*  For ``a`` or ``area`` elements without the ``href`` attribute, a warning tip "No href attribute" is displayed.
   If click interactions are set on elements in this state, they may not be operable with the keyboard, or users of assistive technologies may not be able to recognize them as interactive targets, so correction is required.

Sections
========

When "Sections" is checked, tips are displayed for ``article``, ``section``, ``nav``, ``aside``, ``main``, ``form``, and ``search`` elements, and for elements whose ``role`` attribute is one of ``article``, ``banner``, ``complementary``, ``contentinfo``, ``main``, ``form``, ``navigation``, ``region``, ``search``, or ``application``.

These elements are used to divide the content of a page into sections, and help users of assistive technologies understand the structure of the page and skip unwanted content. (See :ref:`exp-page-structure`)

*  Landmark tips display the type of the landmark.
   Check that the role is appropriate.
*  If an accessible name is given, name tips display the name of the section.
   Check that the name is appropriate, and that no landmarks with the same name and the same role exist on the page.

Tables
======

When "Tables" is checked, tips are displayed for ``table`` elements and related elements.

*  "Table size" tips display the number of rows and columns of the table, and "Position" tips display the position of each cell.
*  "Table header" tips display the content of the table headers (``th`` elements) corresponding to each cell.
   Especially for complex tables, check that headers and cells are properly associated.

Lists
=====

When "Lists" is checked, tips are displayed for ``ul``, ``ol``, and ``dl`` elements and their list items.

*  The type of the list and the number of items are displayed.
   Check that content that should be expressed as a list is marked up appropriately.

Language
========

When "Language" is checked, tips are displayed for elements with the ``lang`` attribute.

*  You can check the language setting of the entire page (the ``lang`` attribute of the ``html`` element) and the specifications for parts where the language changes.
   Check that the language is set appropriately.
   Language specification is important for screen readers to read content aloud with the correct pronunciation. (See :ref:`exp-text-lang`)

WAI-ARIA
========

When "WAI-ARIA" is checked, tips are displayed for elements with WAI-ARIA attributes.

*  WAI-ARIA attribute tips display the names and values of the attributes applied to elements.
   Check that attributes such as ``aria-expanded`` and ``aria-selected`` are set appropriately and change as expected in response to operations.
*  Warning tips are displayed for elements with the ``aria-hidden="true"`` attribute.
   Elements with this attribute cannot be perceived by users of assistive technologies such as screen readers.
   If there are elements other than decorative ones that are visually visible but have ``aria-hidden``, correction is required.

Live Regions
============

Using the "Live Region Announcements" feature described above, you can check the following points about dynamically changing content:

*  Dynamic changes such as status messages are announced by ARIA live regions
*  No unintended content is announced, and announcements do not occur too frequently

***********
Usage Notes
***********

*  The display positions of tips may sometimes shift. In such cases, press the "Re-run" button in the popup
*  Some Web sites may become slow when tips or announcements are displayed. When viewing such sites, uncheck "Show tips" and "Announce live regions"
*  In parts that use frames or Shadow DOM, tips and live regions may not be displayed due to technical constraints
*  Interactive mode may interfere with mouse operations on Web pages
*  To reiterate, checks with Accessibility Visualizer are not a substitute for verification with actual assistive technologies such as screen readers. See also :ref:`exp-screen-reader-check`

*********************
Reference Information
*********************

*  `Accessibility Visualizer User's Guide <https://github.com/ymrl/a11y-visualizer/blob/main/docs/en/UsersGuide.md>`__
