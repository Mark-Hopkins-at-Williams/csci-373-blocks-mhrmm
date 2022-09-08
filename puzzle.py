from search import SearchSpace, dfs


def move(position, direction):
    """Determines the new position after moving a given direction from an initial position.

    The position coordinates are in 3-dimensional Euclidean space. The possible directions
    are North ('N'), South ('S'), East ('E'), West ('W'), Up ('U'), and Down ('D').

    Parameters
    ----------
    position : tuple[int]
        The initial position, expressed as (x,y,z) coordinates
    direction : str
        The direction in which to travel ('N','S','E','W','U','D')

    Returns
    -------
    int, int, int
        The (x,y,z) coordinates of the new position, after moving the given direction
        from the initial position

    Raises
    ------
    ValueError
        If the provided direction is not a member of the set {'N','S','E','W','U','D'}
    """

    x, y, z = position
    if direction == "E":
        return x+1, y, z
    elif direction == "W":
        return x-1, y, z
    elif direction == "N":
        return x, y+1, z
    elif direction == "S":
        return x, y-1, z
    elif direction == "U":
        return x, y, z+1
    elif direction == "D":
        return x, y, z-1
    else:
        raise ValueError(f"Unrecognized direction: {direction}")


def positions_visited(trajectory):
    """Enumerates the positions (in 3-d Euclidean space) visited by a trajectory.

    A trajectory is a list of directions. The possible directions
    are North ('N'), South ('S'), East ('E'), West ('W'), Up ('U'), and Down ('D').

    The position coordinates are in 3-dimensional Euclidean space. It is assumed that
    one begins at the origin, i.e. position (0,0,0).

    Parameters
    ----------
    trajectory : list[str]
        A sequence of directions to travel from the origin.

    Returns
    -------
    list[tuple[int]]
        The positions visited by the given trajectory. Each position is a tuple (x,y,z).
    """

    positions = [(0,0,0)]
    for direction in trajectory:
        next_position = move(positions[-1], direction)
        positions.append(next_position)
    return positions


def shift_into_positive_space(positions):
    """Translates a list of positions into the positive sector of 3-d Euclidean space.

    The coordinates are shifted such that their relative positions remain the same.

    Parameters
    ----------
    positions : list[tuple[int]]
        A list of 3-d coordinates.

    Returns
    -------
    list[tuple[int]]
        The input list of coordinates, shifted so that none of them are in "negative" space,
        i.e. none of them contain negative numbers.
    """

    min_x = min([x for x,_,_ in positions])
    min_y = min([y for _,y,_ in positions])
    min_z = min([z for _,_,z in positions])
    return [(x-min_x, y-min_y, z-min_z) for x, y, z in positions]


def is_connected(positions):
    if len(positions) == 0:
        return True
    else:
        open_list = [positions[0]]
        closed_list = set()
        positions = set(positions[1:])
        while len(open_list) > 0:
            position, open_list = open_list[0], open_list[1:]
            for adjacent in [move(position, d) for d in ['N', 'S', 'E', 'W', 'U', 'D']]:
                if adjacent in positions:
                    open_list.append(adjacent)
                    positions.remove(adjacent)
            closed_list.add(position)
        return len(positions) == 0



