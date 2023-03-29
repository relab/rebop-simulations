import random


class Committee:
    def __init__(self, committee_id, committee_size: int, leader, committee: list):
        self.c_id = committee_id
        self. committee_size = committee_size

        self.committee = committee
        self.leader = leader
