import math
# import random

# from committee import Committee
from process import Process
from reputation_calculations import committee_reputation, leader_reputation, choose_leader_random, choose_committee_random


class Simulation:
    def __init__(self, pool_size, committee_size, t_rounds=1, T=1, c=0, alpha=1, rho=0):
        self.pool_size = pool_size  # total number of processes committee is choosen from, pool size
        self.committee_size = committee_size
        self.total_rounds = t_rounds

        self.block_chain = []
        self.pool = []  # A list of all the processes that are part of the network, and the committee is selected from
        self.com_counter = 0
        self.reward_pool = 100

        self.T = T  # number of relevant rounds, last T number of rounds used to calculate reputation
        # self.c = c  # Number of rounds before new committee is selected

        self.H = 100
        self.alpha = alpha
        self.rho = rho

    def one_round_v2(self):
        leader = leader_reputation(self.pool, self.block_chain, self.committee_size, self.T, self.H, self.alpha)  # rep
        if len(self.block_chain) > 1:
            committee = committee_reputation(self.pool, self.committee_size, self.block_chain, self.T, self.H)  # rep
        else:
            committee = choose_committee_random(self.committee_size, self.pool)

        # committee = self.choose_committee_random()  # random

        block = leader.propose_block(self.block_chain)  # committee leader proposes block
        block.committee_at_block = committee

        for voters in committee:  # committee members vote
            voters.voting(block)

        if len(block.initial_voters) >= (2*math.floor(self.committee_size/3)):  # checking if the enough com. members voted
            self.block_chain.append(block)

        if len(self.block_chain) > 1:  # leader collects votes for h-1
            leader.leader_vote_collection(self.committee_size, self.block_chain)

            self.distribute_reward()
            # looks always at h-1, rewrds all the voters on h-1,
            # and the leader of h earns a bonus for collecting the votes from h-1 and distributing the rewards to the
            # voters on h-1
        else:
            block.signatures = block.initial_voters  # automatically confirms votes for genesis block
        self.com_counter += 1  # used for setting unique committee id

    def one_round_rebop(self):  # no reputation, no committee selection, used to test
        leader = leader_reputation(self.pool, self.block_chain, self.committee_size, self.T, self.H, self.alpha)  # random leader
        committee = self.pool  # constant committee, original rebop

        # com = Committee(self.com_counter, self.committee_size, leader, committee)

        block = leader.propose_block(self.block_chain)  # committee leader proposes block
        block.committee_at_block = committee

        for validator in committee:  # committee members vote
            if validator.id != leader.id:
                validator.voting(block)

        if len(block.initial_voters) >= (2*math.floor(self.committee_size/3)):  # checking if the enough com. members voted
            self.block_chain.append(block)

        if len(self.block_chain) > 1:  # leader collects votes for h-1
            leader.leader_vote_collection(self.committee_size, self.block_chain)

            self.distribute_reward()
            # looks always at h-1, rewrds all the voters on h-1,
            # and the leader of h earns a bonus for collecting the votes from h-1 and distributing the rewards to the
            # voters on h-1
        else:
            block.signatures = block.initial_voters  # automatically confirms votes for genesis block
        self.com_counter += 1  # used for setting unique committee id

    def one_round_random(self):  # no reputation, no committee selection, used to test
        leader = choose_leader_random(self.pool)  # random leader
        committee = self.pool  # constant committee, original rebop

        # com = Committee(self.com_counter, self.committee_size, leader, committee)

        block = leader.propose_block(self.block_chain)  # committee leader proposes block
        block.committee_at_block = committee

        for validator in committee:  # committee members vote
            if validator.id != leader.id:
                validator.voting(block)

        if len(block.initial_voters) >= (2*math.floor(self.committee_size/3)):  # checking if the enough com. members voted
            self.block_chain.append(block)

        if len(self.block_chain) > 1:  # leader collects votes for h-1
            leader.leader_vote_collection(self.committee_size, self.block_chain)

            self.distribute_reward()
            # looks always at h-1, rewrds all the voters on h-1,
            # and the leader of h earns a bonus for collecting the votes from h-1 and distributing the rewards to the
            # voters on h-1
        else:
            block.signatures = block.initial_voters  # automatically confirms votes for genesis block
        self.com_counter += 1  # used for setting unique committee id

    def distribute_reward(self):  # takes in whole blockchain
        pre_block = self.block_chain[len(self.block_chain) - 2]  # block h-1
        for validators in pre_block.signatures:  # voter reward
            validators.total_reward += self.reward_pool/(len(pre_block.signatures))
        self.block_chain[-1].proposer.total_reward += ((self.reward_pool*5)/100)
        # proposer of last element h, earns bonus for collecting/validating votes for block h-1


if __name__ == '__main__':

    # Committe selection (v2)
    s1 = Simulation(20, 10, 100000)   # assume for now that new committee is selected for each new round
    for x in range(0, 17):
        s1.pool.append(Process(len(s1.pool), 1, 1, 0))
    for x in range(0, 3):
        s1.pool.append(Process(len(s1.pool), 2, 2, 0))
    for r in range(s1.total_rounds):
        s1.one_round_v2()
    print(f"Committee selection (v2): After {s1.total_rounds} rounds")
    print("-------------")
    for p in s1.pool:
        print(p)
    all_rewards = 0
    for p in s1.pool:
        all_rewards += p.total_reward
    print(all_rewards/s1.total_rounds)
    print()



    # Rebop
    s2 = Simulation(20, 20, 100000)   # assume for now that new committee is selected for each new round

    for x in range(0, 17):
        s2.pool.append(Process(len(s2.pool), 1, 1, 0))
    for x in range(0, 3):
        s2.pool.append(Process(len(s2.pool), 2, 2, 0))

    for r in range(s1.total_rounds):
        s1.one_round_rebop()
    print(f"Rebop: After {s1.total_rounds} rounds")
    print("-------------")
    for p in s1.pool:
        print(p)
    all_rewards = 0
    for p in s1.pool:
        all_rewards += p.total_reward
    print(all_rewards/s1.total_rounds)

