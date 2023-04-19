from timeit import default_timer as timer
from setup import Setup
from process import CorrectProcess, ColludingProcess, ByzantineProcess

# TODO: Edit explanation file

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

def main():
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
    alpha = 1
    beta = 1

    print(f"Rounds: {rounds}\n"
          f"T: {T}\n"
          f"Correct: {corect_processes}\n"
          f"Colluding: {colluding_processes}\n"
          f"Pool Size: {pool_size}\n"
          f"Committee Size: {committee_size}\n"
          f"Alpha: {alpha}\n"
          f"Beta: {beta}\n"
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


if __name__ == '__main__':
    main()
