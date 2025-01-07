import streamlit as st
import re
import mysql.connector
import bcrypt
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# Function to hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Save user
def save_user(username, password):
    hashed_password = hash_password(password)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        return False

# Check password strength
def check_password_strength(password):
    points_gained = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        points_gained += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check uppercase
    if re.search(r'[A-Z]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one uppercase letter.")

    # Check lowercase
    if re.search(r'[a-z]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one lowercase letter.")

    # Check numbers
    if re.search(r'[0-9]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one number.")

    # Check special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        points_gained += 1
    else:
        feedback.append("Include at least one special character.")

    strength_score = (points_gained / 5) * 100
    return strength_score, points_gained, feedback

# Load common passwords from password.txt
def load_password_list():
    with open("password.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

# Streamlit App
st.title("Password Strength Analyzer with Common Password Check")

# Load common passwords
common_passwords = load_password_list()

# Tabs
tabs = st.tabs(["Sign-Up", "Login"])

with tabs[0]:
    st.header("Sign-Up")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Sign-Up"):
        if username and password:
            # Check password strength
            strength_score, points_gained, feedback = check_password_strength(password)

            if points_gained < 5:
                st.error("Password does not meet the criteria:")
                for suggestion in feedback:
                    st.write(f"- {suggestion}")
            elif password in common_passwords:
                st.error("Easily hackable password! Choose a stronger password.")
            else:
                # Save user
                if save_user(username, password):
                    st.success("User registered successfully!")
                else:
                    st.error("Username already exists. Please choose another.")

with tabs[1]:
    st.header("Login")
    login_username = st.text_input("Enter your username (Login):")
    login_password = st.text_input("Enter your password (Login):", type="password")

    if st.button("Login"):
        if login_username and login_password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", (login_username,))
            result = cursor.fetchone()
            conn.close()
            if result and bcrypt.checkpw(login_password.encode(), result[0].encode()):
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")
