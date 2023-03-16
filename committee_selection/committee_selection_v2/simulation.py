from committee import Committee
from process import Process


class Simulation:
    def __init__(self, pool_size, committe_size, t_rounds=0, T=0, c=0, alpha=0, rho=0):
        self.pool_size = pool_size # total number of processes committe is choosen from, pool size
        self.committe_size = committe_size
        self.total_rounds = t_rounds

        self.block_chain = []
        self.pool = [] # A list of all the processes that are part of the network
        self.list_of_committees = []
        self.com_counter = 0

        self.T = T #number of rounds, last T number of rounds used to calculate reputation
        self.c = c # Number of rounds before new committe is selected

        self.H = 100
        self.alpha = alpha
        self.rho = rho

        # pool is populated
        for x in range(0, self.pool_size):
            self.pool.append(Process(len(self.pool), 1, 1, 0))

    def distribute_reward(self):
        pass

    def one_round(self): # assume for now that new committee is selected for each new round
        com = Committee(self.com_counter, self.committe_size, self.pool)
        # if len(self.block_chain) > 1:
        block = com.leader.propose_block(self.block_chain)
        for validator in com.committee:
            if validator.type == 1: # correct
                validator.correct_validator(block)

            elif validator.type == 2: # Colluding
                validator.colluding_validator(block)

            elif validator.type == 3: # byzantine
                pass

        if com.leader.type == 1:
            com.leader.correct_leader(block)
            if block.isConfirmed(self.committe_size):
                self.block_chain.append(block)

        elif com.leader.type == 2:
            com.leader.colluding_leader(block)


        elif com.leader.type == 3:
            pass


        self.com_counter += 1


if __name__ == '__main__':
    s1 = Simulation(200, 50)
    s1.one_round()
