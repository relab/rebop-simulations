class Block:
    def __init__(self, id, content, proposer):
        self.id = id  # Unique id for each block
        self.content = content #Some random number as block content
        self.initial_voters = [] #List of validators who sign the block
        self.signatures = []
        self.numberOfSignatures = 0 #Number of initial_voters
        self.proposer = proposer # id of Proposer/leader who proposed the block
        self.committee_at_block = None  # committe that was assigned to vote on block, dict with vote/not_vote? list
        # for now
        self.exNum = 0  # Number of validators who signed the block, but got excluded, have to think more about how
                        # to find these, how to distinguish between all initial_voters, and those who got their votes excluded

    def isValid(self):
        return True

    def is_confirmed(self, size):
        if len(self.signatures) > (2 * (size / 3)):
            return True
        return False
