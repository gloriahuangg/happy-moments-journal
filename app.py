# app.py
import streamlit as st
import sqlite3
import bcrypt
import base64
from datetime import datetime
import random
from PIL import Image
import io

# Database setup
conn = sqlite3.connect('happy_journal.db', check_same_thread=False)
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS happy_moments
             (id INTEGER PRIMARY KEY, user_id INTEGER, note TEXT, image BLOB, created_at TIMESTAMP)''')
conn.commit()

# Helper functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def register_user(username, password):
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user and verify_password(password, user[2]):
        return user
    return None

def save_happy_moment(user_id, note, image):
    image_bytes = image.getvalue() if image else None
    c.execute("INSERT INTO happy_moments (user_id, note, image, created_at) VALUES (?, ?, ?, ?)",
              (user_id, note, image_bytes, datetime.now()))
    conn.commit()

def get_random_happy_moment(user_id):
    c.execute("SELECT * FROM happy_moments WHERE user_id=?", (user_id,))
    moments = c.fetchall()
    if moments:
        return random.choice(moments)
    return None

# Streamlit app
st.title("Happy Moments Journal")

# Session state
if 'user' not in st.session_state:
    st.session_state.user = None

# Sidebar for login/logout
if st.session_state.user:
    st.sidebar.write(f"Welcome, {st.session_state.user[1]}!")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
else:
    choice = st.sidebar.selectbox("Login/Signup", ["Login", "Sign Up"])
    
    if choice == "Sign Up":
        with st.sidebar.form("signup_form"):
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            signup_button = st.form_submit_button("Sign Up")
            
        if signup_button:
            if register_user(new_user, new_password):
                st.sidebar.success("User registered successfully. Please log in.")
            else:
                st.sidebar.error("Username already exists. Please choose a different one.")
    
    elif choice == "Login":
        with st.sidebar.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
        
        if login_button:
            user = login_user(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password")

# Main app functionality
if st.session_state.user:
    tab1, tab2 = st.tabs(["Add Happy Moment", "Happy Moment"])
    
    with tab1:
        st.header("Log a Happy Moment")
        note = st.text_area("What made you happy today?")
        image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
        if st.button("Save Happy Moment"):
            if note:
                save_happy_moment(st.session_state.user[0], note, image)
                st.success("Happy moment saved!")
            else:
                st.warning("Please enter a note for your happy moment.")
    
    with tab2:
        st.header("If you are home sick or feel sad...")
        if st.button("Show me a happy memory"):
            moment = get_random_happy_moment(st.session_state.user[0])
            if moment:
                st.write(f"On {moment[4]}, you wrote:")
                st.write(moment[2])
                if moment[3]:
                    image = Image.open(io.BytesIO(moment[3]))
                    st.image(image, caption="Your happy moment image")
            else:
                st.info("You haven't added any happy moments yet. Start by adding one!")

else:
    st.info("Please login or sign up to use the Happy Moments Journal.")