.. _intro-intro:

####################################
About freee Accessibility Guidelines
####################################

************************************
Background of Guidelines Development
************************************

Within freee K.K., as initiatives aimed at improving product accessibility have progressed, several reference materials have been compiled by volunteers.
This document is designed to consolidate these pieces of information in one place and continuously update them, with the goal of providing more user-friendly materials for development on the ground.

As for guidelines related to Web accessibility, the `Web Content Accessibility Guidelines (WCAG) 2.0 <WCAG20_>`_, which became a W3C Recommendation in 2008, is widely used internationally.
Furthermore, WCAG 2.0 has become an international standard as ISO/IEC 40500:2012 and as a corresponding identical standard in Japanese Industrial Standards as JIS X 8341-3:2016, making it a frequently referenced guidelines document in Japan as well.

Although ideally, adopting WCAG directly as an internal guideline would be beneficial, in practice, it poses significant challenges.
This is because WCAG is written in a technology-neutral manner.
This ensures that the guidelines can be applied to technologies used on the Web in the future that may shift from HTML, CSS, and JavaScript, and it may also become applicable to media other than the Web.
However, as a result, the expression has become abstract, making it difficult to understand in the development field.
To avoid this problem, we decided to compile our own guidelines that follow the content of WCAG while keeping in mind the usability in the development field.

The freee Accessibility Guidelines are edited with the following policy:

*  Avoid abstract and difficult-to-understand expressions as much as possible, and use concrete expressions with development using HTML/CSS/JavaScript and application development for iOS and Android in mind.
*  By adhering to the guidelines outlined in this document, the aim is to achieve compliance with WCAG 2.1 at Level AA.
*  Classify according to the type of content targeted, such as images, links, forms, so that what needs to be done for each can be understood.
*  Review the levels of the WCAG 2.1 success criteria which the guidelines are based on, considering the nature of freee's products.
*  Clearly state the methods for checking whether each guideline has been met as much as possible.
*  Provide reference information and examples to aid understanding.

The guidelines presented in this document are based on `WCAG 2.1 <WCAG21_>`_, which became a W3C Recommendation in 2018.
WCAG 2.1 includes additional items reflecting changes in the situation after the development of WCAG 2.0, but the changes maintain compatibility, so meeting WCAG 2.1 also meets WCAG 2.0 and JIS X 8341-3:2016.

***************************
Structure of the Guidelines
***************************

This document categorizes the essential elements (guidelines) for ensuring accessibility into categories based on their applicability.

Each guideline consists of the main text of the guideline, in addition to the following information:

Target Platforms
================

The targeted entities for each guideline are indicated as follows:

Web
   Desktop Web and mobile Web (things displayed in browsers and in Web views)
Mobile
   Mobile applications

Intent
======

This section briefly outlines the needs of users that each guideline intends to meet.
By understanding the core issue that each guideline aims to address, it facilitates a more accurate assessment of whether the guideline have been fulfilled.

Corresponding Success Criteria of WCAG 2.1
==========================================

This section indicates which success criteria of WCAG 2.1 each guideline is based on.
It serves as a reference for determining which success criteria of WCAG 2.1 are met by fulfilling this guideline.
It includes the criteria number, level, and links to the original text.

Additionally, a list of guidelines corresponding to each success criterion of WCAG 2.1 is provided in :ref:`info-wcag21-mapping`.

Supplementary Information
=========================

Where necessary, links to reference information for a better understanding of the "Intent" and supplementary information about the methods of verification may be provided.

Related FAQs
============

Links are provided to FAQs listed in :ref:`faq-index` that are related to the guideline.

.. _intro-intro-check:

Checklist Items
===============

This section provides examples of checks to determine whether the guideline has been met.
The examples given here are merely illustrative, and there may exist more appropriate methods of verification.

Each checklist item consists of the main text of the checklist item, along with the following information:

Check ID
--------

Each checklist item is assigned an ID.
All checks are compiled in :ref:`check-index` and linked via the "Check ID".

Applicable Stages
-----------------

The applicable stages are categorized according to the type of checklist item as follows:

Design
   Items that should primarily be checked at the specification determination or design stage.
Code
   Items that require review of markup or coding for determination, primarily to be checked during implementation.
Product
   Items that can be judged based on behavior when actually operated, mainly to be checked after implementation.

Target Platforms
----------------

Similar to guidelines, the intended application targets for each checklist item are indicated as follows:

