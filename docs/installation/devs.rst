For developers and contributors
===============================

Setting up a dedicated code editor
''''''''''''''''''''''''''''''''''

Using a code editor or IDE is useful when contributing to a codebase. Many products are available;
use what is most familiar. For new developers, we recommend
`VS Code <https://code.visualstudio.com>`_ since it is lightweight, free, and has a breadth of
community extensions.

Make your copy of mrsimulator on GitHub
'''''''''''''''''''''''''''''''''''''''

Making a copy of someone's code on GitHub is the same as making a *fork*.  A fork is a complete
copy of the code and its revision history.

1. Log in to a `GitHub account <https://github.com>`_.
2. Go to the `mrsimulator Github <https://github.com/deepanshs/mrsimulator>`_ home page.
3. Click on the *fork* button.

You will see a short animation of Octocat scanning a book on a flatbed scanner.
After that, you should find yourself on the home page for your forked copy of mrsimulator.


Create a development environment
''''''''''''''''''''''''''''''''

It is good practice to create separate virtual environments when developing packages.
There are many environment managers available; however, we recommend using
`Anaconda or Miniconda <https://docs.anaconda.com/anaconda/install/>`_.

.. note::

    For Mac users with Apple Silicon, Anaconda and Miniconda are natively supported on M1 as of
    `release 2022.05 <https://www.anaconda.com/blog/new-release-anaconda-distribution-now-supporting-m1>`__.
    See the
    `downloads page <https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links>`_
    for compatible versions.

    If your Python is built for Apple Silicon, the following command should display a similar
    output.

    .. code-block:: bash

        $ file `which python`
        /some/path/to/python: Mach-O 64-bit executable arm64


The following is an example of creating a Conda environment.

.. code-block:: bash

    $ conda create -n mrsimulator-dev python=3.12

The above command will create a new environment named *mrsimulator-dev* using Python 3.12.
To activate the environment, use

.. code-block:: bash

    $ conda activate mrsimulator-dev


Make sure git is installed on your computer
'''''''''''''''''''''''''''''''''''''''''''

`Git <https://git-scm.com>`_ is a source code management system.
It keeps track of the changes made to the code and manages contributions from
several individuals.  You may notice that much of its terminology comes from
river and tree metaphors, i.e., source, fork, branch, upstream, etc.  You may read
about git at the `Git Basics <https://git-scm.com/book/>`_.

If you are using anaconda/miniconda, you probably have git pre-installed. To check,
type in terminal

.. code-block:: bash

    $ git --version
    # if git is installed, you will get something like git version 2.30.2

If git is not installed, `install <https://git-scm.com/downloads>`_ it before continuing.


**Basic git configuration:**

Follow the instructions at
`Set Up Git <https://docs.github.com/en/github/getting-started-with-github/set-up-git#set-up-git>`_
at GitHub to configure:

- your user name and email in your copy of git.
- authentication, so you don’t have to type your GitHub password every time you

You'll need to access GitHub from the command line.


Copy your fork of mrsimulator from GitHub to your computer
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Unless you plan on always editing the code using the online Github editor, you may need to
copy the fork of **MRSimulator** from your GitHub account to your computer. Make a complete
copy of the fork with

.. code-block:: bash

    $ git clone --recursive https://github.com/your-user-name/mrsimulator.git

Insert *your-user-name* with your GitHub account username. If there is an error in this
stage, it is probably an error in setting up authentication.

You now have a copy of the **MRSimulator** fork from your GitHub account to your local
computer into a **MRSimulator** folder.

