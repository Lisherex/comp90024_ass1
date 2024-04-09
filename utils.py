import os
import re


# read file by lazy read
def read_file(FILE_PATH, rank, size):
    f_size = os.path.getsize(FILE_PATH)

    # get size for 1 node to read
    node_read_size = f_size // size

    # the starting point of each node
    node_begin = node_read_size * rank
    bytes_read = 0

    f = open(FILE_PATH, 'rb')
    f.seek(node_begin)

    for line in f:
        if rank == 0 or bytes_read > 0:
            yield line.decode()

        bytes_read += len(line)
        if bytes_read >= node_read_size:
            break

    f.close()


# get created at from line
def get_content(line):
    created_at_match = re.search(r'"created_at":"(.*?)"', line)
    sentiment_match = re.search(r'"sentiment":([-\d.]+)', line)
    sentiment = 0

    if created_at_match:
        created_at = created_at_match.group(1)
        if sentiment_match:
            sentiment = float(sentiment_match.group(1))

        time_created = [created_at[5:7], created_at[8:10], created_at[11:13]]
        return tuple(time_created), sentiment

    else:
        return None

def happiest_hour(s_a):
    temp_max = 0
    happy_hour = None
    for mm in range(12):
        for dd in range(31):
            for hh in range(24):
                if s_a[mm][dd][hh] > temp_max:
                    temp_max = s_a[mm][dd][hh]
                    happy_hour = [mm, dd, hh]
    return happy_hour, temp_max

def happiest_day(s_a):
    temp_max = 0
    happy_day = None
    for mm in range(12):
        for dd in range(31):
            day_sum = 0
            for hh in range(24):
                day_sum += s_a[mm][dd][hh]
            if day_sum > temp_max:
                temp_max = day_sum
                happy_day = [mm, dd]
    return happy_day, temp_max

def most_active_hour(c_a):
    temp_max = 0
    active_hour = None
    for mm in range(12):
        for dd in range(31):
            for hh in range(24):
                if c_a[mm][dd][hh] > temp_max:
                    temp_max = c_a[mm][dd][hh]
                    active_hour = [mm, dd, hh]
    return active_hour, temp_max

def most_active_day(c_a):
    temp_max = 0
    active_day = None
    for mm in range(12):
        for dd in range(31):
            day_sum = 0
            for hh in range(24):
                day_sum += c_a[mm][dd][hh]
            if day_sum > temp_max:
                temp_max = day_sum
                active_day = [mm, dd]
    return active_day, temp_max