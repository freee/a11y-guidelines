.. _exp-markup-semantics:

###############################################
The Importance of Properly Marking Up Semantics
###############################################

We refer to the information that indicates the structure of a document as "semantics."
Examples include headings, paragraphs, lists, and the items that compose them.

In many cases where content is received visually, we determine the semantics from visual information such as text size, font type, and layout.
For example, a phrase displayed in large letters at the center of the top of the screen is judged as the heading that represents the content of the page.

However, assistive technologies, including screen readers, currently cannot accurately infer such semantics from visual characteristics.
Therefore, assistive technologies determine semantics based on how they are described in HTML.
In the example mentioned earlier, if the heading text is in an ``h1`` element, assistive technology can understand that it is a heading and communicate this to the user.
However, if it is in a ``div`` or ``span`` element and only the text size has been altered using CSS, the assistive technology cannot recognize it as a heading.

The ability of assistive technologies, particularly screen readers, to convey correct semantics to users leads to more efficient content utilization.
An example of this can be the use of the "heading jump" feature to skim through content.

Many screen readers have the capability to jump between multiple ``h1`` to ``h6`` elements on a page, allowing for the reading of headings in sequence.
This feature enables users to skim by picking up headings or by reading only the text immediately following a heading, similar to skimming.
Since many visually impaired users who utilize screen readers cannot see the entire screen at once, they are unable to quickly determine whether the accessed page contains the information they need.
Thus, being able to utilize content through such techniques leads to more efficient content utilization.

It is extremely important to use appropriate markup that represents the semantics corresponding to the content in order to enable assistive technologies to properly analyze and communicate the content to users.

.. include:: /inc/info2gl/exp-markup-semantics.rst

.. include:: /inc/info2faq/exp-markup-semantics.rst

