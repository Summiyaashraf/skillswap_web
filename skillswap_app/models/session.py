class Session:
    def __init__(self, skill, buyer, seller):
        self.skill = skill
        self.buyer = buyer
        self.seller = seller
        self.status = "Pending"

    def complete(self):
        self.status = "Completed"

    def __repr__(self):
        return f"{self.skill.name} | Buyer: {self.buyer.username}, Seller: {self.seller.username}, Status: {self.status}"
