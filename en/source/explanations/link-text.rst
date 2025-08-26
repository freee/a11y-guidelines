.. _exp-link-text:

############################################
Making It Easy to Guess the Link Destination
############################################

Making it easier to predict whether a link leads to the desired information improves the user experience for everyone.

For users with physical disabilities who take more time to operate a mouse, it is especially important to make it easier to predict the content of a linked page and thereby prevent unnecessary page transitions.

Additionally, screen reader users may use their screen reader's feature to list all links on a page to find the one they need.
Many users also find links by repeatedly pressing the :kbd:`Tab` / :kbd:`Shift+Tab` keys to move the focus.
In these cases, it is crucial that the link text (the content of the ``a`` element) enables users to predict the content of the destination page.

.. list-table:: Examples of problematic link text (link text is in quotation marks)
   :header-rows: 1

   *  -  Inadvisable
      -  Recommended
   *  -  "Click here" for XX
      -  "Click here for XX"
   *  -  "Read more"
      -  "Read more about XX"
   *  -  "Details"
      -  "Details about XX"

You can also meet the guidelines if the link's purpose is clear from the markup.

Specifically, consider a page with multiple links that have the same link text and meet the following conditions:

*  If the links are in different sections of the page, the headings are properly marked up, making it clear which section each link is in.
*  If a list contains links with the same link text, the list items are properly marked up, making it clear which list item each link belongs to.
*  If a table has links with the same link text in each row, the ``table`` element and related elements are properly marked up, making the row and column of each link clear.

.. include:: /inc/info2gl/exp-link-text.rst
