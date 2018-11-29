import json
import os
from sys import argv

from google.protobuf import json_format

from google.cloud.speech import types
from format_response import format_transcript
from goog import transcribe_gcs


# Runs transcription for each file inside the specified directory
def auto_run(directory):
    for file in os.listdir(directory):
        if file.endswith('.json'):
            file_path = os.path.join(directory, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                result = json_format.Parse(f.read(), types.cloud_speech_pb2.LongRunningRecognizeResponse())
                format_transcript(result.results, file_path[:-4])  # output .srt formatted version of transcription

            print(file_path)
        else:
            continue


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Azathoth\Documents\my-google-credentials.json'
    directory = argv[1]
    auto_run(directory)

    # transcribe_gcs(r'E:\Projects\lecture_generator\audio_in\other\mono-Zakázaná Česká reklama T-Mobile 2014.wav')
