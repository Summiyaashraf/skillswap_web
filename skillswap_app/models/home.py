import streamlit as st

def run_homepage():
    # Hero Section (Responsive)
    st.title("Welcome to Skill Marketplace! 🌟")
    
    # Hero image for responsive design
    st.image("https://via.placeholder.com/600x200", caption="Skill Marketplace Logo", width=600)

    st.subheader("Unlock your potential. Find the right skills, buy or sell, and level up your career.")
    st.button("Get Started")

    # How It Works Section (Responsive)
    st.subheader("How It Works 🤔")
    st.write("""
        1. Browse skills listed by professionals.
        2. Choose the skills you want to learn or provide.
        3. Complete the payment and start your learning journey or offer your expertise.
    """)

    # About Us Section (Responsive)
    st.subheader("About Us 💼")
    st.write("""
        We are a platform that connects professionals and learners. Our goal is to provide a space for 
        people to share their skills and access new learning opportunities.
    """)

    # Top Categories Section (Responsive)
    st.subheader("Top Skill Categories 📚")
    categories = ["Web Development", "Data Science", "Graphic Design", "Marketing", "Cybersecurity"]
    
    # Use columns for responsive layout
    col1, col2 = st.columns(2)
    with col1:
        st.button(f"Explore {categories[0]}")
        st.button(f"Explore {categories[1]}")
    with col2:
        st.button(f"Explore {categories[2]}")
        st.button(f"Explore {categories[3]}")
        st.button(f"Explore {categories[4]}")

# Custom CSS for mobile responsiveness
st.markdown("""
    <style>
        @media only screen and (max-width: 600px) {
            .streamlit-expanderHeader {
                font-size: 16px !important;
            }
            h1 {
                font-size: 24px;
            }
            .stButton>button {
                width: 100%;
                font-size: 14px;
            }
            .stTextInput input {
                font-size: 14px;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Display homepage
if "is_logged_in" in st.session_state:
    run_homepage()
else:
    st.warning("Please login to explore the marketplace.")
