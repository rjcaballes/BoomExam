# Use an official Python runtime as a parent image
FROM python:3.8.12-slim-buster

WORKDIR /usr/app/src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir transformers[torch] streamlit

# copies the app files to the docker image
COPY / ./

# Run app.py when the container launches
CMD ["streamlit", "run", "main.py"]
