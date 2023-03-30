import random
import math
from block import Block


class Process:
    def __init__(self, id, type, group, target):
        self.id = id
        self.type = type
        self.group = group
        self.target = target

        self.proposed_blocks = []
        self.last_block_proposed = 0  # the id of the last block proposed
        self.proposer_count = 0  # how many times it proposed a block in last T

        self.voting_opportunities = 0  # For last T
        self.voted = 0  # For last T

        self.comm_rep = 0.0
        self.lead_rep = 0.0
        self.total_reward = 0  # stake

    def propose_block(self, block_chain):
        r = random.randint(0, 100)
        b = Block(len(block_chain), r, self)
        self.proposed_blocks.append(b)
        return b

    def voting(self, block):  # they vote on the current block h
        if self.type == 1:  # correct
            self.correct_validator(block)

        elif self.type == 2:  # colluding
            self.colluding_validator(block)

        elif self.type == 3:  # byzantine
            pass

    def leader_vote_collection(self, committe_size: int, block_chain):  # leader "confirms" block h-1, pre_block
        pre_block = block_chain[len(block_chain) - 2]
        if self.type == 1:
            self.correct_leader(pre_block)

        elif self.type == 2:
            self.colluding_leader(pre_block, committe_size)

        elif self.type == 3:
            self.byzantine_leader(committe_size, pre_block)

    def correct_validator(self, block):
        block.initial_voters.append(self)

    def colluding_validator(self, block):
        if self.group != block.proposer.group: # colluding
            if random.randint(1, 2) == 1:
                block.initial_voters.append(self)
        else:  # always votes for block proposed by process in the same (colluding) group # TODO: look at it...
            block.initial_voters.append(self)

    def byzantine_validator(self, block):
        if self.target != block.proposer.group:  # byzantine
            block.initial_voters.append(self)

    def correct_leader(self, pre_block):
        pre_block.signatures = pre_block.initial_voters

    def colluding_leader(self, pre_block, committe_size):
        all_removed = 0
        limit = (math.floor(committe_size/3)) - (committe_size - len(pre_block.initial_voters))  # should be len(committee)
        temp = sorted(pre_block.initial_voters, key=lambda v: v.total_reward, reverse=True)  # sorts list of init_voters by total_reward earned, descending
        for voter in temp:
            if self.group == voter.group:
                pre_block.signatures.append(voter)
            else:
                if all_removed < limit:  # need to add in sorting of the list of voters based on stake
                    all_removed += 1
                    continue
                else:
                    pre_block.signatures.append(voter)

    def byzantine_leader(self, pre_block, committe_size):
        all_removed = 0
        limit = (math.floor(committe_size/3)) - (committe_size - len(pre_block.initial_voters))  # should be len(committee)
        temp = sorted(pre_block.initial_voters, key=lambda v: v.total_reward, reverse=True)  # sorts list of init_voters by total_reward earned, descending
        for voter in temp:
            if self.target != voter.group:
                pre_block.signatures.append(voter)
            else:
                if all_removed < limit:  # need to add in sorting of the list of voters based on stake
                    all_removed += 1
                    continue
                else:
                    pre_block.signatures.append(voter)

    def __str__(self):
        return f"ID: {self.id}, type: {self.type}, group: {self.group} Total Reward: {self.total_reward}"
