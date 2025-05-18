class Skill:
    def __init__(self, name, description, price, owner):
        self.name = name
        self.description = description
        self.price = price
        self.owner = owner

    def update_price(self, new_price):
        self.price = new_price

    def get_info(self):
        return f"{self.name} by {self.owner}: {self.description} - Rs {self.price}"
