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

    sim_output = [avg_corr_reward, avg_coll_reward, alpha, beta, rho, sigma]
    # corect_processes, colluding_processes, pool_size, committee_size, rounds, T, C]

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

    sim_results = []  # a list holding multiple list, where each element in the sublist is a line of data
    sim_id = 0
    for sim in alpha_beta:

        one_sim = []
        for rho in rho_interval:
            for sigma in sigma_interval:
                one_sim.append(collusion_one_simulation(correct_processes, colluding_processes, pool_size, committee_size,
                                                            rounds, T, C, sim[0], sim[1], rho, sigma))
        for lines in one_sim:
            lines.insert(0, sim_id)
        sim_results.append(one_sim)
        sim_id += 1


    end = timer()
    print(f"\nExecution time: {(end - start)/60} minutes\n")

    # ouput a list of the infoprmation to be stored in csv file:
    # avg_corr_reward, avg_coll_reward, alpha, beta, rho, sigma, corect_processes, colluding_processes,
    # pool_size, committee_size, rounds, T, C


    return sim_results, int(len(sim_results))


# ikke relevant: TODO: tar inn data, sjekker om samme sim har blitt gjort tidligere hvis ja, appender ikke. hvis nei
# appender
def write_collusion_data(sim_results):
    collumn_names = [ "sim_id", "avg_corr_reward", "avg_coll_reward", "alpha", "beta", "rho", "sigma"]
                    #  "corect_processes","colluding_processes", "pool_size", "committee_size", "rounds", "T", "C"]

    with open("colluding_data.csv", "w", newline="") as csv_f:
        sim_writer = csv.writer(csv_f, delimiter=";")
        sim_writer.writerow(collumn_names)
        for sim in sim_results:
            sim_writer.writerows(sim)




def read_collusion_data(number_of_sims):
    sim_counter = 1
    with open("colluding_data.csv", "r") as csv_f:
        sim_reader = csv.reader(csv_f, delimiter=";")
        next(sim_reader) # skips the first line (header/collumn names)

        '''
        Now we have a csv file, where each line is sim with a unique combination of alpha, beta, rho, sigma.
        what we want is to take all the lines with the same alpha and beta and create a matrix out of them.
        so if there are 5 sets of alphas and betas --> 5 sets of data
        
        we write to file 1 sim at a time, so the 
        each line will be a list/string, like the one we wrote to the file
        so when writing to file we give eah line a sim_id, all the 
        
        
        we make a dict where alpha/beta is the key and  a list of the rest of the line as the values
        so the we have a dict with multipl lists as values, where each list is one intesrection between rho/sigma + 
        the two rewards
        so that when creating the matrix we can take one dict, take out the value (list of rho/sigma + rewards)
        '''
        sim_info = []
        data_list = [] # list: [[], [], []] when numberof sims is 3, so each sublist is for one sim
        for i in range(number_of_sims):
            data_list.append([])

        data = {}
        
        for row in sim_reader:
            id = row[0]
            list = data.get(id,[])
            
            colluding_delta = float(row[2]) - float(row[1])
            
            list.append({
              "rho": float(row[5]),
              "sigma": float(row[6]),
              "delta": colluding_delta
            })
            data[id]=list
        return data
        
        '''
        for row in sim_reader:
            alpha_beta = (row[3], row[4])
            colluding_delta = float(row[2]) - float(row[1])
            liste = [int(row[0]), alpha_beta, float(row[5]), float(row[6]), colluding_delta]
            data_list[int(row[0])].append(liste)
        return data_list 
        '''



def colluding_plot(data_list):
    fig, ax = plt.subplots()
    
    min_val, max_val = 0, 3

    intersection_matrix = np.random.randint(1, 2, size=(max_val,max_val))
    for point in data_list:
        i = int(point["rho"]*(max_val-1))
        j = int(point["sigma"]*(max_val-1))
        intersection_matrix[i,j] = point["delta"]
        ax.text(i, j, str(point["delta"])) # i=rho, j=sigma, c=verdien på det punktet
    
    
    print(intersection_matrix)

    ax.matshow(intersection_matrix)  # cmap=plt.cm.blues

    plt.show()
    
    '''
    ax.matshow(intersection_matrix)  # cmap=plt.cm.blues
  
    for i in range(0, len(data_list)):
        if data_list[i] is False:
            del data_list[i]

    # Three levels of lists:
    # data_list --> list holding data of one sim --> list containing one data point in a specific sim

    matrix_data = []
    for data in data_list[0]:
    '''



    '''
    To create the matrix plot with color i need:
    1. reward delta which is in the cells, sequence is based on rho:sigma
    
    rho as the rows and 
    sigma as the collumns 
    
    so if we put all of the  delta values of a specifi rho in a list --> one row 
    that way we will have a matrix where all of the rows are rho (left side), and number of elements
    in each of the lists as the number of collumns, 
    ax.text(i, j, str(c)) # i=rho, j=sigma, c=verdien på det punktet
     

    '''


def main():
    data = read_collusion_data(2)
    for exp in data:
      colluding_plot(data[exp])
  

if __name__ == '__main__':
    #colluding_sim, number_of_sims = complete_culloding_sim()
    #write_collusion_data(colluding_sim)
    print(read_collusion_data(10))






