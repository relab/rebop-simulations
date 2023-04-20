from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy as np
from simulation_setup.setup import Setup
from simulation_setup.process import CorrectProcess, ColludingProcess

# TODO: find a solution for rho vs omit_vite and sigma vs no_vote, in process.py


def collusion_simulation(corect_processes, colluding_processes, pool_size, committee_size, rounds, T, c, alpha,
                         beta, rho, sigma):
    sim = Setup(pool_size, committee_size, rounds, T, c, alpha, beta, rho, sigma)  # last 4: alpha, beta, rho
    for x in range(0, corect_processes):
        sim.pool.append(CorrectProcess(len(sim.pool), 1, 0))
    for x in range(0, colluding_processes):
        sim.pool.append(ColludingProcess(len(sim.pool), 2, 0))
    for r in range(sim.total_rounds):
        sim.one_round()

    cor_group = []
    col_group = []
    for p in sim.pool:
        if type(p) is CorrectProcess:
            cor_group.append(p.total_reward)
        elif type(p) is ColludingProcess:
            col_group.append(p.total_reward)

    avg_corr_reward = sum(cor_group)/(sum(cor_group) + sum(col_group))/corect_processes  # avg. reward of 1 corr process
    avg_coll_reward = sum(col_group)/(sum(cor_group) + sum(col_group))/colluding_processes

    return avg_corr_reward, avg_coll_reward


def culloding_sim_set(alpha, beta):
    start = timer()
    corect_processes = 17
    colluding_processes = 3
    pool_size = int(corect_processes + colluding_processes)
    committee_size = int(pool_size / 2)
    rounds = 10000
    T = 1000
    c = 1

    rho_interval = [0.0, 0.25, 0.50, 0.75, 1]
    sigma_interval = [0.0, 0.25, 0.50, 0.75, 1]
    # alpha = 1
    # beta = 1

    print(f"Rounds: {rounds}\n"
          f"T: {T}\n"
          f"Correct: {corect_processes}\n"
          f"Colluding: {colluding_processes}\n"
          f"Pool Size: {pool_size}\n"
          f"Committee Size: {committee_size}\n"
          # f"Alpha: {alpha}\n"
          # f"Beta: {beta}\n"
          f"Number of simulation: {len(rho_interval)*len(sigma_interval)}")

    corr_reward_fractions = {}
    coll_reward_fractions = {}
    parameters = []

    for rho in rho_interval:
        for sigma in sigma_interval:
            corr, coll = collusion_simulation(corect_processes, colluding_processes, pool_size, committee_size, rounds,
                                              T, c, alpha, beta, rho, sigma)
            param_tuple = (rho, sigma)
            parameters.append(param_tuple)
            corr_reward_fractions[param_tuple] = corr
            coll_reward_fractions[param_tuple] = coll

    print(f"Correct Processes:\n"
          f"rho(om), sigma(nv) : reward")
    for key, value in corr_reward_fractions.items():
        print(key, " : ", value)

    print(f"Colluding Processes:\n"
          f"rho(om), sigma(nv) : reward")
    for key, value in coll_reward_fractions.items():
        print(key, " : ", value)


    end = timer()
    print(f"\nExecution time: {(end - start)/60} minutes\n")

    # plot_rewards(coll_reward_fractions)


def plot_rewards(reward_dict):
    rho = []
    sigma = []
    reward_list = []
    for key in reward_dict.keys():
        rho.append(key[0])
        sigma.append(key[1])
    for values in reward_dict.values():
        reward_list.append(values)
    x_sigma = np.array(sigma)
    y_rho = np.array(rho)
    y_reward = np.array(reward_list)

    plt.plot(x_sigma, y_reward, marker = 'o')
    plt.show()



if __name__ == '__main__':
    print(f"Alpha: {1}, Beta: {0}")  # rebop - baseline
    culloding_sim_set(2, 0) # alpha, beta

    print(f"Alpha: {2}, Beta: {0}")
    culloding_sim_set(2, 0) # alpha, beta

    print(f"Alpha: {2}, Beta: {1}")
    culloding_sim_set(2, 1) # alpha, beta

    print(f"Alpha: {4}, Beta: {2}")
    culloding_sim_set(2, 0) # alpha, beta
































    '''
    reward_dict = {
        (0.0, 0.0)  :  0.05000976288105,
        (0.0, 0.25)  :  0.04154487003248075,
        (0.0, 0.5)  :  0.034051691891285554,
        (0.0, 0.75)  :  0.02605990001872475,
        (0.0, 1)  :  0.01922699198617304,
        (0.25, 0.0)  :  0.050455158894574303,
        (0.25, 0.25)  :  0.0417554857022614,
        (0.25, 0.5)  :  0.034002480620952104,
        (0.25, 0.75)  :  0.024856882261670574,
        (0.25, 1)  :  0.017892416603716644,
        (0.5, 0.0)  :  0.05062841885095545,
        (0.5, 0.25)  :  0.041504452788438374,
        (0.5, 0.5)  :  0.03181567841843399,
        (0.5, 0.75)  :  0.023869796906624597,
        (0.5, 1)  :  0.01780523227429853,
        (0.75, 0.0)  :  0.04978003469281175,
        (0.75, 0.25)  :  0.039979205781500333,
        (0.75, 0.5)  :  0.03125925430270717,
        (0.75, 0.75)  :  0.024003672728069164,
        (0.75, 1)  :  0.016198445241349873,
        (1, 0.0)  :  0.04876950280062022,
        (1, 0.25)  :  0.03820573541355146,
        (1, 0.5)  :  0.029892974180260184,
        (1, 0.75)  :  0.02228630448301183,
        (1, 1)  :  0.013310363538243816,
    }
    plot_rewards(reward_dict)
    '''

