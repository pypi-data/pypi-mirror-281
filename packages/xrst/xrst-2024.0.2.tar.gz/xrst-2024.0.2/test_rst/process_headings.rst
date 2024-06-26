.. _process_headings-name:

!!!!!!!!!!!!!!!!
process_headings
!!!!!!!!!!!!!!!!

.. meta::
   :keywords: process_headings, add, labels, index, entries, headings

.. index:: process_headings, add, labels, index, entries, headings

.. _process_headings-title:

Add labels and index entries for headings
#########################################

.. contents::
   :local:

.. meta::
   :keywords: prototype

.. index:: prototype

.. _process_headings@Prototype:

Prototype
*********

.. literalinclude:: ../../xrst/process_headings.py
   :lines: 242-250,512-517
   :language: py

.. meta::
   :keywords: conf_dict

.. index:: conf_dict

.. _process_headings@conf_dict:

conf_dict
*********
is a python dictionary representation of the configuration file.

.. meta::
   :keywords: local_toc

.. index:: local_toc

.. _process_headings@local_toc:

local_toc
*********
is the xrst command line local_toc setting.

.. meta::
   :keywords: data_in

.. index:: data_in

.. _process_headings@data_in:

data_in
*******
contains the data for a page before the headings are processed.

.. meta::
   :keywords: file_name

.. index:: file_name

.. _process_headings@file_name:

file_name
*********
name of the file that contains the input data for this page.
This is only used for error reporting.

.. meta::
   :keywords: page_name

.. index:: page_name

.. _process_headings@page_name:

page_name
*********
is the name of this page.

.. meta::
   :keywords: not_in_index_list

.. index:: not_in_index_list

.. _process_headings@not_in_index_list:

not_in_index_list
*****************
is a list of compiled regular expressions. If pattern is in this list,
*word* is a lower case version of a word in the heading text, and
pattern.fullmatch( *word* ) returns a match, an index entry is not
generated for word.

.. meta::
   :keywords: data_out

.. index:: data_out

.. _process_headings@data_out:

data_out
********
is a copy of data_in with the following extra command added:

 #. The index entries, and meta keyword entries (same as index),
    and the :ref:`heading_links@Labels` for this page.
 #. The command \\n{xrst@before_title} is placed directly before the
    first heading for this page; i.e. its title.
    This is makes it easy to add the page number to the heading text.

.. meta::
   :keywords: page_title

.. index:: page_title

.. _process_headings@page_title:

page_title
**********
This is the heading text in the first heading for this page.
There can only be one heading at this level.

.. meta::
   :keywords: pseudo_heading

.. index:: pseudo_heading

.. _process_headings@pseudo_heading:

pseudo_heading
**************
This is an automatically generated heading for this page. It is intended
to come before the page_title heading.
It has three lines each terminated by a newline:

 1. an overline line
 2. heading text line for this page title
 3. an underline line

.. meta::
   :keywords: keywords

.. index:: keywords

.. _process_headings@keywords:

keywords
********
This is a space separated list of all the keywords that are in the index
for this page.
