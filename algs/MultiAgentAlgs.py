import greetings


def manhattanDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def evaluation_function(player_pos, enemy_pos, coins, game_score):
    score = 0.0
    for enemy in enemy_pos:
        manhattan_distance = manhattanDistance(player_pos, enemy)
        score += manhattan_distance
        # score = 0 if manhattan_distance == 0 else math.log2(manhattan_distance)
    for coin in coins:
        if [player_pos[0] + 1, player_pos[1]] == coin:
            score += 5
        if [player_pos[0], player_pos[1] + 1] == coin:
            score += 5
        if [player_pos[0], player_pos[1] - 1] == coin:
            score += 5
        if [player_pos[0] - 1, player_pos[1]] == coin:
            score += 5
    score += game_score
    return score


class ReflexAgent:
    def __init__(self, player_pos, enemy_pos, coin_pos, score, life, grid):
        self.player_pos = player_pos
        self.enemy_pos = list(enemy_pos)
        self.coin_pos = coin_pos
        self.score = score
        self.life = life
        self.grid = grid

    def get_possible_moves(self, neighbours):
        moves = []
        for neighbour in neighbours:
            if 0 <= neighbour[0] < len(self.grid[0]):
                if 0 <= neighbour[1] < len(self.grid):
                    next_cell = [int(neighbour[0]), int(neighbour[1])]
                    if self.grid[int(next_cell[1])][next_cell[0]] != '1':
                        moves.append(next_cell)
        return moves

    def is_win(self):
        return self.score == 70

    def is_lose(self):
        return self.life == 0

    def action(self):
        pass


class AlphaBetaAgent(ReflexAgent):
    def minimizer(self, depth, agent, alpha, beta):

        neighbours = [[int(self.enemy_pos[agent - 1][0] + 1), int(self.enemy_pos[agent - 1][1])],
                      [int(self.enemy_pos[agent - 1][0] - 1), int(self.enemy_pos[agent - 1][1])],
                      [int(self.enemy_pos[agent - 1][0]), int(self.enemy_pos[agent - 1][1] + 1)],
                      [int(self.enemy_pos[agent - 1][0]), int(self.enemy_pos[agent - 1][1] - 1)]]
        actions = self.get_possible_moves(neighbours=neighbours)
        scores = []
        min_score = greetings.inf
        for action in actions:
            self.enemy_pos[agent - 1] = action
            if agent == 2:
                score = self.alphabeta(depth - 1, agent=0, maximizing=True)[0]
            else:
                score = self.alphabeta(depth, agent=agent + 1, maximizing=False)[0]
            scores.append(score)
            min_score = min(scores)
            beta = min(beta, min_score)
            if beta < alpha:
                break

        min_indexes = [i for i, score in enumerate(scores) if score == min_score]
        best_score = -9999
        best_move = -1
        for i in min_indexes:
            score = evaluation_function(actions[i], self.enemy_pos, self.coin_pos, self.score)
            if score > best_score:
                best_score = score
                best_move = i
        chosen_action = actions[best_move]

        return min_score, chosen_action

    def alphabeta(self, depth, alpha=-greetings.inf, beta=greetings.inf, agent=0, maximizing=True):
        if depth == 0 or self.is_win() or self.is_lose():
            return evaluation_function(self.player_pos, self.enemy_pos, self.coin_pos, self.score), None
        if maximizing:
            return self.maximizer(depth, agent, alpha, beta)
        else:
            return self.minimizer(depth, agent, alpha, beta)

    def maximizer(self, depth, agent, alpha, beta):
        neighbours = [[int(self.player_pos[0] + 1), int(self.player_pos[1])],
                      [int(self.player_pos[0] - 1), int(self.player_pos[1])],
                      [int(self.player_pos[0]), int(self.player_pos[1] + 1)],
                      [int(self.player_pos[0]), int(self.player_pos[1] - 1)]]
        actions = self.get_possible_moves(neighbours=neighbours)
        scores = []

        max_score = -greetings.inf
        for action in actions:
            self.player_pos = action
            scores.append(self.alphabeta(depth, agent=agent + 1, maximizing=False)[0])
            max_score = max(scores)
            alpha = max(alpha, max_score)

            if alpha > beta:
                break

        max_indexes = [i for i, score in enumerate(scores) if score == max_score]
        best_score = -9999
        best_move = -1
        for i in max_indexes:
            score = evaluation_function(actions[i], self.enemy_pos, self.coin_pos, self.score)
            if score > best_score:
                best_score = score
                best_move = i
        chosen_action = actions[best_move]

        return max_score, chosen_action

    def action(self):
        return self.alphabeta(2)[1]


