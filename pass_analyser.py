import streamlit as st
import re

def check_password_strength(password):
    strength_score = 0
    total_points = 5
    points_gained = 0
    feedback = []

    if len(password) >= 8:
        points_gained += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    if re.search(r'[A-Z]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one uppercase letter.")
    if re.search(r'[a-z]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one lowercase letter.")
    if re.search(r'[0-9]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one number.")
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one special character.")
    strength_score = (points_gained / total_points) * 100

    return strength_score, points_gained, feedback
st.title("Password Strength Analyzer")
username = st.text_input("Enter your username:")
password = st.text_input("Enter your password:", type="password")

if st.button("Submit"):
    if username and password:
        strength_score, points_gained, feedback = check_password_strength(password)
        st.subheader("Password Strength:")
        st.write(f"**Points Gained:** {points_gained} / 5")
        st.write(f"**Strength Score:** {strength_score:.2f}%")
        if points_gained < 3:
            st.error("Weak Password")
        elif points_gained == 3 or points_gained == 4:
            st.warning("Moderate Password")
        else:
            st.success("Strong Password")

        if feedback:
            st.subheader("Suggestions to Improve Password:")
            for suggestion in feedback:
                st.write(f"- {suggestion}")
    else:
        st.error("Please enter both username and password.")
