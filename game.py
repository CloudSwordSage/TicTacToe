import os
import copy

init_board = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' ']]

def str2list(board: list[list[str]]) -> list[list[int]]:
    """
    将二维字符列表转换成二维整数列表。
    
    Args:
        board (list[list[str]]): 二维字符列表，只包含字符' ','X','O'。
    
    Returns:
        list[list[int]]: 二维整数列表，字符' ','X','O'分别被替换为整数0,1,2。
    
    """
    _board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                _board[i][j] = 0
            elif board[i][j] == 'X':
                _board[i][j] = 1
            else:
                _board[i][j] = 2
    return _board

def list2str(board: list[list[int]]) -> list[list[str]]:
    """
    将二维整数列表转换成二维字符列表。
    
    Args:
        board (list[list[int]]): 二维整数列表，只包含整数0,1,2。
    
    Returns:
        list[list[str]]: 二维字符列表，整数0被替换为字符' '，整数1被替换为字符'X'，整数2被替换为字符'O'。
    """
    _board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                _board[i][j] = ' '
            elif board[i][j] == 1:
                _board[i][j] = 'X'
            else:
                _board[i][j] = 'O'
    return _board

def print_board(board: list[list[str]], disappear: list[tuple[int]]=[]) -> None:
    """
    打印井字棋游戏棋盘，并可在指定位置标记即将消失的棋子。
    
    Args:
        board (list[list[str]]): 井字棋游戏棋盘，每个元素为一个字符串，表示对应位置的棋子或空格。
        disappear (list[tuple[int]], optional): 即将消失的棋子的位置列表，每个元素为一个包含两个整数的元组，分别表示行索引和列索引。默认为空列表。
    
    Returns:
        None
    
    """

    os.system('cls')
    _board = list2str(copy.deepcopy(board))
    if len(disappear) > 0:
        for i, j in disappear:
            _board[i][j] = '\033[2m{}\033[0m'.format(_board[i][j])
    print(' {} | {} | {} '.format(_board[0][0], _board[0][1], _board[0][2]))
    print('---|---|---')
    print(' {} | {} | {} '.format(_board[1][0], _board[1][1], _board[1][2]))
    print('---|---|---')
    print(' {} | {} | {} '.format(_board[2][0], _board[2][1], _board[2][2]))

def is_win(board: list[list[int]], player: int) -> bool:
    """
    判断玩家是否在棋盘上获胜。
    
    Args:
        board (list[list[int]]): 3x3的棋盘，每个位置上的整数表示该位置上的棋子所属玩家，0表示空位置。
        player (int): 玩家编号，1或2。
    
    Returns:
        bool: 若玩家在棋盘上获胜则返回True，否则返回False。
    
    """
    # 对角线
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    elif board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    # 横线
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True
    # 竖线
    for j in range(3):
        if board[0][j] == player and board[1][j] == player and board[2][j] == player:
            return True
    return False

move_id2move_actions = {
    0:(0, 0),
    1:(0, 1),
    2:(0, 2),
    3:(1, 0),
    4:(1, 1),
    5:(1, 2),
    6:(2, 0),
    7:(2, 1),
    8:(2, 2)
}

move_actions2move_id = {
    (0, 0):0,
    (0, 1):1,
    (0, 2):2,
    (1, 0):3,
    (1, 1):4,
    (1, 2):5,
    (2, 0):6,
    (2, 1):7,
    (2, 2):8
}

def get_legal_position_id(board: list[list[int]]) -> list[int]:
    """
    获取在给定棋盘上所有合法的落子位置ID列表
    
    Args:
        board (list[list[int]]): 9x9棋盘，其中0表示空位，1到9表示不同玩家的棋子
    
    Returns:
        list[int]: 所有合法的落子位置ID列表，按字典序排列
    
    """
    ans = []
    for i in range(9):
        y, x = move_id2move_actions[i]
        if board[y][x] == 0:
            ans.append(i)
    return ans

