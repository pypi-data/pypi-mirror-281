.. _add_before_title-name:

!!!!!!!!!!!!!!!!
add_before_title
!!!!!!!!!!!!!!!!

.. meta::
   :keywords: add_before_title, if, pdf,, add, page, number, name, title

.. index:: add_before_title, if, pdf,, add, page, number, name, title

.. _add_before_title-title:

If PDF, Add Page Number and Name to Title
#########################################

.. contents::
   :local:

.. meta::
   :keywords: prototype

.. index:: prototype

.. _add_before_title@Prototype:

Prototype
*********

.. literalinclude:: ../../xrst/add_before_title.py
   :lines: 58-62,143-145
   :language: py

.. meta::
   :keywords: data_in

.. index:: data_in

.. _add_before_title@data_in:

data_in
*******
data for this page before replacement.

 #. data_in must contain '\\n{xrst@before_title}'
    which is referred to as the command below.
 #. The page title must come directly after the command
    and start with a newline.
 #. The page title may have an rst overline directly before the
    heading text and must have an underline directly after it.
 #. If both an overline and underline follow, they must be equal.

.. meta::
   :keywords: target

.. index:: target

.. _add_before_title@target:

target
******
if *target* is ``html`` , the command is removed and no other action
is taken. Otherwise, the *page_number* following by the *page_name* is
added at the font of the title for this page.
The underline (and overline if present) are extended by the number of
characters added to the title.

.. meta::
   :keywords: page_number

.. index:: page_number

.. _add_before_title@page_number:

page_number
***********
This is a page number that identifies this page in the table of contents.

.. meta::
   :keywords: page_name

.. index:: page_name

.. _add_before_title@page_name:

page_name
*********
This is the name of the page.

.. meta::
   :keywords: data_out

.. index:: data_out

.. _add_before_title@data_out:

data_out
********
the return data_out is the data after replacement.
