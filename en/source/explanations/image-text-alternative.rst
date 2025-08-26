.. _exp-image-text-alternative:

##############################
Describing Images Through Text
##############################

Images may not be adequately accessible to users who are totally blind or have low vision.

For users who are totally blind, it is clear that they cannot see the images.
Additionally, the current capabilities of image recognition and prediction features in some screen readers are far from perfect, and it is not feasible to rely solely on these features.

On the other hand, users with low vision may find images difficult to view due to factors such as the size of the image or the color combinations used.

To avoid these problems, it is necessary to provide text that conveys the same information as the image.
More specifically, a text description of the image should be provided.
It is important that the information is neither insufficient nor excessive.
It is certainly not good if the information provided is insufficient, but providing too much is also undesirable.

The amount and detail of the description needed depend on the content of the image and the context in which it is used.

Example 1:
For an icon that performs a specific function, if the function of the icon is widely recognized, it is appropriate to provide text that describes that function.
However, if the meaning of the icon is not clear to most people, it may be necessary to describe its visual characteristics (depending on the creator's intent).

Example 2:
If there is an image depicting a graph, and the surrounding text sufficiently explains the content of the graph such that the image only aids in understanding, then it is sufficient to provide text that indicates it is a graph.
However, if meaningful information cannot be obtained without viewing the image, it will be necessary to provide a textual description of the graph's trends or the numerical data on the graph.

It is necessary to consider the context and content when preparing descriptions, aiming for as much consistency as possible.
A collection of examples to help determine the appropriate descriptions is planned to be developed.

For short descriptions, using the ``alt`` attribute of the ``img`` element, or possibly the ``aria-label`` or ``aria-labelledby`` attributes, would be suitable.
For longer descriptions, in addition to using the ``aria-describedby`` attribute or the ``figcaption`` element, it is also possible to place a link to a detailed description or text containing detailed explanations around the image.

The above is applicable when the image contains meaningful information.
If the image is purely decorative and contains no meaningful information, it is necessary to write in such a way that assistive technologies like screen readers can ignore the presence of the image.

Specifically, an empty ``alt`` attribute can be added to the ``img`` element (``<img src="image.png" alt="">``), or ``role="presentation"`` can be used.

Moreover, in situations like Example 2 above, an appropriate description must be attached since the graph image provides information.
While one might think that the image description is not needed when the content's meaning is clear without the description, text descriptions are useful not only for totally blind users.
Low vision users who primarily rely on screen readers might realize there is a graph and decide to enlarge it for a closer look.
Also, knowing that there is a graph can facilitate communication with sighted individuals for a totally blind user.

.. include:: /inc/info2gl/exp-image-text-alternative.rst

.. include:: /inc/info2faq/exp-image-text-alternative.rst
