from .ngram_scraper import load_ngram_data
from random import choice, randint

with open("hack/words.txt") as f:
    WORDS = [l.strip() for l in f.readlines()]

with open("hack/tags.txt") as f:
    TAGS = [l.strip() for l in f.readlines()]

def random_bigram():
    word = choice(WORDS)
    tag = "*_ADJ"
    # ordering
    ## !! NOPE: for now always *_ADJ word
    return tag + " " + word

def create_challenge():
    while True:
        ngram = random_bigram()
        results = load_ngram_data(ngram, randint(1700, 2000))
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

    return {"correct": correct, "guesses": guesses}

def evaluate_challenge(challenge, response):
    points = (10, 5, 2, 0)
    return points[challenge["correct"].index(response)]