Web
   Desktop Web and mobile Web (things displayed in browsers and in Web views).
Mobile
   Mobile applications.

Note that for checklist items corresponding to multiple guidelines, the "Target Platforms" indicated in the guideline and the checklist item may not always match.
(For example, the target platform for a guideline is Web only, but the corresponding checklist item's target platform includes both Web and mobile.)

Severity
--------

The severity indicator represents the impact of not meeting a checklist item, categorized into four levels:

[CRITICAL]
   Some people may become unable to operate.
[MAJOR]
   Some people may find operation or information retrieval significantly difficult.
[NORMAL]
   A fair number of people may find it inconvenient.
[MINOR]
   There are issues, but the impact is small.


Examples
--------

For items applicable to "Code," specific examples of implementation methods may be provided.

For items applicable to "Product," specific methods of conducting checks may be shown.

***********************************************************************
The Levels of WCAG Success Criteria and the Severity of Checklist Items
***********************************************************************

In WCAG 2.1, each success criterion is assigned one of three levels: A, AA, or AAA.
Although the WCAG text mentions that level A is the minimum and level AAA is the highest, there is no clear definition of each level.
Generally, level A is seen as the minimum standard to be met, level AA aims to make content accessible to more people, and level AAA represents even stricter criteria to enhance accessibility further.

The level of WCAG conformance for web content is determined by which levels of success criteria have been met.
For example, our guidelines aim to achieve a state equivalent to WCAG 2.1 level AA conformance, which means meeting all the success criteria of levels A and AA.

Meanwhile, each guideline is based on the success criteria of WCAG 2.1.
Initially, when these guidelines were developed, the levels assigned to these success criteria were used as a reference to allocate two levels of priority, [MUST] or [SHOULD], to each guideline.
However, for the following reasons, this priority system was abolished in Ver. 202309.1:

*  For a single guideline item, there could be multiple checklist items with different severities, making the relationship between the priority of the guideline and the severity of the checklist items unclear.
*  For instance, the severity of a checklist item listed under a [MUST] priority guideline could be [MINOR], complicating the relationship between the guideline's priority and the checklist item's severity.
*  A single guideline could be associated with multiple WCAG success criteria of different levels, making the relationship between the guideline's priority and the WCAG levels unclear.
*  In practice within freee, checklist items that provide more specific scenarios than guideline are overwhelmingly more referenced, resulting in the severity of checklist items being consulted more often than the priority of the guidelines.

Although the priority system has been abolished, the policy of aiming for WCAG 2.1 level AA equivalence remains unchanged, and each guideline is primarily based on the success criteria of levels A and AA of WCAG 2.1.

Considering the nature of freee's products, some success criteria are treated at different levels than those specified in WCAG.
These specifics are listed in :ref:`info-priority-diff`.

*****************
Related Documents
*****************

*  `Web Content Accessibility Guidelines (WCAG) 2.0 <WCAG20_>`_
*  `Web Content Accessibility Guidelines (WCAG) 2.1 <WCAG21_>`_

***********************
Status of This Document
***********************

This document has been developed for use in the development of new products and the improvement of existing products within freee K.K.
Believing there are parts of it that could be of reference in Web development outside of freee as well, it is made publicly available.

Efforts are continuously made to make this document more understandable by adding reference information and examples and improving expressions.

The latest version of this document is published at the following URL:

HTML version
   https://a11y-guidelines.freee.co.jp/
GitHub Release Page
   https://github.com/freee/a11y-guidelines/releases/latest

For proposals for the improvement of this document, please notify us on `GitHub <https://github.com/freee/a11y-guidelines/>`__.

Copyright and License Conditions
================================

|cclogo| The "freee Accessibility Guidelines" are created by freee K.K. and are provided under the `Creative Commons Attribution 4.0 International License <https://creativecommons.org/licenses/by/4.0/>`__.

Copyright © |copyright|.

Version Information
===================

Version of This Document:
   |release|
Guideline Version:
   |guidelines_version_string|
Checksheet Version:
   |checksheet_version|
Updated:
   |published_date|

.. _WCAG20: https://www.w3.org/TR/WCAG20/
.. _WCAG21: https://www.w3.org/TR/WCAG21/

.. |cclogo| image:: https://i.creativecommons.org/l/by/4.0/88x31.png
   :alt: Creative Commons Attribution 4.0 International (CC BY 4.0) License

