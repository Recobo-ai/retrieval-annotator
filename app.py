import SessionState
import pandas as pd
import streamlit as st
import os
import uuid
from annotation_mongo import MongoAnnotation


annotator_name = os.environ["ANNOTATOR_NAME"]
annotator_file_name = os.environ["DATA_FILE_PATH"]

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
min_page_num = 0
annotator_page_num = mongo_annotation_manager.get_page_number(
    annotator_name=annotator_name
)
if annotator_page_num:
    min_page_num = annotator_page_num

# A variable to keep track of which product we are currently displaying
session_state = SessionState.get(
    page_number=0,
    answer_1=str(uuid.uuid4()),
    answer_2=str(uuid.uuid4()),
    global_checbox=str(uuid.uuid4()),
    checbox_1=str(uuid.uuid4()),
    checbox_2=str(uuid.uuid4()),
)
data = pd.read_csv(annotator_file_name)
data = data.fillna("")
last_page = len(data) // N
input_page_num = st.number_input(
    "Enter a page number", min_page_num, last_page, min_page_num
)
if input_page_num > 0:
    session_state.page_number = input_page_num
st.write(f"Page: {session_state.page_number}/{last_page}")
# Add a next button and a previous button

prev, _, next = st.columns([1, 10, 1])

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
all_checkbox = st.checkbox(
    "Select/De-Select all", key=session_state.global_checbox, value=False
)

# Index into the sub dataframe
sub_df = data.iloc[start_idx:end_idx]
col1, col2 = st.columns((1, 9))
col3, col4 = st.columns((1, 9))
col5, col6 = st.columns((1, 1))

question_1_marked = col1.checkbox("", value=all_checkbox, key=session_state.checbox_1)
question_1 = col2.text_input("question_1", value=sub_df.iloc[0]["question"])
question_2_marked = col3.checkbox(
    "question_2", value=all_checkbox, key=session_state.checbox_2
)
question_2 = col4.text_input("", value=sub_df.iloc[1]["question"])
answer_1 = col5.text_input("answer_1", key=session_state.answer_1)
answer_2 = col6.text_input("answer_2", key=session_state.answer_2)

if sub_df.iloc[0]["context"] == sub_df.iloc[1]["context"]:
    context = st.write(sub_df.iloc[0]["context"])
    if next.button("Save"):
        data = []
        if question_1_marked:
            data.append(
                {
                    "_id": sub_df.iloc[0]["question_id"],
                    "question": question_1,
                    "context": sub_df.iloc[0]["context"],
                    "annotator": annotator_name,
                    "page_number": session_state.page_number,
                    "answer": answer_1,
                }
            )
        if question_2_marked:
            data.append(
                {
                    "_id": sub_df.iloc[1]["question_id"],
                    "question": question_2,
                    "context": sub_df.iloc[0]["context"],
                    "annotator": annotator_name,
                    "page_number": session_state.page_number,
                    "answer": answer_2,
                }
            )
        for annotation in data:
            save_response = mongo_annotation_manager.write_to_mongo(annotation)
            st.info(save_response)
        session_state.answer_1 = str(uuid.uuid4())
        session_state.answer_2 = str(uuid.uuid4())
else:
    st.error("Warning! Contexts are not matching...")
