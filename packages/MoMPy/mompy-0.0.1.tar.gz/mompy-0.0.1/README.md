MoMPy: Moment matrix generation and managing package for SDP hierarchies.

This is a package to generate moment matrices for SDP hierarchies. The package contains the following relevant functions:

 - MomentMatrix: generates the moment matrix with operational equivalences already taken into account (except normalisation).

 - normalisation_contraints: takes into account normalisation constraints. This is to be called inside the SDP and added as a constraint!

More information in the code files.