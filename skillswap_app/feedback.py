import streamlit as st
import json
import os

class Feedback:
    def __init__(self, username):
        self.username = username
        self.feedback_data = self.load_feedback()

    def load_feedback(self):
        if os.path.exists("feedbacks.json"):
            with open("feedbacks.json", "r") as f:
                feedbacks = json.load(f)
            return feedbacks.get(self.username, {})
        return {}

    def save_feedback(self, skill, rating, comment):
        all_feedbacks = self.load_all_feedbacks()
        if self.username not in all_feedbacks:
            all_feedbacks[self.username] = {}

        all_feedbacks[self.username][skill] = {
            "rating": rating,
            "comment": comment
        }

        with open("feedbacks.json", "w") as f:
            json.dump(all_feedbacks, f)

    def load_all_feedbacks(self):
        if os.path.exists("feedbacks.json"):
            with open("feedbacks.json", "r") as f:
                return json.load(f)
        return {}

    def display_feedback_form(self, skill):
        st.subheader(f"Leave Feedback for '{skill}' Skill")

        rating = st.slider("Rating (1 to 5)", 1, 5)
        comment = st.text_area("Your Comment", "")
        
        submitted = st.button("Submit Feedback")
        if submitted:
            self.save_feedback(skill, rating, comment)
            st.success("Feedback submitted successfully!")

    def display_user_feedback(self, skill):
        if skill in self.feedback_data:
            feedback = self.feedback_data[skill]
            st.write(f"⭐ **Rating**: {feedback['rating']}")
            st.write(f"💬 **Comment**: {feedback['comment']}")
        else:
            st.write("No feedback yet.")

# Streamlit page for feedback system
def run_feedback_page():
    st.title("✍️ Feedback & Reviews")

    if "username" in st.session_state:
        username = st.session_state["username"]
        feedback = Feedback(username)

        skill = st.selectbox("Select Skill to Leave Feedback", ["Skill 1", "Skill 2", "Skill 3"])  # You can replace this with dynamic data

        # Display user feedback if any
        feedback.display_user_feedback(skill)

        # Provide a form to leave feedback if not already given
        feedback.display_feedback_form(skill)
        
    else:
        st.warning("Please login to leave feedback.")
