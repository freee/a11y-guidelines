.. _exp-tab-order-check:

####################################################
Checking with the :kbd:`Tab` / :kbd:`Shift+Tab` Keys
####################################################

The purpose of checks using the :kbd:`Tab` / :kbd:`Shift+Tab` keys is to confirm the following:

*  Whether operation is possible using only a keyboard
*  Whether focus moves in a natural order
*  Whether behavior that could confuse the user is avoided

*******************************
Operation Using Only a Keyboard
*******************************

Some users with limited upper limb mobility who find it difficult to operate pointing devices like a mouse primarily use a keyboard to operate their PC.
Additionally, many input methods using voice recognition and interfaces using switches that are used by such users are designed to emulate keyboard behavior.
Therefore, by enabling operation using only a keyboard, the likelihood of being able to operate without problems is increased, even when inputting with such assistive technologies.

In addition to users with limited upper limb mobility, screen reader users also fundamentally operate using only a keyboard.
While the specific behavior and operation methods may differ from when a screen reader is not being used, the fact that a pointing device is not used is the same.
Therefore, it is important to enable operation using only a keyboard from the perspective of making it usable for screen reader users as well.

In the case of operation using only a keyboard, it is necessary to meet the following points:

*  All operable components (links, buttons, form fields, etc.) can be reached with the :kbd:`Tab` / :kbd:`Shift+Tab` keys:

   When operating with only a keyboard, unlike when a mouse can be used, it is not possible to move the focus to any arbitrary position on the screen.
   Therefore, it is necessary to ensure that components that can be operated can be reliably navigated to using only keyboard operations.

*  Operable components can also be operated from the keyboard:

   Since the premise is that a mouse is not necessarily being used, operable components need to be operable with only a keyboard.

   -  Events that are triggered by a mouse click should also be triggered by pressing the :kbd:`Enter` key
   -  There is no information displayed or functionality executed only by mouseover (hover)

*  The focused component can be visually distinguished:

   For example, when pressing a button, if you are using a mouse, you can move the mouse pointer over the target button and click it. However, if you are using only a keyboard, you generally need to move the focus to the desired button with the :kbd:`Tab` / :kbd:`Shift+Tab` keys and then press the :kbd:`Enter` or :kbd:`Space` key.
   In this case, if you cannot visually tell which component is focused, you cannot determine if the focus is on the desired button.
   This problem occurs when the display that indicates focus (a focus indicator) is hidden, such as when ``outline: none`` is specified in CSS.

Note that these checks must always be performed without a screen reader.
As mentioned above, the specific behavior and operation methods may differ when using a screen reader and when not using one.

Reference: How to Operate with the Mouse Pointer Hidden
=======================================================

You can hide the mouse pointer by following these steps.
If there are any operations that cannot be performed in this state when not using a screen reader, the guidelines are not being met.

#. Create a bookmark (bookmarklet) with the following code as its target.

   .. raw:: html

      <details><summary>Show code</summary>

   .. code-block:: javascript

      javascript:(function(){var s=document.createElement('style');s.innerText="*{cursor:none !important;pointer-events:none !important}*:focus{cursor: none !important;pointer-events:none !important}";document.head.appendChild(s)})()

   .. raw:: html

      </details>
      <a href="javascript:(function(){var s=document.createElement('style');s.innerText='*{cursor:none !important;pointer-events:none !important}*:focus{cursor: none !important;pointer-events:none !important}';document.head.appendChild(s)})()">Bookmarklet to hide the mouse pointer</a>

#. With the page to be checked displayed, run this bookmarklet.

Related Guidelines
==================

*  Input Devices: :ref:`gl-input-device-keyboard-operable`
*  Input Devices: :ref:`gl-input-device-focus-indicator`
*  Forms: :ref:`gl-form-keyboard-operable`

********************
Focus Movement Order
********************

As mentioned earlier, when not using a mouse, focus is primarily moved with the :kbd:`Tab` / :kbd:`Shift+Tab` keys.
In this case, the focus movement order needs to be natural from the following perspectives:

*  Screen layout:

   In most cases, moving from left to right and from top to bottom is a natural order. If there are places where the order is reversed or where the focus moves to a distant location on the screen, there may be a problem.

*  Expected operation procedure:

   Mainly in input forms, it is necessary to check that the focus movement order corresponds to the expected order of information input.

*  Context:

   In most cases, there will be no problem if the focus moves in a natural order from the perspective of the screen layout and operation procedure mentioned above, but it is also necessary to confirm that the focus movement order matches the order in which the content is read.

Related Guidelines
==================

*  Input Devices: :ref:`gl-input-device-focus`
*  Links: :ref:`gl-link-tab-order`
*  Forms: :ref:`gl-form-tab-order`

*******************************
Behavior That Confuses the User
*******************************

You need to check that no unexpected behavior occurs when the focus is moved with the :kbd:`Tab` / :kbd:`Shift+Tab` keys.
The guidelines require that components do not exhibit the following behaviors when focus is moved:

*  Page transitions
*  Form submissions
*  Displaying modal dialogs

Such behaviors can not only confuse the user but also lead to them performing unintended actions.

See also :ref:`exp-form-dynamic-content`.

.. include:: /inc/info2gl/exp-tab-order-check.rst

.. include:: /inc/info2faq/exp-tab-order-check.rst
