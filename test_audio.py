import os
with open('extracted_audio_3.wav','rb') as f:
	bin = f.read()
	with open('test.wav','wb') as f1:
		f1.write(bin)

pipeline = Pipeline.from_pretrained(
  "pyannote/speaker-diarization-3.0",
  use_auth_token="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")