class MinimaxAgent(ReflexAgent):
    def minimizer(self, depth, agent):

        neighbours = [[int(self.enemy_pos[agent - 1][0] + 1), int(self.enemy_pos[agent - 1][1])],
                      [int(self.enemy_pos[agent - 1][0] - 1), int(self.enemy_pos[agent - 1][1])],
                      [int(self.enemy_pos[agent - 1][0]), int(self.enemy_pos[agent - 1][1] + 1)],
                      [int(self.enemy_pos[agent - 1][0]), int(self.enemy_pos[agent - 1][1] - 1)]]
        actions = self.get_possible_moves(neighbours=neighbours)
        scores = []
        for action in actions:
            self.enemy_pos[agent - 1] = action
            if agent == 2:
                scores.append(self.minimax(depth - 1, agent=0, maximizing=True)[0])
            else:
                scores.append(self.minimax(depth, agent=agent + 1, maximizing=False)[0])
        # print("Scores", scores)
        min_score = min(scores)
        min_indexes = [i for i, score in enumerate(scores) if score == min_score]
        best_score = -9999
        best_move = -1
        for i in min_indexes:
            score = evaluation_function(actions[i], self.enemy_pos, self.coin_pos, self.score)
            if score > best_score:
                best_score = score
                best_move = i

        chosen_action = actions[best_move]

        return min_score, chosen_action

    def minimax(self, depth, agent=0, maximizing=True):
        if depth == 0 or self.is_win() or self.is_lose():
            return evaluation_function(self.player_pos, self.enemy_pos, self.coin_pos, self.score), None
        if maximizing:
            return self.maximizer(depth, agent)
        else:
            return self.minimizer(depth, agent)

    def maximizer(self, depth, agent):
        neighbours = [[int(self.player_pos[0] + 1), int(self.player_pos[1])],
                      [int(self.player_pos[0] - 1), int(self.player_pos[1])],
                      [int(self.player_pos[0]), int(self.player_pos[1] + 1)],
                      [int(self.player_pos[0]), int(self.player_pos[1] - 1)]]
        actions = self.get_possible_moves(neighbours=neighbours)
        scores = []
        for action in actions:
            self.player_pos = action
            scores.append(self.minimax(depth, agent=agent + 1, maximizing=False)[0])

        max_score = max(scores)
        max_indexes = [i for i, score in enumerate(scores) if score == max_score]
        best_score = -9999
        best_move = -1
        for i in max_indexes:
            score = evaluation_function(actions[i], self.enemy_pos, self.coin_pos, self.score)
            if score > best_score:
                best_score = score
                best_move = i
        chosen_action = actions[best_move]

        return max_score, chosen_action

    def action(self):
        return self.minimax(2)[1]


class ExpectimaxAgent(ReflexAgent):
    def minimizer(self, depth, agent):

        neighbours = [[int(self.enemy_pos[agent - 1][0] + 1), int(self.enemy_pos[agent - 1][1])],
                      [int(self.enemy_pos[agent - 1][0] - 1), int(self.enemy_pos[agent - 1][1])],
                      [int(self.enemy_pos[agent - 1][0]), int(self.enemy_pos[agent - 1][1] + 1)],
                      [int(self.enemy_pos[agent - 1][0]), int(self.enemy_pos[agent - 1][1] - 1)]]
        actions = self.get_possible_moves(neighbours=neighbours)
        scores = []
        prob = 1.0 / len(actions)
        for action in actions:
            self.enemy_pos[agent - 1] = action
            if agent == 2:
                scores.append(self.expectimax(depth - 1, agent=0, maximizing=True)[0])
            else:
                scores.append(self.expectimax(depth, agent=agent + 1, maximizing=False)[0] * prob)
        min_score = min(scores)
        min_indexes = [i for i, score in enumerate(scores) if score == min_score]
        best_score = -9999
        best_move = -1
        for i in min_indexes:
            score = evaluation_function(actions[i], self.enemy_pos, self.coin_pos, self.score)
            if score > best_score:
                best_score = score
                best_move = i
        chosen_action = actions[best_move]

        return min_score, chosen_action

    def expectimax(self, depth, agent=0, maximizing=True):
        if depth == 0 or self.is_win() or self.is_lose():
            return evaluation_function(self.player_pos, self.enemy_pos, self.coin_pos, self.score), None
        if maximizing:
            return self.maximizer(depth, agent)
        else:
            return self.minimizer(depth, agent)

    def maximizer(self, depth, agent):
        neighbours = [[int(self.player_pos[0] + 1), int(self.player_pos[1])],
                      [int(self.player_pos[0] - 1), int(self.player_pos[1])],
                      [int(self.player_pos[0]), int(self.player_pos[1] + 1)],
                      [int(self.player_pos[0]), int(self.player_pos[1] - 1)]]
        actions = self.get_possible_moves(neighbours=neighbours)
        scores = []

        for action in actions:
            self.player_pos = action
            scores.append(self.expectimax(depth, agent=agent + 1, maximizing=False)[0])

        max_score = max(scores)
        max_indexes = [i for i, score in enumerate(scores) if score == max_score]
        best_score = -9999
        best_move = -1
        for i in max_indexes:
            score = evaluation_function(actions[i], self.enemy_pos, self.coin_pos, self.score)
            if score > best_score:
                best_score = score
                best_move = i
        chosen_action = actions[best_move]
        return max_score, chosen_action

    def action(self):
        # scores = self.expectimax(2)
        # print("Scores",scores)
        return self.expectimax(1)[1]
