from __future__ import annotations
from typing import NamedTuple, List, Tuple, Iterator, Dict, Set, Optional
from collections import Counter
import math


# https://github.com/joelgrus/advent2020/blob/master/advent2020/day20.py

Edge = str


class Edges(NamedTuple):
    top: Edge
    bottom: Edge
    left: Edge
    right: Edge


Pixels = List[List[str]]


class Tile(NamedTuple):
    tile_id: int
    pixels: Pixels

    def rotate(self, n: int) -> Tile:
        # n is the number of rotations clockwise
        pixels = self.pixels

        for _ in range(n):
            rotated = []
            for col in range(len(pixels[0])):
                rotated.append([row[col] for row in reversed(pixels)])
            pixels = rotated
        # Returns a NEW NamedTuple with the rotated pixels
        return self._replace(pixels=pixels)

    def reflect_vertical(self, do: bool = False) -> Tile:
        # Reflect in the vertical meaning rows are reversed
        pixels = [list(reversed(row)) for row in self.pixels] if do else self.pixels
        return self._replace(pixels=pixels)

    def reflect_horizontal(self, do: bool = False) -> Tile:
        # Reflect across the horizontal meaning columns are reversed
        pixels = list(reversed(self.pixels)) if do else self.pixels
        return self._replace(pixels=pixels)

    def all_transformations(self) -> Iterator[Tile]:
        # Returns the 8 tiles that can be found using rotations and
        # reflections. Only need to use one of the reflections to
        # find them all
        for reflect_h in [True, False]:
            for n in [0, 1, 2, 3]:
                yield self.reflect_horizontal(reflect_h).rotate(n)

    def print(self) -> None:
        for row in self.pixels:
            print("".join(row))

    def show(self) -> None:
        for row in self.pixels:
            print("".join(row))

    @property
    def top(self) -> str:
        return "".join(self.pixels[0])

    @property
    def bottom(self) -> str:
        return "".join(self.pixels[-1])

    @property
    def left(self) -> str:
        return "".join([row[0] for row in self.pixels])

    @property
    def right(self) -> str:
        return "".join([row[-1] for row in self.pixels])

    def edges(self, reverse: bool = False) -> Edges:
        # Returns the edges either as is or after rotating
        # the tile by 180
        if reverse:
            return self.rotate(2).edges()
        # Make sure to give edges not referencing those in the tile
        return Edges(top=self.top, bottom=self.bottom, right=self.right, left=self.left)

    @staticmethod
    def process_raw(raw: str) -> Tile:
        # Converts the raw tile string into a tile object
        lines = raw.split("\n")
        tile_id = int(lines[0].split()[-1][:-1])
        pixels = [list(line) for line in lines[1:]]
        return Tile(tile_id, pixels)


def process(raw: str) -> List[Tile]:
    tiles = raw.split("\n\n")
    return [Tile.process_raw(tile) for tile in tiles]


def find_corners(tiles: List[Tile]) -> List[Tile]:
    # Finds the corner tiles and orient so they are in the top
    # left

    # Counts as the different edges both reversed and non-reversed
    edge_counts = Counter(
        edge
        for tile in tiles
        for reverse in [True, False]
        for edge in tile.edges(reverse)
    )

    corners = []

    # Finds the tiles with two edges which appear only once in the
    # counter which means they must be in the corner
    for tile in tiles:
        edges_with_no_matches = 0
        for edge in tile.edges():
            if edge_counts[edge] == 1 and edge_counts[edge[::-1]] == 1:
                edges_with_no_matches += 1

        # Check all rotations to put the top and left as the outer edges
        if edges_with_no_matches == 2:
            for n in [0, 1, 2, 3]:
                tile = tile.rotate(n)
                edges = tile.edges()
                if edge_counts[edges.left] == 1 and edge_counts[edges.top] == 1:
                    corners.append(tile)
                    break

    return corners


# This is a partially filled in tile formation
Assembly = List[List[Optional[Tile]]]


class Constraint(NamedTuple):
    # Requires that the tile in location (row, col) has
    # edges matching those around it if they exist
    row: int
    col: int
    top: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None
    right: Optional[str] = None

    def satisfied_by(self, tile: Tile) -> bool:
        # Check if the tile given satisfies the constraint
        if self.top and tile.top != self.top:
            return False
        if self.bottom and tile.bottom != self.bottom:
            False
        if self.left and tile.left != self.left:
            return False
        if self.right and tile.right != self.right:
            return False
        return True

    @property
    def num_constraints(self) -> int:
        return (
            (self.top is not None)
            + (self.bottom is not None)
            + (self.left is not None)
            + (self.right is not None)
        )


