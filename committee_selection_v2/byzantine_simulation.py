from timeit import default_timer as timer
from simulation_setup.process import CorrectProcess, ByzantineProcess
from simulation_setup.setup import Setup

# TODO: add message loss
# TODO: look at byz fraction vs ideal


def byzantine_simulation():
    start = timer()
    pool_size = 48
    committee_size = int(pool_size / 2)
    rounds = 10000
    T = 1000
    c = 1  # default for byz
    rho = 1  # default for byz

    print(f"Rounds: {rounds}\n"
          f"T: {T}\n"
          f"Pool Size: {pool_size}\n"
          f"Committee Size: {committee_size}")

    # Byzantine 1 - alpha 1, beta 1
    byz_sim = Setup(pool_size, committee_size, rounds, T, c, 1, 1, rho)   # last 4: alpha, beta, rho, sigma

    # 4 groups of correct processes
    for x in range(0, 16):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 1, 0))
    for x in range(0, 1):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 2, 0))
    for x in range(0, 3):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 3, 0))
    for x in range(0, 8):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 4, 0))

    # 3 Byzantine Groups with separate targets
    for x in range(0, 5):
        byz_sim.pool.append(ByzantineProcess(len(byz_sim.pool), 5, 2, False, True))
    for x in range(0, 10):
        byz_sim.pool.append(ByzantineProcess(len(byz_sim.pool), 6, 3, False, True))
    for x in range(0, 5):
        byz_sim.pool.append(ByzantineProcess(len(byz_sim.pool), 7, 4, False, True))


    for r in range(byz_sim.total_rounds):
        byz_sim.one_round()

    cor_group_1 = []
    cor_group_2 = []
    cor_group_3 = []
    cor_group_4 = []
    byz_group_5 = []
    byz_group_6 = []
    byz_group_7 = []
    for p in byz_sim.pool:
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

    sum_all = sum(cor_group_1) + sum(cor_group_2) + sum(cor_group_3) + sum(cor_group_4) + sum(byz_group_5) + sum(
        byz_group_6) + sum(byz_group_7)

    print(f"\nByzantine v1: alpha: {byz_sim.alpha}, beta: {byz_sim.beta}")

    print(f"Avg. reward for correct process in gr. 1:"
          f" {(sum(cor_group_1)/sum_all) / len(cor_group_1)}" )
    print(f"Avg. reward for correct process in gr. 2:"
          f" {(sum(cor_group_1)/sum_all) / len(cor_group_2)}" )
    print(f"Avg. reward for correct process in gr. 3:"
          f" {(sum(cor_group_1)/sum_all) / len(cor_group_3)}" )
    print(f"Avg. reward for correct process in gr. 4:"
          f" {(sum(cor_group_1)/sum_all) / len(cor_group_4)}" )
    print(f"Avg. reward for byzantine process in gr. 5:"
          f" {(sum(byz_group_5)/sum_all) / len(byz_group_5)}" )
    print(f"Avg. reward for byzantine process in gr. 6:"
          f" {(sum(byz_group_6)/sum_all) / len(byz_group_6)}" )
    print(f"Avg. reward for byzantine process in gr. 7:"
          f" {(sum(byz_group_7)/sum_all) / len(byz_group_7)}" )


    end = timer()
    print(f"\nExecution time: {(end - start)/60} minutes\n")


if __name__ == '__main__':
    byzantine_simulation()
