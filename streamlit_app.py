import streamlit as st
import sqlite3

# Function to get candidates based on the position, along with their image file names
def get_candidates(position):
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute("SELECT name, image FROM candidates WHERE position=?", (position,))
    candidates = c.fetchall()  # Returns a list of tuples (name, image)
    conn.close()
    return candidates

# Function to check if a voter has already voted
def has_voted(registration_number):
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute("SELECT has_voted FROM voters WHERE registration_number=?", (registration_number,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Function to mark a voter as having voted
def mark_as_voted(registration_number):
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute("UPDATE voters SET has_voted=1 WHERE registration_number=?", (registration_number,))
    conn.commit()
    conn.close()

# Function to add a voter if not already in database
def add_voter(registration_number):
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO voters (registration_number) VALUES (?)", (registration_number,))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("College Election Voting")

# Manage navigation state
if "page" not in st.session_state:
    st.session_state.page = "registration"

# Registration page
if st.session_state.page == "registration":
    registration_number = st.text_input("Enter your registration number:")

    if st.button("Submit"):
        if registration_number:
            st.session_state.registration_number = registration_number  # Store the registration number in session state
            add_voter(registration_number)
            if has_voted(registration_number):
                st.warning("You have already voted.")
                st.session_state.page = "completed"
            else:
                st.success("Welcome! Proceed to vote.")
                st.session_state.page = "voting"
        else:
            st.error("Please enter your registration number.")

# Voting page
if st.session_state.page == "voting":
    st.header("Vote for President")
    president_candidates = get_candidates("President")
    president_choice = st.radio("Select a candidate for President:", [candidate_name for candidate_name, _ in president_candidates], key="president_choice")

    cols = st.columns(2)  # Create two columns
    for i, (candidate_name, candidate_image) in enumerate(president_candidates):
        with cols[i % 2]:  # Alternate between the two columns
            st.image(candidate_image, caption=candidate_name, width=150, use_column_width=False)
            # Radio buttons are handled by st.radio above

    st.header("Vote for Vice President")
    vice_president_candidates = get_candidates("Vice President")
    vice_president_choice = st.radio("Select a candidate for Vice President:", [candidate_name for candidate_name, _ in vice_president_candidates], key="vice_president_choice")

    cols = st.columns(2)  # Create two columns
    for i, (candidate_name, candidate_image) in enumerate(vice_president_candidates):
        with cols[i % 2]:  # Alternate between the two columns
            st.image(candidate_image, caption=candidate_name, width=150, use_column_width=False)
            # Radio buttons are handled by st.radio above

    st.header("Vote for Secretary")
    secretary_candidates = get_candidates("Secretary")
    secretary_choice = st.radio("Select a candidate for Secretary:", [candidate_name for candidate_name, _ in secretary_candidates], key="secretary_choice")

    cols = st.columns(2)  # Create two columns
    for i, (candidate_name, candidate_image) in enumerate(secretary_candidates):
        with cols[i % 2]:  # Alternate between the two columns
            st.image(candidate_image, caption=candidate_name, width=150, use_column_width=False)
            # Radio buttons are handled by st.radio above

    st.header("Vote for Joint Secretary")
    joint_secretary_candidates = get_candidates("Joint Secretary")
    joint_secretary_choice = st.radio("Select a candidate for Joint Secretary:", [candidate_name for candidate_name, _ in joint_secretary_candidates], key="joint_secretary_choice")

    cols = st.columns(2)  # Create two columns
    for i, (candidate_name, candidate_image) in enumerate(joint_secretary_candidates):
        with cols[i % 2]:  # Alternate between the two columns
            st.image(candidate_image, caption=candidate_name, width=150, use_column_width=False)
            # Radio buttons are handled by st.radio above

    if st.button("Submit Vote"):
        if (president_choice and vice_president_choice and secretary_choice and joint_secretary_choice):
            mark_as_voted(st.session_state.registration_number)  # Use the stored registration number
            st.success("Thank you for voting!")
            st.session_state.page = "completed"
        else:
            st.error("Please select a candidate for each position.")

# Completion page
if st.session_state.page == "completed":
    if has_voted(st.session_state.registration_number):
        st.warning("You have already voted.")
    else:
        st.info("Voting process completed. Thank you for participating!")
