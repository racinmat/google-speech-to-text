import os
from sys import argv
from goog import transcribe_gcs


# Runs transcription for each file inside the specified directory
def auto_run(directory):
    files = os.listdir(directory)
    for file in files:
        if ' ' in file:
            os.rename(os.path.join(directory, file),
                      os.path.join(directory, file.replace(' ', '_')))  # Removes any spaces in the file names

    for file in os.listdir(directory):  # Get each .mp4 file in directory and run transcription
        if file.endswith('.wav'):
            file_path = os.path.join(directory, file)
            transcribe_gcs(file_path)
            print(file_path)
        else:
            continue


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Azathoth\Documents\my-google-credentials.json'
    directory = argv[1]
    auto_run(directory)

    # transcribe_gcs(r'E:\Projects\lecture_generator\audio_in\other\mono-Zakázaná Česká reklama T-Mobile 2014.wav')
