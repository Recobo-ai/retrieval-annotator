# base image
FROM python:3.7

# streamlit-specific commands
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
    [general]\n\
    email = \"\"\n\
    " > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
    [server]\n\
    enableCORS = false\n\
    " > /root/.streamlit/config.toml'

# exposing default port for streamlit
EXPOSE 8501

# copy over and install packages
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# copying everything over
COPY . .

# set environment variables
ARG MONGO_USERNAME
RUN echo $MONGO_USERNAME
ENV MONGO_USERNAME=$MONGO_USERNAME
ARG MONGO_PASSWORD
RUN echo $MONGO_PASSWORD
ENV MONGO_PASSWORD=$MONGO_PASSWORD
ARG ANNOTATOR_NAME
RUN echo $ANNOTATOR_NAME
ENV ANNOTATOR_NAME=$ANNOTATOR_NAME
ARG DATA_FILE_PATH
RUN echo $DATA_FILE_PATH
ENV DATA_FILE_PATH=$DATA_FILE_PATH

CMD streamlit run app.py