===============
NIST alloy data
===============

Contact: `Boris Wilthan`_

Identifier: `doi:10.18434/M32153`_

For more information, please visit us at https://trc.nist.gov/metals_data

Description
-----------

The NIST Alloy data Application Programming Interface (API) provides access to thermophysical property data with a focus on unary, binary, and ternary metal systems with a programmatic interface. This interface may be accessed through a fully RESTful web service. This archive contains examples of programmatic interfaces with specific search parameters for example data retrievals.

The purpose of this repository is to house community driven code examples for the retrieval and use of the NIST alloy data. All code including retrieval, analysis, and graphical routines are welcome in this repository.

The code examples here are public use and the data retrieved are publicly available however an authentication key may be required to pull data. This authentication key may be requested free of charge from TRCalloy@nist.gov and is used to manage data dissemination. 

Directory Structure
-------------------

1. */code_examples/wget* -- This directory holds example code to pull metal alloy data using the **wget** application.
2. */code_examples/curl* -- This directory holds example code to pull metal alloy data using the **curl** application.
3. */code_examples/python* -- This directory holds example code to pull metal alloy data using the **python** scripting language.
4. */documentation* -- This directory holds the API documentation and description of the input and output data formats.
5. */output_examples* -- This directory holds the output data JSON files from calls initiated by the example code.
6. */search_examples* -- This directory holds the input search JSON used by the example code to generate the output data JSON.


.. _Boris Wilthan: mailto:boris.wilthan@nist.gov
.. _Scott Townsend: mailto:scott.townsend@nist.gov
.. _`doi:10.18434/M32153`: https://doi.org/10.18434/M32153