def find_constraints(assembly: Assembly) -> Iterator[Constraint]:
    # Creates constraints for partially filled in pattern. Do not
    # give constraints for filled in tiles or locations with no
    # constraints

    n = len(assembly)
    for i, row in enumerate(assembly):
        for j, tile in enumerate(row):
            # If there is a tile pass
            if assembly[i][j]:
                continue
            constraints: Dict[str, str] = {}
            if i > 0 and (nbr := assembly[i - 1][j]):
                constraints["top"] = nbr.bottom
            if i < n - 1 and (nbr := assembly[i + 1][j]):
                constraints["bottom"] = nbr.top
            if j > 0 and (nbr := assembly[i][j - 1]):
                constraints["left"] = nbr.right
            if j < n - 1 and (nbr := assembly[i][j + 1]):
                constraints["right"] = nbr.left

            if constraints:
                yield Constraint(i, j, **constraints)


def assemble_image(tiles: List[Tile]) -> Assembly:
    """
    Take the tiles and figure out how to stick them together
    """
    num_tiles = len(tiles)
    side_length = int(math.sqrt(num_tiles))
    corners = find_corners(tiles)

    # Pick a corner, any corner
    tile = corners[0]

    # Create an empty assembly
    assembly: Assembly = [
        [None for _ in range(side_length)] for _ in range(side_length)
    ]

    # Put this corner tile in the top left
    assembly[0][0] = tile

    # Keep track of which tiles I've already placed
    placed: Dict[int, Tuple[int, int]] = {tile.tile_id: (0, 0)}

    # Repeat until all tiles have been placed
    while len(placed) < num_tiles:
        # Just care about unplaced tiles
        tiles = [t for t in tiles if t.tile_id not in placed]

        # Find the constraints based on all the tiles placed so far
        # and order them by descending # of constraints
        constraints = list(find_constraints(assembly))
        constraints.sort(key=lambda c: c.num_constraints, reverse=True)

        # Did I find a tile to add, so we can break out of inner loops
        found_one = False

        # Try constraints one at a time and see if we can find a tile
        # that satisfies them
        for constraint in constraints:
            for tile in tiles:
                # try all rotations for this tile, to see if any satisfies this constraint
                for rot in tile.all_transformations():
                    if constraint.satisfied_by(rot):
                        # place this rotation (which is a tile) at i, j
                        assembly[constraint.row][constraint.col] = rot
                        placed[rot.tile_id] = (constraint.row, constraint.col)
                        found_one = True
                        break
                if found_one:
                    break
            if found_one:
                break

    return assembly


def glue(assembly: Assembly) -> Pixels:
    """
    Glue together the Tiles into a single grid of pixels,
    removing the edges of each tile
    """
    N = len(assembly)
    n = len(assembly[0][0].pixels)
    nout = (n - 2) * N
    glued = [["" for _ in range(nout)] for _ in range(nout)]
    for i, row in enumerate(assembly):
        for j, tile in enumerate(row):
            cropped = [line[1:-1] for line in tile.pixels[1:-1]]
            for ii, crow in enumerate(cropped):
                for jj, pixel in enumerate(crow):
                    glued[i * (n - 2) + ii][j * (n - 2) + jj] = pixel

    return glued


SEA_MONSTER_RAW = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #"""

# Coordinates (matrix-wise) of #s for sea monster
SEA_MONSTER = [
    (i, j)
    for i, row in enumerate(SEA_MONSTER_RAW.split("\n"))
    for j, col in enumerate(row)
    if col == "#"
]


def find_sea_monsters(pixels: Pixels) -> Iterator[Tuple[int, int]]:
    # Gives the coordinates of the top left corner of the sea monsters in
    # the image
    for i, row in enumerate(pixels):
        for j, col in enumerate(row):
            try:
                if all(pixels[i + di][j + dj] == "#" for di, dj in SEA_MONSTER):
                    yield (i, j)
            except IndexError:
                continue


def roughness(full_pattern: Pixels) -> int:
    # Counts the #s that are not as part of a sea monster
    tile = Tile(0, full_pattern)

    # For each of the 8 transformations find the list of sea monsters
    finds = [(t, list(find_sea_monsters(t.pixels))) for t in tile.all_transformations()]

    finds = [(t, sea_monster) for t, sea_monster in finds if sea_monster]

    # Only one should have sea monsters
    assert len(finds) == 1

    t, sea_monsters = finds[0]

    sea_monster_pixels = {
        (i + di, j + dj) for i, j in sea_monsters for di, dj in SEA_MONSTER
    }

    return sum(
        col == "#" and (i, j) not in sea_monster_pixels
        for i, row in enumerate(t.pixels)
        for j, col in enumerate(row)
    )


with open("day20input") as f:
    raw = f.read()
    tiles = process(raw)
    corners = find_corners(tiles)
    assert len(corners) == 4
    print(math.prod(tile.tile_id for tile in corners))
    full_pattern = assemble_image(tiles)
    glued = glue(full_pattern)
    print(roughness(glued))
