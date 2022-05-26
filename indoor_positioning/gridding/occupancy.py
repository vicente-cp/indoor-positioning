
from shapely.geometry import Point
import numpy as np
import matplotlib.pyplot as plt


class OccupancyGridMap:
    def __init__(self, affine_layout, cell_size):
        """Class associated to a discretized grid of square cells which correspond to the occupancy map of a respective floor.


        Args:
            affine_layout (_type_): _description_
            cell_size (float): Size of the grid cells in meters
        """

        self.layout = affine_layout
        self.layout_width = self.layout.bounds[2]
        self.layout_height = self.layout.bounds[3]
        self.cell_size = cell_size
        bounds = (self.layout).bounds
        self.grid_map = np.zeros((int(np.ceil(bounds[2]/self.cell_size)),
                                  int(np.ceil(bounds[3]/self.cell_size))), dtype=np.bool)
        self._populate_grid()

    def _populate_grid(self):
        it = np.nditer(self.grid_map, flags=["multi_index"])
        import copy
        self.helper_grid = copy.deepcopy(self.grid_map)
        for _ in it:
            idx_in_coords = self._idx_to_coords(it.multi_index)
            self.grid_map[it.multi_index] = self.layout.contains(Point(idx_in_coords))

    def _idx_to_coords(self, idx_point):
        """Converts the index values to meter coordinates in the respective grid map

        Args:
            idx_point (tuple(int, int)): _description_

        Returns:
            tuple(float, float): Meter coordinates in the grid map
        """

        #  0.5 must be added to the ix so it considers the middle of the grid square instead of a corner
        coords = tuple([(ix+0.5)*self.cell_size for ix in idx_point])
        return coords

    def _coords_to_idx(self, coords):
        """Converts coords from meters to the idx in the respective grid map

        Args:
            coords (tuple(float, float)): Coords in meters

        Returns:
            tuple(int, int): Index in the grid closest to that of the input coordinates
        """
        np_idx = np.round(coords/self.cell_size - 0.5)
        idx = tuple(np_idx)
        return idx

    def plot_grid_map(self, alpha=1, min_val=0, origin='lower'):
        """
        Plot the respective grid map
        """
        plt.imshow(self.grid_map, vmin=min_val, vmax=1, origin=origin, interpolation='none', alpha=alpha)
        plt.draw()
