import json
import os
import sys
from sys import argv

from google.protobuf import json_format

from google.cloud.speech import types
from format_response import format_transcript
from goog import transcribe_gcs


# Runs transcription for each file inside the specified directory
def auto_run(directory):
    for file in os.listdir(directory):
        if not file.endswith('.json'):
            continue
        file_path = os.path.join(directory, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            result = json_format.Parse(f.read(), types.cloud_speech_pb2.LongRunningRecognizeResponse())
            format_transcript(result.results, file_path[:-5])  # output .srt formatted version of transcription

        print(file_path)


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Azathoth\Documents\my-google-credentials.json'
    directory = argv[1]
    # sys.setrecursionlimit(1)
    auto_run(directory)
