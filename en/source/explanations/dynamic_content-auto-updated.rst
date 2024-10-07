.. _exp-dynamic-content-auto-updated:

##########################################
Issues with Content Changing Automatically
##########################################

Some users with cognitive or attention disabilities may find it difficult to understand information when the following types of content are displayed on the same page along with other content:

*  Automatically updated
*  Moving
*  Flashing
*  Auto-scrolling

If these dynamic changes do not occur automatically or only last for a short period, such content is generally not problematic. However, in cases where they persist, WCAG requires that users be able to control these dynamic changes.

Furthermore, stricter WCAG success criterion prohibits interruptions, such as push notifications, except in emergencies. Interruptions can not only break the concentration of users with cognitive or attention disabilities, but can also disrupt screen reader users, causing confusion by interrupting the reading of information. To avoid such confusion, WCAG allows interruptions only when it is needed for protecting health, property, or safety.

If brightness alternates at a specific frequency (causing a flashing effect) within a certain area of the page, it may trigger photosensitive seizures in some users.
WCAG’s Level A success criterion allows flashing under certain conditions.
On the other hand, the Level AAA success criterion sets a stricter condition, allowing no more than 3 flashes per second in any situation.
However, it may be difficult to precisely meet or verify compliance with the limited conditions of Level A.
Since this is a matter of user safety, freee has adopted the stricter Level AAA success criterion.

Reference: This success criterion was added in response to the so-called `Pokémon Shock <https://en.wikipedia.org/wiki/Denn%C5%8D_Senshi_Porygon>`__ incident.

.. include:: /inc/info2gl/exp-dynamic-content-auto-updated.rst
