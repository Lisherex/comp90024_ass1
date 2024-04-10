from mpi4py import MPI
import numpy as np
import re
import os
from typing import Iterator, Optional, Tuple

class Dataset:
    """
    Class for processing and analyzing a dataset containing sentiment and time information.

    Attributes:
        FILE_PATH (str): The file path to the dataset.
        comm: The MPI communicator.
        rank (int): The rank of the MPI process.
        size (int): The size of the MPI communicator (total number of processes).
        SHAPE (tuple): The shape of the arrays used for sentiment and count aggregation.
        patternFor_created_at (str): The regex pattern to extract the created_at time information from each row.
        patternFor_sentiment (str): The regex pattern to extract the sentiment information from each row.
        row_generator (Iterator[str]): An iterator over the rows of the file.
        sentiment_a (np.ndarray): An array to store aggregated sentiment scores.
        count_a (np.ndarray): An array to store counts of occurrences.
        countSum (np.ndarray): Aggregated counts after reduction to the master process.
        sentimentSum (np.ndarray): Aggregated sentiment scores after reduction to the master process.
    """
    def __init__(self, FILE_PATH: str, patternFor_created_at: str, patternFor_sentiment: str) -> None:
        """
        Initializes the Dataset object with file path, patterns for data extraction, and MPI settings.

        Args:
            FILE_PATH (str): The path to the dataset file.
            patternFor_created_at (str): Regex pattern for extracting 'created_at' field from the dataset.
            patternFor_sentiment (str): Regex pattern for extracting 'sentiment' field from the dataset.
        """
        self.FILE_PATH = FILE_PATH
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.SHAPE = (12, 31, 24)

        self.patternFor_created_at = patternFor_created_at
        self.patternFor_sentiment = patternFor_sentiment
        self.row_generator = None
        
        self.sentiment_a = np.zeros(shape=self.SHAPE, dtype=float)
        self.count_a = np.zeros(shape=self.SHAPE, dtype=float)

        self.countSum = None
        self.sentimentSum = None

    def initialize(self):
        """
        Initializes the data processing by reading the file, calculating sentiment scores for each hour,
        and performing MPI reduction to aggregate data on the master process.

        This method sets up the data structures necessary for analysis and aggregates data across
        MPI processes. It should be called after creating a Dataset instance and before performing
        any data analysis.
        """
        self.row_generator = self.readFile()
        self.calSentimentScoreForEachHour()
        self.sentimentSum, self.countSum = self.reduceToMaster()


    def readFile(self) -> Iterator[str]:
        """
        Reads and yields rows from the file based on the rank of the MPI process.

        Yields:
            str: A row from the file.
        """
        fileSize = os.path.getsize(self.FILE_PATH)
        # for unevenly divided data, the last rank get the rest data
        nodeReadSize = fileSize // self.size + (fileSize % self.size > self.rank)

        if self.rank == self.size - 1:
            nodeReadSize += fileSize % self.size

        node_beginRead = nodeReadSize * self.rank
        bytesRead = 0

        with open(self.FILE_PATH, "rb") as f:
            if self.rank > 0:
                f.seek(node_beginRead - 1)
                while True:
                    c = f.read(1)
                    bytesRead += 1
                    if c == b"\n" or bytesRead >= nodeReadSize:
                        break

            bytesRead = 0
            for row in f:
                if bytesRead + len(row) > nodeReadSize:
                    break
                try:
                    yield row.decode('utf-8', errors='replace')
                except UnicodeDecodeError:
                    continue
                bytesRead += len(row)

    def getData(self, row: str) -> Optional[Tuple[Tuple[str, str, str], Optional[float]]]:
        """
        Extracts relevant data from a row based on specified patterns.

        Args:
            patternFor_created_at (str): Regular expression pattern to match the 'created_at' field (raw string).
            patternFor_sentiment (str): Regular expression pattern to match the 'sentiment' field (raw string).
            row (str): The row from which data is to be extracted.

        Returns:
            Optional[Tuple[Tuple[str, str, str], Optional[float]]]: A tuple containing a tuple of time components (year, month, day) and the sentiment value, if available.
        """
        created_at_match = re.search(self.patternFor_created_at, row)
        sentiment_match = re.search(self.patternFor_sentiment, row)
        sentiment = 0

        # Check if 'created_at' is found
        if created_at_match:
            # Extract year, month, and day from the 'created_at' match
            created_at = created_at_match.group(1)
            year = created_at[5:7]
            month = created_at[8:10]
            day = created_at[11:13]
            time_components = (year, month, day)

            # If 'sentiment' is found, convert it to float
            if sentiment_match:
                try:
                    sentiment = float(sentiment_match.group(1))
                except ValueError:
                    pass
            return (time_components, sentiment)
        
        # If 'created_at' is not found, return None
        return None
    
    def calSentimentScoreForEachHour(self) -> None:
        """
        Calculates Sentiment Score for each hour of each day of each year based on rows from the generator.
        """
        for row in self.row_generator:
            processedRow = self.getData(row)
            if processedRow is not None:
                create_at, sentiment = processedRow
                try:
                    mm, dd, hh = map(int, create_at[:3])
                    self.count_a[mm-1][dd-1][hh-1] += 1
                    self.sentiment_a[mm-1][dd-1][hh-1] += sentiment
                except ValueError as e:
                    print(f"Error processing row {row}: {e}")


    def reduceToMaster(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Uses MPI reduce operation to aggregate sentiment_a and count_a arrays from all processes to the master process.

        Returns:
            Tuple[Optional[np.ndarray], Optional[np.ndarray]]: A tuple containing the aggregated sentiment_a and count_a arrays on the master process.
            Other processes will receive a tuple of None.
        """
        return self.comm.reduce(self.sentiment_a, op=MPI.SUM, root=0), self.comm.reduce(self.count_a, op=MPI.SUM, root=0)

    



    
