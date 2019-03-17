from .ngram_scraper import load_ngram_data
from random import choice, randint

with open("ngram_guesser/words.txt") as f:
    WORDS = [l.strip() for l in f.readlines()]

# with open("ngram_guesser/tags.txt") as f:
#     TAGS = [l.strip() for l in f.readlines()]

def random_bigram():
    word = choice(WORDS)
    tag = "*_ADJ"
    # ordering
    ## !! NOPE: for now always *_ADJ word
    return tag + " " + word

def create_challenge():
    while True:
        ngram = random_bigram()
        year = randint(1700, 2000)
        results = load_ngram_data(ngram, year)
        if len(results) >= 4:
            break
    results.sort(key=lambda x: x[1])
    results.reverse()

    correct = [results[i][0] for i in range(4)]
    indices = [i for i in range(4)]
    guesses = []
    for i in range(4):
        guesses.append(
            correct[
                indices.pop(
                    randint(0, len(indices) - 1)
                )
            ]
        )

    return {"correct": correct, "guesses": guesses, "year": year}

def evaluate_challenge(challenge, response):
    points = (10, 5, 2, 0)
    index = challenge["correct"].index(response)
    pts = points[index]
    msg = "Your answer was {}. The correct answer was {}, followed by {}. Your picked the answer with rank of {}. You get {} points. ".format(
        response,
        challenge["correct"][0],
        ", ".join([challenge["correct"][i] for i in range(1, len(challenge["correct"]))]),
        index + 1,
        pts)
    return pts, msg

def challenge_wording(challenge):
    ret = "Which of the following pairs was the most common in the year {}? ".format(challenge["year"])
    for i in range(len(challenge["guesses"])):
        word = challenge["guesses"][i]
        ret += "For, {}, repeating, {}, press {}, followed by a hash. ".format(word, word, i)
    return ret