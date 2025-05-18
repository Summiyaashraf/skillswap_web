import streamlit as st
import json
import os

class TransactionManager:
    def __init__(self, buyer):
        self.buyer = buyer
        self.transactions = self.load_transactions()

    def load_transactions(self):
        if os.path.exists("transactions.json"):
            with open("transactions.json", "r") as f:
                transactions = json.load(f)
            return transactions
        return []

    def get_user_transactions(self):
        user_transactions = []
        for transaction in self.transactions:
            if transaction["buyer"] == self.buyer:
                user_transactions.append(transaction)
        return user_transactions

    def display_transactions(self):
        user_transactions = self.get_user_transactions()

        if user_transactions:
            st.subheader(f"Your Transaction History")
            for transaction in user_transactions:
                st.write(f"📅 Date: {transaction['date']}")
                st.write(f"💸 Provider: {transaction['provider']}")
                st.write(f"💡 Skill: {transaction['skill']}")
                st.write(f"💰 Price: Rs.{transaction['price']}")
                st.write("---")
        else:
            st.write("You have no transactions yet.")


# Streamlit page to display transaction history:
def run_transaction_page():
    st.title("🧾 Transaction History")

    if "username" in st.session_state:
        buyer = st.session_state["username"]
        tm = TransactionManager(buyer)
        tm.display_transactions()
    else:
        st.warning("Please login to view your transaction history.")
