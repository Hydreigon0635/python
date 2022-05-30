from __future__ import annotations
from typing import Optional
from typing import List
import random
import heapq
from typing import Callable, Dict

CELL_TYPE_START: str = 'S'
CELL_TYPE_PASSAGE: str = ''
CELL_TYPE_WALL: str = 'W'
CELL_TYPE_GOAL: str = 'G'
CELL_TYPE_PATH: str = '*'

class Location:
    def __init__(self, row: int, column: int) -> None:
        self.row: int = row
        self.column: int = column
class Maze:
    #生成する迷路のグリッドの縦の件数
    _ROW_NUM: int = 7

    #生成する迷路のグリッドの横の件数
    _COLUMN_NUM: int = 15

    #生成する壁の比率。１．０に近いほど壁が多くなる
    _WALL_SPARSENESS: float = 0.3

    def __init__(self) -> None:
        
        #ランダムな迷路のグリッドの生成・制御などを扱うクラス
        self._set_start_and_goal_location()
        self._grid: List[List[str]] = []
        self._fill_grid_by_passage_cell()
        self._set_wall_type_to_cells_randomly()
        self._set_start_and_goal_type_to_cell()

    def _set_start_and_goal_location(self) -> None:
        self.start_loc: Location = Location(row = 0, column = 0)
        self.goal_loc: Location = Location(
            row = self._ROW_NUM - 1,
            column = self._COLUMN_NUM - 1)

    def _fill_grid_by_passage_cell(self) -> None:

        for row in range(self._ROW_NUM):
            row_cells: List[str] = []
            for column in range(self._COLUMN_NUM):
                row_cells.append(CELL_TYPE_PASSAGE)
            self._grid.append(row_cells)

    def _set_wall_type_to_cells_randomly(self) -> None:
        for row in range(self._ROW_NUM):
            for column in range(self._COLUMN_NUM):
                probability = random.uniform(0.0, 1.0)
                if probability >= self._WALL_SPARSENESS:
                    continue
                self._grid[row][column] = CELL_TYPE_WALL
    
    def _set_start_and_goal_type_to_cell(self) -> None:
        self._grid[self.start_loc.row][self.start_loc.column] = CELL_TYPE_START
        self._grid[self.goal_loc.row][self.goal_loc.column] = CELL_TYPE_GOAL

    def __str__(self) -> str:
        grid_str: str = ''
        for row_cells in self._grid:
            grid_str += '-' * self._COLUMN_NUM * 2
            grid_str += '\n'
            for cell_type in row_cells:
                grid_str += cell_type
                grid_str += '|'
            grid_str += '\n'
        return grid_str


if __name__ == '__main__':
    maze = Maze()
    print(maze)
  


