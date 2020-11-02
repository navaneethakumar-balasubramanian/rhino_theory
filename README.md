
# Rhino Theory

rhino_theory: Software for modeling  theoretical wavelets and post processing functions for the dcrhino_lib extracted features.
		
- theory/core.py: TheoreticalWavelet class that tries to a theoretical wavelet for a given pipe, rock and other frequency domain related args;
- theory/constants.py: Constants related to rhino and mwd columns;
- theory/derived_physics.py: (research) functions to transform velocity logs to a fracture factor and RQD.
- theory/feature_extraction.py: Second layer of feature extraction (post process to dcrhino_lib's feature extraction) to generate uncalibrated modulus, velocity and pseudo-density;
- theory/function_handler.py: A helper class to model by optimization (using scipy's curve_fit) the rock properties vs the extracted features of the theoretical wavelets by pipe.
- theory/plotting.py: wiggle plot function;

Edited
## Installing rhino_theory

1. `git clone` the repo;
2. `cd` into the cloned repo folder; 
3. Install the package using pip: `pip install -e .`

## Running the web app

1. `python theory/app/index.py`

# Maintainer

This repo is maintained by [@bruno](https://github.com/brunorpinho) from
[DataCloud](http://datacloud.com/). If you are not from DataCloud, you shouldn't be here.
