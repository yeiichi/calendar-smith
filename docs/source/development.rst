Development
===========

**Calendar-Smith** is open source and welcomes contributions!

GitHub Repository
-----------------

The source code is hosted on GitHub:
https://github.com/yeiichi/calendar-smith

Development setup
-----------------

The project uses ``uv`` for dependency management.

.. code-block:: bash

   git clone https://github.com/yeiichi/calendar-smith.git
   cd calendar-smith
   pip install -e ".[dev]"

Running tests
-------------

To run the full test suite:

.. code-block:: bash

   pytest

To check code coverage:

.. code-block:: bash

   pytest --cov=calendar_smith

Building documentation
----------------------

To build the documentation locally:

.. code-block:: bash

   cd docs
   make html

The output will be in ``docs/build/html``.

Style and quality
-----------------

We aim for high quality and minimal dependencies:

- **Zero External Dependencies:** Only the Python Standard Library (3.10+) should be used in the core code.
- **Type Annotations:** All public APIs should have type hints.
- **Testing:** New features must include tests.
- **Documentation:** New features should be documented in the relevant files.

Releasing
---------

The project uses `python-semantic-release` for automated versioning and changelog generation.

When a pull request is merged to the ``main`` branch, the version is automatically bumped based on the commit messages (following Conventional Commits).

---

Notes
-----

- Follow the existing code style.
- Use meaningful commit messages.
- Ensure all tests pass before submitting a pull request.
