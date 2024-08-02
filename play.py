from mcts import MCTS
from game import Game, print_board, move_actions2move_id

import random

game = Game()

def policy_value_fn(state:Game) -> tuple[list[tuple[int, float]], float]:
    """
    根据游戏状态，计算策略值函数，返回可选动作的概率分布和叶子节点的值。
    
    Args:
        state (Game): 游戏状态对象。
    
    Returns:
        tuple[list[tuple[int, float]], float]: 一个元组，包含两个元素：
            - list[tuple[int, float]]: 一个列表，包含可选动作的概率分布，每个元素是一个元组，包含可选动作和对应的概率。
            - float: 叶子节点的值，初始化为0.0。
    
    """
    legal_moves = state.availables
    action_probs = [(move, 1.0 / len(legal_moves)) for move in legal_moves]
    leaf_value = 0.0
    return action_probs, leaf_value

def random_policy_value(state:Game) -> tuple[list[tuple[int, float]], float]:
    """
    根据给定游戏状态生成随机的策略值和叶子节点值。
    
    Args:
        state (Game): 游戏状态对象，包含游戏当前状态信息。
    
    Returns:
        tuple[list[tuple[int, float]], float]: 一个元组，包含两个元素：
            - list[tuple[int, float]]: 一个列表，包含可选动作的随机概率分布，每个元素是一个元组，包含可选动作和对应的概率。
            - float: 叶子节点的值，初始化为0.0。
    
    """
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