import random



class Committee:
    def __init__(self, committee_id, committee_size: int, leader, committee: list):
        self.c_id = committee_id
        self. committee_size = committee_size

        self.committee = committee
        self.leader = leader


    # maybe put both methods in constructor/make them return/put them in  sim class?
    def choose_leader_random(self):
        self.leader = random.choice(self.pool)  # TODO: change this to be in line with new design

    def choose_committee_random(self):
        new_committee = []
        while len(new_committee) < self.committee_size:
            potential_member = random.choice(self.pool)  # TODO: change this to be in line with new design
            if (potential_member in new_committee) or (potential_member is self.leader):
                continue
            else:
                new_committee.append(potential_member)
        self.committee = new_committee


