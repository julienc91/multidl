# -*- coding: utf-8 -*-


class TransitionError(Exception):

    def __init__(self, state, new_state):
        super().__init__('Cannot change from {} to {}'
                         .format(state, new_state))
