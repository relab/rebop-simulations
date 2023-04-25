from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy as np
from simulation_setup.setup import Setup
from simulation_setup.process import CorrectProcess, ColludingProcess
import csv


def collusion_one_simulation(corect_processes, colluding_processes, pool_size, committee_size, rounds, T, C, alpha, beta,
                             rho, sigma):
    sim = Setup(pool_size, committee_size, rounds, T, C, alpha, beta, rho, sigma)
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

    sim_output = [avg_corr_reward, avg_coll_reward, alpha, beta, rho, sigma, corect_processes, colluding_processes,
                  pool_size, committee_size, rounds, T, C]

    return sim_output


def complete_culloding_sim():
    start = timer()
    correct_processes = 20
    colluding_processes = 6
    pool_size = int(correct_processes + colluding_processes)
    committee_size = int(pool_size / 2)
    rounds = 10000
    T = 1000
    C = 1

    rho_interval = [0.0, 0.5, 1.0]  # [0.0, 0.25, 0.50, 0.75, 1]
    sigma_interval = [0.0, 0.5, 1.0]  # [0.0, 0.25, 0.50, 0.75, 1]
    alpha_beta = [(1, 0), (2, 0)]  # [(1, 0), (2, 0), (2, 1), (4, 0), (10, 1)]

    sim_results = []
    for sim in alpha_beta:
        for rho in rho_interval:
            for sigma in sigma_interval:
                sim_results.append(collusion_one_simulation(correct_processes, colluding_processes, pool_size, committee_size,
                                                            rounds, T, C, sim[0], sim[1], rho, sigma))


    end = timer()
    print(f"\nExecution time: {(end - start)/60} minutes\n")

    # ouput a list of the infoprmation to be stored in csv file:
    # avg_corr_reward, avg_coll_reward, alpha, beta, rho, sigma, corect_processes, colluding_processes,
    # pool_size, committee_size, rounds, T, C

    return sim_results


# ikke relevant: TODO: tar inn data, sjekker om samme sim har blitt gjort tidligere hvis ja, appender ikke. hvis nei
# appender
def write_collusion_data(sim_ouput):
    collumn_names = ["avg_corr_reward", "avg_coll_reward","alpha", "beta", "rho", "sigma", "corect_processes",
                     "colluding_processes", "pool_size", "committee_size", "rounds", "T", "C"]

    with open("colluding_data.csv", "w", newline="") as csv_f:
        sim_writer = csv.writer(csv_f, delimiter=";")
        sim_writer.writerow(collumn_names)
        sim_writer.writerows(sim_ouput)



def read_collusion_data():
    with open("colluding_data.csv", "r") as csv_f:
        sim_reader = csv.reader(csv_f, delimiter=";")
        next(sim_reader) # skips the first line (header/collumn names)

        '''
        Now we have a csv file, where each line is sim with a unique combination of alpha, beta, rho, sigma.
        what we want is to take all the lines with the same alpha and beta and create a matrix out of them.
        so if there are 5 sets of alphas and betas --> 5 sets of data
        
        each line will be a list/string, like the one we wrote to the file
        we make a dict where alpha/beta is the key and  a list of the rest of the line as the values
        so the we have a dict with multipl lists as values, wehere each list is one intesrection between rho/sigma
        so that when creating the matrix we can take one dict
        '''




if __name__ == '__main__':
    colluding_sim = complete_culloding_sim()
    write_collusion_data(colluding_sim)
