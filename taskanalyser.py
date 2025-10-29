class Team:
    def __init__(self, code, name):
        self.code =code
        self.name = name
        self.member = []
    def add_member(self, member):
        self.member.append(member)
