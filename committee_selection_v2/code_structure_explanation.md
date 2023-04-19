This is a short text explaining the different part of the code:

4 main .py files:
simulation.py: where the simulation is run, has method one_round that runs like the flowchart

block.py: defines a block class, used to create indiviual blocks as block objects

process.py: defines an individual process, so every individ. process is an object of this class

reputation_calculation.py: holds functions that are used to create leaders and committees, either based
                           on reputation or random (used to test stuff). these functions take certain arguments and
                           return a committee (list of process objects), or a leader (individ. process object). these
                           functions are used by the one_round methods in simulation class

Simulation class in simulation.py:
2 main methods: one_round() and distribute_reward()

one_round:
there are 2 different versions but only two are relevant one_round_rebop which is my version of arians original
simulation
of rebop and one_round_v2 which includes selection of committee based on reputation. They both use the leader_reputation
 function to select a leader based on reputation but they differ on how they choose the committee. the origininal rebop
 has a constant committee and the v2 has committee selction based on reputation.

logic of one_round methods:
1. leader is selceted from pool/committee
2. committee is selceted (for v2), (as a list of processes)
3. leader proposes a new block h
4. the new committee are saved in the block (h), through the committee_at_block variable of the block object
5. the committee members vote on the block (h), for each voter the votes method in process.py is called, and their votes
 are added to the initial_votes list in the block object. this variable is used to save all the votes cast by the comm.memb.
6. if atleast 2/3 of the committe has voted, the block (h) is appended to the blockchain
7. then current leader handles/validates the votes cast on block h-1, the validating/omission of votes happens in the
leader_vote_collection method in process.py. all the votes he decides to validate (not omit) will be appended to the
list of signatures in the block (h-1). so if the leader omits votes because he is of type "colluding" or "byzantine", the
signatures list will be shorter/smaller than the list of initial votes, the differences are the omissions.
8. then in the end the rewards are distributed for block h-1, the rewarding is based on the signatures and not on the
list of initial_voters. the voters recorded in signatures get their portion of the reward pool, (100 by default) and the
 leader gets his bonus

reputation_calculation.py

the calculation for leader reputation is done in the leader_reputation function, it takes in the pool of processes among
other things, and return a leader (process object) works the same as arians original rebop

the calculation/selection of committee members based on reputation is done by the committee_reputation function. It also
takes in a pool of processes (a list) among other things, and return a committee chosen based on reputation (a list)
the reputation for committee selection is calculated based on how often he votes when he has had the chance in the last
T rounds, a percentage. feks .9 means he voted 9 out of 10 possible times.



Simple Simulation:

Rounds: 10.000
T: 1000
Correct: 17
Colluding: 3
Pool Size: 20
Committee Size: 10

Baseline v1: alpha: 1, beta: 0
Average reward among correct processes, 1 round: 0.05405159919308808
Average reward among colluding processes, 1 round: 0.027040937905834197

Committee selection v2: alpha: 0, beta: 1
Average reward among correct processes, 1 round: 0.05517511423900382
Average reward among colluding processes, 1 round: 0.020674352645645044

Committee selection (v3): alpha: 1, beta: 1
Average reward among correct processes, 1 round: 0.056605567186036945
Average reward among colluding processes, 1 round: 0.012568452612457327


Committee selection (v3): alpha: 0, beta: 0
Average reward among correct processes, 1 round: 0.05303834594032522
Average reward among colluding processes, 1 round: 0.03278270633815707

Execution time: 0.83709778 minutes


Sim 2

Rounds: 10.000
T: 1000
Correct: 17
Colluding: 3
Pool Size: 20
Committee Size: 10

Baseline v1: alpha: 1, beta: 0
Average reward among correct processes, 1 round: 0.05401001173435555
Average reward among colluding processes, 1 round: 0.027276600171985212

Committee selection v2: alpha: 0, beta: 1
Average reward among correct processes, 1 round: 0.05523126675746138
Average reward among colluding processes, 1 round: 0.02035615504105218

Committee selection (v3): alpha: 1, beta: 1
Average reward among correct processes, 1 round: 0.05626814293185125
Average reward among colluding processes, 1 round: 0.014480523386176239


