from __future__ import annotations
from typing import Optional
from typing import List
import random
import heapq
from typing import Callable, Dict

# 入口用の定数値。
CELL_TYPE_START: str = 'S'

# 通路用の定数値。
CELL_TYPE_PASSAGE: str = ' '

# 壁の定数値。
CELL_TYPE_WALL: str = 'W'

# 出口の定数値。
CELL_TYPE_GOAL: str = 'G'

# 算出されたルートのパス用の定数値。
CELL_TYPE_PATH: str = '*'

class Location:

    def __init__(self, row: int, column: int) -> None:
        """
        迷路のグリッドの位置情報単体を扱うクラス。

        Parameters
        ----------
        row : int
            位置の行番号。0からスタートし、上から下に向かって1ずつ
            加算される。
        column : int
            位置の列番号。0からスタートし、左から右に向かって1ずつ
            加算される。
        """
        self.row: int = row
        self.column: int = column


class Maze:

    # 生成する迷路のグリッドの縦の件数。
    _ROW_NUM: int = 7

    # 生成する迷路のグリッドの横の件数。
    _COLUMN_NUM: int = 15

    # 生成する壁の比率。1.0に近いほど壁が多くなる。
    _WALL_SPARSENESS: float = 0.3

    def __init__(self) -> None:
        """
        ランダムな迷路のグリッドの生成・制御などを扱うクラス。

        Notes
        -----
        ランダムに各セルタイプが設定されるため、必ずしもスタートから
        ゴールに到達できるものができるわけではない点には注意。
        """

        self._set_start_and_goal_location() #入り口と出口の座標の属性の設定
        self._grid: List[List[str]] = [] #二重配列の_gridを初期化
        self._fill_grid_by_passage_cell()
        self._set_wall_type_to_cells_randomly()
        self._set_start_and_goal_type_to_cell()

    def _set_start_and_goal_location(self) -> None:
        """
        開始地点（入口）とゴール（出口）の座標の属性を設定する。
        """
        self.start_loc: Location = Location(row=3, column=5)
        self.goal_loc: Location = Location(
            row=self._ROW_NUM - 1,
            column=self._COLUMN_NUM - 1)

    def _fill_grid_by_passage_cell(self) -> None:
        """
        全てのセルに対してセルの追加を行い、通路のセルタイプを設定する。
        """
        for row in range(self._ROW_NUM):
            row_cells: List[str] = [] #row_cellsを文字列配列として初期化
            for column in range(self._COLUMN_NUM): #row_cellを二次元配列にする
                row_cells.append(CELL_TYPE_PASSAGE)
            self._grid.append(row_cells)

    def _set_wall_type_to_cells_randomly(self) -> None:
        """
        グリッドの各セルへ、ランダムに壁のセルタイプを設定する。
        """
        for row in range(self._ROW_NUM):
            for column in range(self._COLUMN_NUM):
                probability = random.uniform(0.0, 1.0)
                if probability >= self._WALL_SPARSENESS:
                    continue
                self._grid[row][column] = CELL_TYPE_WALL

    def _set_start_and_goal_type_to_cell(self) -> None:
        """
        開始（入口）とゴール（出口）の位置にそれぞれの
        セルタイプを設定する。
        """
        self._grid[self.start_loc.row][self.start_loc.column] = \
            CELL_TYPE_START
        self._grid[self.goal_loc.row][self.goal_loc.column] = \
            CELL_TYPE_GOAL

    def is_goal_loc(self, location: Location) -> bool:
        """
        指定された位置がゴールの位置かどうかの真偽値を取得する。

        Parameters
        ----------
        location : Location
            判定用の位置。

        Returns
        -------
        result : bool
            ゴールの位置であればTrueが設定される。
        """
        if (location.row == self.goal_loc.row
                and location.column == self.goal_loc.column):
            return True
        return False

    def get_movable_locations(self, location: Location) -> List[Location]:
        """
        指定された位置から、移動が可能な位置のリストを取得する。

        Parameters
        ----------
        location : Location
            基準となる位置のインスタンス。

        Returns
        -------
        movable_locations : list of Location
            移動可能な位置のインスタンスを格納したリスト。
        """
        movable_locations: List[Location] = []

        # 上に移動可能かどうかの判定処理。
        if location.row + 1 < self._ROW_NUM:
            is_wall: bool = self._grid[location.row + 1][location.column] \
                == CELL_TYPE_WALL
            if not is_wall:
                movable_locations.append(
                    Location(row=location.row + 1, column=location.column))

        # 下に移動可能かどうかの判定処理。
        if location.row - 1 >= 0:
            is_wall = self._grid[location.row - 1][location.column] \
                == CELL_TYPE_WALL
            if not is_wall:
                movable_locations.append(
                    Location(row=location.row - 1, column=location.column))

        # 右に移動可能かどうかの判定処理。
        if location.column + 1 < self._COLUMN_NUM:
            is_wall = self._grid[location.row][location.column + 1] \
                == CELL_TYPE_WALL
            if not is_wall:
                movable_locations.append(
                    Location(row=location.row, column=location.column + 1))

        # 左に移動可能かどうかの判定処理。
        if location.column - 1 >= 0:
            is_wall = self._grid[location.row][location.column - 1] \
                == CELL_TYPE_WALL
            if not is_wall:
                movable_locations.append(
                    Location(row=location.row, column=location.column - 1))

        return movable_locations

    def set_path_type_to_cells(self, path: List[Location]) -> None:
        """
        入口と出口までの指定されたパス内に含まれるセルに対して、
        パスのセルタイプを設定する。

        Parameters
        ----------
        path : list of Location
            探索で得られた入口から出口までの各セルの位置情報を
            格納したリスト。
        """
        for location in path:
            self._grid[location.row][location.column] = CELL_TYPE_PATH

        # パス内に含まれている入口と出口の部分は、それぞれ元の
        # セルタイプを反映する。
        self._grid[self.start_loc.row][self.start_loc.column] = \
            CELL_TYPE_START
        self._grid[self.goal_loc.row][self.goal_loc.column] = \
            CELL_TYPE_GOAL

    def get_manhattan_distance(self, location: Location) -> int:
        """
        対象の位置と出口（ゴール）の位置間でのマンハッタン距離を
        取得する。

        Parameters
        ----------
        location : Location
            対象の位置のインスタンス。

        Returns
        -------
        distance : int
            対象の位置と出口の位置間のマンハッタン距離。列方向の
            差異の絶対値と行方向の差異の絶対値の合計が設定される。
        """
        x_distance: int = abs(location.column - self.goal_loc.column)
        y_distance: int = abs(location.row - self.goal_loc.column)
        distance: int = x_distance + y_distance
        return distance

    def __str__(self) -> str:
        """
        グリッドの各セルのタイプの文字列を取得する。

        Returns
        -------
        grid_str : str
            グリッドの各セルのタイプの文字列。
        """
        grid_str: str = ''
        for row_cells in self._grid:
            grid_str += '-' * self._COLUMN_NUM * 2
            grid_str += '\n'
            for cell_type in row_cells:
                grid_str += cell_type
                grid_str += '|'
            grid_str += '\n'
        return grid_str


