import streamlit as st
import pandas as pd
import time
# st.cache_data.clear()
st.title("Round Robin Speed Dating App")

filename = './Students_list_for_speed_dating.csv'

def round_robin_csv_to_df(filename_or_path):
    """
    This function takes a csv file and returns a DataFrame with Round-Robin style pairings 
    for Project Speed Dating, ensuring each unique student combination appears only once,
    while properly handling odd numbers of students.
    """
    student_list = [] # create a list to store student names
    with open(filename) as file: # open the file
        for line in file:
            student_list.append(line.strip())   # add each line to the list

    student_list = student_list[1:] # remove the header

    # we assign a new student, if there is an odd number of them. 
    # This way, we avoid issue with the middle student
    if len(student_list) % 2 == 1:
        student_list.append('X')
    
    student_dict = {} # we create a dictionary to store the student names and their number in the list
    for student in student_list: # we iterate over the student list and assign a number to each student
        i = student_list.index(student)
        student_dict[student] = i+1
    
    # we create a list of students IDs
    students = list(range(1, len(student_list) + 1))

    # Track used pairs to avoid duplicates
    used_pairs = set()
    # we initialize a list to hold the rotations
    rotations = []

    #for each round, we create new pairings list
    for round in range(len(student_list) - 1):
        pairings = []
        # Pair students in a round-robin fashion
        for i in range(len(student_list) // 2):
            student1 = students[i]
            student2 = students[-(i + 1)]

            # Create a sorted tuple to represent the pair (regardless of order)
            pair = tuple(sorted([student1, student2]))
            if pair not in used_pairs:
                    pairings.append((student1, student2))
                    used_pairs.add(pair)
            else:
                pass
        # Append the pairings to the rotations list
        rotations.append(pairings)

        # Rotate the students, keeping the first student in place
        students = [students[0]] + students[-1:] + students[1:-1]

    data = [] # we create an empty list to host the pairings
    d2 = {v: k for k, v in student_dict.items()} # We create a dictionary for reverse mapping

    for i, round in enumerate(rotations, start=1):
        for student1, student2 in round:
            data.append({
                    'Round': i,
                    'Student 1': d2.get(student1),
                    'Student 2': d2.get(student2)
                })
    round_robin_df = pd.DataFrame(data)
    #returns a DataFrame for easier Manipulation
    return round_robin_df


df = round_robin_csv_to_df(filename)

# Assuming df is your DataFrame with columns: round, student1, student2
selected_round = st.select_slider(
            'Select Round',
            options=df['Round'])
st.write("Current round is", selected_round)
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