Committee selection (v3): alpha: 0, beta: 0
Average reward among correct processes, 1 round: 0.05296098059408005
Average reward among colluding processes, 1 round: 0.03322110996687969

Execution time: 0.86805053 minutes


Sim 4:

Rounds: 30.000
T: 5000
Correct: 17
Colluding: 3
Pool Size: 20
Committee Size: 10

Baseline v1: alpha: 1, beta: 0
Average reward among correct processes, 1 round: 0.05402479743263131
Average reward among colluding processes, 1 round: 0.02719281454842258

Committee selection v2: alpha: 0, beta: 1
Average reward among correct processes, 1 round: 0.05499782503445033
Average reward among colluding processes, 1 round: 0.02167899147144813

Committee selection (v3): alpha: 1, beta: 1
Average reward among correct processes, 1 round: 0.056635115202193644
Average reward among colluding processes, 1 round: 0.012401013854236004

Committee selection (v3): alpha: 0, beta: 0
Average reward among correct processes, 1 round: 0.05296088382499414
Average reward among colluding processes, 1 round: 0.033221658325033175

Execution time: 12.290314305 minutes



Sim 5:

Rounds: 10000
T: 1000
Correct: 17
Colluding: 3
Pool Size: 20
Committee Size: 10
Alpha: 1
Beta: 1
Number of simulation: 25


Correct Processes:
rho(om), sigma(nv) : reward
(0.0, 0.0)  :  0.049998277138638234
(0.0, 0.25)  :  0.051492081758973976
(0.0, 0.5)  :  0.05281440731330255
(0.0, 0.75)  :  0.054224723526107396
(0.0, 1)  :  0.055430530825969465
(0.25, 0.0)  :  0.04991967784213394
(0.25, 0.25)  :  0.051454914287836225
(0.25, 0.5)  :  0.0528230916551261
(0.25, 0.75)  :  0.054437020777352255
(0.25, 1)  :  0.055666044128755886
(0.5, 0.0)  :  0.049889102555713744
(0.5, 0.25)  :  0.051499214213804996
(0.5, 0.5)  :  0.053208997926158706
(0.5, 0.75)  :  0.054611212310595666
(0.5, 1)  :  0.0556814295986532
(0.75, 0.0)  :  0.05003881740715087
(0.75, 0.25)  :  0.05176837545032347
(0.75, 0.5)  :  0.053307190417169324
(0.75, 0.75)  :  0.05458758716563485
(0.75, 1)  :  0.05596498025152649
(1, 0.0)  :  0.050217146564596436
(1, 0.25)  :  0.05208134080937327
(1, 0.5)  :  0.05354829867407174
(1, 0.75)  :  0.05489065215005674
(1, 1)  :  0.056474641728545216

Colluding Processes:
rho(om), sigma(nv) : reward
(0.0, 0.0)  :  0.05000976288105
(0.0, 0.25)  :  0.04154487003248075
(0.0, 0.5)  :  0.034051691891285554
(0.0, 0.75)  :  0.02605990001872475
(0.0, 1)  :  0.01922699198617304
(0.25, 0.0)  :  0.050455158894574303
(0.25, 0.25)  :  0.0417554857022614
(0.25, 0.5)  :  0.034002480620952104
(0.25, 0.75)  :  0.024856882261670574
(0.25, 1)  :  0.017892416603716644
(0.5, 0.0)  :  0.05062841885095545
(0.5, 0.25)  :  0.041504452788438374
(0.5, 0.5)  :  0.03181567841843399
(0.5, 0.75)  :  0.023869796906624597
(0.5, 1)  :  0.01780523227429853
(0.75, 0.0)  :  0.04978003469281175
(0.75, 0.25)  :  0.039979205781500333
(0.75, 0.5)  :  0.03125925430270717
(0.75, 0.75)  :  0.024003672728069164
(0.75, 1)  :  0.016198445241349873
(1, 0.0)  :  0.04876950280062022
(1, 0.25)  :  0.03820573541355146
(1, 0.5)  :  0.029892974180260184
(1, 0.75)  :  0.02228630448301183
(1, 1)  :  0.013310363538243816

Execution time: 5.593584471666666 minutes


Process finished with exit code 0











