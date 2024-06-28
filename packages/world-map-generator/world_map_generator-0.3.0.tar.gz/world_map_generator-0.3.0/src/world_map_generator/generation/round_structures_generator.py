from math import sqrt, cos, atan2
from typing import Optional, Callable, List, Tuple

import numpy as np

from world_map_generator.default_values import DEFAULT_CHUNK_WIDTH, DEFAULT_ROUND_STRUCTURE_GRID_STEP
from .chunk_generator import ChunkGenerator
from world_map_generator.generation.primitives.round_structure import STEP_ROUND_STRUCTURE_TYPE, RoundStructureType, \
    RoundStructureInstance
from world_map_generator.utils import Bounding, get_position_seed
from ..map.chunk import ValueChunk


def get_base_round_structure_type(seed: int,
                                  round_structure_node_x: int, round_structure_node_y: int,
                                  tile_x: int, tile_y: int) -> RoundStructureType | None:
    return STEP_ROUND_STRUCTURE_TYPE


def get_value_intersection_max(v1: float, v2: float) -> float:
    return max(v1, v2)


def get_value_intersection_sum(v1: float, v2: float) -> float:
    return v1 + v2


def get_value_intersection_sum_clip(clip: Optional[float] = 1) -> Callable[[float, float], float]:
    def sum_clip(s1: float, s2: float) -> float:
        return min(clip, s1 + s2)

    return sum_clip


def get_d_xy_euclidean(dx: float, dy: float) -> float:
    r_square = dx * dx + dy * dy
    dxy = sqrt(r_square)
    return dxy


def get_d_xy_l3(dx: float, dy: float) -> float:
    r_3 = abs(dx * dx * dx) + abs(dy * dy * dy)
    # print(r_3)
    dxy = pow(r_3, 1.0 / 3)
    return dxy


def get_d_xy_l3_abs(dx: float, dy: float) -> float:
    r_3 = dx * dx * dx + dy * dy * dy
    dxy = pow(abs(r_3), 1.0 / 3)
    return dxy


def get_d_xy_l4(dx: float, dy: float) -> float:
    r_4 = pow(dx, 4) + pow(dy, 4)
    dxy = pow(r_4, 0.25)
    return dxy


def get_d_xy_l05(dx: float, dy: float) -> float:
    r_4 = sqrt(abs(dx)) + sqrt(abs(dy))
    dxy = r_4 * r_4
    return dxy


def get_d_xy_euclidean_cos(cos_periods: Optional[float] = 1) -> Callable[[float, float], float]:
    def get_d_xy_euclidean_cos_with_period(dx: float, dy: float) -> float:
        rotation = atan2(dx, dy)
        r_square = dx * dx + dy * dy - dx * dy * cos(cos_periods * rotation)
        dxy = sqrt(r_square)
        return dxy
    return get_d_xy_euclidean_cos_with_period


def get_d_xy_max(dx: float, dy: float) -> float:
    return max(abs(dx), abs(dy))


def get_d_xy_min(dx: float, dy: float) -> float:
    return min(abs(dx), abs(dy))


def get_d_xy_sum(dx: float, dy: float) -> float:
    return abs(dx) + abs(dy)