Understanding *Remotes*
'''''''''''''''''''''''

In git, the name for another location of the same repository is *remote*.
The repository that contains the latest "official" development version is traditionally
called the *upstream* remote. You can read more about
`remotes on Git Basics <https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes>`_.

At this point, your local copy of **MRSimulator** doesn't know where the *upstream* development
version of **MRSimulator** is. To let git know, change into the **MRSimulator** folder you created in
the previous step and add a remote:

.. code-block:: bash

    cd mrsimulator
    git remote add mrsimulator git://github.com/deepanshs/mrsimulator.git

You can check that everything is set up correctly so far by asking git to show you all of the
remotes it knows about for your local repository of **MRSimulator** with ``git remote -v``, which
should display

.. code-block:: bash

    upstream git://github.com/deepanshs/mrsimulator.git (fetch)
    upstream git://github.com/deepanshs/mrsimulator.git (push)
    origin git@github.com:your-user-name/mrsimulator.git (fetch)
    origin git@github.com:your-user-name/mrsimulator.git (push)


Build the development version of mrsimulator
''''''''''''''''''''''''''''''''''''''''''''

OS-dependent prerequisites
""""""""""""""""""""""""""

.. note::
    Installing OS-dependent prerequisites is a one-time process. If you are
    upgrading to a newer version of mrsimulator, skip to the next section.

.. only:: html

  .. tabs::

    .. tab:: Linux

      .. include:: source_install/linux.rst

    .. tab:: Mac OSX

      .. include:: source_install/macosx.rst

    .. tab:: Windows

      .. include:: source_install/windows.rst

.. only:: not html

  Linux
  -----
  .. include:: source_install/linux.rst

  Mac OSX
  -------
  .. include:: source_install/macosx.rst

  Windows
  -------
  .. include:: source_install/windows.rst


Build and install
"""""""""""""""""

Before building the development version of mrsimulator, install the development requirement
packages with pip. In the directory where your copy of **MRSimulator** is, type:

.. code-block:: bash

    $ pip install -r requirements-dev.txt
    $ pip install -e .

As before, if you get an error that you don’t have the permission to install the
package into the default site-packages directory, you may try installing by adding the
``--user`` option.

.. note::

    If you are using a Mac with Apple Silicon and unable to install **MRSimulator**,
    `open an issue <https://github.com/deepanshs/mrsimulator/issues/new/choose>`__ on
    the GitHub page.


Note for the developers and contributors
''''''''''''''''''''''''''''''''''''''''

**Before commits**: **MRSimulator** follows Python community standards for writing code and documentation.
To help guide the developers and contributors toward these standards, we have created
a *.pre-commit-config.yaml* file that, when used with ``pre-commit``, will inspect
the code and document for issues. To set up ``pre-commit``, type the following one-time
install statements in the terminals,

.. code-block:: bash

    $ pre-commit install

Once set up, navigate to the root level of the **MRSimulator** folder and type

.. code-block:: bash

    $ pre-commit run

The above statement auto-fixes some issues and lists others for you to fix. Review the
changes and address the listed issues before a git commit.

.. You can also set up the git hook script to automatically run *pre-commit* on git commits
.. with the ``pre-commit install``. Read more about
.. `pre-commit <https://pre-commit.com/#3-install-the-git-hook-scripts>`_.

.. note::
    The pre-commit command ignores unstaged changes. Before running ``pre-commit run``, make sure
    to stage files for a commit.

**Running tests**: We use the pytest module for unit tests. At the root level
of the **MRSimulator** folder, type

.. code-block:: bash

    $ pytest

which will run a series of tests alerting you to any unit tests that fail.

**Checking test coverage**: To check which lines in the codebase are covered when running a test,
use the following command.

.. code-block:: bash

    $ pytest --cov-report=html

To view the unit test coverage report, open the *mrsimulator/htmlcov/index.html* file in a
web browser.

**Building docs**: We use the sphinx Python documentation generator for building docs. Navigate
to the *docs* directory within the **MRSimulator** folder, and type,

.. code-block:: bash

    $ make html

The above command will build the documentation and store the build at
*mrsimulator/docs/_build/html*. Open the *index.html* file in a web browser within this folder
to view the locally-built documentation.

.. **Submitting pull requests** Make sure all the tests pass and the documentation build
.. is successful before creating a pull request.

.. We recommend the
.. following C-compiler for the OS types:
.. - Mac OS - ``clang``
.. - Linux - ``gcc``
.. - Windows - ``msvc`` (https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)
