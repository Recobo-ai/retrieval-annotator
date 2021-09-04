# Retrieval Annotator
A simple UI powered by Mongo DB cloud for annotating custom domain specific datasets for Information Retrieval tasks.
TODO:
Add dataset schema example
Run the Docker using followig commands:

Build Image:
```bash
docker build -f Dockerfile -t app:latest --build-arg MONGO_USERNAME=<MONGO_USERNAME> \
--build-arg MONGO_PASSWORD=<MONGO_PASSWORD> ANNOTATOR_NAME=<ANNOTATOR_NAME> \
--build-arg DATA_FILE_PATH=<DATA_FILE_PATH> .
```

Run Container:
```bash
docker run -p 8501:8501 app:latest
```

Here's how the screen looks like while annotation:
<img src="https://user-images.githubusercontent.com/6007894/132026752-2cb1a0ad-9304-4746-bf04-d4177a4d2218.png"/>


