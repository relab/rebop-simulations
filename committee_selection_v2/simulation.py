import math
from timeit import default_timer as timer
# import random

# from committee import Committee
from process import Process, CorrectProcess, ColludingProcess, ByzantineProcess
from reputation_calculations import committee_reputation, leader_reputation, choose_leader_random, choose_committee_random


class Simulation:
    def __init__(self, pool_size, committee_size, t_rounds, T, c=1, alpha=0, beta=10, rho=0):
        self.pool_size = pool_size  # total number of processes committee is choosen from, pool size
        self.committee_size = committee_size
        self.total_rounds = t_rounds

        self.block_chain = []
        self.pool = []  # A list of all the processes that are part of the network, and the committee is selected from
        self.com_counter = 0
        self.reward_pool = 100

        self.T = T  # number of relevant rounds, last T number of rounds used to calculate reputation
        self.c = c  # Number of rounds before new committee is selected, feks c = 5, changed every fifth round

        self.H = 100
        self.alpha = alpha  # for leader rep.
        self.beta = beta  # for commmittee rep.
        self.rho = rho

    def one_round_v2(self):
        self.com_counter += 1
        leader = leader_reputation(self.pool, self.block_chain, self.committee_size, self.T, self.H, self.alpha)  # rep
        if self.com_counter % self.c == 0:
            if len(self.block_chain) > 1:
                committee = committee_reputation(self.pool, self.committee_size, self.block_chain, self.T, self.H,
                                                 self.beta)  # rep
            else:
                committee = choose_committee_random(self.committee_size, self.pool)
        else:
            if len(self.block_chain) > 1:
                committee = self.block_chain[-1].committee_at_block
            else:
                committee = choose_committee_random(self.committee_size, self.pool)

        block = leader.propose_block(self.block_chain)  # committee leader proposes block
        block.committee_at_block = committee

        for voters in committee:  # committee members vote
            voters.voting(block)

        if len(block.initial_voters) >= (2*math.floor(self.committee_size/3)):  # checking if the enough com. members voted
            self.block_chain.append(block)

        if len(self.block_chain) > 1:  # leader collects votes for h-1
            leader.leader_vote_collection(self.committee_size, self.block_chain, self.rho)

            self.distribute_reward()
            # looks always at h-1, rewrds all the voters on h-1,
            # and the leader of h earns a bonus for collecting the votes from h-1 and distributing the rewards to the
            # voters on h-1
        else:
            block.signatures = block.initial_voters  # automatically confirms votes for genesis block
        self.com_counter += 1  # used for setting unique committee id

    def one_round_rebop(self):  # leader reputation + random committee selection from pool, baseline
        leader = leader_reputation(self.pool, self.block_chain, self.committee_size, self.T, self.H, self.alpha)  # random leader
        committee = choose_committee_random(self.committee_size, self.pool)   # constant committee, original rebop

        block = leader.propose_block(self.block_chain)  # committee leader proposes block
        block.committee_at_block = committee

        for validator in committee:  # committee members vote
            if validator.id != leader.id:
                validator.voting(block)

        if len(block.initial_voters) >= (2*math.floor(self.committee_size/3)):  # checking if the enough com. members voted
            self.block_chain.append(block)

        if len(self.block_chain) > 1:  # leader collects votes for h-1
            leader.leader_vote_collection(self.committee_size, self.block_chain, self.rho)

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
    pool_size = int(corect_processes + colluding_processes)
    committee_size = int(pool_size / 2)
    rounds = 10000
    T = 1000
    c = 1
    rho = 1

    print(f"Rounds: 10.000\n"
          f"T: 1000\n"
          f"Correct: {corect_processes}\n"
          f"Colluding: {colluding_processes}\n"
          f"Pool Size: {pool_size}\n"
          f"Committee Size: {committee_size}")

    # Committe selection - Baseline, beta=0
    s1 = Simulation(pool_size, committee_size, rounds, T, c, 1, 0, rho)   # last 3: alpha, beta, rho
    for x in range(0, corect_processes):
        s1.pool.append(CorrectProcess(len(s1.pool), 1, 0))
    for x in range(0, colluding_processes):
        s1.pool.append(ColludingProcess(len(s1.pool), 2, 0))
    for r in range(s1.total_rounds):
        s1.one_round_v2()

    cor_group = []
    col_group = []
    for p in s1.pool:
        if type(p) is CorrectProcess:
            cor_group.append(p.total_reward)
        elif type(p) is ColludingProcess:
            col_group.append(p.total_reward)
    print(f"\nBaseline v1: alpha: {s1.alpha}, beta: {s1.beta}")

    print(f"Average reward among correct processes, 1 round: {(sum(cor_group)/(sum(cor_group) + sum(col_group))/corect_processes)}")
    print(f"Average reward among colluding processes, 1 round: "
          f"{(sum(col_group)/(sum(cor_group) + sum(col_group))/colluding_processes)}")


    # Committe selection alpha=0, beta 1
    s2 = Simulation(pool_size, committee_size, rounds, T, c, 0, 1, rho)   # last 3: alpha, beta, rho
    for x in range(0, corect_processes):
        s2.pool.append(CorrectProcess(len(s2.pool), 1, 0))
    for x in range(0, colluding_processes):
        s2.pool.append(ColludingProcess(len(s2.pool), 2, 0))
    for r in range(s2.total_rounds):
        s2.one_round_v2()

    cor_group = []
    col_group = []
    for p in s2.pool:
        if type(p) is CorrectProcess:
            cor_group.append(p.total_reward)
        elif type(p) is ColludingProcess:
            col_group.append(p.total_reward)
    print(f"\nCommittee selection v2: alpha: {s2.alpha}, beta: {s2.beta}")
    print(f"Average reward among correct processes, 1 round: {(sum(cor_group)/(sum(cor_group) + sum(col_group))/corect_processes)}")
    print(f"Average reward among colluding processes, 1 round: "
          f"{(sum(col_group)/(sum(cor_group) + sum(col_group))/colluding_processes)}")


    # Committe and leader selection, alpha=1, beta=1
    s3 = Simulation(pool_size, committee_size, rounds, T, c, 1, 1, rho)   # last 3: alpha, beta, rho
    for x in range(0, corect_processes):
        s3.pool.append(CorrectProcess(len(s3.pool), 1, 0))
    for x in range(0, colluding_processes):
        s3.pool.append(ColludingProcess(len(s3.pool), 2, 0))
    for r in range(s3.total_rounds):
        s3.one_round_v2()

    cor_group = []
    col_group = []
    for p in s3.pool:
        if type(p) is CorrectProcess:
            cor_group.append(p.total_reward)
        elif type(p) is ColludingProcess:
            col_group.append(p.total_reward)

    print(f"\nCommittee selection (v3): alpha: {s3.alpha}, beta: {s3.beta}")
    print(f"Average reward among correct processes, 1 round: {(sum(cor_group)/(sum(cor_group) + sum(col_group))/corect_processes)}")
    print(f"Average reward among colluding processes, 1 round: "
          f"{(sum(col_group)/(sum(cor_group) + sum(col_group))/colluding_processes)}")
    print()


 # Random Committe and leader selection, alpha=0, beta=0
    s4 = Simulation(pool_size, committee_size, rounds, T, c, 0, 0, rho)   # last 3: alpha, beta, rho
    for x in range(0, corect_processes):
        s4.pool.append(CorrectProcess(len(s4.pool), 1, 0))
    for x in range(0, colluding_processes):
        s4.pool.append(ColludingProcess(len(s4.pool), 2, 0))
    for r in range(s4.total_rounds):
        s4.one_round_v2()

    cor_group = []
    col_group = []
    for p in s4.pool:
        if type(p) is CorrectProcess:
            cor_group.append(p.total_reward)
        elif type(p) is ColludingProcess:
            col_group.append(p.total_reward)

    print(f"\nCommittee selection (v3): alpha: {s4.alpha}, beta: {s4.beta}")
    print(f"Average reward among correct processes, 1 round: {(sum(cor_group)/(sum(cor_group) + sum(col_group))/corect_processes)}")
    print(f"Average reward among colluding processes, 1 round: "
          f"{(sum(col_group)/(sum(cor_group) + sum(col_group))/colluding_processes)}")


    end = timer()
    print(f"\nExecution time: {(end - start)/60} minutes")



