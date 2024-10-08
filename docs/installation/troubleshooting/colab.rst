==================================
Google Colab and Jupyter Notebooks
==================================

If you are new to Google Colab or just need a refresher, we suggest going through
`Google's introduction to Colaboratory <https://colab.research.google.com/?utm_source=scs-index>`__.

Google Colab has the same functionality as a Jupyter Notebook. The main difference is that
Jupyter Notebooks are run on your local machine. The `Jupyter Notebook documentation
<https://jupyter-notebook.readthedocs.io/en/stable/index.html>`__ details installation and use.

.. However, if you're new to Python, we recommend using `Google Colab <https://colab.research.google.com>`__.

Updating Numpy
""""""""""""""

Google Colab is versatile and platform-independent, but some pre-installed libraries may be
old versions. When running **MRSimulator** on Google Colab, an incompatible version of ``numpy`` will
cause the following error

.. code-block:: bash

    ValueError: numpy.ndarray size changed, which may indicate binary incompatibility. Expected 88 from C header got 80 from PyObject

To update ``numpy`` in
Google Colab and execute the following command in a new cell.

.. code-block:: shell

    !pip install -U numpy

This step may take a few seconds. After updating, a warning should pop up saying

.. code-block:: shell

    WARNING: The following packages were previously imported in this runtime: [numpy]    You must restart the runtime to use newly installed versions.

Press the restart runtime button, and ``numpy`` should be up-to-date. Remember to re-run all code
cells since all previous outputs are cleared after restarting the runtime.

Order of Cell Execution
"""""""""""""""""""""""

For Jupyter Notebooks and Google Colab, the order of cell execution is important. If a variable
``foo`` is referenced before assignment, Python will throw ``NameError: name 'foo' is not defined``.

If you get this error when working in a notebook, first check the cell where your variable was
defined has been executed. A cell can be executed by pressing ``shift + enter`` while the text
cursor is in that cell or by pressing the run button near the top-left of the cell.

Similarly, if you've reassigned a variable but the code doesn't reflect that reassignment,
check to ensure the cell where the variable was reassigned has been executed. Value changes
are only recognized after cell execution.
