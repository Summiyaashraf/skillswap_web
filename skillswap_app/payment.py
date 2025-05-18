import streamlit as st
import json
import os
from datetime import datetime
import stripe

# 🔐 Use your test secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  

class PaymentManager:
    def __init__(self, skill, provider, price):
        self.skill = skill
        self.provider = provider
        self.price = int(price) * 100  # Stripe uses paisa, not rupees
        self.buyer = st.session_state.get("username")

    def process_payment(self):
        if not self.buyer:
            st.error("You must be logged in to purchase.")
            return False

        st.subheader("💳 Enter Card Details")
        card_number = st.text_input("Card Number", placeholder="4242 4242 4242 4242")
        exp_month = st.text_input("Expiry Month", placeholder="MM")
        exp_year = st.text_input("Expiry Year", placeholder="YYYY")
        cvc = st.text_input("CVC", placeholder="123")

        if st.button(f"Pay Rs.{self.price // 100}"):
            try:
                # 1. Create a Payment Method
                payment_method = stripe.PaymentMethod.create(
                    type="card",
                    card={
                        "number": card_number,
                        "exp_month": exp_month,
                        "exp_year": exp_year,
                        "cvc": cvc,
                    },
                )

                # 2. Create a Payment Intent
                payment_intent = stripe.PaymentIntent.create(
                    amount=self.price,
                    currency="inr",  # or "usd" for dollars
                    payment_method=payment_method.id,
                    confirm=True,
                )

                self.save_transaction()
                st.success("🎉 Payment Successful!")
                return True

            except stripe.error.CardError as e:
                st.error(f"Payment failed: {e.user_message}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

        return False

    def save_transaction(self):
        transaction = {
            "buyer": self.buyer,
            "provider": self.provider,
            "skill": self.skill,
            "price": self.price // 100,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        transactions = []
        if os.path.exists("transactions.json"):
            with open("transactions.json", "r") as f:
                transactions = json.load(f)

        transactions.append(transaction)

        with open("transactions.json", "w") as f:
            json.dump(transactions, f, indent=4)

# Streamlit page usage example:
def run_payment_page():
    st.title("🛒 Buy a Skill")

    with open("skills.json", "r") as f:
        skills = json.load(f)

    for skill in skills:
        with st.expander(f"🎯 {skill['title']} - Rs.{skill['price']}"):
            st.write(skill["description"])
            st.write(f"👩‍🏫 Provided by: **{skill['provider']}**")

            if "username" in st.session_state and st.session_state["username"] != skill["provider"]:
                pm = PaymentManager(skill["title"], skill["provider"], skill["price"])
                pm.process_payment()
            else:
                st.info("You can't buy your own skill.")