'''


    # Byzantine

    start_2 = timer()
    pool_size_2 = 100
    committee_size_2 = int(pool_size / 2)
    rounds_2 = 30000
    T_2 = 5000
    c_2 = 1
    rho_2 = 1

    print(f"Rounds: 30.000\n"
          f"T: 5000\n"
          f"Pool Size: {pool_size_2}\n"
          f"Committee Size: {committee_size_2}")

    # Byzantine 1 - alpha 1, beta 1
    s5 = Simulation(pool_size_2, committee_size_2, rounds_2, T_2, c_2, 1, 1, rho_2)   # last 3: alpha, beta, rho
    # 4 groups of correct processes
    for x in range(0, 16):
        s5.pool.append(CorrectProcess(len(s5.pool), 1, 0))
    for x in range(0, 1):
        s5.pool.append(CorrectProcess(len(s5.pool), 2, 0))
    for x in range(0, 3):
        s5.pool.append(CorrectProcess(len(s5.pool), 3, 0))
    for x in range(0, 8):
        s5.pool.append(CorrectProcess(len(s5.pool), 4, 0))

    # 3 Byzantine Groups with separate targets
    for x in range(0, 5):
        s5.pool.append(ByzantineProcess(len(s5.pool), 5, 2, False, True))
    for x in range(0, 10):
        s5.pool.append(ByzantineProcess(len(s5.pool), 6, 3, False, True))
    for x in range(0, 5):
        s5.pool.append(ByzantineProcess(len(s5.pool), 7, 4, False, True))


    for r in range(s5.total_rounds):
        s5.one_round_v2()

    cor_group_1 = []
    cor_group_2 = []
    cor_group_3 = []
    cor_group_4 = []
    byz_group_5 = []
    byz_group_6 = []
    byz_group_7 = []
    for p in s5.pool:
        if p.group == 1:
            cor_group_1.append(p.total_reward)
        elif p.group == 2:
            cor_group_2.append(p.total_reward)
        elif p.group == 3:
            cor_group_3.append(p.total_reward)
        elif p.group == 4:
            cor_group_4.append(p.total_reward)

        elif p.group == 5:
            byz_group_5.append(p.total_reward)
        elif p.group == 6:
            byz_group_6.append(p.total_reward)
        elif p.group == 7:
            byz_group_7.append(p.total_reward)

    all = sum(cor_group_1) + sum(cor_group_2) + sum(cor_group_3) + sum(cor_group_4)
    print(f"\nByzantine v1: alpha: {s5.alpha}, beta: {s5.beta}")

    print(f"Average reward among correct processes, 1 round: {(sum(cor_group)/(sum(cor_group) + sum(col_group))/corect_processes)}")
    print(f"Average reward among colluding processes, 1 round: "
          f"{(sum(col_group)/(sum(cor_group) + sum(col_group))/colluding_processes)}")




'''





