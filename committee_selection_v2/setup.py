import math
from reputation_calculations import committee_reputation, leader_reputation, choose_committee_random

# TODO: Edit explanation.md file


class Setup:
    def __init__(self, pool_size, committee_size, t_rounds, T, c=1, alpha=0, beta=10, rho=0, sigma=1):
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
        self.rho = rho  # prevalence of vote omission by leader
        self.sigma = sigma  # prevalence of no vote by validator

    def one_round(self):
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
            voters.voting(block, self.sigma)

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
