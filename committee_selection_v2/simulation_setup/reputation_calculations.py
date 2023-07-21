import random


def committee_reputation(pool, committee_size, block_chain, T, H, beta):
    for p in pool:
        p.comm_rep = 1
        p.voting_opportunities = 0
        p.voted = 0
    start = len(block_chain)-2
    end = len(block_chain) - T
    for i in range(start, end, -1):
        if i < 0:
            break
        for com_member in block_chain[i].committee_at_block:
            com_member.voting_opportunities += 1
        for com_member in block_chain[i].signatures:
            com_member.voted += 1

    for p in pool:
        if p.voting_opportunities > 0:
            p.comm_rep = (p.voted/p.voting_opportunities)**beta  # * self.H,

    reputation = [p.comm_rep*H for p in pool]
    committee = random.choices(pool, weights=reputation, k=committee_size)
    return committee


def leader_reputation(pool, block_chain, committee_size, T, H, alpha):
    for p in pool:
        p.lead_rep = 1
        p.proposer_count = 0
    start = len(block_chain)-2
    end = len(block_chain) - T
    for i in range(start, end, -1):
        if i < 0:
            break
        l_rep = ((len(block_chain[i].signatures) / committee_size) - 0.66) / 0.34
        l_rep = l_rep**alpha
        block_chain[i+1].proposer.proposer_count += 1
        block_chain[i+1].proposer.lead_rep = ((block_chain[i+1].proposer.lead_rep * (block_chain[
            i+1].proposer.proposer_count-1) + l_rep)) / block_chain[i+1].proposer.proposer_count
    reputation = [p.lead_rep*H for p in pool]
    if sum(reputation) < 0:
        print(reputation)
    r = random.choices(pool, weights=reputation, k=1)
    leader = r[0]
    return leader  # put as leader


def choose_leader_random(pool):
    leader = random.choice(pool)
    return leader


def choose_committee_random(committee_size, pool):
    new_committee = []
    while len(new_committee) < committee_size:
        potential_member = random.choice(pool)
        if potential_member in new_committee:  # or (potential_member is self.leader):
            continue
        else:
            new_committee.append(potential_member)
    return new_committee
