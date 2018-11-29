import math


# subtitle rules:
#   one record should be visible 1,2 to 6 seconds
#   it can not be longer than 40 characters (spaces included) per line,
#   it must contain 1 to 2 lines

def is_subtitle_time_too_long(words, max_seconds):
    start_seconds, end_seconds = get_words_timing(words)
    interval = end_seconds - start_seconds
    return interval > max_seconds


def is_subtitle_length_too_long(words, max_length):
    line = ' '.join([w.word for w in words])
    return len(line) >= max_length


def should_split_subtitle(words, max_length, max_seconds):
    if is_subtitle_time_too_long(words, max_seconds):
        return True

    if is_subtitle_length_too_long(words, max_length):
        return True

    return False


def split_to_chunks(words, max_length, max_seconds):
    first_part_words = []
    rest_of_words = words
    while rest_of_words and \
            not is_subtitle_length_too_long(first_part_words + [rest_of_words[0]], max_length) and \
            not is_subtitle_time_too_long(first_part_words + [rest_of_words[0]], max_seconds):
        first_word = rest_of_words.pop(0)
        first_part_words.append(first_word)
    if not first_part_words and rest_of_words:
        print('some word is too long, it will be as single chunk')
        first_word = rest_of_words.pop(0)
        first_part_words.append(first_word)
    if rest_of_words:
        return [first_part_words] + split_to_chunks(rest_of_words, max_length, max_seconds)
    return [first_part_words]


def split_subtitle(subtitle, max_length, max_seconds):
    words = list(subtitle.words)
    return split_to_chunks(words, max_length, max_seconds)


def get_words_timing(words):
    start_time = words[0].start_time
    end_time = words[-1].end_time

    start_seconds = start_time.seconds + start_time.nanos * 1e-9
    end_seconds = end_time.seconds + end_time.nanos * 1e-9

    return start_seconds, end_seconds


# Convert the raw transcription into proper .srt format
def format_transcript(results, file_path):
    def add_srt_subtitle(line, words, file):

        start_seconds, end_seconds = get_words_timing(words)

        file.write(str(counter) + '\n')
        file.write(format_time(start_seconds) + ' --> ' + format_time(end_seconds) + '\n')
        file.write(line + "\n\n")

    def format_time(seconds: float, offset=0):  # time conversion/formatting for timestamps
        frac, whole = math.modf(seconds)
        f = frac * 1000
        m, s = divmod(whole, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d,%03d" % (h, m, s, (f + offset * 1000))

    """Used to break up large transcript sections to prevent multi-line subtitles"""

    with open(file_path + '.srt', 'w', encoding='utf-8') as file:
        counter = 0  # Used for numbering lines in file

        for result in results:
            print(result)
            subtitles = result.alternatives
            for subtitle in subtitles:
                print(subtitle)
                words = subtitle.words
                print(subtitle.words)
                if should_split_subtitle(words, max_length=40, max_seconds=6):
                    for chunk in split_subtitle(subtitle, max_length=40, max_seconds=6):
                        line = ' '.join([w.word for w in chunk])
                        counter += 1
                        add_srt_subtitle(line, chunk, file)
                else:
                    line = subtitle.transcript
                    words = subtitle.words
                    counter += 1
                    add_srt_subtitle(line, words, file)
