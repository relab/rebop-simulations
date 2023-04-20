import random
import math
from simulation_setup.block import Block

# TODO: find a solution for rho vs omit_vite and sigma vs no_vote, in process.py


class Process:
    def __init__(self, id, group, target, no_vote=False, omit_vote=False):
        self.id = id
        # self.type = type
        self.group = group
        self.target = target

        self.no_vote = no_vote
        self.omit_vote = omit_vote

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

    def __str__(self):
        return f"ID: {self.id}, type: {type(self)}, group: {self.group}, target: {self.target} Total Reward:" \
               f" {self.total_reward}"


class CorrectProcess(Process):
    def voting(self, block, sigma):
        block.initial_voters.append(self)

    def leader_vote_collection(self, committe_size, block_chain, rho):
        pre_block = block_chain[len(block_chain) - 2]
        pre_block.signatures = pre_block.initial_voters


class ColludingProcess(Process):  # uses rho and sigma and not omit/novote
    def voting(self, block, sigma):
        r = random.randint(0, 100)
        if self.group != block.proposer.group and r < (sigma*100):
            if random.randint(1, 2) == 1:
                block.initial_voters.append(self)
        else:  # always votes for block proposed by process in the same (colluding) group # TODO: look at it...
            block.initial_voters.append(self)

    def leader_vote_collection(self, committe_size, block_chain, rho):
        pre_block = block_chain[len(block_chain) - 2]
        all_removed = 0
        limit = (math.floor(committe_size/3)) - (committe_size - len(pre_block.initial_voters))  # should be len(committee)
        temp = sorted(pre_block.initial_voters, key=lambda v: v.total_reward, reverse=True)  # sorts list of init_voters by total_reward earned, descending
        r = random.randint(0, 100)
        if r < (rho*100):
            for voter in temp:
                if self.group == voter.group:
                    pre_block.signatures.append(voter)
                else:
                    if all_removed < limit:  # need to add in sorting of the list of voters based on stake
                        all_removed += 1
                        continue
                    else:
                        pre_block.signatures.append(voter)
        else:
            pre_block.signatures = pre_block.initial_voters



class ByzantineProcess(Process):  # uses omit_vote and no_vote and not rho/sigma
    def voting(self, block, sigma):
        if self.target != block.proposer.group and not self.no_vote:  # byzantine
            block.initial_voters.append(self)

    def leader_vote_collection(self, committe_size, block_chain, rho):
        pre_block = block_chain[len(block_chain) - 2]
        all_removed = 0
        limit = (math.floor(committe_size/3)) - (committe_size - len(pre_block.initial_voters))  # should be len(committee)
        temp = sorted(pre_block.initial_voters, key=lambda v: v.total_reward, reverse=True)  # sorts list of init_voters by total_reward earned, descending
        r = random.randint(0, 100)
        if self.omit_vote:
            for voter in temp:
                if self.target != voter.group:
                    pre_block.signatures.append(voter)
                else:
                    if all_removed < limit:  # need to add in sorting of the list of voters based on stake
                        all_removed += 1
                        continue
                    else:
                        pre_block.signatures.append(voter)
        else:
            pre_block.signatures = pre_block.initial_voters
