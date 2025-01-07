import streamlit as st
import re

# Load common passwords from password.txt
def load_password_list():
    with open("password.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

# Function to check password strength
def check_password_strength(password):
    strength_score = 0
    total_points = 5
    points_gained = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        points_gained += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    # Check for uppercase
    if re.search(r'[A-Z]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one uppercase letter.")
    
    # Check for lowercase
    if re.search(r'[a-z]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one lowercase letter.")
    
    # Check for numbers
    if re.search(r'[0-9]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one number.")
    
    # Check for special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one special character.")
    
    strength_score = (points_gained / total_points) * 100
    return strength_score, points_gained, feedback

# Streamlit Interface
st.title("Password Strength Analyzer and Login System")

# Load common passwords
common_passwords = load_password_list()

# Tabs for Sign-Up and Login
tabs = st.tabs(["Sign-Up", "Login", "Simulate Attack"])

with tabs[0]:
    st.header("Sign-Up")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Sign-Up"):
        if username and password:
            strength_score, points_gained, feedback = check_password_strength(password)

            if points_gained < 5:
                st.error("Password does not meet the criteria:")
                for suggestion in feedback:
                    st.write(f"- {suggestion}")
            else:
                # Check if password is in the common password list
                if password in common_passwords:
                    st.error("Hacked! Your password is too common.")
                else:
                    st.success("User registered successfully!")

with tabs[1]:
    st.header("Login")
    login_username = st.text_input("Enter your username (Login):")
    login_password = st.text_input("Enter your password (Login):", type="password")

    if st.button("Login"):
        if login_username and login_password:
            # Simulate login check - Here we would normally compare against the stored hash
            if login_password in common_passwords:
                st.error("Hacked! This password is too common.")
            else:
                st.success("Login successful!")
            
with tabs[2]:
    st.header("Simulate Attack")
    attack_password = st.text_input("Enter a password to simulate an attack:")

    if st.button("Simulate Attack"):
        if attack_password in common_passwords:
            st.error(f"The password '{attack_password}' is easily guessable!")
        else:
            st.success(f"The password '{attack_password}' is not in the common password list.")
