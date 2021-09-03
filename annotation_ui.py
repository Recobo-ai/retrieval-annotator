import SessionState
import pandas as pd
import streamlit as st
import os
from annotation_mongo import MongoAnnotation


annotator_name = "Shahrukh Khan"
annotator_file_name = "dataset.csv"

## mongo credentials from environment variables
credentials = {
    "mongo_username": os.environ["MONGO_USERNAME"],
    "mongo_password": os.environ["MONGO_PASSWORD"],
}

mongo_db_config = {
    "mongo_connect_url": "mongodb+srv://{}:{}@cluster0.lhdpw.mongodb.net/{}?retryWrites=true&w=majority",
    "mongo_db": "chemical_domain_annotations",
    "mongo_collection": "chemical_domain_annotations",
}
mongo_annotation_manager = MongoAnnotation(credentials, mongo_db_config)

# Number of entries per screen
N = 2

st.markdown(f" {annotator_name} @ Chemical Data Annotations")

# A variable to keep track of which product we are currently displaying
session_state = SessionState.get(page_number=0)

data = pd.read_csv(annotator_file_name)
last_page = len(data) // N
input_page_num = st.number_input("Enter a page number", 0, last_page, 0)
if input_page_num > 0:
    session_state.page_number = input_page_num
st.write(f"Page: {session_state.page_number}/{last_page}")
# Add a next button and a previous button

prev, _, next = st.beta_columns([1, 10, 1])

# """if next.button("Next"):
#     all_checkbox = False
#     if session_state.page_number + 1 > last_page:
#         session_state.page_number = 0
#     else:
#         session_state.page_number += 1

# if prev.button("Previous"):
#     all_checkbox = False
#     if session_state.page_number - 1 < 0:
#         session_state.page_number = last_page
#     else:
#         session_state.page_number -= 1"""

# Get start and end indices of the next page of the dataframe
start_idx = session_state.page_number * N
end_idx = (1 + session_state.page_number) * N

## global checkbox
all_checkbox = st.checkbox("Select/De-Select all")

# Index into the sub dataframe
sub_df = data.iloc[start_idx:end_idx]
col1, col2 = st.beta_columns((1, 9))
col3, col4 = st.beta_columns((1, 9))

question_1_marked = col1.checkbox("", value=all_checkbox)
question_1 = col2.text_input("Questions", value=sub_df.iloc[0]["question"])
question_2_marked = col3.checkbox(" ", value=all_checkbox)
question_2 = col4.text_input("", value=sub_df.iloc[1]["question"])
if sub_df.iloc[0]["context"] == sub_df.iloc[1]["context"]:
    context = st.write(sub_df.iloc[0]["context"])
else:
    st.error("Warning! Contexts are not matching...")


if next.button("Save"):
    data = []
    if question_1_marked:
        data.append(
            {
                "_id": sub_df.iloc[0]["question_id"],
                "question": question_1,
                "context": sub_df.iloc[0]["context"],
                "annotator": annotator_name,
            }
        )
    if question_2_marked:
        data.append(
            {
                "_id": sub_df.iloc[1]["question_id"],
                "question": question_2,
                "context": sub_df.iloc[0]["context"],
                "annotator": annotator_name,
            }
        )
    for annotation in data:
        save_response = mongo_annotation_manager.write_to_mongo(annotation)
        st.info(save_response)
