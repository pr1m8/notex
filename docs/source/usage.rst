Usage
=====

### Upload a PDF for Processing

Use `curl`:

.. code-block:: bash

    curl -F "file=@sample.pdf" http://127.0.0.1:5001/upload

### Download Processed PDF

Get your `project_id` from the upload response:

.. code-block:: bash

    curl -X GET "http://127.0.0.1:5001/api/download_pdf?project_id=your_project_id"
