import streamlit as st

class Skill:
    def __init__(self, name, description, price, image_url):
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url

    def display_skill(self):
        st.image(self.image_url, width=100)  # Display skill image
        st.subheader(self.name)
        st.write(self.description)
        st.write(f"Price: {self.price} USD")
        st.button(f"Buy {self.name}")

    @staticmethod
    def get_sample_skills():
        return [
            Skill("Web Development", "Learn HTML, CSS, and JavaScript.", 50, "https://via.placeholder.com/150"),
            Skill("Python Programming", "Learn Python for data science.", 40, "https://via.placeholder.com/150"),
            Skill("Graphic Design", "Master Photoshop and Illustrator.", 60, "https://via.placeholder.com/150")
        ]

# Streamlit page for displaying skills
def run_skills_page():
    st.title("🖼️ Browse Skills")

    skills = Skill.get_sample_skills()

    for skill in skills:
        skill.display_skill()

# Call to display on the Streamlit app
if "is_logged_in" in st.session_state:
    run_skills_page()
else:
    st.warning("Please login to browse skills.")