'''
print(f"Committee selection (v2): After {s1.total_rounds} rounds")
    print("-------------")
    for p in s1.pool:
        print(p)
        

    all_rewards = 0
    for p in s1.pool:
        all_rewards += p.total_reward
    print(all_rewards/s1.total_rounds)
    print()

 # Baseline: rebop + random committee
    s2 = Simulation(pool_size, committee_size, rounds, T, 1)   # assume for now that new committee is selected for each
    # new round

    for x in range(0, corect_processes):
        s2.pool.append(CorrectProcess(len(s2.pool), 1, 0))
    for x in range(0, colluding_processes):
        s2.pool.append(ColludingProcess(len(s2.pool), 2, 0))

    for r in range(s2.total_rounds):
        s2.one_round_rebop()

    print(f"Rebop: After {s2.total_rounds} rounds")
    print("-------------")
    

    cor_group_2 = []
    col_group_2 = []
    for p in s2.pool:
        if type(p) is CorrectProcess:
            cor_group_2.append(p.total_reward)
        elif type(p) is ColludingProcess:
            col_group_2.append(p.total_reward)

    print()
    print(f"Rebop: After {s2.total_rounds} rounds, (T:{s2.T})")
    print(f"Average reward among correct processes, 1 round: {(sum(cor_group_2)/(sum(cor_group_2) + sum(col_group_2))/corect_processes)}")
    print(f"Average reward among colluding processes, 1 round: "
          f"{(sum(col_group_2)/(sum(cor_group_2) + sum(col_group_2))/colluding_processes)}")
    print()

'''
