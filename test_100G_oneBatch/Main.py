from Dataset import Dataset
from Utils import Utils

if __name__ == "__main__":
    FILE_PATH = r'/data/gpfs/projects/COMP90024/twitter-100gb.json'
    patternFor_created_at = r'"created_at":"(.*?)"'
    patternFor_sentiment = r'"sentiment":([-\d.]+)'

    twitterData = Dataset(FILE_PATH, patternFor_created_at, patternFor_sentiment)
    twitterData.initialize()

    if twitterData.rank == 0:
        happy_hour, hour_sentiment = Utils.getHappiestHour(twitterData.sentimentSum)
        happy_day, day_sentiment = Utils.getHappiestDay(twitterData.sentimentSum)
        active_hour, hour_count = Utils.getMostActiveHour(twitterData.countSum)
        active_day, day_count = Utils.getMostActiveDay(twitterData.countSum)

        print('The Happiest Hour:', happy_hour, 'with sentiment of', hour_sentiment)
        print('The Happiest Day:', happy_day, 'with sentiment of', day_sentiment)
        print('The Most Active Hour:', active_hour, 'with tweets of', hour_count)
        print('The Most Active day:', active_day, 'with tweets of', day_count)