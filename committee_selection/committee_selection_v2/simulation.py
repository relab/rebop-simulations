import random

from committee import Committee
from process import Process


class Simulation:
    def __init__(self, pool_size, committe_size, t_rounds=0, T=0, c=0, alpha=1, rho=0):
        self.pool_size = pool_size # total number of processes committe is choosen from, pool size
        self.committe_size = committe_size
        self.total_rounds = t_rounds

        self.block_chain = []
        self.pool = [] # A list of all the processes that are part of the network, and the committe is selected from
        self.com_counter = 0
        self.reward_pool = 100

        self.T = T  # number of relevant rounds, last T number of rounds used to calculate reputation
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
                if com_member in self.block_chain[i].signatures:  # TODO: signatures or initial votes...?
                    com_member.voting_opportunities += 1
                    com_member.voted += 1
                else:
                    com_member.voting_opportunities += 1
            for p in self.pool:
                p.comm_rep = (p.voted/p.voting_opportunities)  # * self.H,

            reputation = [p.comm_rep*self.H for p in self.pool]  # Todo: need to exclude current leader
            committee = random.choices(self.pool, weights=reputation, k=100)
            return committee

    def leader_reputation(self):
        for p in self.pool:
            p.lead_rep = 1
            p.proposer_count = 0
        for i in range(len(self.block_chain)-2, len(self.block_chain) - self.T, -1):
            if i < 0:
                break
            l_rep = ((len(self.block_chain[i].signatures)/self.committe_size) - 0.66) / 0.34
            l_rep = l_rep**self.alpha
            self.block_chain[i+1].proposer.proposer_count += 1
            self.block_chain[i+1].proposer.lead_rep = (self.block_chain[i+1].proposer.lead_rep * self.block_chain[
                i+1].proposer.proposer_count-1 + l_rep) / self.block_chain[i+1].proposer.proposer_count
        reputations = [p.lead_rep*self.H for p in self.pool]
        r = random.choices(self.pool, weights=reputations, k=1)
        leader = r[0]
        return leader  # this leader is then put as leader

    def distribute_reward(self, block, committee):
        for validator in block.signatures:
            validator.t_reward += self.reward_pool/(len(block.signatures))
        committee.leader.t_reward += ((self.reward_pool*5)/100)

    def one_round(self): # assume for now that new committee is selected for each new round
        com = Committee(self.com_counter, self.committe_size, self.pool)  # TODO: fiks committe class params
        com.choose_leader_random()
        com.choose_committee_random()
        block = com.leader.propose_block(self.block_chain)
        block.committee_at_block = com.committee

        for validator in com.committee:
            validator.voting(block)

        com.leader.leader_vote_collection(block, self.committe_size, self.block_chain)

        self.distribute_reward(block, com)
        self.com_counter += 1


if __name__ == '__main__':
    s1 = Simulation(200, 50)
    s1.one_round()
