from mpi4py import MPI
import numpy as np
from utils import *

FILE_PATH = 'data/twitter-50mb.json'

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

SHAPE = (12, 31, 24)
sentiment_a = np.zeros(shape=SHAPE, dtype=float)
count_a = np.zeros(shape=SHAPE, dtype=float)

for line in read_file(FILE_PATH, rank, size):
    if get_content(line) is not None:
        create_at, sentiment = get_content(line)
        count_a[create_at[0]-1, create_at[1]-1, create_at[2]-1] += 1
        sentiment_a[create_at[0]-1, create_at[1]-1, create_at[2]-1] += sentiment

total_sentiment_a = comm.reduce(sentiment_a, op=MPI.SUM, root=0)
total_count_a = comm.reduce(count_a, op=MPI.SUM, root=0)

if rank == 0:
    happy_hour, hour_sentiment = happiest_hour(total_sentiment_a)
    happy_day, day_sentiment = happiest_day(total_sentiment_a)
    active_hour, hour_count = most_active_hour(total_count_a)
    active_day, day_count = most_active_day(total_count_a)