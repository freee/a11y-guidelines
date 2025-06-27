.. _exp-keyboard-notrap:


#################################
Problems Caused by Keyboard Traps
#################################

The guidelines require that if a user can use the keyboard to move the focus to a component on a page, they must also be able to move the focus away from that component using the keyboard.

This requirement was established because a common problem during the era of Java applets and Flash was that users who only used a keyboard would often get their focus trapped within an embedded Java applet or Flash player, unable to move it out.
While this situation is less common on pages implemented with standard HTML, it can still occur with React components and embedded audio/video players.

When this happens, the user is unable to access any content outside of that component.
This means that no matter how accessible other parts of the page are, the entire page becomes unusable if this problem occurs. Therefore, it is essential to prevent such situations.

It is necessary to allow users to move the focus out of a component with simple key presses like :kbd:`Tab` / :kbd:`Shift+Tab`, arrow keys, or :kbd:`Esc`.

.. include:: /inc/info2gl/exp-keyboard-notrap.rst
