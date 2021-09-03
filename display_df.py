import SessionState
import pandas as pd
import streamlit as st


annotator_name = "Shahrukh Khan"
annotator_file_name = "auto-mpg.csv"

# Number of entries per screen
N = 2

st.markdown(f" {annotator_name} @ Chemical Data Annotations")

# A variable to keep track of which product we are currently displaying
session_state = SessionState.get(page_number=0)

data = pd.read_csv(annotator_file_name)
last_page = len(data) // N

# Add a next button and a previous button

prev, _, next = st.beta_columns([1, 10, 1])

if next.button("Next"):

    if session_state.page_number + 1 > last_page:
        session_state.page_number = 0
    else:
        session_state.page_number += 1

if prev.button("Previous"):

    if session_state.page_number - 1 < 0:
        session_state.page_number = last_page
    else:
        session_state.page_number -= 1

# Get start and end indices of the next page of the dataframe
start_idx = session_state.page_number * N
end_idx = (1 + session_state.page_number) * N

# Index into the sub dataframe
sub_df = data.iloc[start_idx:end_idx]
col1, col2 = st.beta_columns((1, 9))
col3, col4 = st.beta_columns((1, 9))

question_1_marked = col1.checkbox("")
question_1 = col2.text_input("Questions", value=sub_df.iloc[0]["mpg"])
question_2_marked = col3.checkbox(" ")
question_2 = col4.text_input("", value=sub_df.iloc[1]["mpg"])

context = st.write(
    "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum",
)
