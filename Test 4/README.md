python -m venv venv
venv\Scripts\activate

# TO BE INSTALLED
1. pip install transformers
2. pip install torch
3. pip install streamlit

# to run the app
1. docker build . -t summarization
2. docker run -p 8000:8000 summarization


# run locally without docker
streamlit run main.py

# show the different docker images running
docker images

