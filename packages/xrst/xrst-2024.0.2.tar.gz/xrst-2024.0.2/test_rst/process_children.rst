.. _process_children-name:

!!!!!!!!!!!!!!!!
process_children
!!!!!!!!!!!!!!!!

.. meta::
   :keywords: process_children, add, child, information, page

.. index:: process_children, add, child, information, page

.. _process_children-title:

Add child information to a page
###############################

.. contents::
   :local:

.. meta::
   :keywords: prototype

.. index:: prototype

.. _process_children@Prototype:

Prototype
*********

.. literalinclude:: ../../xrst/process_children.py
   :lines: 59-68,145-147
   :language: py

.. meta::
   :keywords: data_in

.. index:: data_in

.. _process_children@data_in:

data_in
*******
is the data for this page after the toc_command function has processed
the toc commands.

.. meta::
   :keywords: list_children

.. index:: list_children

.. _process_children@list_children:

list_children
*************
is a list of the page names for the children of this page.
If this list is empty, data_out is equal to data_in.

.. meta::
   :keywords: data_out

.. index:: data_out

.. _process_children@data_out:

data_out
********
The return value data_out has the child information added.

 #. A hidden table of contents (toctree) for the children is added at the
    end of data_out.
 #. If the TOC command in data_in is {xrst_TOC_list} or {xrst_TOC_table},
    the corresponding links will replace the command.
 #. If the child command is {xrst_TOC_hidden}, the command is removed
    and no table of links is added.
 #. If there is no TOC command and list_children is non-empty,
    the toc_table style is used for the links to the children which are
    placed at the end of the data_out (before the toctree).
