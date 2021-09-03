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

CMD streamlit run app.py