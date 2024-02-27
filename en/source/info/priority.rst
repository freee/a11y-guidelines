.. _info-priority-diff:

#########################################################
Our Guidelines and the Level of WCAG 2.1 Success Criteria
#########################################################

Our guidelines have been formulated with the policy of ensuring content can achieve Conformance Level AA of WCAG 2.1.
Therefore, each guideline is based primarily on the success criteria of Levels A and AA of WCAG 2.1, though there are some exceptions.
In considering the guidelines, we have reviewed all success criteria of WCAG 2.1, including those of Level AAA.
The levels assigned to each success criterion have been reconsidered in light of the nature of freee's products, and for some criteria, it has been decided to assume levels different from those indicated by WCAG 2.1.

Here, we present a list of the success criteria for which the levels have been revised from those indicated by WCAG 2.1, along with the reasons for the revision.

************************************
Success Criteria with Revised Levels
************************************

.. include:: /inc/misc/priority-diff.rst

*******************************
Reasons for Revising the Levels
*******************************

Many of the success criteria for which the levels were revised have been assumed to be of a higher level than those indicated in WCAG 2.1, under the judgment that they hold greater importance in freee's products.
For success criteria that were revised for reasons different from this, those reasons are provided below.

Success Criterion 1.2.6
^^^^^^^^^^^^^^^^^^^^^^^

To make audio information accessible to individuals with hearing impairments, there are methods such as providing captions and sign language interpretation.
Among the hearing impaired, some are more adept at communication using written text, while others may prefer communication through sign language.
(Of course, there are also individuals who are equally proficient in both.)

Since the effectiveness of text information versus sign language varies from user to user, from the perspective of ensuring information access, both are equally important.
Our guidelines do not target success criteria at Level AAA as per WCAG 2.1, hence, adhering strictly to the levels indicated by WCAG 2.1 could potentially overlook the provision of sign language interpretation, even if it were feasible.

Ideally, like captions, it would be preferable to treat it as Level A, but considering the difficulty of implementation, we have decided to designate it as Level AA.

Success Criterion 1.3.5
^^^^^^^^^^^^^^^^^^^^^^^

This success criterion requires that for form controls asking for user input, the type of information expected to be input is clearly identified.
The explanation for this success criterion in `Understanding Identify Input Purpose <https://www.w3.org/WAI/WCAG21/Understanding/identify-input-purpose.html>`_  suggests the use of the ``autocomplete`` attribute as a specific method.

Form controls utilizing the ``autocomplete`` attribute can facilitate easier input in situations where the inputs are consistently the same values or when there are few items to input.
However, in other cases, it may lead to inadvertent errors.

In freee's products, due to their nature, there are pages with numerous form controls, and many items do not always require the input of fixed values.
Therefore, using the ``autocomplete`` attribute carelessly to meet the guideline's criteria could potentially detract from usability.

Considering these factors, we have decided not to include an item corresponding to this success criterion in our guidelines.

Success Criterion 1.4.13
^^^^^^^^^^^^^^^^^^^^^^^^

This success criterion aims to make content displayed via mouseover (hover) more accessible to users utilizing magnification.
Specifically, it intends to prevent the content from becoming hidden contrary to the user's intent and to allow the user to hide the content when necessary.

Among these, the phenomenon where content becomes hidden contrary to the user's intent could potentially make it impossible for users to utilize the content depending on the situation.
Considering this, our guidelines have singled out this aspect and treated it as an item equivalent to Level A.
