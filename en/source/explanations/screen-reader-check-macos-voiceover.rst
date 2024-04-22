.. _exp-screen-reader-check-macos-vo:

##########################################
How to Perform Checks With macOS VoiceOver
##########################################

This document outlines the recommended settings for VoiceOver, the screen reader for macOS, its basic usage, and how to perform basic checks.

It's important to note that iOS also includes a screen reader named VoiceOver [#]_, but the VoiceOver on macOS is entirely different. This article focuses solely on macOS VoiceOver, and any mention of "VoiceOver" refers to macOS VoiceOver.

When explaining key operations in this document, notations like :kbd:`VO + →` are used, which means pressing the “VoiceOver key” along with :kbd:`→`, as explained in :ref:`macos-vo-vokey`.
Also, :kbd:`F1` to :kbd:`F12` refer to the function keys at the top of the keyboard, which may require pressing the :kbd:`fn` key simultaneously depending on your settings. (Refer to :ref:`macvo-fnkey`)

.. [#] :ref:`exp-screen-reader-check-ios-voiceover`

***************************************************
The Role of macOS VoiceOver in Accessibility Checks
***************************************************

As stated in :ref:`exp-screen-reader-check-nvda`, freee standardizes on the latest versions of NVDA on Windows and Google Chrome for necessary screen reader checks.
This is because the majority of screen reader users in Japan use Windows [#]_, and ensuring accessibility for these users is deemed crucial.

However, not all checks need to be conducted with NVDA; some can also be performed with macOS VoiceOver.
While NVDA is recommended for final checks, macOS VoiceOver can be used without issues for checks during development, especially in the following cases:

*  Verifying the behavior of existing components that have been confirmed to have no issues with NVDA.
*  Checking the behavior of parts implemented with static HTML.

For new components, it's highly recommended to conduct checks with NVDA from an early stage in development.

There may be instances where something works without issues on macOS VoiceOver but has problems on NVDA, or vice versa.
The ideal is to achieve functionality that works flawlessly in both environments, but at freee, the minimum goal is to ensure it works correctly with NVDA.

.. [#] `第3回支援技術利用状況調査報告書 <https://jbict.net/survey/at-survey-03>`__

***********
Preparation
***********

Starting and Stopping VoiceOver
===============================

VoiceOver can be started or stopped using any of the following methods:

1. Press :kbd:`Command + F5`.
2. Quickly press the Touch ID three times while pressing the :kbd:`Command` key.
3. Ask Siri to “turn on VoiceOver” (to start) or “turn off VoiceOver” (to stop).

Methods 1 and 2 will start VoiceOver if it's not already running and stop it if it is.

.. _macvo-fnkey:

Function Key Settings
---------------------

As mentioned, the :kbd:`Command + F5` key may require the addition of the :kbd:`fn` key depending on your settings.
If you frequently use function keys, consider configuring them to not require pressing the :kbd:`fn` key.

Here are the steps for setting up in macOS Ventura:

1. Select :menuselection:`Apple Menu --> System Settings`.
2. Choose "Keyboard" from the sidebar.
3. Click on "Keyboard Shortcuts" on the right side.

   .. image:: /img/macvo/macvo-settings-keyboard.png
      :alt: Screenshot: Selecting Keyboard in System Settings

4. Select "Function Keys" from the sidebar.
5. On the right, turn on "Use F1, F2, etc., keys as standard function keys."

   .. image:: /img/macvo/macvo-settings-fnkey.png
      :alt: Screenshot: Setting Function Keys

CF: `How to use the function keys on your Mac - Apple Support <https://support.apple.com/en-us/102439>`__

Operation for First-time VoiceOver Users
========================================

When VoiceOver is started for the first time, a “Welcome Dialog” will appear, and a voice will read the content on the screen.

.. image:: /img/macvo/macvo-welcome-dialog.png
   :alt: Screenshot: VoiceOver Welcome Dialog

From this dialog, you can access the VoiceOver Quick Start, but at this point, you should close this screen by pressing the :kbd:`V` key.
The VoiceOver Quick Start is provided to help visually impaired users learn how to use VoiceOver on their own.
It can be launched anytime while VoiceOver is running by pressing :kbd:`VO + Command + F8`.
It's useful for gaining a deeper understanding of how to operate VoiceOver.

Recommended Settings
====================

Pressing :kbd:`VO + F8` while VoiceOver is running launches the VoiceOver Utility, where various VoiceOver settings can be changed.
This interface displays settings categories on the left and the settings options for the currently selected category on the right.

In this section, we outline the recommended settings for performing accessibility checks, organized by category.

General
-------

.. image:: /img/macvo/macvo-util-general.png
   :alt: Screenshot: VoiceOver Utility (Selecting "General")

Uncheck "Show Welcome Dialog at VoiceOver Startup." This prevents the welcome dialog mentioned earlier from being displayed.

Visuals
-------

.. image:: /img/macvo/macvo-util-visual.png
   :alt: Screenshot: VoiceOver Utility (Selecting "Visuals")

In the "Panels and Menus" tab, enable "Show Caption Panel."
This allows the content VoiceOver is reading to be displayed on the screen.

Commanders
----------

.. image:: /img/macvo/macvo-util-commander-trackpad.png
   :alt: Screenshot: VoiceOver Utility (Selecting "Trackpad Commander" in "Commanders")

In the "Trackpad Commander" tab, uncheck "Enable Trackpad Commander."
If enabled, the trackpad can be used for VoiceOver commands, which prevents normal mouse operations.

.. image:: /img/macvo/macvo-util-commander-quicknav.png
   :alt: Screenshot: VoiceOver Utility (Selecting "Quick Nav" in "Commanders")

In the "Quick Nav" tab, uncheck "Enable Quick Nav."
When enabled, this setting allows for operations without the VO key, which might be convenient for regular VoiceOver users.
However, for conducting accessibility checks with VoiceOver, enabling this mode by mistake could lead to confusion, so we recommend keeping this setting disabled.

**********************
Things You Should Know
**********************

.. _macos-vo-vokey:

VoiceOver Key (:kbd:`VO` Key) and :kbd:`VO` Key Lock
====================================================

With VoiceOver activated, pressing certain keys in combination with others enables VoiceOver functions.
This combination is known as the "VoiceOver Key (:kbd:`VO` Key)."
The default settings designate both the :kbd:`Control + Option` combination and the :kbd:`Caps Lock` key as the VoiceOver Key.

Pressing :kbd:`VO + ;` locks the :kbd:`VO` key, allowing you to perform various VoiceOver key commands without continuously pressing the :kbd:`VO` key.
However, this changes the behavior of all key commands, so caution is needed.
For example, in this state, pressing :kbd:`Command + F5` is interpreted as pressing :kbd:`VO + Command + F5`, and VoiceOver will not exit.

If key commands do not behave as expected, it's possible the :kbd:`VO` key is locked.
In such cases, press :kbd:`VO + ;` again to unlock.

VoiceOver Cursor and Keyboard Focus
===================================

When VoiceOver is enabled, a distinctive rectangle known as the VoiceOver cursor appears on the screen.
As the VoiceOver cursor moves, it reads aloud the items it encounters, making them the target for operations.

By default, the VoiceOver cursor and keyboard focus or cursor are synchronized, typically residing in the same location.
However, they are actually independent, and their positions might not always match.

Similarly, the VoiceOver cursor and mouse pointer are independent entities.
While the default settings allow them to move independently, this behavior can be changed in the settings.

Moving the VoiceOver Cursor
===========================

The VoiceOver cursor can be moved by pressing the :kbd:`VO` key in conjunction with the arrow keys.
Typically, moving to the right with :kbd:`VO + →` progresses through the screen content, while moving to the left with :kbd:`VO + ←` allows for revisiting previous content.

As mentioned, the location of the VoiceOver cursor determines what is targeted for operations.
For instance, if the VoiceOver cursor is on a link, pressing :kbd:`VO + Spc` achieves the same result as clicking that link.
If the VoiceOver cursor is over an operable item, detailed instructions on how to operate it will be read aloud after a short pause.

Pressing the arrow keys without the :kbd:`VO` key moves the cursor as it would without VoiceOver activated, shifting the keyboard focus accordingly.
Depending on the settings, the VoiceOver cursor may or may not follow the cursor.

Operating Items
===============

When moving the VoiceOver cursor over text content with :kbd:`VO + →` and :kbd:`VO + ←`, navigation occurs in units of sentences or similarly coherent chunks of text.
However, the unit of movement might sometimes be larger, such as the elements of a window's layout.

For example, when the VoiceOver cursor is on the Google Chrome toolbar and moves rightward to the content of a displayed page, it might announce "Web content" upon reaching the page content.
This happens because VoiceOver interprets the section displaying the page as a single element.

In such cases, it's necessary to "enter" the element with the VoiceOver cursor to explore its interior.
The key command for this action is :kbd:`VO + Shift + ↓`.

In the example of Google Chrome mentioned above, pressing :kbd:`VO + Shift + ↓` when "Web content" is announced allows the VoiceOver cursor to enter the part of the page displaying content.
In this state, using :kbd:`VO + →` and :kbd:`VO + ←` enables page content review.
Additionally, elements like tables or lists within the page may be interpreted as single elements.
In such cases, using :kbd:`VO + Shift + ↓` allows you to enter these elements with the VoiceOver cursor for further exploration.
To exit the current element and move the VoiceOver cursor outside, use :kbd:`VO + Shift + ↑`.

Rotor
=====

Pressing :kbd:`VO + U` while VoiceOver is active displays a menu known as the rotor.
This menu shows a list of elements within the window that is currently focused.
For instance, if a Web page displayed in Google Chrome is focused when the rotor menu is opened, items such as links, headings, form controls, tables, and landmarks will be shown, depending on what is contained on the page.

You can switch which item's list is displayed using the left and right arrow keys.
Once you've selected the item whose list you want to view, you can navigate within that list using the up and down arrow keys.
Pressing the Enter key on an item within the list will move the focus to that item.

Key Commands to Know
====================

:kbd:`VO + A`
   Read from where the VoiceOver cursor is located.
:kbd:`VO + Shift + F4`
   Moves the VoiceOver cursor to the current keyboard focus.
:kbd:`VO + Command + F4`
   Moves the keyboard focus to the current VoiceOver cursor position.
:kbd:`VO + Shift + F5`
   Moves the VoiceOver cursor to the mouse pointer's location.
:kbd:`Ctrl`
   Pauses VoiceOver speech, pressing again resumes speech.
:kbd:`VO + K`
   Keyboard Help (Press once to enter help mode, press again to exit. In help mode, the name and function of the pressed key are read aloud.)

Reference Information
=====================

The information provided here is only a small part of what VoiceOver can do.
For more detailed information on how to use VoiceOver and its features, refer to the following:

*  `VoiceOver User Guide for Mac <https://support.apple.com/guide/voiceover/welcome/mac>`__

This guide can also be accessed from the help menu which appears when :kbd:`VO + H` is pressed.

******************
Web Content Checks
******************

Here, we explain the basic concepts and frequently performed operations when conducting checks on Web content.

When checking Web content, it is essential to ensure that all information is accessible via the VoiceOver cursor.
The basic operations involve navigating forward with :kbd:`VO + →` and moving backward with :kbd:`VO + ←`.

The size of a unit advanced or reversed with these key commands is generally by paragraph.
In cases where the text includes links, the linked portion is treated as a single unit.
Additionally, the unit of advancement when reading can vary depending on the HTML elements used.
If the reading stops midway through the text when navigating forward with :kbd:`VO + →`, it is not a problem as long as pressing :kbd:`VO + →` again continues the reading from where it left off.

Pressing :kbd:`VO + F3` allows you to have the content that was just read aloud repeated.
(To be precise, this command is to describe the item where the VoiceOver cursor is currently located.)

Making VoiceOver Read Longer text
=================================

Pressing :kbd:`VO + A` allows you to have VoiceOver read aloud the content from the current position of the VoiceOver cursor onwards.

Depending on the settings, the VoiceOver cursor may automatically move to the position of the mouse pointer. If not set up this way, pressing :kbd:`VO + Shift + F5` moves the VoiceOver cursor to the location of the mouse pointer.
By using this method, and navigating the VoiceOver cursor to the desired location with :kbd:`VO + →` or :kbd:`VO + ←`, then pressing :kbd:`VO + A`, you can verify the reading of specific sections.

Additionally, pressing :kbd:`VO + Shift + Home` (or :kbd:`VO + Shift + FN + ←` on a laptop) moves the VoiceOver cursor to the beginning of the page.
Combining this action with :kbd:`VO + A` allows for the entire page to be read aloud.

To stop the reading midway, press the :kbd:`Ctrl` key.
If you press :kbd:`Ctrl` to pause the reading and then do not perform any other action, pressing :kbd:`Ctrl` again will resume the reading.
Alternatively, pressing :kbd:`VO + A` again can also continue the reading from where it was paused.


Interactable Components
=======================

For components that accept some form of interaction, such as expandable menus or accordions, it is necessary to ensure they can be operated with a keyboard.

Specifically, move the VoiceOver cursor and keyboard focus onto the component and attempt to execute key operations on it.

By default, the VoiceOver cursor and keyboard focus are synchronized, but if they are not set up this way, use one of the following actions to move the VoiceOver cursor and keyboard focus onto the desired component:

*  Move the keyboard focus onto the component, then press :kbd:`VO + Shift + F4`.
*  Move the VoiceOver cursor onto the component, then press :kbd:`VO + Command + F4`.

When performing key operations, press keys such as the arrow keys, :kbd:`Enter`, :kbd:`Spc`, and :kbd:`Esc` without combining them with the :kbd:`VO` key to check their behavior.
If new content is displayed as a result, verify that this content can be read with the VoiceOver cursor.

VoiceOver Key Commands for Navigation
=====================================

When VoiceOver is active, you can navigate through the content using key commands such as the following:

.. list-table:: Key Commands Available in VoiceOver (excerpt)
   :header-rows: 1

   *  -  Key Command
      -  Description
   *  -  :kbd:`VO + Command + H` 、 :kbd:`Shift + VO + Command + H`
      -  Next, previous heading
   *  -  :kbd:`VO + Command + X` 、 :kbd:`Shift + VO + Command + X`
      -  Next, previous list (``ul``, ``ol``, ``dl`` elements)
   *  -  :kbd:`VO + Command + G` 、 :kbd:`Shift + VO + Command + G`
      -  Next, previous image
   *  -  :kbd:`VO + Command + J` 、 :kbd:`Shift + VO + Command + J`
      -  Next, previous form control
   *  -  :kbd:`VO + Command + T` 、 :kbd:`Shift + VO + Command + T`
      -  Next, previous table
