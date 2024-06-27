# masterthesis

The code for my masterthesis in astroparticle-physics about **sterile neutrino detection with neural networks in neutron beta decay**

# Disclaimer

All models use the pytorch backend. Training models using GPU is possible and was tested with nvidias CUDA and apples Metal Performance Shaders (MPS) backend.

The theoretical backbone of all the beta spectra used and generated in my code is based on the TRModel package (i.e. the beta_decay.py script). All of the response matrices used are also from the TRModel package. 

# General Information

The code in this repository does a few things:
- Generating and modifying beta spectra
- Training different kinds of Neural Networks for classification of beta spectra
- Evaluating Neural Networks regarding their sensitivity to a sterile neutrino signature

# How to use the code

E.g. In google colab:

```
!pip install git+https://github.com/lucafally/masterthesis.git
```

Or to clone the repository (also possible in colab):

```
!git clone https://github.com/lucafally/masterthesis.git
```

Them simply run one of the available jupyter notebooks.
