import json
from typing import AnyStr, Optional, List, Tuple, Any

import numpy as np

from world_map_generator.default_values import DEFAULT_CHUNK_WIDTH
from world_map_generator.map.biome import BASE_BIOME_TYPE, BiomeType, biome_tile_to_dict, dict_to_biome_tile


class Chunk:
    """Chunk with tiles packed in numpy matrix.

    Attributes:
        x               Global x position in chunk grid.
        y               Global y position in chunk grid.
        chunk_width     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        chunk_type      Type of the chunk which is basically is class name (f.e. ValueChunk or BiomeChunk).
        tiles           Matrix of float values packed in numpy matrix with size [chunk_width x chunk_width].
    """

    def __init__(self, x: int, y: int, chunk_width: Optional[int] = DEFAULT_CHUNK_WIDTH,
                 tiles: Optional[np.ndarray[Any, np.dtype]] = None):
        """Chunk with tiles packed in numpy matrix.
        :param x:               Global x position in chunk grid.
        :param y:               Global y position in chunk grid.
        :param chunk_width:     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        :param tiles:           Matrix of float values packed in numpy matrix with size [chunk_width x chunk_width].
        """
        self.position = (x, y)
        self._chunk_width = chunk_width
        if tiles is not None:
            self.tiles = tiles
        else:
            self.tiles = np.full((self.chunk_width, self.chunk_width), 0.0)

    @property
    def chunk_width(self) -> int:
        return self._chunk_width

    @property
    def chunk_type(self) -> str:
        return type(self).__name__

    def get_tile(self, x: int, y: int) -> np.ndarray[Any, np.dtype[Any]]:
        return self.tiles[x][y]

    def set_tile(self, x: int, y: int, value: float):
        self.tiles[x][y] = value

    def __str__(self) -> AnyStr:
        output = '{"chunk_width": ' + str(self.chunk_width)
        output += ', "position": ' + str(self.position)

        # output += ', "tiles": ['
        # for i in range(self.chunk_width):
        #     for j in range(self.chunk_width - 1):
        #         output += str(self.tiles[i, j]) + ', '
        # output += str(self.tiles[self.chunk_width - 1, self.chunk_width - 1]) + ']'

        output += "}"
        return output

    def to_dict(self) -> dict[str, Any]:
        tiles = [[0.0 for i in range(self.chunk_width)] for j in range(self.chunk_width)]
        for x in range(self.chunk_width):
            for y in range(self.chunk_width):
                tiles[x][y] = self.get_tile(x, y)
        chunk_dict = {
            "chunk_width": self.chunk_width,
            "chunk_type": self.chunk_type,
            "x": self.position[0],
            "y": self.position[1],
            "tiles": tiles,
        }
        return chunk_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class ValueChunk(Chunk):
    """Chunk with tiles packed in numpy matrix.

    Attributes:
        x               Global x position in chunk grid.
        y               Global y position in chunk grid.
        chunk_width     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        tiles           Matrix of float values packed in numpy matrix with size [chunk_width x chunk_width].
    """

    def __init__(self, x: int, y: int, chunk_width: Optional[int] = DEFAULT_CHUNK_WIDTH,
                 tiles: Optional[np.ndarray[Any, np.dtype]] = None):
        """Chunk with tiles packed in numpy matrix.
        :param x:               Global x position in chunk grid.
        :param y:               Global y position in chunk grid.
        :param chunk_width:     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        :param tiles:           Matrix of float values packed in numpy matrix with size [chunk_width x chunk_width].
        """
        if tiles is not None and (tiles.shape[0] != chunk_width or tiles.shape[1] != chunk_width):
            raise Exception("Tiles should be matrix with size [chunk_width x chunk_width]!")
        super().__init__(x, y, chunk_width, tiles)
        if tiles is None:
            self.tiles = np.full((self.chunk_width, self.chunk_width), 0.0)

    def to_dict(self) -> dict[str, Any]:
        tiles = [[0.0 for i in range(self.chunk_width)] for j in range(self.chunk_width)]
        for x in range(self.chunk_width):
            for y in range(self.chunk_width):
                tiles[x][y] = self.get_tile(x, y)
        chunk_dict = {
            "chunk_width": self.chunk_width,
            "chunk_type": self.chunk_type,
            "x": self.position[0],
            "y": self.position[1],
            "tiles": tiles,
        }
        return chunk_dict


