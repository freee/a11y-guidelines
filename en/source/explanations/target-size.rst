.. _exp-target-size:

###########################################################################
Issues Related to Click and Tap Target Sizes and How to Verify Target Sizes
###########################################################################

Users with upper limb disabilities may find precise actions challenging.
Similarly, among users with low vision, some may struggle with detailed mouse movements.
If the clickable or tappable area size (target size) of icons and form controls is too small, it becomes difficult for these users to click or tap on the desired location.

WCAG stipulates that form controls do not need to meet the target size requirements if their appearance has not been modified from the browser's default display.
Moreover, by properly marking up the labels of form fields, labels can also become part of the click or tap target, thus increasing the target size.

Text links within sentences are not subject to the guidelines related to target size.
However, the usability issue of having too small a target size remains the same for links, so it's beneficial to consider creatively adjusting the link text to ensure a user-friendly target size.

************************************
How to Verify Click/Tap Target Sizes
************************************

The size of elements that receive clicks or taps can be checked using the browser's developer tools.
However, this method requires accurately specifying the element whose size is to be checked and may not be straightforward when the size is controlled in complex ways.

Therefore, it's beneficial to use a simple method that involves displaying a square with a side of 44px on the screen and comparing this square to the size of the target.

Specifically, by using the following bookmarklet, you can display a square with a red border of 44px on one side, containing a smaller square with a blue border of 24px on one side that follows the mouse pointer.

#. Create a bookmark (bookmarklet) with the following code.

   .. raw:: html

      <details><summary>display the code</summary>

   .. code-block:: javascript

      javascript:(function(){var d = document,e=d.createElement('div'),g=d.createElement('div'),w=window;d.body.appendChild(e);e.appendChild(g);e.setAttribute('style','position:absolute;top:0;left:0;z-index:2147483647;box-sizing:border-box;width:44px;height:44px;border:1px solid #f00;background:#fff;opacity:0.5;transform: translate(-50%,-50%);pointer-events:none;');g.setAttribute('style','position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);box-sizing:border-box;width:24px;height:24px;border:1px solid #00f;');w.onmousemove=(function(v){e.style.left=w.scrollX+v.clientX+'px';e.style.top=w.scrollY+v.clientY+'px'})})()

   .. raw:: html

      </details>
      <a href="javascript:(function(){var d = document,e=d.createElement('div'),g=d.createElement('div'),w=window;d.body.appendChild(e);e.appendChild(g);e.setAttribute('style','position:absolute;top:0;left:0;z-index:2147483647;box-sizing:border-box;width:44px;height:44px;border:1px solid #f00;background:#fff;opacity:0.5;transform: translate(-50%,-50%);pointer-events:none;');g.setAttribute('style','position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);box-sizing:border-box;width:24px;height:24px;border:1px solid #00f;');w.onmousemove=(function(v){e.style.left=w.scrollX+v.clientX+'px';e.style.top=w.scrollY+v.clientY+'px'})})()">A Bookmarklet to Display a Square of 44x44 px</a>

#. With the target page displayed, execute this bookmarklet.

.. include:: /inc/info2gl/exp-target-size.rst

.. include:: /inc/info2faq/exp-target-size.rst
