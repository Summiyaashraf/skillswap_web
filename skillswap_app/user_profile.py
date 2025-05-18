import streamlit as st
import json
import os

class UserProfile:
    def __init__(self, username):
        self.username = username
        self.profile_data = self.load_profile()

    def load_profile(self):
        if os.path.exists("profiles.json"):
            with open("profiles.json", "r") as f:
                profiles = json.load(f)
            return profiles.get(self.username, {})
        return {}

    def update_profile(self, new_data):
        profiles = self.load_all_profiles()
        profiles[self.username] = new_data
        with open("profiles.json", "w") as f:
            json.dump(profiles, f)

    def load_all_profiles(self):
        if os.path.exists("profiles.json"):
            with open("profiles.json", "r") as f:
                return json.load(f)
        return {}

    def display_profile(self):
        st.subheader("Your Profile")
        
        if not self.profile_data:
            st.write("No profile data found.")
            return
        
        # Display personal info
        st.write(f"👤 **Username**: {self.profile_data.get('username', 'N/A')}")
        st.write(f"📧 **Email**: {self.profile_data.get('email', 'N/A')}")
        
        # Display skills
        st.write("💼 **Listed Skills**:")
        listed_skills = self.profile_data.get('skills', [])
        for skill in listed_skills:
            st.write(f"- {skill}")

        # Display bought skills
        st.write("💡 **Bought Skills**:")
        bought_skills = self.profile_data.get('bought_skills', [])
        for skill in bought_skills:
            st.write(f"- {skill}")
        
        # Optionally, provide a form to edit the profile
        st.write("📝 **Update Profile Information**:")
        with st.form("profile_form"):
            email = st.text_input("Email", self.profile_data.get('email', ''))
            skills = st.text_area("Skills (comma separated)", ', '.join(listed_skills))
            submitted = st.form_submit_button("Update Profile")
            
            if submitted:
                new_data = {
                    'username': self.username,
                    'email': email,
                    'skills': skills.split(", "),
                    'bought_skills': bought_skills
                }
                self.update_profile(new_data)
                st.success("Profile updated successfully!")


# Streamlit page to display user profile
def run_profile_page():
    st.title("🧍‍♂️ User Profile")

    if "username" in st.session_state:
        username = st.session_state["username"]
        profile = UserProfile(username)
        profile.display_profile()
    else:
        st.warning("Please login to view your profile.")
