# Setup Instructions for Assignment 3

1. Begin by either using the ami ["ami-763a311e"](https://github.com/BVLC/caffe/wiki/Caffe-on-EC2-Ubuntu-14.04-Cuda-7) from AWS EC2 (Ubuntu 14.04, g2.2x large). Alternately, follow the instructions [here](https://github.com/BVLC/caffe/wiki/Install-Caffe-on-EC2-from-scratch-%28Ubuntu,-CUDA-7,-cuDNN%29) and install setup from scratch.

2. This setup does not contain pyopencl. To install pyopencl, follow the steps given below.

- sudo apt-get update
- sudo apt-get install python-mako
- sudo apt-get install libffi*
- sudo pip install pyopencl

3. To verify your installation, type the following on your command line:

>> python -c "import pyopencl as cl"

Continue with the instructions as defined below.

# Running your code

We are currently using pyopencl for our optimisation requirements.

