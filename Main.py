import time

import json
import ijson
from pyspark import SparkContext
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

    dataset = Dataset()

    import re
    def processRow(row):
        created_at_match = re.search(r'"created_at":"(.*?)"', row)
        sentiment_match = re.search(r'"sentiment":([-\d.]+)', row)
        sentiment = 0        
        if created_at_match:
            created_at = created_at_match.group(1)
            # 如果找到 sentiment，则更新 sentiment 变量
            if sentiment_match:
                sentiment = float(sentiment_match.group(1))
            
            print("Created At:", created_at)
            print("Sentiment:", sentiment)
        else:
            print("The required field 'created_at' is missing.")

    for row in islice(dataset.reader, 16):
        print(row)
        processRow(row)
        print()

