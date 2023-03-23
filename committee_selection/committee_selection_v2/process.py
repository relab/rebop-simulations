import random
import math
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
        self.t_reward = 0  # stake

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

    def byzantine_validator(self, block):
        pass


    def voting(self, block):
        if self.type == 1: # correct
            self.correct_validator(block)

        elif self.type == 2: # Colluding
            self.colluding_validator(block)

        elif self.type == 3: # byzantine
            pass

    def correct_leader(self, block):
        block.signatures = block.initial_voters

    def colluding_leader(self, block, committe_size):
        t_removed = 0
        limit = (math.floor(committe_size/3)) - (committe_size - len(block.initial_voters))
        for voter in block.initial_voters:
            if self.group == voter.group:
                block.signatures.append(voter)
            else:
                if t_removed < limit:
                    t_removed += 1
                    continue
                else:
                    block.signatures.append(voter)

    def byzantine_leader(self, block, committe_size):
        pass

    def leader_vote_collection(self, block, committe_size, block_chain):
        if self.type == 1:
            self.correct_leader(block)

        elif self.type == 2:
            self.colluding_leader(block, committe_size)

        elif self.type == 3:
            self.byzantine_leader(block, committe_size)

        if block.isConfirmed(committe_size):
            block_chain.append(block)
