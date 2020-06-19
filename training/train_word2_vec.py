import argparse
from string import ascii_letters, digits

import pandas as pd
from gensim.models import Word2Vec
from gensim.models import phrases
from nltk.data import load

from training.utils import stripword

translator = str.maketrans(ascii_letters, ascii_letters, digits)
tokenizer = load('tokenizers/punkt/english.pickle')


def main(args):
    data = pd.read_csv(args['data_csv'], index_col=0)
    sentences = [stripword(row.translate(translator).lower).split(' ') for row in data['Sentence']]
    bigram_transformer = phrases.Phrases(sentences)
    bigram = phrases.Phraser(bigram_transformer)
    currentmodel = Word2Vec(bigram[sentences], workers=-1, sg=0, size=args['model_size'], min_count=5,
                            window=['window_size'], sample=1e-3)
    currentmodel.init_sims(replace=True)
    currentmodel.save("app/word2vec/word2vec_retrained")
    print('Saved as app/word2vec/word2vec_retrained')


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="train classifier"
    )
    parser.add_argument(
        "-d", "--data_csv", help="the csv data file to train the model on",
        default='data/raw/coronavirus_news_sentences.csv', required=False
    )
    parser.add_argument(
        "-w", "--window_size", help="size of word2vec window",
        default=5, required=False, type=int
    )
    parser.add_argument(
        "-s", "--model_size", help="size of word2vec model",
        default=100, required=False, type=int
    )
    return parser


if __name__ == "__main__":
    # execute only if run as a script
    parser = init_argparse()
    args = parser.parse_args()
    main(vars(args))
