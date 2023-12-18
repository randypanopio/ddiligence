import random
from datetime import date



# TODO migrate to db
def retrieve_daily_messages():
    # Simulate a list of messages retrieved from an SQL database
    messages = [
        {"author": "Common Finance Mantra",
         "message": "Past Performance is Not Indicative of Future Results."},

        {"author": "Latin Proverb",
         "message": "Audentes Fortuna Iuvat - Fortune Favours the Brave"},

        {"author": "Abraham Lincoln",
         "message": "You cannot escape the responsibility of tomorrow by evading it today."},

        {"author": "Confucius",
         "message": "When prosperity comes, do not use all of it"},


        {"author": "Federal Reserve, sometimes",
         "message": "Money Printer Go Brrr"},

        {"author": "Benjamin Graham",
         "message": "To be an investor you must be a believer in a better tomorrow."},
        {"author": "Benjamin Graham",
         "message": "Investing isn't about beating others at their game. It's about controlling yourself at your own game."},
        {"author": "Benjamin Graham",
                   "message": "The intelligent investor is a realist who sells to optimists and buys from pessimists."},

        {"author": "Warren Buffett",
         "message": "Rule No. 1 is never lose money. Rule No. 2 is never forget Rule No. 1."},
        {"author": "Warren Buffett",
         "message": "The most important thing to do if you find yourself in a hole is to stop digging."},
        {"author": "Warren Buffett",
         "message": "The most important quality for an investor is temperament, not intellect."},
        {"author": "Warren Buffett",
                   "message": "The most important investment you can make is in yourself."},
        {"author": "Warren Buffett",
                   "message": "Never invest in a business you cannot understand."},



        {"author": "/r/wallstreetbets",
         "message": "What's an exit strategy?"},
        {"author": "/r/wallstreetbets",
         "message": "Diamond Hands > Paper Hands"},
        {"author": "/r/wallstreetbets",
         "message": "To the moon!"},
    ]
    # randomly choose 10 from db, for now done here, but query should be doing this randomizing
    random.seed(str(date.today()))
    random.shuffle(messages)
    return messages[:10] # return capped 10
