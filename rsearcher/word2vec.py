# -*- coding: utf-8 -*-
from typing import List, Tuple

from gensim.models.word2vec import Word2Vec

__all__ = ['Word2VecModel']


class Word2VecModel:

    def __init__(self, path_model: str):
        self.model: Word2Vec = Word2Vec.load(path_model)

    def similar_words(self, query_words: List[str], threshold: float=0.9)\
            -> List[Tuple[str, float]]:
        word_pairs: List[Tuple[str, float]] = []

        for word in query_words:
            word_pairs.append((word, 1.0))

            similar_pairs: List[Tuple[str, float]] = self.model.most_similar(word)

            for pair in similar_pairs:
                if pair[1] > threshold:
                    word_pairs.append(pair)

        return word_pairs

    @staticmethod
    def most_significant_word_pairs(word_pairs: List[Tuple[str, float]], threshold: float=0.9)\
            -> List[Tuple[str, float]]:
        sorted_pairs: List[Tuple[str, float]] = sorted(word_pairs, key=lambda x: x[1], reverse=True)
        for i, pair in enumerate(sorted_pairs):
            if pair[1] <= threshold:
                sorted_pairs.pop(i)

        return sorted_pairs

    def similarity(self, source: str, target: str)\
            -> float:
        return self.model.similarity(source, target)
