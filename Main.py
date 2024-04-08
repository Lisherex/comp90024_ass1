#import time

#import json
#import ijson
#from pyspark import SparkContext
from mpi4py import MPI
import os
from itertools import islice

filePathes = [
    "data/twitter-1mb.json",
    "data/twitter-50mb.json"
]

class Dataset:
    def __init__(self, filePath: str = filePathes[1], skipFirstAndLast: str = True) -> None:
        self.filePath = filePath
        self.reader = self.genFilesReader(skipFirstAndLast)
        self.rank = rank
        self.size = size

    def genFilesReader(self, skipFirstAndLast:str = True):
        f_size = os.path.getsize(self.filePath)
        node_size = f_size//self.size
        starting = self.rank * node_size
        bytes_read = 0

        with open(self.filePath, encoding='utf-8') as f:
            f.seek(starting, 0)
            iterator = iter(f)
            if skipFirstAndLast:
                next(iterator, None)
                prev_row = next(iterator, None)
                for current_row in iterator:
                    if self.rank == 0 or bytes_read > 0:
                        yield prev_row
                    bytes_read += len(current_row)
                    prev_row = current_row
            else:
                for row in iterator:
                    if self.rank == 0 or bytes_read > 0:
                        yield row
                    bytes_read += len(row)
        f.close()


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

    # get the happiest hour -> [mmdd, hh], double
    def happiest_hour(s_d):
        temp_max = 0
        happy_hour = None
        for mmdd in s_d.keys():
            for hh in s_d[mmdd].keys():
                if s_d[mmdd][hh] > temp_max:
                    temp_max = s_d[mmdd][hh]
                    happy_hour = [mmdd, hh]
        return happy_hour, temp_max

    # get the happiest day -> mmdd, int
    def happiest_day(s_d):
        temp_max = 0
        happy_day = None
        for mmdd in s_d.keys():
            day_sum = 0
            for hh in s_d[mmdd].keys():
                day_sum += s_d[mmdd][hh]
                if day_sum > temp_max:
                    temp_max = day_sum
                    happy_day = mmdd
        return happy_day, temp_max

    # most active hour -> [mmdd, hh], double
    def active_hour(c_d):
        temp_max = 0
        active_hour = None
        for mmdd in c_d.keys():
            for hh in c_d[mmdd].keys():
                if c_d[mmdd][hh] > temp_max:
                    temp_max = c_d[mmdd][hh]
                    active_hour = [mmdd, hh]
        return active_hour, temp_max

    # get the active day -> mmdd, int
    def active_day(c_d):
        temp_max = 0
        active_day = None
        for mmdd in c_d.keys():
            day_sum = 0
            for hh in c_d[mmdd].keys():
                day_sum += c_d[mmdd][hh]
                if day_sum > temp_max:
                    temp_max = day_sum
                    active_day = mmdd
        return active_day, temp_max

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    dataset = Dataset(size, rank)

    # create dict for sum_sentiment sentiment_d = {[mmdd]:{[hh]: sum_sentiment}}
    sentiment_d = {}
    # create dict for twitter_count count_d = {[mmdd]:{[hh]: count}}
    count_d = {}

    #for row in islice(dataset.reader, 16):
        #processRow(row, sentiment_d, count_d)

    for row in dataset.reader:
        processRow(row, sentiment_d, count_d)


    if rank == 0:
        happy_hour, max_hour = happiest_hour(sentiment_d)
        happy_day, max_day = happiest_day(sentiment_d)
        active_hour, hour_count = active_hour(count_d)
        active_day, day_count = active_day(count_d)
        print(happy_hour, max_hour,happy_day, max_day,active_hour, hour_count,active_day, day_count)





