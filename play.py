from mcts import MCTS
from game import Game, print_board, move_actions2move_id

import random

game = Game()

def policy_value_fn(state):
    legal_moves = state.availables
    action_probs = [(move, 1.0 / len(legal_moves)) for move in legal_moves]
    leaf_value = 0.0
    return action_probs, leaf_value

def random_policy_value(state):
    legal_moves = state.availables
    action_probs = [(move, random.random()) for move in legal_moves]
    leaf_value = 0.0
    return action_probs, leaf_value

mcts = MCTS(random_policy_value, 1, 2000)
print_board(game.board, disappear=game.disappear)
choose = int(input('请选择先手：1.随机 2.人类 3.AI\n>>> '))
if choose == 1:
    start = random.randint(2, 3)
else:
    start = choose
game.init_board(start_player=start - 1)
if start == 2:
    while True:
        availables = game.availables
        move = tuple(map(int, input('请输入落子位置：').split()))
        move = (move[0] - 1, move[1] - 1)
        move_id = move_actions2move_id[move]
        while move_id not in availables:
            move = tuple(map(int, input('请输入落子位置：').split()))
            move = (move[0] - 1, move[1] - 1)
            move_id = move_actions2move_id[move]
        game.do_move(move_id)
        print_board(game.board, disappear=game.disappear)
        done, winner = game.game_end()
        if done:
            if winner is None:
                print('平局！')
            else:
                print(f'{"玩家" if winner == 1 else "AI"}获胜！')
            break
        move = mcts.get_move(game)
        mcts.update_with_move(-1)
        game.do_move(move)
        print_board(game.board, disappear=game.disappear)
        done, winner = game.game_end()
        if done:
            if winner is None:
                print('平局！')
            else:
                print(f'{"玩家" if winner == 1 else "AI"}获胜！')
            break
else:
    while True:
        move = mcts.get_move(game)
        mcts.update_with_move(-1)
        game.do_move(move)
        print_board(game.board, disappear=game.disappear)
        done, winner = game.game_end()
        if done:
            if winner is None:
                print('平局！')
            else:
                print(f'{"玩家" if winner == 1 else "AI"}获胜！')
            break
        availables = game.availables
        move = tuple(map(int, input('请输入落子位置：').split()))
        move = (move[0] - 1, move[1] - 1)
        move_id = move_actions2move_id[move]
        while move_id not in availables:
            move = tuple(map(int, input('请输入落子位置：').split()))
            move = (move[0] - 1, move[1] - 1)
            move_id = move_actions2move_id[move]
        game.do_move(move_id)
        print_board(game.board, disappear=game.disappear)
        done, winner = game.game_end()
        if done:
            if winner is None:
                print('平局！')
            else:
                print(f'{"玩家" if winner == 1 else "AI"}获胜！')
            break