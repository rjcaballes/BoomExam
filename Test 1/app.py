import json
import requests

# Assuming 'file_path' is the path to your JSON file
file_path = "train-v2.0.json"

# Open the file with explicit encoding (UTF-8 in this case)
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# get the available questions and answers for a given topic
def get_qa(topic, data):
    q = []
    a = []
    for d in data['data']:
        if d['title']==topic:
            for paragraph in d['paragraphs']:
                for qa in paragraph['qas']:
                    if not qa['is_impossible']:
                        q.append(qa['question'])
                        a.append(qa['answers'][0]['text'])
            return q,a
        
questions, answers = get_qa(topic='Premier_League', data=data)

print("Number of available questions: {}".format(len(questions)))

json_data = {
  'questions':questions,
  'answers':answers,
}

response = requests.post(
  'http://localhost:8000/set_context',
  json=json_data
)

res = response.json()

print (res)


new_questions = [
    'How many teams compete in the Premier League ?',
    'When does the Premier League starts and finishes ?',
    'Who has the highest number of goals in the Premier League ?',
]

json_data = {
  'questions':new_questions,
}

response = requests.post(
  'http://localhost:8000/get_answer',
  json=json_data
)

for d in response.json():
  print('\n'.join(["{} : {}".format(k, v) for k,v in d.items()])+'\n')