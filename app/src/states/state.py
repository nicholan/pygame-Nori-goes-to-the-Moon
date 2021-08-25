class State():
    """
    Base state class that other states will inherit from.
    """
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def on_event(self, event):
        pass

    def update(self, delta):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        if len(self.game.state_stack) > 1:
            self.game.state_stack.pop()