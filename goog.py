import json
import os
import os.path as osp
import pickle
import time

from google.protobuf.json_format import MessageToDict, MessageToJson
from process_video import process_video
from upload_to_gcloud import upload_to_gcloud
from format_response import format_transcript
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def transcribe_gcs(audio_file_path):
    bucket_name = 'european-germany-bucket'  # Your gcloud bucket name
    print(audio_file_path)
    audio_file_name = osp.basename(audio_file_path)
    print(audio_file_name)
    # todo: do checking if it's already uploaded or not and upload it only if it's missing
    # upload_to_gcloud(bucket_name, source_file_name=audio_file_path, destination_blob_name=audio_file_name)

    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()
    audio = types.RecognitionAudio(
        uri="gs://" + bucket_name + "/" + audio_file_name)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        language_code='cs-CZ',
        # sample_rate_hertz=16000,
        enable_word_time_offsets=True
    )
    operation = client.long_running_recognize(config, audio)

    while not operation.done():
        print('Waiting for results...')
        time.sleep(30)   # 30 seconds

    result = operation.result()

    results = result.results

    with open(audio_file_path + '.json', 'w', encoding='utf-8') as f:
        result_dict = MessageToDict(result)
        json.dump(result_dict, f, indent=True)

    with open(audio_file_path + '.txt', 'w', encoding='utf-8') as raw_text_file:
        for result in results:
            for alternative in result.alternatives:
                raw_text_file.write(alternative.transcript + '\n')

    # format_transcript(results, audio_file_path)  # output .srt formatted version of transcription