class DotsGenerator(ChunkGenerator):
    """ Generator of round structure map chunks.

    Attributes:
        seed                        Number which is used in procedural generation.
                                    If it wasn't specified it will be generated randomly.
        chunk_width                 Chunk size which defines tiles matrix.
                                    Tile matrix size which should be [chunk_width x chunk_width].
                                    Chunk width should be the power of 2.
        round_structure_grid_step   Step between two closest base grid region centers.
                                    Near one region center will be created round structure
                                    selected by get_round_structure_type method.
        center_shift_amplitude      Max value on which round structure's center could be shifted along axis.
        filling_value               Value that will be used in empty tiles.
        max_possible_impact_radius  Maximum possible max_r value of RoundStructureType
                                    that can be returned with your get_round_structure_type method.
        get_round_structure_type    Method which contains logic about round structure type placement on map.
                                    Method returns RoundStructureType or None.
                                    Where input parameters are:
                                        seed - round structure map seed for generation (int),
                                        round_structure_node_x - x of round structure node in base grid (int),
                                        round_structure_node_x - y of round structure node in base grid (int),
                                        tile_x - tile x (int),
                                        tile_y - tile y (int).
        get_value_intersection      Method returns float values in points which belong to different
                                    round structure instances.
                                    Where input parameters are:
                                        v1 - value from firsts round structure (float),
                                        v2 - value from second round structure (float).
        get_d_xy                    Method returns distance between two points (x1, y1) and (x2, y2).
                                    So this method describes space metric for this generator.
                                    Note that optimizer will clip all structures which don't feat bounding square
                                    (Euclidian square with sides: 2 * round_structure_type.max_r).
                                    Where input parameters are:
                                        dx - x distance which equals: x1 - x2 (float),
                                        dy - y distance which equals: y1 - y2 (float).
    """

    def __init__(self, seed: Optional[int] = None, chunk_width: Optional[int] = DEFAULT_CHUNK_WIDTH,
                 round_structure_grid_step: Optional[int] = DEFAULT_ROUND_STRUCTURE_GRID_STEP,
                 center_shift_amplitude: Optional[int] = DEFAULT_ROUND_STRUCTURE_GRID_STEP,
                 filling_value: Optional[float] = 0.0,
                 max_possible_impact_radius: Optional[int] = DEFAULT_ROUND_STRUCTURE_GRID_STEP,
                 get_round_structure_type: Callable[[int, int, int, int, int],
                                                    RoundStructureType | None] = get_base_round_structure_type,
                 get_value_intersection: Optional[Callable[[float, float], float]] = get_value_intersection_sum_clip(),
                 get_d_xy: Optional[Callable[[float, float], float]] = get_d_xy_euclidean):
        """ Generator of round structure map chunks.
        :param seed:                        Number which is used in procedural generation.
                                            If it wasn't specified it will be generated randomly.
        :param chunk_width:                 Chunk size which defines tiles matrix.
                                            Tile matrix size which should be [chunk_width x chunk_width].
                                            Chunk width should be the power of 2.
        :param round_structure_grid_step:   Step between two closest base grid region centers.
                                            Near one region center will be created round structure
                                            selected by get_round_structure_type method.
        :param center_shift_amplitude:      Max value on which round structure's center could be shifted along axis.
        :param filling_value:               Value that will be used in empty tiles.
        :param max_possible_impact_radius:  Maximum possible max_r value of RoundStructureType
                                            that can be returned with your get_round_structure_type method.
        :param get_round_structure_type:    Method which contains logic about round structure type placement on map.
                                            Method returns RoundStructureType or None.
                                            Where input parameters are:
                                                seed - round structure map seed for generation (int),
                                                round_structure_node_x - x of round structure node in base grid (int),
                                                round_structure_node_x - y of round structure node in base grid (int),
                                                tile_x - tile x (int),
                                                tile_y - tile y (int).
        :param get_value_intersection:      Method returns float values in points which belong to different
                                            round structure instances.
                                            Where input parameters are:
                                                v1 - value from firsts round structure (float),
                                                v2 - value from second round structure (float).
        :param get_d_xy:                    Method returns distance between two points (x1, y1) and (x2, y2).
                                            So this method describes space metric for this generator.
                                            Note that optimizer will clip all structures which don't feat bounding
                                            square (Euclidian square with sides: 2 * round_structure_type.max_r).
                                            Where input parameters are:
                                                dx - x distance which equals: x1 - x2 (float),
                                                dy - y distance which equals: y1 - y2 (float).
        """
        super().__init__(seed, chunk_width)
        self._filling_value = filling_value
        self._round_structure_grid_step = round_structure_grid_step
        self._center_shift_amplitude = center_shift_amplitude
        if center_shift_amplitude > round_structure_grid_step:
            raise Exception("round_structure_grid_step should be larger than center_shift_amplitude!")
        self._max_possible_impact_radius = max_possible_impact_radius
        self._get_round_structure_type = get_round_structure_type
        self._get_value_intersection = get_value_intersection
        self._get_d_xy = get_d_xy
        self._clean_value_matrix()

    @property
    def round_structure_grid_step(self):
        return self._round_structure_grid_step

    @property
    def center_shift_amplitude(self) -> int:
        return self._center_shift_amplitude

    @property
    def filling_value(self) -> float:
        return self._filling_value

    @property
    def max_possible_impact_radius(self) -> int:
        return self._max_possible_impact_radius

    @property
    def get_round_structure_type(self):
        return self._get_round_structure_type

    @property
    def get_value_intersection(self):
        return self._get_value_intersection

    @property
    def get_d_xy(self):
        return self._get_d_xy

    def _clean_value_matrix(self):
        """ Sets values of value_matrix (matrix of all values needed to generate one chunk) to zeros. """
        self.value_matrix = np.full((self.chunk_width, self.chunk_width), self.filling_value)

    def get_closest_round_structures_bounding(self, chunk_x: int, chunk_y: int) -> Bounding:
        """
        Returns the bounding for round_structure instances which are close enough to impact chunk generation
        in specified coordinates.
        """
        left_impact_distance = (chunk_x * self.chunk_width
                                - self.round_structure_grid_step * self.center_shift_amplitude
                                - self.max_possible_impact_radius)
        round_structure_grid_left = (left_impact_distance // self.round_structure_grid_step) - 1
        bottom_impact_distance = (chunk_y * self.chunk_width
                                  - self.round_structure_grid_step * self.center_shift_amplitude
                                  - self.max_possible_impact_radius)
        round_structure_grid_bottom = (bottom_impact_distance // self.round_structure_grid_step) - 1
        right_impact_distance = ((chunk_x + 1) * self.chunk_width
                                 + self.round_structure_grid_step * self.center_shift_amplitude
                                 + self.max_possible_impact_radius)
        round_structure_grid_right = (right_impact_distance // self.round_structure_grid_step) + 1
        top_impact_distance = ((chunk_y + 1) * self.chunk_width
                               + self.round_structure_grid_step * self.center_shift_amplitude
                               + self.max_possible_impact_radius)
        round_structure_grid_top = (top_impact_distance // self.round_structure_grid_step) + 1
        return Bounding(round_structure_grid_left, round_structure_grid_bottom,
                        round_structure_grid_right, round_structure_grid_top)

    def get_round_structure_center(self, round_structure_node_x: int, round_structure_node_y: int) \
            -> Tuple[float, float]:
        """ Returns position of round structure center. """
        pos_seed = get_position_seed(round_structure_node_x, round_structure_node_y, self.seed)
        np.random.seed(pos_seed)
        rnd = np.random.rand(2)
        round_structure_center_x = self.round_structure_grid_step * (
            round_structure_node_x + 2 * self.center_shift_amplitude * (rnd[0] - 0.5))
        round_structure_center_y = self.round_structure_grid_step * (
            round_structure_node_y + 2 * self.center_shift_amplitude * (rnd[1] - 0.5))
        return round_structure_center_x, round_structure_center_y

    def get_closest_round_structures(self, chunk_x: int, chunk_y: int) -> List[RoundStructureInstance]:
        """ Returns list of round structure instances which are close enough to impact chunk generation. """
        round_structure_grid_bounding = self.get_closest_round_structures_bounding(chunk_x, chunk_y)
        round_structures = []
        for i in range(round_structure_grid_bounding.left, round_structure_grid_bounding.right + 1):
            for j in range(round_structure_grid_bounding.bottom, round_structure_grid_bounding.top + 1):
                rs_center = self.get_round_structure_center(i, j)
                rs_type = self.get_round_structure_type(seed=self.seed,
                                                        round_structure_node_x=i,
                                                        round_structure_node_y=j,
                                                        tile_x=rs_center[0],
                                                        tile_y=rs_center[1])
                is_no_structure = rs_type is None
                if is_no_structure:
                    continue
                # There is no intersections if structure bounding (square) does not intersect chunk
                is_no_intersections_x = (rs_center[0] + rs_type.max_r < chunk_x * self.chunk_width
                                         or rs_center[0] - rs_type.max_r > (chunk_x + 1) * self.chunk_width)
                is_no_intersections_y = (rs_center[1] + rs_type.max_r < chunk_y * self.chunk_width
                                         or rs_center[1] - rs_type.max_r > (chunk_y + 1) * self.chunk_width)
                if is_no_intersections_x or is_no_intersections_y:
                    continue
                round_structure_instance = RoundStructureInstance(rs_center[0],
                                                                  rs_center[1],
                                                                  rs_type)
                round_structures.append(round_structure_instance)
        return round_structures

    def _get_tile_value(self, x: int, y: int, round_structures: List[RoundStructureInstance]) -> float:
        """ Generate tile value near specified round structures.

        :param x: tile x coordinate
        :param y: tile y coordinate
        :param round_structures: list of round structure instances which are close enough
                                 to impact current tile generation
        :return: output tile value
        """
        output = self.filling_value
        for rs in round_structures:
            rs_type = rs.round_structure_type
            max_r = rs_type.max_r
            max_value = rs_type.max_value
            dx = x - rs.x
            dy = rs.y - y
            dxy = self.get_d_xy(dx, dy)
            if dxy < max_r:
                radius_function = rs_type.radius_function
                params = rs_type.parameters
                cur_r = radius_function(r=dxy, max_r=max_r, dx=dx, dy=dy, max_value=max_value,
                                        parameters=params, filling_value=self.filling_value)
                if output == self.filling_value:
                    output = cur_r
                else:
                    output = self.get_value_intersection(output, cur_r)
        return output

    def _generate_chunk_for_round_structures(self, chunk_x: int, chunk_y: int,
                                             round_structures: List[RoundStructureInstance]) -> ValueChunk:
        """
        Chunk generation for round structure map.

        :param chunk_x: chunk x position in world
        :param chunk_y: chunk y position in world
        :param round_structures: list of closest round structure instances
        :return: numpy matrix with size = [chunk_width x chunk_width]
        """
        self._clean_value_matrix()
        output_chunk_left = self.chunk_width * chunk_x
        output_chunk_bottom = self.chunk_width * chunk_y

        for i in range(self.chunk_width):
            for j in range(self.chunk_width):
                x, y = i + output_chunk_left, j + output_chunk_bottom
                tile_value = self._get_tile_value(x, y, round_structures)
                self.value_matrix[i][j] = tile_value

        output_chunk = ValueChunk(chunk_x, chunk_y, self.chunk_width, self.value_matrix)
        return output_chunk

    def generate_chunk(self, chunk_x: int, chunk_y: int) -> ValueChunk:
        """
        Chunk generation for round structure map.

        :param chunk_x: chunk x position in world
        :param chunk_y: chunk y position in world
        :return: round structure map chunk with size = [chunk_width x chunk_width]
        """
        closest_round_structures = self.get_closest_round_structures(chunk_x, chunk_y)
        return self._generate_chunk_for_round_structures(chunk_x, chunk_y, closest_round_structures)
