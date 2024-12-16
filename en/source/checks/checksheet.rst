.. _checks-checksheet:

########################################
Google Spreadsheet for Performing Checks
########################################

A Google Spreadsheet that contains information for each check item is available.

-  `Accessibility Check List for General Publication <https://docs.google.com/spreadsheets/u/0/d/1nRnqXG2tRQ7wLTkEAE1o8N-7s9500h4B2Gj3l7AbKL4/edit>`__

Note that the file includes both the Japanese and the English sheets.

Please create a copy of this spreadsheet on Google Drive for your use.

.. _checksheet-semver:

********************************************************
About the Version Number of the Accessibility Check List
********************************************************

For convenience, version numbers are provided for the accessibility check list.
As of the time of writing this document, the version is noted in cell A24 of the first sheet.

Starting from V3.0.0, version numbers consist of three digits separated by periods (.): major version number, minor version number, and revision number.
For example, if the version number is 3.0.1, the major version number is 3, the minor version number is 0, and the revision number is 1.

Each number is updated according to the following guidelines:

Major Version
   In case of significant changes, such as changes in the structure of the check list.
Minor Version
   In case of additions, deletions, or changes in the intent of existing check items.
Revision
   In case of changes that do not affect the results of the check, such as typo corrections or changes in wording without changes in intent.

.. _checksheet-history:

***************************************
Accessibility Check List Update History
***************************************

Here, we list updates related to the English translation since the introduction of V4.3.7, when we began providing translations for all sheets.
For the changes to the original Japanese version, please refer to the `Japanese version of this page </checks/checksheet.html>`__.

V6.0.0 (December 16, 2024)
==========================

*  Conducted a review of how to record  check results on the check sheet and revised the wording for items applicable to "Product"
*  Addition to the check procedures of :ref:`check-0471`
*  Addition to the implementation examples of :ref:`check-0461`

V5.1.0 (September 26, 2024)
===========================

*  Added checklist item for the new guideline, Input Device: :ref:`gl-input-device-mobile-standard-gestures` corresponding to the design target: :ref:`check-0154`

V5.0.2 (August 19, 2024)
========================

*  Explicitly state the method to check the appropriateness of the content being read aloud in the example of :ref:`check-0411`.

V5.0.1 (August 16, 2024)
========================

*  Added an example of how to perform the check using axe DevTools on :ref:`check-0681`.
*  Typographical error correction

V5.0.0 (August 9, 2024)
=======================

*  Reviewed the checklist items whose applicable stage is "Product"

   -  For some items indicating check procedures, divided the description of check methods into multiple examples
   -  Added a mechanism to the Accessibility Check List to determine the check results by reflecting the state of the check results for each check method when multiple examples of check methods are provided
   -  Changed the posting order of checklist items in the Accessibility Check List to match how the checks are performed within freee K.K.

V4.3.7 (February 15, 2024)
==========================

*  Added English translations for all sheets.

