import streamlit as st
import json
import os

class User:
    def __init__(self, username):
        self.username = username
        self.skills = self.load_data("skills.json")
        self.transactions = self.load_data("transactions.json")

    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return []

    def get_listed_skills(self):
        return [s for s in self.skills if s.get("provider") == self.username]

    def get_bought_skills(self):
        return [t for t in self.transactions if t.get("buyer") == self.username]

    def display_profile(self):
        st.title("👤 User Profile")
        st.success(f"Welcome, **{self.username}**!")

        st.subheader("📧 Email / Username")
        st.write(self.username)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📜 Listed Skills")
            listed = self.get_listed_skills()
            if listed:
                for skill in listed:
                    st.markdown(f"✅ **{skill['title']}** - {skill['description']}")
            else:
                st.info("No skills listed yet.")

        with col2:
            st.subheader("🛍️ Bought Skills")
            bought = self.get_bought_skills()
            if bought:
                for t in bought:
                    st.markdown(f"💼 **{t['skill']}** - from **{t['provider']}**")
            else:
                st.info("No purchases yet.")

        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.success("You have been logged out.")
            st.experimental_rerun()


# Main Streamlit app logic
if "is_logged_in" in st.session_state and st.session_state["is_logged_in"]:
    user = User(st.session_state["username"])
    user.display_profile()
else:
    st.warning("Please login to view your profile.")
