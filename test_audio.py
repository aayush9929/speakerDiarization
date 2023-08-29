import os
with open('extracted_audio_3.wav','rb') as f:
	bin = f.read()
	with open('test.wav','wb') as f1:
		f1.write(bin)
