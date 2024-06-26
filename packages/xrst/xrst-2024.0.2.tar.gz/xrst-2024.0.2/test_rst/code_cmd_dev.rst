.. _code_cmd_dev-name:

!!!!!!!!!!!!
code_cmd_dev
!!!!!!!!!!!!

.. meta::
   :keywords: code_cmd_dev, process, xrst, code, commands, page

.. index:: code_cmd_dev, process, xrst, code, commands, page

.. _code_cmd_dev-title:

Process the xrst code commands for a page
#########################################

.. contents::
   :local:

.. meta::
   :keywords: prototype

.. index:: prototype

.. _code_cmd_dev@Prototype:

Prototype
*********

.. literalinclude:: ../../xrst/code_command.py
   :lines: 121-125,226-228
   :language: py

.. meta::
   :keywords: data_in

.. index:: data_in

.. _code_cmd_dev@data_in:

data_in
*******
is the data for the page before the
:ref:`code commands <code_cmd-name>` have been processed.

.. meta::
   :keywords: file_name

.. index:: file_name

.. _code_cmd_dev@file_name:

file_name
*********
is the name of the file that this data comes from. This is only used
for error reporting.

.. meta::
   :keywords: page_name

.. index:: page_name

.. _code_cmd_dev@page_name:

page_name
*********
is the name of the page that this data is in. This is only used
for error reporting.

.. meta::
   :keywords: rst2project_dir

.. index:: rst2project_dir

.. _code_cmd_dev@rst2project_dir:

rst2project_dir
***************
is a relative path from the :ref:`config_file@directory@rst_directory`
to the :ref:`config_file@directory@project_directory` .

.. meta::
   :keywords: data_out

.. index:: data_out

.. _code_cmd_dev@data_out:

data_out
********
is a copy of data_in with the xrst code commands replaced by a corresponding
sphinx command.
