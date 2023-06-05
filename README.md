# 3D_visualization_in_python
A presentation of some functionnalities of two VTK-based python libraries : PyVista and Vedo

To execute the notebooks you will need :
- python
- jupyter-notebook and ipywidgets : pip install ipywidgets
- vedo : pip install vedo
- pyvista : pip install 'pyvista[all,trame]' (don't forget the quotes !) <- trame is needed to display pyvista window into jupyter notebooks

To begin, have a look at slides/ecosystem.png and then explore the notebooks !

This repo is largely work in progress, if something seems to not work or wrong, do not hesitate to let me know.

A youtube video based on a first version of this repo is available at : https://www.youtube.com/watch?v=m68NjYSD7gU&list=PLBFtqeJgRBGies4qp_XWlrsYxgDePEmtp

TODO list :
- add saving info
- more on PyVista/Vedo data structures and how to manually created objects
- more types of custom filters with various data types
- notebooks on link between vtk/vedo/pyvista
- integration with Qt (and other GUI tools, web, ... ?)
