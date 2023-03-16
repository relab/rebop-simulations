import random
from block import Block


class Process:
    def __init__(self, id, type, group, target):
        self.id = id
        self.type = type
        self.total_reward = 0.0
        self.group = group
        self.target = target

        self.proposed_blocks = []
        self.last_block_proposed = 0 # the id of the last block proposed

        self.comm_rep = 0.0
        self.lead_rep = 0.0

    def propose_block(self, blocks):
        r = random.randint(0, 100)
        b = Block(len(blocks), r, self)
        self.proposed_blocks.append(b)
        return b

    def correct_validator(self, block):
        block.initial_voters.append(self)

    def colluding_validator(self, block):
        if self.group != block.proposer.group:
            if self.id % 2 == 0:
                block.initial_voters.append(self)
        else:
            block.initial_voters.append(self)

    def byzantine_validator(self):
        pass

    def correct_leader(self, block):
        block.signatures = block.initial_voters


    def colluding_leader(self, block):
        for voters in block.initial_voters:
            pass

    def byzantine_leader(self):
        pass