class SnakePuzzleSearchSpace(SearchSpace):

    def __init__(self, multipliers, cube_width):
        super().__init__()
        #self.multipliers = (2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2)
        self.multipliers = multipliers
        self.pivot_points = set([sum(self.multipliers[:i]) for i in range(len(self.multipliers))])
        self.start_state = ('E',)
        self.cube_width = cube_width
        self.goal_positions = set([(x,y,z)
                                   for x in range(0, cube_width)
                                   for y in range(0, cube_width)
                                   for z in range(0, cube_width)])


    def at_pivot(self, state):
        return len(state) in self.pivot_points


    def get_start_state(self):
        """Returns the start state.

        A state of this search space is a sequence of directions. The start state
        contains a single arbitrary initial direction ('E').

        Returns
        -------
        tuple[str]
            The start state
        """

        return self.start_state


    def is_goal_state(self, state):
        """Checks whether a given state is a goal state.

        To qualify as a goal state, the state trajectory should visit all
        positions in a 3x3 cube (without visiting the same position twice).

        Parameters
        ----------
        state : tuple[str]
            A state of the search space, i.e. a sequence of directions

        Returns
        -------
        bool
            True iff the state is a goal state
        """

        positions = shift_into_positive_space(positions_visited(state))
        return set(positions) == self.goal_positions

    def is_valid_state(self, state):
        """Checks whether a given state can possibly lead to a goal state.

        In other words, this method checks whether there is some sequence of directions
        that can be appended to the given state (which is also a sequence of directions)
        in order to create a goal state.

        Parameters
        ----------
        state : tuple[str]
            A state of the search space, i.e. a sequence of directions

        Returns
        -------
        bool
            True iff the state can possibly be extended to become a goal state.
        """
        positions = shift_into_positive_space(positions_visited(state))
        max_x = max([x for x,_,_ in positions])
        max_y = max([y for _,y,_ in positions])
        max_z = max([z for _,_,z in positions])
        unvisited = list(self.goal_positions - set(positions))
        return max(max_x, max_y, max_z) < self.cube_width and len(set(positions)) == len(positions) and is_connected(unvisited)

    def get_successors(self, state):
        """Determines the possible successors of a state.

        A state is a sequence of directions. To generate its successor, we append a direction
        that forces the "snake" to make a 90-degree turn along some axis. In other words,
        one cannot append the direction in which the snake is already heading, nor can one
        append the completely opposite direction.

        For instance, if the state is (U, N, W), then we cannot append directions "W" (the
        direction in which the snake is currently going) or "E" (the opposite direction)
        to derive a successor.

        This method also filters out successors that lead to "invalid" states, as determined
        by the .is_valid_state() method.

        Parameters
        ----------
        state : tuple[str]
            A state of the search space, i.e. a sequence of directions

        Returns
        -------
        list[tuple[str]]
            The list of valid successor states.
        """

        if len(state) >= sum(self.multipliers):
            return []
        next_directions = []
        if not self.at_pivot(state):
            next_directions = [state[-1]]
        elif state[-1] in ["E", "W"]:
            next_directions = ["N", "S", "U", "D"]
        elif state[-1] in ["N", "S"]:
            next_directions = ["E", "W", "U", "D"]
        elif state[-1] in ["U", "D"]:
            next_directions = ["E", "W", "N", "S"]
        candidates = [state + (direction,) for direction in next_directions]
        return [candidate for candidate in candidates if self.is_valid_state(candidate)]


class StandardSnakePuzzle(SnakePuzzleSearchSpace):
    def __init__(self):
        super().__init__(multipliers=(2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2),
                         cube_width=3)

class SnakePuzzleB(SnakePuzzleSearchSpace):
    def __init__(self):
        super().__init__(multipliers=(2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2),
                         cube_width=3)

class SnakePuzzleC(SnakePuzzleSearchSpace):
    def __init__(self):
        super().__init__(multipliers=(1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2),
                         cube_width=3)


class LargeSnakePuzzle(SnakePuzzleSearchSpace):
    def __init__(self):
        super().__init__(multipliers=(1,3,1,1,1,1,1,1,1,1,1,2,1,3,1,1,1,3,2,1,1,1,1,1,
                                      2,2,1,1,1,1,1,1,1,1,2,1,2,1,2,1,3,1,1,2,1,2),
                         cube_width=4)

def puzzle_solution():
    return dfs(StandardSnakePuzzle())

def solution_b():
    return dfs(SnakePuzzleC())

def solution_c():
    return dfs(SnakePuzzleC())

if __name__ == '__main__':
    print('-'.join(dfs(ThirdSnakePuzzle())))