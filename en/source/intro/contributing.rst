.. _intro-contributing:

###########################
About Editing This Document
###########################

This document is managed in the following repository on GitHub:

https://github.com/freee/a11y-guidelines

For content modifications, additions, or corrections of typos and errors, please notify us through the Issues or Pull Requests in the above repository.

If you wish to create a Pull Request, first fork the above repository. Create a working branch in your forked repository, make the necessary changes, and then create a Pull Request against the develop branch of the above repository.
Below, we summarize the information related to editing this document.

***********************************
Setting Up Your Working Environment
***********************************

Required Environment
====================

To process the source of this document and generate HTML files, an environment where Python and GNU Make can run is required.

In our development environment, we have confirmed the operation with Python 3.9.x and GNU Make 4.3.

Building the Development Environment
====================================

First, clone the forked git repository.
This repository includes the `Deque Systems Inc.'s axe-core repository`_ as a submodule, so please specify the ``--recursive`` option when executing ``git clone``:

.. code:: shell

   git clone --recursive <<repository-path>

Afterward, if necessary, execute the following command to update the submodule:

.. code:: shell

   git submodule update --init --recursive

Next, install the required Python modules:

.. code-block:: shell

   pip install --upgrade -r requirements.txt

Generating HTML Files
=====================

The information needed to generate HTML files is described in the Makefile, and GNU Make is required.

Execute the following in the repository's top directory to generate HTML files:

.. code:: shell

   make html

In environments where it is necessary to run the ``python`` command as an alias such as ``python3``, execute it as follows:

.. code:: shell

   make PYTHON=python3 html

The generated HTML files are output under :file:`ja/build/html` for the Japanese version and under :file:`en/build/html` for the English version.

Source Code
===========

This document is created with the assumption that it will be processed by `Sphinx`_.
Overall, it is written in reStructuredText, but guidelines, checklist items, and FAQs are processed by converting files written in YAML into reStructuredText.

The repository's root directory contains the following directories:

:file:`ja`
   Files written in Japanese reStructuredText are included.
:file:`en`
   Contains files translated from the :file:`ja` directory into English. Untranslated files are included in Japanese as they are.
:file:`data`
   :file:`yaml`
      Contains YAML files describing the contents of guidelines, checklist items, FAQs, and related information.
   :file:`json`
      Contains schema definitions for files in the :file:`yaml` directory and files needed to process these files.
:file:`tools`
   :file:`yaml2rst`
      Contains scripts and related files needed to generate the required reStructuredText.
      Originally, it was a script for processing YAML files and outputting reStructuredText files, thus this name, but now it also includes the functionality to process the source code of axe-core and output the necessary reStructuredText file.
:file:`vendor`
   Contains the source code of repositories referenced as submodules.
   Currently, this includes the source code of axe-core.

Executing ``yaml2rst``
======================

Executing the ``tools/yaml2rst/yaml2rst.py`` script allows you to generate the necessary reStructuredText files.
There are several command-line options, but the following two are necessary for manual execution:

``--lang`` or ``-l`` option
   Specifies the language of the reStructuredText files to output. Specify :samp:`ja` for Japanese and :samp:`en` for English.
``--basedir`` or ``-b`` option
   Specifies the directory where the :file:`data` directory is located. This processes the YAML files in this directory to output reStructuredText files.

For example, executing the following in the repository's root directory outputs the Japanese reStructuredText files in the :file:`ja/source/inc` and :file:`ja/source/faq` directories.

.. code:: shell

   python tools/yaml2rst/yaml2rst.py -l ja -b .

Note that executing ``make html`` in the root directory also includes the execution of this script, along with the necessary processes to output HTML for both the Japanese and English versions.

*************
Editing Files
*************

Guidelines, checklist items, and FAQs are edited by modifying the YAML files under the :file:`data/yaml` directory.
Pages that contain these items are structured to ``include`` reStructuredText files generated from these YAML files.

On the other hand, there are files primarily written in reStructuredText, such as those in the :file:`source/explanations` directory.
To modify these pages, edit the relevant reStructuredText files directly.

Notation Rules
==============

The Japanese part of this document is written in accordance with the `JTF Style Guide for Translators Working into Japanese`_ published by the `Japan Translation Federation`_.
The :file:`.textlintrc` in the repository's root directory contains the rules of textlint currently in use, though it is not yet complete.

About the English Version
=========================

The normative version of this document is in Japanese.
Currently, there are untranslated pages, and for these, the source of the Japanese version is included as it is.
The English version is a translation of the content of the Japanese version, but where there are differences, the content of the Japanese version takes precedence.

We try to update the English version simultaneously with the Japanese version, but there are cases where the update of the Japanese version precedes.

Also, currently, there are untranslated pages, and for these, the source of the Japanese version is included as it is. We plan to progressively translate into English.

For pages where an English translation exists, including the following code in the source code of the Japanese version generates a link to the English version.

.. code-block:: rst

   .. translated:: true

.. _Deque Systems Inc.'s axe-core repository: https://github.com/dequelabs/axe-core
.. _Japan Translation Federation: https://www.jtf.jp/
.. _JTF Style Guide for Translators Working into Japanese: https://www.jtf.jp/tips/styleguide
.. _Sphinx: https://www.sphinx-doc.org/en/master/
