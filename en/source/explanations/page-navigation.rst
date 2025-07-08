.. _exp-page-navigation:

##############################################################################
Designing and Implementing Navigation for Improved Usability and Accessibility
##############################################################################

The navigation mechanisms and site structure significantly impact a Web site's usability.
This short article explains the importance of consistent navigation, clearly indicating the page's location, and providing multiple pathways.

*********************
Consistent Navigation
*********************

Users with low vision who use magnification to view a screen may operate by looking at only a portion of it.
For such users, if the order and layout of navigation links are consistent across all pages, it becomes easier to infer the page structure, allowing them to find the desired functions more quickly and easily.

Furthermore, for screen reader users, having the screen reader announce all common navigation elements on every page is time-consuming and inefficient.
However, if the order and layout are consistent, it is not always necessary to read out the same content every time.

What is crucial here is that in addition to visual consistency in the order and layout, consistent markup should also be used.
Screen readers add information to convey the semantics indicated by the markup.
Therefore, even if something appears visually the same, if the markup differs, the way it is read aloud will also differ, leading to a lack of consistency in the spoken output.

**************************************
Clearly Indicating the Page's Location
**************************************

Clearly indicating where a page is located within the site's structure is crucial for users to understand that structure.
Understanding the site structure helps users reach their target page more easily and facilitates assumptions when performing various operations.

For example, displaying a breadcrumb trail that shows the hierarchical structure from the site's top page helps users understand the position of the current page.

Furthermore, indicating which global navigation item the current page belongs to also helps users understand the site structure.
This can be achieved by visually highlighting the global navigation item.
Additionally, by appropriately using the ``aria-current`` attribute, screen reader users can also be informed of which item the current page belongs to.

***************************
Providing Multiple Pathways
***************************

If a page has only one pathway, it becomes difficult to reach for users who don't accurately understand or can't easily infer the site structure.
To mitigate this issue, providing multiple pathways is recommended.

Specifically, pages reachable from the global navigation fulfill this condition, as they can be accessed from anywhere within the site.
Also, if a page can be reached via a link within a specific page as well as by some other means, this condition is met.
Here are some specific examples:

*  Links from a help page
*  Links from site search results
*  Links from a list page in addition to links from results displayed using the list page's filter function

However, there is no need to provide multiple pathways for pages that only make sense when displayed in a specific context, such as the following examples:

*  Pages displayed in the middle of a wizard
*  Pages displayed only when a specific operation is performed, such as showing operation results

.. include:: /inc/info2gl/exp-page-navigation.rst
