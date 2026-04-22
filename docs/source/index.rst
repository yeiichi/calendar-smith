calendar-smith documentation
============================

**Calendar-Smith** is a zero-dependency, high-performance Python utility for fiscal year calculations, ISO week mapping, and safe date parsing.

It provides both a command-line interface (CLI) and a Python API for building
reproducible data processing pipelines without the overhead of heavy libraries.

Example
-------

.. code-block:: bash

   calendar-smith fiscal-year 2026-04-22 --system jp
   calendar-smith windows 2026-03-17 7 4
   calendar-smith tz 2026-03-20T10:00:00+09:00 America/New_York

Getting started
---------------

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   recipes
   cli

Python API
----------

.. toctree::
   :maxdepth: 2

   python-api
   api

Development & History
---------------------

.. toctree::
   :maxdepth: 2

   development
   changelog

