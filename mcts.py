import copy
import numpy as np

class TreeNode:
    def __init__(self, parent=None, prior_p=0.0):
        self.parent = parent
        self.children = {}
        self.n_visits = 0.0
        self.Q = 0.0
        self.U = 0.0
        self.P = prior_p
    
    def select(self, c_puct):
        return max(self.children.items(),
                   key=lambda act_node: act_node[1].get_score(c_puct))
    
    def expand(self, action_priors):
        for action, prob in action_priors:
            if action not in self.children:
                self.children[action] = TreeNode(parent=self, prior_p=prob)
    
    def update(self, leaf_value):
        self.n_visits += 1
        self.Q += 1.0 * (leaf_value - self.Q) / self.n_visits
    
    def update_recursive(self, leaf_value):
        if self.parent:
            self.parent.update_recursive(-leaf_value)
        self.update(leaf_value)
    
    def get_score(self, c_puct):
        self.U = c_puct * self.P * np.sqrt(self.parent.n_visits) / (1 + self.n_visits)
        return self.Q + self.U
    
    def is_leaf(self):
        return self.children == {}
    
    def is_root(self):
        return self.parent is None
    
class MCTS:
    def __init__(self, policy_value_fn, c_puct=1.0, n_playout=2000):
        self.root = TreeNode(None, 1.0)
        self.c_puct = c_puct
        self.policy = policy_value_fn
        self.n_playout = n_playout
    
    def playout(self, state):
        node = self.root
        while True:
            if node.is_leaf():
                break
            action, node = node.select(self.c_puct)
            state.do_move(action)
        action_probs, leaf_value = self.policy(state)
        end, winner = state.game_end()
        if not end:
            node.expand(action_probs)
        else:
            if winner is None:
                leaf_value = 0.0
            else:
                leaf_value = 1.0 if winner == state.current_player_id else -1.0
        node.update_recursive(-leaf_value)
    
    def get_move(self, state):
        for _ in range(self.n_playout):
            _state = copy.deepcopy(state)
            self.playout(_state)
        return max(self.root.children.items(), key=lambda act_node: act_node[1].n_visits)[0]
    
    def update_with_move(self, last_move):
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
            self.root.parent = None
        else:
            self.root = TreeNode(None, 1.0)

