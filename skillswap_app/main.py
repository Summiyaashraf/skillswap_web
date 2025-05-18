import streamlit as st
import bcrypt
import sqlite3
import stripe
import os
from auth import signup_user, login_user
from database import create_user_table
from database import create_skill_table, add_skill_to_db, get_all_skills


# Create DB tables
create_user_table()

create_skill_table()


# Session variables initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_update_password' not in st.session_state:
    st.session_state.show_update_password = False

# Stripe API Key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY") 
# Page Config
st.set_page_config(page_title="SkillBarter", layout="wide")

# CSS Styling
st.markdown("""
    <style>
        .main {
            background-color: #ffffff;
            padding: 20px;
            font-family: 'Poppins', sans-serif;
        }
        h1, h2, h3 {
            color: #222;
        }
        div.stButton > button {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white;
            padding: 0.6em 2em;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background: #1d3b8b;
            color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Classes --------------------
class User:
    def __init__(self, username, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

class Skill:
    def __init__(self, title, description, price, provider_username):
        self.title = title
        self.description = description
        self.price = price
        self.provider_username = provider_username

class Session:
    def __init__(self, skill, buyer, provider):
        self.skill = skill
        self.buyer = buyer
        self.provider = provider

    def __str__(self):
        return f"{self.buyer.username} bought '{self.skill.title}' from {self.provider.username} for ${self.skill.price}"

class Database:
    def __init__(self):
        self.users = []
        self.skills = []
        self.sessions = []

    def add_user(self, user):
        self.users.append(user)

    def find_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def add_skill(self, skill):
        self.skills.append(skill)

    def list_skills(self):
        return self.skills

    def add_session(self, session):
        self.sessions.append(session)

# Initialize Database
db = Database()

# -------------------- Header --------------------
st.image("https://via.placeholder.com/150x80.png?text=SkillShare", width=200)
st.title("💼 SkillBarter - Sell & Buy Skills")

# -------------------- Login / Sign Up --------------------
if not st.session_state.logged_in:
    st.title("SkillSwap - Login or Signup")
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if not username or not password:
                st.warning("Please enter both username and password.")
            else:
                success = login_user(username, password)
                if success:
                    st.success(f"Welcome {username}!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

    elif choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            if not new_user or not new_pass:
                st.warning("Please fill in both username and password.")
            elif len(new_pass) < 6:
                st.warning("Password should be at least 6 characters long.")
            else:
                success, msg = signup_user(new_user, new_pass)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

# -------------------- Main App after Login --------------------
if st.session_state.get("logged_in", False):
    st.write(f"### 👋 Welcome to SkillSwap, {st.session_state.username}!")

    # Sidebar Navigation
    menu = ["Home", "List Skills", "Offer Skill", "Buy Skill", "My Sessions"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("You have been logged out.")
        st.rerun()

    # -------------------- Page Views --------------------
    if choice == "Home":
        st.header("👋 Welcome to SkillBarter!")
        st.markdown("""
        ### A place where you can offer and buy skills!
        - Create an account to start offering your talents.
        - Browse and purchase skills from others.
        - Track your learning sessions.
        """)
    
    elif choice == "List Skills":
        st.header("📜 Available Skills")
        skills = get_all_skills()
        if skills:
            for title, description, price, provider_username in skills:
                st.markdown(f"### {title}")
                st.write(f"{description}")
                st.write(f"💲 Price: ${price}")
                st.write(f"👤 Provider: {provider_username}")
                st.markdown("---")
        else:
            st.info("No skills listed yet.")

    elif choice == "Offer Skill":
        st.header("📤 Offer Your Skill")
        title = st.text_input("Skill Title")
        description = st.text_area("Skill Description")
        price = st.number_input("Price", min_value=1)
        if st.button("Add Skill"):
            if title and description and price:
                add_skill_to_db(title, description, price, st.session_state.username)
                st.success("Skill offered successfully!")
            else:
                st.warning("Please fill all fields.")

    elif choice == "Buy Skill":
        st.header("🛒 Buy a Skill")
        skills = get_all_skills()

        if skills:
            skills_available = [f"{title} by {provider_username}" for title, _, _, provider_username in skills]
            selected = st.selectbox("Select a Skill", skills_available)
            skill_title, provider_username = selected.split(" by ")

            selected_skill = next((s for s in skills if s[0] == skill_title and s[3] == provider_username), None)

            if selected_skill:
                title, description, price, provider = selected_skill
                st.markdown(f"### {title}")
                st.write(description)
                st.write(f"💲 Price: ${price}")
                st.write(f"👤 Provider: {provider}")
                if st.button("Buy Now"):
                    try:
                        checkout_session = stripe.checkout.Session.create(
                            payment_method_types=["card"],
                            line_items=[{
                                "price_data": {
                                    "currency": "usd",
                                    "product_data": {
                                        "name": title,
                                    },
                                    "unit_amount": int(price * 100),
                                },
                                "quantity": 1,
                            }],
                            mode="payment",
                            success_url="http://localhost:8501?success=true",
                            cancel_url="http://localhost:8501?cancel=true",
                        )
                        st.success("Redirecting to payment...")
                        st.markdown(f"[👉 Click here to Pay Now]({checkout_session.url})", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Stripe error: {e}")
        else:
            st.info("No skills listed yet.")
