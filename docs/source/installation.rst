Installation
============

**Calendar-Smith** is a zero-dependency, high-performance Python utility.

Standard installation
---------------------

Install it directly from PyPI:

.. code-block:: bash

   pip install calendar-smith

Development setup
-----------------

To contribute to the project or run the test suite, install in editable mode with development dependencies:

.. code-block:: bash

   git clone https://github.com/yeiichi/calendar-smith.git
   cd calendar-smith
   pip install -e ".[dev]"

Verification
------------

To verify that the installation was successful, check the version:

.. code-block:: bash

   calendar-smith --version

Or try a simple CLI command:

.. code-block:: bash

   calendar-smith-nth --date 2026-04-22

Compatibility
-------------

- **Python version:** 3.10 or higher.
- **Operating system:** Windows, macOS, or Linux.
- **Dependencies:** None.

---

Notes
-----

- The package is intentionally lightweight and uses only the Python Standard Library.
- If you use ``uv``, you can run the CLI without installing the package: ``uvx calendar-smith-nth --date 2026-04-22``.
