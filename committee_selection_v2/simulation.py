import math
from timeit import default_timer as timer
# import random

# from committee import Committee
from process import Process
from reputation_calculations import committee_reputation, leader_reputation, choose_leader_random, choose_committee_random


class Simulation:
    def __init__(self, pool_size, committee_size, t_rounds, T, c=0, alpha=1, beta=1, rho=0):
        self.pool_size = pool_size  # total number of processes committee is choosen from, pool size
        self.committee_size = committee_size
        self.total_rounds = t_rounds

        self.block_chain = []
        self.pool = []  # A list of all the processes that are part of the network, and the committee is selected from
        self.com_counter = 0
        self.reward_pool = 100

        self.T = T  # number of relevant rounds, last T number of rounds used to calculate reputation
        # self.c = c  # Number of rounds before new committee is selected, 

        self.H = 100
        self.alpha = alpha  # for leader rep.
        self.beta = beta  # for commmittee rep.
        self.rho = rho

    def one_round_v2(self):
        leader = leader_reputation(self.pool, self.block_chain, self.committee_size, self.T, self.H, self.alpha)  # rep
        if len(self.block_chain) > 1:
            committee = committee_reputation(self.pool, self.committee_size, self.block_chain, self.T, self.H,
                                             self.beta)  # rep
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
        committee = choose_committee_random(self.committee_size, self.pool)   # constant committee, original rebop

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
    start = timer()
    corect_processes = 17
    colluding_processes = 3
    pool_siz = int(corect_processes + colluding_processes)
    committee_size = int(pool_siz/2)
    rounds = 10000
    T = 1000

    # Committe selection (v2)
    s1 = Simulation(pool_siz, committee_size, rounds, T)   # assume for now that new committee is selected for each new
    # round
    for x in range(0, corect_processes):
        s1.pool.append(Process(len(s1.pool), 1, 1, 0))
    for x in range(0, colluding_processes):
        s1.pool.append(Process(len(s1.pool), 2, 2, 0))
    for r in range(s1.total_rounds):
        s1.one_round_v2()
    '''    
    print(f"Committee selection (v2): After {s1.total_rounds} rounds")
    print("-------------")
    for p in s1.pool:
        print(p)
    all_rewards = 0
    for p in s1.pool:
        all_rewards += p.total_reward
    print(all_rewards/s1.total_rounds)
    print()'''

    cor_group = []
    col_group = []
    for p in s1.pool:
        if p.type == 1:
            cor_group.append(p.total_reward)
        elif p.type == 2:
            col_group.append(p.total_reward)
    print(f"Committee selection (v2): After {s1.total_rounds} rounds (T:{s1.T})")
    print(f"Correct: {corect_processes}\n"
          f"Colluding: {colluding_processes}\n"
          f"Pool Size: {pool_siz}\n"
          f"Committee Size: {committee_size}")
    print(f"Ideal average reward among processes, 1 round: {(s1.reward_pool+5/s1.pool_size)/(s1.reward_pool+5/pool_siz)}")
    print(f"Average reward among correct processes, 1 round: {((sum(cor_group)/len(cor_group))/s1.total_rounds)/(s1.reward_pool+5/pool_siz)}")
    print(f"Average reward among colluding processes, 1 round: {((sum(col_group)/len(col_group))/s1.total_rounds)/(s1.reward_pool+5/pool_siz)}")
    print()

    end = timer()
    print(f"Execution time: {(end - start)/60} minutes")

    # Rebop
    s2 = Simulation(pool_siz, committee_size, rounds, T)   # assume for now that new committee is selected for each new round

    for x in range(0, corect_processes):
        s2.pool.append(Process(len(s2.pool), 1, 1, 0))
    for x in range(0, colluding_processes):
        s2.pool.append(Process(len(s2.pool), 2, 2, 0))

    for r in range(s2.total_rounds):
        s2.one_round_rebop()

    '''print(f"Rebop: After {s2.total_rounds} rounds")
    print("-------------")
    for p in s2.pool:
        print(p)
    all_rewards = 0
    for p in s2.pool:
        all_rewards += p.total_reward
    print(all_rewards/s2.total_rounds)
    '''

    cor_group_2 = []
    col_group_2 = []
    for p in s2.pool:
        if p.type == 1:
            cor_group_2.append(p.total_reward)
        elif p.type == 2:
            col_group_2.append(p.total_reward)

    print(f"Rebop: After {s2.total_rounds} rounds, (T:{s2.T})")
    print(f"Correct: {corect_processes}\n"
          f"Colluding: {colluding_processes}\n"
          f"Pool Size: {pool_siz}\n"
          f"Committee Size: {committee_size}")
    print(f"Ideal average reward among processes, 1 round: {((s2.reward_pool+5)/s2.pool_size)/((s2.reward_pool+5)/pool_siz)}")
    print(f"Average reward among correct processes, 1 round: "
          f"{((sum(cor_group_2)/len(cor_group_2))/s2.total_rounds)/((s2.reward_pool+5)/pool_siz)}")
    print(f"Average reward among colluding processes, 1 round: "
          f"{((sum(col_group_2)/len(col_group_2))/s2.total_rounds)/((s2.reward_pool+5)/pool_siz)}")
    print()


    end = timer()
    print(f"Execution time: {(end - start)/60} minutes")


# Byzantine
