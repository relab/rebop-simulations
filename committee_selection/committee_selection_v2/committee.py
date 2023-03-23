import random


class Committee:
    def __init__(self, committee_id, committee_size, pool:list):
        self.c_id = committee_id
        self. committee_size = committee_size
        self.pool = pool

        self.committee = []
        self.leader = None


    def choose_committee_reputation(self):
        pass

    def choose_leader_reputation(self):
        pass

    # maybe put both methods in constructor/make them return/put them in  sim class?
    def choose_leader_random(self):
        old_leader = self.leader
        while self.leader is old_leader and self.leader not in self.committee:
            self.leader = random.choice(self.pool)

    def choose_committee_random(self):
        new_committee = []
        while len(new_committee) < self.committee_size:
            potential_member = random.choice(self.pool)
            if (potential_member in new_committee) or (potential_member is self.leader):
                continue
            else:
                new_committee.append(potential_member)
        self.committee = new_committee

