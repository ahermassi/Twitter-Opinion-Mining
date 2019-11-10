import csv
import re
import shutil
import string
from tempfile import NamedTemporaryFile
import time

def clean_text(tweet_file):
    '''
    This function removes all unnecessary entities, including:
    URLs, @user mentions, punctuation, hashtags
    '''

    tempfile = NamedTemporaryFile(delete=False)

    with open(tweet_file, 'rb') as csvfile, tempfile:
        reader = csv.reader(csvfile, delimiter='\n', quotechar='"')
        next(reader, None)
        fieldnames = ['text', 'timestamp']
        writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            for r in row:

                txt = r.split(',')[:-1][0]
                # Remove links
                txt = re.sub('((www\.[\s]+)|(https?://[^\s]+)|([^\s]+twitter.com/[^\s]+))', 'URL', txt)
                # Remove @user (mentions)
                txt = re.sub('(@[^\s]+)', 'USERNAME', txt)
                # Remove punctuation
                replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
                txt = txt.translate(replace_punctuation)
                # Remove hashtags
                txt = re.sub(r'#([^\s]+)', r'\1', txt)
                writer.writerow({'text': txt.replace("\n", ""), 'timestamp': ''.join(r.split(',')[-1])})

    shutil.move(tempfile.name, tweet_file)

def pre_process(file_list, frame):
    for f in file_list:
        clean_text(f)
    time.sleep(5)
    frame.config(text="Done!")