class Node:

    def __init__(
            self, location: Location, parent: Optional[Node],
            cost: float, heuristic:float) -> None:
        """
        迷路の位置や推移の情報などを保持するためのノード単体のデータを
        扱うクラス。

        Parameters
        ----------
        location : Location
            対象の位置情報を扱うインスタンス。
        parent : Node or None
            移動前の位置情報を扱うノードのインスタンス。探索開始時
            などにはNoneとなる。
        cost : float
            開始位置から該当のノードの位置までのコスト値（g(n)で
            得られる値）。
        heuristic : float
            このノードから出口までの距離の推定値（h(n)で得られる値）。
        """
        self.location: Location = location
        self.parent: Optional[Node] = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other_node: Node) -> bool:
        """
        比較のオペレーター( < )による処理のためのメソッド。
        優先度付きキューの制御のために利用される。

        Parameters
        ----------
        other_node : Node
            比較対象となる他のノードのインスタンス。

        Returns
        -------
        result_bool : bool
            比較結果。算出処理は入口からのコスト（g(n)）と
            ヒューリスティックの値（h(n)）の合算値の比較で
            行われる。
        """
        left_value: float = self.cost + self.heuristic
        right_value: float = other_node.cost + other_node.heuristic
        result_bool: bool = left_value < right_value
        return result_bool


