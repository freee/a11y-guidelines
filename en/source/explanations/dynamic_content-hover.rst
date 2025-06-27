.. _exp-dynamic-content-hover:

########################################################
Content Displayed on Mouseover (Hover) and Magnification
########################################################

When new content is displayed, triggered by a mouseover (hover) with the mouse pointer or by receiving keyboard focus, it can hinder access, especially for low-vision users who rely on magnification.

When using magnification, only a portion of the content is displayed on the screen at any given time.
Users navigate by moving the mouse pointer to switch the magnified area, eventually piecing together the entire content.

First, during this process, the mouse pointer can unintentionally trigger a mouseover display.
When this happens, the newly displayed content can obscure the content the user was viewing or the component they were trying to interact with, preventing them from continuing their task.

Of course, this is not an issue if the content displayed on mouseover does not interfere with the use of other content, but it is not realistic to anticipate all the different magnification levels used by various users.
If, at this point, the user could hide the mouseover content without moving the mouse pointer, for example, by pressing the :kbd:`Esc` key, they could easily resume their previous task.

On the other hand, if a user with magnification wants to read the content displayed on mouseover, they may need to scroll, especially if the displayed content occupies a large area.
However, if the content disappears when the mouse pointer moves away from the object that triggered the mouseover, they cannot perform this operation.
To avoid this problem, it is necessary to ensure that the content remains visible as long as the mouse pointer is over the newly displayed content.

As a result, using magnification often requires more operations and takes more time to read the same content compared to not using it.
Therefore, it is generally recommended that content displayed on mouseover not automatically hide itself, except when the user actively performs an action to hide it or when the displayed content becomes meaningless (for example, a "loading..." message).

Even when these criteria are met, it is important to note that if the object that triggers the mouseover display is far from where the content is actually displayed, the user may not notice the new content.
It is important to carefully consider whether a mouseover display is truly the best method.

You should also note that when using mouseover as a trigger, it is crucial to also use keyboard focus as a trigger to meet the requirements of :ref:`gl-input-device-keyboard-operable`.

.. include:: /inc/info2gl/exp-dynamic-content-hover.rst
