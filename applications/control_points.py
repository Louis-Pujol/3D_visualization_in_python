import vedo
import numpy as np
import pyvista as pv


class ControlPointsSelector(vedo.Plotter):
    """
    Display grid points on a mesh and allow the user to select them

    Args:
        mesh (vedo.Mesh): the mesh on which the points are displayed
        dim (int): the number of points on each axis of the grid
    """

    def __init__(self, mesh, dim=4, **kwargs):
        """ """
        super().__init__(**kwargs)

        mesh = mesh.clone()

        # Create a uniform grid

        pv_mesh = pv.wrap(mesh.polydata())  # Wrap the mesh in a pyvista object

        # Get the bounds of the mesh
        xmin, xmax, ymin, ymax, zmin, zmax = pv_mesh.bounds
        origin = (xmin, ymin, zmin)
        spacing = (
            (xmax - xmin) / (dim - 1),
            (ymax - ymin) / (dim - 1),
            (zmax - zmin) / (dim - 1),
        )

        # Create the grid
        grid = pv.UniformGrid(
            dimensions=(dim, dim, dim),
            spacing=spacing,
            origin=origin,
        ).extract_all_edges()  # Extract the edges of the grid to keep the wireframe

        # Wrap the grid and its vertices in vedo objects
        self.grid = vedo.Mesh(grid).pickable(False).c("k").linewidth(1).alpha(0.5)
        self.gridpoints = vedo.Points(self.grid.points(), r=10).pickable(False).c("k")
        self.mesh = mesh.pickable(False).alpha(0.5).c("grey")

        self.cpoints = []  # List of control points

        # Instructions
        t = "Press z to add a point\nPress d to delete the last point\nPress q to quit"
        self.instructions = vedo.Text2D(
            t, pos="bottom-left", c="white", bg="green", font="Calco"
        )

        # Add the objects to the scene
        self += [self.mesh, self.grid, self.gridpoints, self.instructions]

        # Callbacks
        self.callid1 = self.add_callback(
            "KeyPress", self._key_press
        )  # When a key is pressed, call self._key_press

    def points(self):
        """Retrieve the 3D coordinates of the clicked points"""
        return np.array(self.cpoints)

    def _key_press(self, evt):
        if evt.keypress == "z":
            # To find the point on the grid, we rely on the screen coordinates (x_pixel, y_pixel)
            # of the grid points and the picked point (x, y) on the screen
            grid_on_screen = self.compute_screen_coordinates(self.gridpoints.points())
            picked_point = evt.picked2d

            # Find the closest point
            distances = np.linalg.norm(grid_on_screen - picked_point, axis=1)
            closest_point = np.argmin(distances)

            # Add the point to the list
            self.cpoints.append(self.gridpoints.points()[closest_point])

            # Update the scene
            if len(self.cpoints) > 1:
                self.pop()
            self.add(vedo.Points(self.cpoints, r=15).pickable(False).c("r"))

        elif evt.keypress == "d":
            if len(self.cpoints) > 0:  # If there are points to delete
                self.cpoints.pop()  # Delete the last point
                self.pop()  # Remove the last point from the scene
                if len(self.cpoints) > 0:  # If there are still points left
                    self.add(
                        vedo.Points(self.cpoints, r=15).pickable(False).c("r")
                    )  # Add them to the scene

        elif evt.keypress == "q":
            self.close()

    def start(self):
        """Start the interaction"""
        self.show(self.mesh, self.grid, self.gridpoints, self.instructions)
        return self
