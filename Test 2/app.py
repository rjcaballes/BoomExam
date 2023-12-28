import websockets
import asyncio
import base64
import json
from config import auth_key
import string
import pyaudio
import sys

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	frames_per_buffer=FRAMES_PER_BUFFER
)
 
# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

running_flag = True


async def send_receive():

	print(f'Connecting websocket to url ${URL}')

	async with websockets.connect(
		URL,
		extra_headers=(("Authorization", auth_key),),
		ping_interval=5,
		ping_timeout=20
	) as _ws:

		await asyncio.sleep(0.1)
		print("Receiving SessionBegins ...")

		session_begins = await _ws.recv()
		print(session_begins)
		print("Sending messages ...")


		async def send():
			while running_flag:
				try:
					data = stream.read(FRAMES_PER_BUFFER)
					data = base64.b64encode(data).decode("utf-8")
					json_data = json.dumps({"audio_data":str(data)})
					await _ws.send(json_data)

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					assert False, "Not a websocket 4008 error"

				await asyncio.sleep(0.01)
		  
			return True
	  

		async def receive():
			while running_flag:
				try:
					result_str = await _ws.recv()
					if json.loads(result_str)['message_type'] == 'FinalTranscript':
						phrase = json.loads(result_str)['text']
						print (phrase)
						res = append_vowel_consonant_markers(phrase)
						print (res)

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					assert False, "Not a websocket 4008 error"
		
		def append_vowel_consonant_markers(sentence):
			words = sentence.split()
			modified_words = []

			for word in words:
				# Remove various punctuation from the end of the word
				cleaned_word = word.rstrip(string.punctuation)

				last_char = cleaned_word[-1].lower()

				if last_char in ['a', 'e', 'i', 'o', 'u']:
					modified_words.append(cleaned_word + '-v')
				else:
					modified_words.append(cleaned_word + '-c')

			modified_sentence = ' '.join(modified_words)
			return modified_sentence
	  
		send_result, receive_result = await asyncio.gather(send(), receive())

while True:
	try:
		asyncio.run(send_receive())
	except KeyboardInterrupt:
		print("Script interrupted. Cleaning up...")
		running_flag = False
		sys.exit()
	finally:
		# Add any final cleanup code here if needed
		pass


	