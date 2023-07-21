from timeit import default_timer as timer
from simulation_setup.process import CorrectProcess, ByzantineProcess
from simulation_setup.setup import Setup


def byzantine_simulation(alpha, beta):
    start = timer()
    pool_size = 52
    committee_size = int(pool_size / 2)
    rounds = 20000
    T = 3000
    c = 1  # default for byz
    rho = 1  # default for byz
    sigma = 1

    print(f"Rounds: {rounds}\n"
          f"T: {T}\n"
          f"Pool Size: {pool_size}\n"
          f"Committee Size: {committee_size}")

    byz_sim = Setup(pool_size, committee_size, rounds, T, c, alpha, beta, rho, sigma)   # last 4: alpha, beta, rho,
    # sigma

    # 6 groups of correct processes
    for x in range(0, 21):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 1, 0))  # rho/sigma = 1 som default
    for x in range(0, 5):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 2, 0, message_loss=0.05))  # 5% message loss
    for x in range(0, 1):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 3, 0))
    for x in range(0, 1):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 4, 0))
    for x in range(0, 1):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 5, 0))
    for x in range(0, 3):
        byz_sim.pool.append(CorrectProcess(len(byz_sim.pool), 6, 0))

    # 4 Byzantine Groups with separate targets
    for x in range(0, 5):
        byz_sim.pool.append(ByzantineProcess(len(byz_sim.pool), 7, 3, 0, 1))
    for x in range(0, 5):
        byz_sim.pool.append(ByzantineProcess(len(byz_sim.pool), 8, 4, 1, 0))
    for x in range(0, 5):
        byz_sim.pool.append(ByzantineProcess(len(byz_sim.pool), 9, 5, 1, 1))
    for x in range(0, 5):
        byz_sim.pool.append(ByzantineProcess(len(byz_sim.pool), 10, 6, 1, 0))


    for r in range(byz_sim.total_rounds):
        byz_sim.one_round()

    cor_group_1 = []
    cor_group_2 = []
    cor_group_3 = []
    cor_group_4 = []
    cor_group_5 = []
    cor_group_6 = []
    byz_group_7 = []
    byz_group_8 = []
    byz_group_9 = []
    byz_group_10 = []
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
            cor_group_5.append(p.total_reward)
        elif p.group == 6:
            cor_group_6.append(p.total_reward)

        elif p.group == 7:
            byz_group_7.append(p.total_reward)
        elif p.group == 8:
            byz_group_8.append(p.total_reward)
        elif p.group == 9:
            byz_group_9.append(p.total_reward)
        elif p.group == 10:
            byz_group_10.append(p.total_reward)

    sum_all = sum(cor_group_1) + sum(cor_group_2) + sum(cor_group_3) + sum(cor_group_4) + sum(cor_group_5) + sum(
        cor_group_6) + sum(byz_group_7) + sum(byz_group_8) + sum(byz_group_9) + sum(byz_group_10)

    print(f"\nByzantine: Alpha: {alpha}, Beta: {beta}")

    print(f"Ideal Avg. percentage of reward for a process:"
          f" {(sum_all/sum_all) / len(byz_sim.pool)}\n" )

    print(f"Avg. percentage of reward for correct process in gr. 1:"
          f" {(sum(cor_group_1)/sum_all) / len(cor_group_1)}" )
    print(f"Avg. percentage of reward for correct process in gr. 2:"
          f" {(sum(cor_group_2)/sum_all) / len(cor_group_2)}" )
    print(f"Avg. percentage of reward for correct process in gr. 3:"
          f" {(sum(cor_group_3)/sum_all) / len(cor_group_3)}" )
    print(f"Avg. percentage of reward for correct process in gr. 4:"
          f" {(sum(cor_group_4)/sum_all) / len(cor_group_4)}" )
    print(f"Avg. percentage of reward for correct process in gr.5:"
          f" {(sum(cor_group_5)/sum_all) / len(cor_group_5)}" )
    print(f"Avg. percentage of reward for correct process in gr. 6:"
          f" {(sum(cor_group_6)/sum_all) / len(cor_group_6)}" )

    print(f"Avg. percentage of reward for byzantine process in gr. 7:"
          f" {(sum(byz_group_7)/sum_all) / len(byz_group_7)}" )
    print(f"Avg. percentage of reward for byzantine process in gr. 8:"
          f" {(sum(byz_group_8)/sum_all) / len(byz_group_8)}" )
    print(f"Avg. percentage of reward for byzantine process in gr. 9:"
          f" {(sum(byz_group_9)/sum_all) / len(byz_group_9)}" )
    print(f"Avg. percentage of reward for byzantine process in gr. 10:"
          f" {(sum(byz_group_10)/sum_all) / len(byz_group_10)}" )


    end = timer()
    print(f"\nExecution time: {(end - start)/60} minutes\n")


if __name__ == '__main__':
    # byzantine_simulation(1, 0)
    # byzantine_simulation(2, 0)
    # byzantine_simulation(2, 1)
    # byzantine_simulation(4, 1)
    # byzantine_simulation(6, 2)
    # byzantine_simulation(10, 1)
    byzantine_simulation(10, 5)
    byzantine_simulation(15, 5)
    byzantine_simulation(15, 10)