class Game:
    def __init__(self) -> None:
        self.board = copy.deepcopy(str2list(init_board))
        self.player1 = [False] * 4
        self.player2 = [False] * 4
    
    def init_board(self, start_player: int) -> None:
        """
        初始化棋盘。
        
        Args:
            start_player (int): 1或2，表示谁先开始。
        
        Returns:
            None
        """
        self.board = copy.deepcopy(str2list(init_board))
        self.player1 = [False] * 4
        self.player2 = [False] * 4
        if start_player == 1:
            self.current_player = 1
        else:
            self.current_player = 2
        self.winner = None
    
    @property
    def availables(self):
        """
        获取当前玩家可落子位置ID列表。
        
        Args:
            None
        
        Returns:
            list[int]: 当前玩家可落子位置ID列表，按字典序排列
        """
        return get_legal_position_id(self.board)
        
    def do_move(self, move_id: int) -> None:
        """
        执行玩家落子。
        
        Args:
            move_id (int): 落子位置ID，从0到8。
        
        Returns:
            None
        """
        y, x = move_id2move_actions[move_id]
        self.board[y][x] = self.current_player
        if self.current_player == 1:
            self.player1.append((y, x))
            if len(self.player1) >= 4:
                self.player1.pop(0)
        else:
            self.player2.append((y, x))
            if len(self.player2) >= 4:
                self.player2.pop(0)

        if self.player1[0]:
            y, x = self.player1[0]
            self.board[y][x] = 0
            self.player1 = self.player1[1:]

        if self.player2[0]:
            y, x = self.player2[0]
            self.board[y][x] = 0
            self.player2 = self.player2[1:]

        if is_win(self.board, self.current_player):
            self.winner = self.current_player
        self.current_player = 3 - self.current_player
    
    def is_win(self) -> tuple[bool, int]:
        """
        判断当前玩家是否获胜。
        
        Args:
            None
        
        Returns:
            bool: 若当前玩家获胜则返回True，否则返回False。
            int: 若当前玩家获胜，则返回该玩家的编号，否则返回None。
        """
        if self.winner is not None:
            return True, self.winner
        return False, None
    
    def game_end(self) -> tuple[bool, int]:
        """
        判断游戏是否结束，并返回结束标志和获胜者编号。
        
        Args:
            无参数。
        
        Returns:
            一个包含两个元素的元组，第一个元素为bool类型，表示游戏是否结束；
            第二个元素为int类型或None，表示获胜者编号，如果游戏未结束或平局则为None。
        
        """
        done, winner = self.is_win()
        if done:
            return True, winner
        else:
            if all(0 not in row for row in self.board):
                return True, None
        return False, None
    
    @property
    def disappear(self) -> list[tuple[int]]:
        """
        返回所有消失玩家位置列表。
        
        Args:
            无参数。
        
        Returns:
            包含所有消失玩家位置的列表，每个位置为一个元组，包含两个整数，分别表示行和列。
        
        """
        ans = []
        if self.player1[1]:
            i, j = self.player1[1]
            ans.append((i, j))
        if self.player2[1]:
            i, j = self.player2[1]
            ans.append((i, j))
        return ans
    
    @property
    def state(self) -> list[list[int]]:
        """
        返回消除后棋盘的状态。
        
        Args:
            无参数。
        
        Returns:
            list[list[int]]: 返回一个二维列表，表示消除后棋盘的状态。
        
        """
        _state = copy.deepcopy(self.board)
        for i, j in self.disappear:
            _state[i][j] = 0
        return _state


if __name__ == '__main__':
    game = Game()
    game.init_board(1)
    while True:
        print_board(game.board, disappear=game.disappear)
        availables = game.availables
        move = tuple(map(int, input('请输入落子位置：').split()))
        move = (move[0] - 1, move[1] - 1)
        move_id = move_actions2move_id[move]
        while move_id not in availables:
            move = tuple(map(int, input('请输入落子位置：').split()))
            move = (move[0] - 1, move[1] - 1)
            move_id = move_actions2move_id[move]
        game.do_move(move_id)
        done, winner = game.game_end()
        if done:
            print_board(game.board, disappear=game.disappear)
            if winner is None:
                print('平局！')
            else:
                print(f'{"X" if winner == 1 else "O"}获胜！')
            break

    # state = [[0, 2, 2], [1, 2, 0], [0, 2, 0]]
    # disappear = [(0, 1), (2, 1)]
    # print_board(state, disappear=disappear)