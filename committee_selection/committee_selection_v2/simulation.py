import math
import random

from committee import Committee
from process import Process


class Simulation: # Todo: take in rep calc from somewhere else, take function as argument/param
    def __init__(self, pool_size, committe_size, t_rounds=1, t=1, c=0, alpha=1, rho=0):
        self.pool_size = pool_size # total number of processes committe is choosen from, pool size
        self.committee_size = committe_size
        self.total_rounds = t_rounds

        self.block_chain = []
        self.pool = [] # A list of all the processes that are part of the network, and the committe is selected from
        self.com_counter = 0
        self.reward_pool = 100

        self.T = t  # number of relevant rounds, last T number of rounds used to calculate reputation
        self.c = c  # Number of rounds before new committe is selected

        self.H = 100
        self.alpha = alpha
        self.rho = rho

        # pool is populated
        for x in range(0, self.pool_size):
            self.pool.append(Process(len(self.pool), 1, 1, 0))

    def committee_reputation(self):
        for p in self.pool:
            p.comm_rep = 1
            p.voting_opportunities = 0
            p.voted = 0

        for i in range(len(self.block_chain)-1, len(self.block_chain) - self.T, -1):  # TODO: -1 or -2????
            if i < 0:
                break
            for com_member in self.block_chain[i].committee_at_block:
                if com_member in self.block_chain[i].signatures:
                    com_member.voting_opportunities += 1
                    com_member.voted += 1
                else:
                    com_member.voting_opportunities += 1
            for p in self.pool:
                p.comm_rep = (p.voted/p.voting_opportunities)  # * self.H,

            reputation = [p.comm_rep*self.H for p in self.pool]
            committee = random.choices(self.pool, weights=reputation, k=100)
            return committee

    def leader_reputation(self): # TODO: dynamic, take it outside, and it make this a param/argument in another func
        for p in self.pool:
            p.lead_rep = 1
            p.proposer_count = 0
        for i in range(len(self.block_chain)-2, len(self.block_chain) - self.T, -1):
            if i < 0:
                break
            l_rep = ((len(self.block_chain[i].signatures) / self.committee_size) - 0.66) / 0.34
            l_rep = l_rep**self.alpha
            self.block_chain[i+1].proposer.proposer_count += 1
            self.block_chain[i+1].proposer.lead_rep = (self.block_chain[i+1].proposer.lead_rep * self.block_chain[
                i+1].proposer.proposer_count-1 + l_rep) / self.block_chain[i+1].proposer.proposer_count
        reputations = [p.lead_rep*self.H for p in self.pool]
        r = random.choices(self.pool, weights=reputations, k=1)
        leader = r[0]
        return leader  # this leader is then put as leader

    def choose_leader_random(self):
        leader = random.choice(self.pool)
        return leader

    def choose_committee_random(self):
        new_committee = []
        while len(new_committee) < self.committee_size:
            potential_member = random.choice(self.pool)
            if potential_member in new_committee: # or (potential_member is self.leader):
                continue
            else:
                new_committee.append(potential_member)
        return new_committee

    
    def one_round(self):
        # leader = self.leader_reputation()  # rep
        # committee = self.committee_reputation()  # rep

        leader = self.choose_leader_random()  # random
        # committee = self.choose_committee_random()  # random

        committee = self.pool  # original rebop, so to not have changing committee
        # TODO: need to exclude leader from being in the committee.... think more about this. leader cannot vote on
        #  the block he proposed...

        com = Committee(self.com_counter, self.committee_size, leader, committee)

        block = com.leader.propose_block(self.block_chain)  # committee leader proposes block
        block.committee_at_block = com.committee

        for validator in com.committee:  # committee members vote
            validator.voting(block)

        if len(block.initial_voters) >= (2*math.floor(self.committee_size/3)):  # checking if the enough com. members voted
            self.block_chain.append(block)

        if len(self.block_chain) > 1:  # leader collects votes for h-1
            com.leader.leader_vote_collection(self.committee_size, self.block_chain)

            self.distribute_reward()
            # looks always at h-1, rewrds all the voters on h-1,
            # and the leader of h earns a bonus for collecting the votes from h-1 and distributing the rewards to the
            # voters on h-1
        else:
            block.signatures = block.initial_voters  # automatically confirms votes for genesis block
        self.com_counter += 1  # used for setting unique committee id


    def distribute_reward(self):  # takes in whole blockchain
        pre_block = self.block_chain[len(self.block_chain) - 1]  # block h-1
        for validators in pre_block.signatures:  # voter reward
            validators.total_reward += self.reward_pool/(len(pre_block.signatures))
        self.block_chain[-1].proposer.total_reward += ((self.reward_pool*5)/100)
        # proposer of last element h, earns bonus for collecting/validating votes for block h-1


if __name__ == '__main__':
    s1 = Simulation(10, 10, 100000)   # assume for now that new committee is selected for each new round
    for r in range(s1.total_rounds):
        s1.one_round()
    print(f"After {s1.total_rounds} rounds")
    print("-------------")
    for p in s1.pool:
        print(p)
