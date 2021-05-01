import json
import logging
from configparser import ConfigParser
import asyncpraw

config_object = ConfigParser()
config_object.read("resources/config.ini")
reddit_config = config_object["REDDIT"]

logging.basicConfig(format="%(asctime)s | %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")


async def get_reddit_crypto_trends():

    reddit = asyncpraw.Reddit(
        client_id=reddit_config["client_id"],
        client_secret=reddit_config["client_secret"],
        user_agent=reddit_config["user_agent"],
        username=reddit_config["username"],
        password=reddit_config["password"],
    )

    subredditname = "cryptocurrency"

    subreddit = await reddit.subreddit(subredditname)

    count = 0
    max_comments = 10000
    logging.warning("Connected to reddit API. Working...")
    words = []
    word_count = {}
    with open("resources/word_bank.json") as file:
        word_bank = json.load(file)

    bad_word_bank = [
        "just",
        "fun",
        "Fun",
        "one",
        "One",
        "Etc",
        "etc",
        "JUST",
        "Just",
        "hot",
        "Hot",
        "swap",
        "Swap",
        "near",
        "Near",
        "Win",
        "win",
    ]

    with open("resources/structured_word_bank.json") as file:
        structured_word_bank = json.load(file)

    async for submission in subreddit.top("day", limit=500):
        comments = await submission.comments()
        await comments.replace_more(limit=0)
        for top_level_comment in comments:
            count += 1
            if count == max_comments:
                break
            word = ""
            for letter in top_level_comment.body:
                if letter == " ":
                    if word and not word[-1].isalnum():
                        word = word[:-1]
                    if word.lower() in word_bank and word not in bad_word_bank:
                        words.append(word.lower())
                    elif word.upper() in word_bank and word not in bad_word_bank:
                        words.append(word.upper())
                    word = ""
                else:
                    word += letter
        if count == max_comments:
            break

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    sorted_list = {
        k: v for k, v in sorted(word_count.items(), key=lambda item: item[1])
    }

    for item in structured_word_bank:
        item.append(0)
    for word in sorted_list:
        for item in structured_word_bank:
            if word in item:
                item[2] = item[2] + sorted_list[word]

    sorted_words = sorted(structured_word_bank, key=lambda x: x[2], reverse=True)
    reddit_trending_currencies = [x for x in sorted_words if x[2] > 0]
    logging.warning("Reddit scrape successful.")
    await reddit.close()
    return reddit_trending_currencies
