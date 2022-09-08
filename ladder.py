from search import SearchSpace, bfs


class WordLadderSearchSpace(SearchSpace):

    def __init__(self, initial_word, goal_word):
        super().__init__()
        with open('english.txt') as reader:
            self.valid_words = [line.strip() for line in reader]
        self.start_state = (initial_word, )
        self.goal_word = goal_word


    def get_start_state(self):
        """Returns the start state.

        A state is a sequence of ladder words. The start state is a singleton sequence
        containing the initial word.

        Returns
        -------
        tuple[str]
            The start state, a singleton sequence containing the initial word
        """

        return self.start_state


    def is_goal_state(self, state):
        """Checks whether a given state is a goal state.

        A state is a sequence of ladder words. A goal state is a sequence of ladder
        word whose final word is the goal word.

        Parameters
        ----------
        state : tuple[str]
            A state of the search space, corresponding to the current sequence of ladder words

        Returns
        -------
        bool
            True iff the state is a goal state
        """

        return state[-1] == self.goal_word


    def get_successors(self, state):
        """Determines the possible successors of a state.

        A state is a sequence of ladder words. A successor is a valid extension of that
        sequence, i.e. the extension word is a valid English word that differs by one
        letter from the former last word in the sequence.

        Parameters
        ----------
        state : tuple[str]
            A state of the search space, i.e. the current sequence of ladder words

        Returns
        -------
        list[tuple[str]]
            The list of valid successor states.
        """

        latest_word = state[-1]
        successor_words = []
        for i in range(len(latest_word)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                if letter != latest_word[i]:
                    candidate = latest_word[:i] + letter + latest_word[i+1:]
                    if candidate in self.valid_words:
                        successor_words.append(candidate)
        return [state + tuple([word]) for word in successor_words]


def word_ladder_solution(initial_word, final_word):
    """Computes an optimal solution to the given word ladder, if one exists.

    Parameters
    ----------
    initial_word : str
        The initial word of the ladder
    final_word : str
        The final (goal) word of the ladder

    Returns
    -------
    tuple[str]
        A solution to the word ladder, expressed as a tuple of strings. If there is no
        valid solution, this function has undetermined behavior (it may run forever).
    """

    return bfs(WordLadderSearchSpace(initial_word, final_word))


if __name__ == '__main__':
    print(word_ladder_solution("train", "prawn"))