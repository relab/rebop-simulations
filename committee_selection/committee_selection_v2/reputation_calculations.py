


def committee_reputation(self):
    for p in self.pool:
        p.comm_rep = 1
        p.voting_opportunities = 0
        p.voted = 0

    for i in range(len(self.block_chain)-1, len(self.block_chain) - self.T, -1):  # TODO: -1 or -2????
        if i < 0:
            break
        for com_member in self.block_chain[i].committee_at_block:
            if com_member in self.block_chain[i].signatures:
                com_member.voting_opportunities += 1
                com_member.voted += 1
            else:
                com_member.voting_opportunities += 1
        for p in self.pool:
            p.comm_rep = (p.voted/p.voting_opportunities)  # * self.H,

        reputation = [p.comm_rep*self.H for p in self.pool]
        committee = random.choices(self.pool, weights=reputation, k=100)
        return committee


def leader_reputation(self): # TODO: dynamic, take it outside, and it make this a param/argument in another func
    for p in self.pool:
        p.lead_rep = 1
        p.proposer_count = 0
    for i in range(len(self.block_chain)-2, len(self.block_chain) - self.T, -1):
        if i < 0:
            break
        l_rep = ((len(self.block_chain[i].signatures) / self.committee_size) - 0.66) / 0.34
        l_rep = l_rep**self.alpha
        self.block_chain[i+1].proposer.proposer_count += 1
        self.block_chain[i+1].proposer.lead_rep = (self.block_chain[i+1].proposer.lead_rep * self.block_chain[
            i+1].proposer.proposer_count-1 + l_rep) / self.block_chain[i+1].proposer.proposer_count
    reputations = [p.lead_rep*self.H for p in self.pool]
    r = random.choices(self.pool, weights=reputations, k=1)
    leader = r[0]
    return leader  # this leader is then put as leader


def choose_leader_random(self):
    leader = random.choice(self.pool)
    return leader


def choose_committee_random(self):
    new_committee = []
    while len(new_committee) < self.committee_size:
        potential_member = random.choice(self.pool)
        if potential_member in new_committee: # or (potential_member is self.leader):
            continue
        else:
            new_committee.append(potential_member)
    return new_committee