class BiomeChunk(Chunk):
    """Chunk with information about biomes types and their weights in tiles.

    Attributes:
        x               Global x position in chunk grid.
        y               Global y position in chunk grid.
        chunk_width     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        tiles           Matrix of biome types information with size [chunk_width x chunk_width].
                        Each tile is a list of tuples.
                        First element of each tuple is biome type weight and second is BiomeType.
    """

    def __init__(self, x: int, y: int, chunk_width: Optional[int] = DEFAULT_CHUNK_WIDTH,
                 tiles: Optional[List[List[List[Tuple[float, BiomeType]]]]] = None):
        """Chunk with information about biomes types and their weights in tiles.
        :param x:               Global x position in chunk grid.
        :param y:               Global y position in chunk grid.
        :param chunk_width:     Tiles matrix size. Tile matrix size which should be [chunk_width x chunk_width].
        :param tiles:           Matrix of biome types information with size [chunk_width x chunk_width].
                                Each tile is a list of tuples.
                                First element of each tuple is biome type weight and second is BiomeType.
        """
        if tiles is not None and (len(tiles) != chunk_width or len(tiles[0]) != chunk_width):
            raise Exception("Tiles should be matrix with size [chunk_width x chunk_width]!")
        super().__init__(x, y, chunk_width, tiles)
        if tiles is None:
            self.tiles = [[[(1, BASE_BIOME_TYPE)]] * self.chunk_width for _ in range(chunk_width)]

    def get_tile(self, x: int, y: int) -> List[Tuple[float, BiomeType]]:
        return self.tiles[x][y]

    def set_tile(self, x: int, y: int, value: List[Tuple[float, BiomeType]]):
        self.tiles[x][y] = value

    def to_dict(self) -> dict[str, Any]:
        tiles = [[{} for i in range(self.chunk_width)] for j in range(self.chunk_width)]
        for x in range(self.chunk_width):
            for y in range(self.chunk_width):
                tiles[x][y] = biome_tile_to_dict(self.get_tile(x, y))
        chunk_dict = {
            "chunk_width": self.chunk_width,
            "chunk_type": self.chunk_type,
            "x": self.position[0],
            "y": self.position[1],
            "tiles": tiles,
        }
        return chunk_dict


def chunk_dict_to_chunk(chunk_as_dict: dict, biomes_list: List[BiomeType] = None) -> ValueChunk | BiomeChunk:
    """
    Converts chunk represented as dictionary to chunk object.

    :param chunk_as_dict: Chunk represented as dictionary.
    :param biomes_list: List of all possible biome types used in chunk (in case if chunk is BiomeChunk).
    :return: Chunk object.
    """
    tiles = chunk_as_dict["tiles"]
    chunk_width = chunk_as_dict["chunk_width"]
    chunk_type = chunk_as_dict["chunk_type"]
    chunk = None
    if chunk_type == "ValueChunk":
        chunk = ValueChunk(chunk_as_dict["x"], chunk_as_dict["y"], chunk_width)
        for x in range(chunk.chunk_width):
            for y in range(chunk.chunk_width):
                chunk.set_tile(x, y, tiles[x][y])
    elif chunk_type == "BiomeChunk":
        chunk = BiomeChunk(chunk_as_dict["x"], chunk_as_dict["y"], chunk_width)
        for x in range(chunk.chunk_width):
            for y in range(chunk.chunk_width):
                chunk.set_tile(x, y, dict_to_biome_tile(tiles[x][y], biomes_list))
    if chunk is None:
        raise Exception(f"Unsupported chunk type {chunk_type}")
    return chunk


def json_to_chunk(chunk_as_json: str, biomes_list: List[BiomeType] = None) -> ValueChunk | BiomeChunk:
    """
    Converts chunk represented as json string to chunk object.

    :param chunk_as_json: Chunk represented as json string.
    :param biomes_list: List of all possible biome types used in chunk (in case if chunk is BiomeChunk).
    :return: Chunk object.
    """
    chunk_as_dict = json.loads(chunk_as_json)
    return chunk_dict_to_chunk(chunk_as_dict, biomes_list)
