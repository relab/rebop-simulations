import random


def committee_reputation(pool, block_chain, T, H):
    for p in pool:
        p.comm_rep = 1
        p.voting_opportunities = 0
        p.voted = 0
    for i in range((len(block_chain)-1), (len(block_chain) - T), -1):  # TODO: -1 or -2????
        if i < 0:
            break
        for com_member in block_chain[i].committee_at_block:
            if com_member in block_chain[i].signatures:
                com_member.voting_opportunities += 1
                com_member.voted += 1
            else:
                com_member.voting_opportunities += 1
        for p in pool:
            p.comm_rep = (p.voted/p.voting_opportunities)  # * self.H,

        reputation = [p.comm_rep*H for p in pool]
        committee = random.choices(pool, weights=reputation, k=100)
        return committee


def leader_reputation(pool, block_chain, committee_size, T, H, alpha):
    for p in pool:
        p.lead_rep = 1
        p.proposer_count = 0
    for i in range(len(block_chain)-2, len(block_chain) - T, -1):
        if i < 0:
            break
        l_rep = ((len(block_chain[i].signatures) / committee_size) - 0.66) / 0.34
        l_rep = l_rep**alpha
        block_chain[i+1].proposer.proposer_count += 1
        block_chain[i+1].proposer.lead_rep = (block_chain[i+1].proposer.lead_rep * block_chain[
            i+1].proposer.proposer_count-1 + l_rep) / block_chain[i+1].proposer.proposer_count
    reputations = [p.lead_rep*H for p in pool]
    r = random.choices(pool, weights=reputations, k=1)
    leader = r[0]
    return leader  # this leader is then put as leader


def choose_leader_random(pool):
    leader = random.choice(pool)
    return leader


def choose_committee_random(committee_size, pool):
    new_committee = []
    while len(new_committee) < committee_size:
        potential_member = random.choice(pool)
        if potential_member in new_committee: # or (potential_member is self.leader):
            continue
        else:
            new_committee.append(potential_member)
    return new_committee
