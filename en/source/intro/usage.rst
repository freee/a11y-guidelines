.. _intro-usage:

#################################################
How to Utilize the freee Accessibility Guidelines
#################################################

This section introduces the intended ways of utilizing these guidelines.

*******************
Use During Planning
*******************

At the planning stage of development or accessibility improvement initiatives, it's beneficial to consider the nature of the content in question and first identify which categories of these guidelines are relevant.
For those tackling accessibility improvements for the first time, reviewing the text and intent of each guideline within these categories, along with the linked reference information, can help understand what actions are necessary and why.

***********************
Utilizing the Checklist
***********************

For conducting checks, freee K.K. utilizes a Google Spreadsheet that compiles the checklist items, as introduced in :ref:`checks-checksheet`.

This spreadsheet is divided into multiple sheets depending on the applicable stage of the check.
These sheets, organized by the stage of development, are to be filled with the check results.
Each checklist item also includes links to related guidelines and reference information, making it easy to revisit guidelines if necessary.

Within freee K.K., the results are marked as PASS/FAIL/Not Applicable.
For checklist items unrelated to a specific page or screen, "Not Applicable" is selected.

Ideally, all check results would be PASS. However, allowing FAIL results may be acceptable based on the impact's magnitude or the provision of alternative methods.
The important thing is not merely having good check results but creating something as accessible as possible to as many users as possible.

*****************
Use During Design
*****************

Keeping the contents of these guidelines in mind while designing products allows for a design that considers basic principles of accessibility.
However, comprehensively covering specific points of attention in the design is not easy, even for those with extensive experience in accessibility.
Therefore, it's advisable to verify that no accessibility issues have crept into the design before moving on to implementation, once the design documentation [#]_ has somewhat progressed.

Specifically, check the design documentation for checklist items applicable to "Design" in each guideline.
Resolving issues found at this stage before implementation makes it easier to ensure accessibility.

.. [#] Here, "design documentation" refers to all materials provided to those who will implement the design, including specifications, visual design documents, and instructions on using UI components.

*************************
Use During Implementation
*************************

If accessibility has been adequately considered in the design documentation, following this documentation during implementation reduces the likelihood of accessibility-related issues arising.
Additionally, verifying checklist items applicable to "Code" can help avoid common problems.

Checklist items applicable to "Product" may also outline the expected behavior of the implementation, so reviewing these before implementation is beneficial.

*********************************
Use During Quality Assurance (QA)
*********************************

During the QA process, along with testing various functions of the product, it's advisable to verify that there are no accessibility issues.
Checklist items applicable to "Product" are intended for checks at this stage.

If there are FAIL results during this stage, considering the severity of the checklist item and other factors to determine the approach to resolution would be beneficial.
