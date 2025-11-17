import streamlit as st
import pandas as pd
import time

st.title("Round Robin Speed Dating App")

filename = './Students_list_for_speed_dating.csv'

def student_round_robin_for_csv(filename_or_path):
    """
    This function takes a csv file and returns a DataFrame with Round-Robin style pairings for Project Speed Dating.
    param: filename_or_path: str: the path to the csv file
    return: pd.DataFrame: a DataFrame with columns ['Round', 'Student 1', 'Student 2']
    """

    student_list = [] # we create an empty list for the student names
    with open(filename_or_path) as file: # we open the file with the student names
        for line in file:
            student_list.append(line.strip()) # we add each name (one per line), stripping any empty space
    student_list = student_list[1:]  # remove the header

    student_dict = {student: i + 1 for i, student in enumerate(student_list)} # we create a dictionary out of the list
    students = list(range(1, len(student_list) + 1))
    # This generates a list of numbers from 1 to the total number of students.
    # Each number serves as a unique identifier for each student and will be used 
    # for pairing in the round-robin process
    rotations = []

#loop runs for one fewer than the number of students, as that's the minimum needed for every unique pair 
# (standard round-robin tournament structure).
    for round in range(len(student_list) - 1): 
        pairings = [] #In each round, a new pairings list is created.
        for i in range(len(student_list) // 2): # nested loop selects pairs—one from the start and one from the end of the current list of student indices (students)
            student1 = students[i]
            student2 = students[-(i + 1)] 
            pairings.append((student1, student2)) #Pair the first and last, second and second-last, etc., guaranteeing all unique combinations
        if len(student_list) % 2 == 1: # If the list length is odd, the code detects this and pairs the middle student with None, signaling a participant without a partner that round.
            pairings.append((students[len(student_list) // 2], None))
        rotations.append(pairings) #After creating all pairings for the round, the code rotates the student list with
        students = [students[0]] + students[-1:] + students[1:-1] #This keeps the first student fixed, moves the last student to the second position, and shifts others forward, ensuring new pairings next round

    d2 = {v: k for k, v in student_dict.items()} #makes a reverse mapping (ID to name) for easy lookup.

    data = [] # we create an empty list to host the pairings
    for i, round in enumerate(rotations, start=1):
        for student1, student2 in round:
            data.append({
                'Round': i,
                'Student 1': d2.get(student1),
                'Student 2': d2.get(student2) if student2 is not None else 'X'
            })
    return pd.DataFrame(data) #returns a DataFrame for easier Manipulation


df = student_round_robin_for_csv(filename)

# Assuming df is your DataFrame with columns: round, student1, student2
rounds = df['Round'].unique()
selected_round = st.slider('Select Round', int(min(rounds)), int(max(rounds)), int(min(rounds)))
filtered = df[df['Round'] == selected_round]
st.dataframe(filtered)

duration = st.number_input('Set timer (seconds)', min_value=1, max_value=3600, value=300)
if st.button('Start Timer'):
    progress_bar = st.progress(0)
    status = st.empty()
    for i in range(duration):
        progress_bar.progress((i + 1) / duration)
        status.write(f"Time left: {duration - i - 1} seconds")
        time.sleep(1)
    st.success("Time's up!")