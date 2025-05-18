class User:
    def __init__(self, username, email, password, balance=0):
        self.username = username
        self.email = email
        self.password = password
        self.balance = balance
        self.skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def update_balance(self, amount):
        self.balance += amount

    def __repr__(self):
        return f"User({self.username}, Skills: {len(self.skills)}, Balance: ${self.balance})"