def get_path_from_goal_node(goal_node: Node) -> List[Location]:
    """
    出口のノードから、探索で取得できた入口 → 出口までのパスを
    取得する。

    Parameters
    ----------
    goal_node : Node
        対象の出口（ゴール）のノードのインスタンス。

    Returns
    -------
    path : list of Location
        入口から出口までの各位置のインスタンスを格納したリスト。
    """
    path: List[Location] = [goal_node.location]
    node: Node = goal_node
    while node.parent is not None:
        node = node.parent
        path.append(node.location)
    path.reverse()
    return path


class PriorityQueue:

    def __init__(self) -> None:
        """
        優先度付きキューの制御を行うためのクラス。
        """
        self._container: List[Node] = []

    @property
    def empty(self) -> bool:
        """
        キューが空かどうかの属性値。

        Returns
        -------
        result : bool
            空の場合にTrueが設定される。
        """
        return not self._container

    def push(self, node: Node) -> None:
        """
        キューへのノードのインスタンスの追加を行う。

        Parameters
        ----------
        node : Node
            追加対象のノードのインスタンス。
        """
        heapq.heappush(self._container, node)

    def pop(self) -> Node:
        """
        キューから優先度の一番高いノードのインスタンスを取り出す。

        Returns
        -------
        node : Node
            取り出されたNodeクラスのインスタンス。
        """
        return heapq.heappop(self._container)


def astar(
        init_loc: Location,
        is_goal_loc_method: Callable[[Location], bool],
        get_movable_locations_method: Callable[[Location], List[Location]],
        hueristic_method: Callable[[Location], int],
        ) -> Optional[Node]:
    """
    A*アルゴリズムによる探索処理を行う。

    Parameters
    ----------
    init_loc : Location
        探索開始位置（迷路の入口の位置）。
    is_goal_loc_method : callable
        対象の位置が出口（ゴール）かどうかの判定を行うメソッド。
    get_movable_locations_method : callable
        対象の位置からの移動先のセルの位置のリストを取得するメソッド。
    hueristic_method : callable
        対象の位置から出口（ゴール）までの位置の間の距離を取得する
        ためのヒューリスティック用のメソッド。

    Returns
    -------
    goal_node : Node or None
        算出された出口の位置のノードのインスタンス。出口までの
        経路が算出できないケースではNoneが設定される。
    """
    frontier_queue: PriorityQueue = PriorityQueue()
    frontier_queue.push(
        node=Node(
            location=init_loc,
            parent=None,
            cost=0,
            heuristic=hueristic_method(init_loc)))

    explored_loc_cost_dict: Dict[Location, float] = {init_loc: 0.0}

    while not frontier_queue.empty:
        current_node: Node = frontier_queue.pop() #１マス移動する
        current_loc: Location = current_node.location #移動後のロケーションに設定

        if is_goal_loc_method(current_loc):
            return current_node

        movable_locations = get_movable_locations_method(current_loc)
        for movable_location in movable_locations:
            new_cost: float = current_node.cost + 1

            # 新しい移動先が既に探索済みで、且つコスト的にも優位ではない
            # 場合にはスキップする。
            if (movable_location in explored_loc_cost_dict and
                    explored_loc_cost_dict[movable_location] <= new_cost):
                continue

            explored_loc_cost_dict[movable_location] = new_cost
            frontier_queue.push(
                node=Node(
                    location=movable_location,
                    parent=current_node,
                    cost=new_cost,
                    heuristic=hueristic_method(movable_location)))
    return None


if __name__ == '__main__':
    maze: Maze = Maze()
    print(maze)

    goal_node: Optional[Node] = astar(
        init_loc=maze.start_loc,
        is_goal_loc_method=maze.is_goal_loc,
        get_movable_locations_method=maze.get_movable_locations,
        hueristic_method=maze.get_manhattan_distance,
    )
    if goal_node is None:
        print('出口が算出できない迷路です。')
    else:
        print('-' * 20)
        path: List[Location] = get_path_from_goal_node(
            goal_node=goal_node)
        maze.set_path_type_to_cells(path=path)
        print('算出されたパス :')
        print(maze)