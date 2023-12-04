#!/bin/bash

# remove Microsoft
rm -r Microsoft/results_*

# remove preprocessed images
rm -r test_set/img_preprocessed_*

# remove SuperSR
rm -r SuperSR/results_*

# remove GFPGAN
rm -r GFPGAN/results_*

# remove HAT
rm -r HAT/HAT/results/*
