import time

#import json
#import ijson
#from pyspark import SparkContext
from itertools import islice

filePathes = [
    "data/twitter-1mb.json",
    "data/twitter-50mb.json"
]

class Dataset:
    def __init__(self, filePath: str = filePathes[1], skipFirstAndLast: str = True) -> None:
        self.filePath = filePath
        self.reader = self.genFilesReader(skipFirstAndLast)

    def genFilesReader(self, skipFirstAndLast:str = True):
        with open(self.filePath, encoding='utf-8') as f:
            iterator = iter(f)
            if skipFirstAndLast:
                next(iterator, None)
                prev_row = next(iterator, None)
                for current_row in iterator:
                    yield prev_row
                    prev_row = current_row
            else:
                for row in iterator:
                    yield row


    @property
    def printFileCounts(self):
        count = 0
        for row in self.file:
            count += 1
        print(f"Total count is {count}")

######################################


    

if __name__ == "__main__":
    import re
    def processRow(row, sentiment_d, count_d):
        created_at_match = re.search(r'"created_at":"(.*?)"', row)
        sentiment_match = re.search(r'"sentiment":([-\d.]+)', row)
        sentiment = 0
        if created_at_match:
            created_at = created_at_match.group(1)
            # 如果找到 sentiment，则更新 sentiment 变量
            if sentiment_match:
                sentiment = float(sentiment_match.group(1))

            update_dict(sentiment_d, sentiment, count_d, created_at)

            #print("Created At:", created_at[5:7]+created_at[8:10], created_at[11:13])
            #print("Sentiment:", sentiment)
        else:
            print("The required field 'created_at' is missing.")

    # put value into dict
    def update_dict(s_d, sentiment, c_d, created_at):
        mmdd = created_at[5:7]+created_at[8:10]
        hh = created_at[11:13]

        # sentiment_dict: value = sum_sentiment
        # count_dict: value = count
        # date in dict
        if mmdd in s_d.keys():
            #if hour in dict
            if hh in s_d[mmdd].keys():
                s_d[mmdd][hh] += sentiment
                c_d[mmdd][hh] += 1
            # if hour not in dict
            else:
                s_d[mmdd][hh] = sentiment
                c_d[mmdd][hh] = 1
        # date not in dict
        else:
            s_d[mmdd] = {}
            s_d[mmdd][hh] = sentiment
            c_d[mmdd] = {}
            c_d[mmdd][hh] = 1







    dataset = Dataset()

    # create dict for sum_sentiment sentiment_d = {[mmdd]:{[hh]: sum_sentiment}}
    sentiment_d = {}
    # create dict for twitter_count count_d = {[mmdd]:{[hh]: count}}
    count_d = {}

    #for row in islice(dataset.reader, 16):
        #processRow(row, sentiment_d, count_d)

    for row in dataset.reader:
        processRow(row, sentiment_d, count_d)

    print(count_d)





