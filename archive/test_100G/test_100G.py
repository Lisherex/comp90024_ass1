from mpi4py import MPI
import numpy as np
from utils import *

FILE_PATH = '/data/gpfs/projects/COMP90024/twitter-100gb.json'

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

SHAPE = (12, 31, 24)
sentiment_a = np.zeros(shape=SHAPE, dtype=float)
count_a = np.zeros(shape=SHAPE, dtype=float)

for line in read_file(FILE_PATH, rank, size):
    if get_content(line) is not None:
        create_at, sentiment = get_content(line)
        mm, dd, hh = int(create_at[0]), int(create_at[1]), int(create_at[2])
        count_a[mm-1][dd-1][hh-1] += 1
        sentiment_a[mm-1][dd-1][hh-1] += sentiment

total_sentiment_a = comm.reduce(sentiment_a, op=MPI.SUM, root=0)
total_count_a = comm.reduce(count_a, op=MPI.SUM, root=0)

if rank == 0:
    happy_hour, hour_sentiment = happiest_hour(total_sentiment_a)
    happy_day, day_sentiment = happiest_day(total_sentiment_a)
    active_hour, hour_count = most_active_hour(total_count_a)
    active_day, day_count = most_active_day(total_count_a)

    print('The Happiest Hour:', happy_hour, 'with sentiment of', hour_sentiment)
    print('The Happiest Day:', happy_day, 'with sentiment of', day_sentiment)
    print('The Most Active Hour:', active_hour, 'with tweets of', hour_count)
    print('The Happiest Hour:', active_day, 'with sentiment of', day_count)
