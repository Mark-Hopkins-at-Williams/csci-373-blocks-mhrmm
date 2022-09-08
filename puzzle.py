from search import SearchSpace, dfs


class PuzzleSearchSpace(SearchSpace):

    def __init__(self):
        super().__init__()
        raise NotImplementedError("Question One.")


    def get_start_state(self):
        """Returns the start state."""
        raise NotImplementedError("Question One.")


    def is_goal_state(self, state):
        """Checks whether a given state is a goal state.

        Parameters
        ----------
        state
            A state of the search space

        Returns
        -------
        bool
            True iff the state is a goal state
        """

        raise NotImplementedError("Question One.")


    def get_successors(self, state):
        """Determines the possible successors of a state.

        For efficiency, it is important to try to only generate successors that
        can possibly lead to a goal state.

        Parameters
        ----------
        state
            A state of the search space

        Returns
        -------
        list
            The list of valid successor states.
        """

        raise NotImplementedError("Question One.")


def puzzle_solution():
    """Computes a solution to the block puzzle distributed in class.

    The solution should be a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory should be
    consistent with the shape of the puzzle and should visit each subcube
    of a 3x3 cube exactly once.
    """

    raise NotImplementedError("Question One.")


def solution_b():
    """Computes a solution to block puzzle B from the assignment.

    The solution should be a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory should be
    consistent with the shape of the puzzle and should visit each subcube
    of a 3x3 cube exactly once.
    """

    raise NotImplementedError("Question Two.")


def solution_c():
    """Computes a solution to block puzzle C from the assignment.

    The solution should be a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory should be
    consistent with the shape of the puzzle and should visit each subcube
    of a 3x3 cube exactly once.
    """

    raise NotImplementedError("Question Two.")
