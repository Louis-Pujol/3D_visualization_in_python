import vedo
import numpy as np
import pyvista as pv


class LandmarksSelector(vedo.Plotter):
    """
    Display  a mesh and allow the user to select points on it

    Args:
        mesh (vedo.Mesh): the mesh on which the points are displayed
    """

    def __init__(self, mesh, **kwargs):
        """ """
        super().__init__(**kwargs)

        mesh = mesh.clone()  # Clone the mesh to avoid modifying the original one

        # Set the mesh properties
        self.mesh = mesh.linewidth(1)
        self.mesh.pickable(
            True
        )  # Make the mesh pickable to be able to select points on it
        self.vertices = vedo.Points(self.mesh.points())

        self.lpoints = []  # List of landmarks points

        # Instructions
        t = "Press e to add a point on the surface\nPress z to add a vertice\nPress d to delete the last point\nPress q to quit"
        self.instructions = vedo.Text2D(
            t, pos="bottom-left", c="white", bg="green", font="Calco"
        )

        # Add the objects to the scene
        self += [self.mesh, self.instructions]

        # Callbacks
        self.callid1 = self.add_callback("KeyPress", self._key_press)

    def points(self, newpts=None):
        """Retrieve the 3D coordinates of the clicked points"""
        return np.array(self.lpoints)

    def _key_press(self, evt):
        if (
            evt.keypress == "z" and evt.actor == self.mesh
        ):  # If the key pressed is z and the cursor is on the mesh
            pt = self.vertices.closest_point(
                evt.picked3d
            )  # get the closest point on the set of vertices (computed in __init__)

            self.lpoints.append(pt)  # Add the point to the list of landmarks
            if len(self.lpoints) > 1:
                self.pop()  # Remove the last set of landmarks from the scene
            # Add the new landmarks to the scene
            self.add(vedo.Points(self.lpoints, r=15).pickable(False).c("r"))

        if (
            evt.keypress == "e" and evt.actor == self.mesh
        ):  # If the key pressed is e and the cursor is on the mesh
            pt = self.mesh.closest_point(
                evt.picked3d
            )  # get the closest point on the mesh
            self.lpoints.append(pt)  # Add the point to the list of landmarks

            if len(self.lpoints) > 1:
                self.pop()  # Remove the last set of landmarks from the scene
            # Add the new landmarks to the scene
            self.add(vedo.Points(self.lpoints, r=15).pickable(False).c("r"))

        if evt.keypress == "d":
            if len(self.lpoints) > 0:  # If there are landmarks
                self.lpoints.pop()  # Remove the last landmark
                self.pop()  # Remove the last set of landmarks from the scene
                if len(self.lpoints) > 0:  # If there are still landmarks
                    self.add(
                        vedo.Points(self.lpoints, r=15).pickable(False).c("r"),
                        resetcam=False,
                    )  # Add the new landmarks to the scene

    def start(self):
        """Start the interaction"""
        self.show(self.mesh, self.instructions, interactive=None)
        return self
