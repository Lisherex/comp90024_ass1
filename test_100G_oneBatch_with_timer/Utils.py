import numpy as np
from typing import Optional, Tuple

class Utils:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def getHappiestHour(sentimentSum: Optional[np.ndarray]) -> Tuple[np.ndarray, float]:
        """
        Finds the hour with the highest sentiment sum.

        Args:
            sentimentSum (Optional[np.ndarray]): A 3D numpy array containing sentiment sums, where
                dimensions represent month, day, and hour, respectively.

        Returns:
            Tuple[np.ndarray, float]: A tuple containing the happiest hour in [month, day, hour] format
            and the sentiment sum for that hour. Indices start from 1 to match natural date/time representation.
        """
        max_val = np.max(sentimentSum)
        max_pos = np.unravel_index(np.argmax(sentimentSum), sentimentSum.shape)
        # index from 0, so add 1 to restore to natural year/month/hour/
        happy_hour = [max_pos[0] + 1, max_pos[1] + 1, max_pos[2] + 1]
        return happy_hour, max_val
    
    @staticmethod
    def getHappiestDay(sentimentSum: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Identifies the day with the highest cumulative sentiment.

        Args:
            sentimentSum (np.ndarray): A 3D numpy array of sentiment sums, with dimensions representing
                month, day, and hour.

        Returns:
            Tuple[np.ndarray, float]: A tuple containing the happiest day in [month, day] format
            and the total sentiment sum for that day. Indices start from 1 for natural date representation.
        """
        day_sums = np.sum(sentimentSum, axis=2)
        temp_max = np.max(day_sums)
        happy_day_idx = np.unravel_index(np.argmax(day_sums), day_sums.shape)
        happy_day = [happy_day_idx[0] + 1, happy_day_idx[1] + 1]
        return happy_day, temp_max
    
    @staticmethod
    def getMostActiveHour(countSum: np.ndarray) ->  Tuple[np.ndarray, float]:
        """
        Determines the hour with the highest activity, based on counts.

        Args:
            countSum (np.ndarray): A 3D numpy array containing counts, where dimensions are month, day, and hour.

        Returns:
            Tuple[np.ndarray, float]: A tuple containing the most active hour in [month, day, hour] format
            and the count for that hour. Indices are adjusted to start from 1 for natural date/time representation.
        """
        temp_max = np.max(countSum)
        active_hour_idx = np.unravel_index(np.argmax(countSum), countSum.shape)
        # index from 0, so add 1 to restore to natural year/month/hour/
        active_hour = [active_hour_idx[0] + 1, active_hour_idx[1] + 1, active_hour_idx[2] + 1]
        return active_hour, temp_max

    @staticmethod
    def getMostActiveDay(countSum: np.ndarray) ->  Tuple[np.ndarray, float]:
        """
        Finds the day with the highest total activity count.

        Args:
            countSum (np.ndarray): A 3D numpy array of counts, with dimensions for month, day, and hour.

        Returns:
            Tuple[np.ndarray, float]: A tuple with the most active day in [month, day] format
            and the total count for that day. Indices start from 1 to match natural date representation.
        """
        day_sums = np.sum(countSum, axis=2)
        temp_max = np.max(day_sums)
        active_day_idx = np.unravel_index(np.argmax(day_sums), day_sums.shape)
        # index from 0, so add 1 to restore to natural year/month/hour/
        active_day = [active_day_idx[0] + 1, active_day_idx[1] + 1]
        return active_day, temp_max