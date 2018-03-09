# -*- coding: utf-8 -*-
import re
from typing import (
    List,
    Optional,
    Union,
    Tuple,
    Set
)

import numpy as np
from pyknp import (
    Juman,
    Jumanpp,
    KNP,
    BList,
    Bunsetsu,
    Tag
)

from .word2vec import Word2VecModel

__all__ = ['Analyst']


class Analyst:

    def __init__(
            self, word2vec_model: Word2VecModel,
            juman_command: str='jumanpp',
            specific_parts: Optional[List[str]]=None
    ) -> None:
        if specific_parts is None:
            specific_parts = ['普通名詞']

        if juman_command == 'juman':
            self.juman: Union[Juman, Jumanpp] = Juman()
        elif juman_command == 'jumanpp':
            self.juman: Union[Juman, Jumanpp] = Jumanpp()
        else:
            raise AttributeError
        self.knp: KNP = KNP(jumancommand=juman_command)

        self.specific_parts: List[str] = specific_parts

        self.word2vec: Word2VecModel = word2vec_model

    def parse(self, sentence: str)\
            -> Tuple[List[str], List[Optional[Tuple[Set[Optional[str]], Set[Optional[str]]]]]]:
        sentence: str = sentence.replace(' ', '').replace('　', '').replace('\n', '').replace('\t', '')

        candidates: List[str] = [elem for elem in re.split(r'。', sentence) if elem != '']
        morph_sets: List[Optional[Tuple[List[str], List[str]]]] = []

        for i, candidate in enumerate(candidates):
            try:
                knp_result: BList = self.knp.parse(candidate)
            except:
                candidates.pop(i)
                continue

            bnst_list: List[Bunsetsu] = knp_result.bnst_list()

            child_morphs: Set[Optional[str]] = set()
            parent_morphs: Set[Optional[str]] = set()

            for bnst in bnst_list:
                for tag in bnst.tag_list():
                    child_morphs = self.append_morphs(child_morphs, tag)
                    parent_morphs = self.append_morphs(parent_morphs, tag.parent)

            child_morphs -= child_morphs & parent_morphs
            parent_morphs -= child_morphs & parent_morphs

            morph_sets.append((list(child_morphs), list(parent_morphs)))

        return (candidates, morph_sets)

    def calc_query_base_score(
            self,
            candidates: List[str],
            morph_sets: Tuple[List, List],
            query_words: List[str]
    ) -> List[float]:
        query_base_scores: List[Optional[float]] = []

        for candidate, morph_set in zip(candidates, morph_sets):
            score: float = 0.0
            length: int = 0

            for query_word in query_words:
                for morph in morph_set[0] | morph_set[1]:
                    length += 1
                    try:
                        score += abs(self.word2vec.similarity(query_word, morph))
                    except KeyError:
                        continue

            # 正規化
            if score != 0.0:
                score /= length

            query_base_scores.append(score)

        return query_base_scores

    def calc_candidate_score(self, candidates: List[str], morph_sets: Tuple[List, List]) -> List[float]:
        candidate_scores: List[Optional[float]] = []

        for candidate, morph_set in zip(candidates, morph_sets):
            score: float = 0.0
            length: int = 0

            for child_morph in morph_set[0]:
                for parent_morph in morph_set[1]:
                    length += 1
                    try:
                        score += abs(self.word2vec.similarity(child_morph, parent_morph))
                    except KeyError:
                        continue

            # 正規化
            if score != 0.0:
                score /= length

            candidate_scores.append(score)

        return candidate_scores

    @staticmethod
    def most_significant_candidates(scores: List[float], candidates: List[str]) -> Optional[List[str]]:
        try:
            assert len(candidates) == len(scores)
        except AssertionError:
            return None

        sorted_score_indices = np.argsort(scores)[::-1][:3]

        significant_candidates: List[str] = []

        for i in sorted_score_indices:
            significant_candidates.append(candidates[i])

        return significant_candidates

    def append_morphs(self, morphs: Set[Optional[str]], tag: Optional[Tag])\
            -> Set[Optional[str]]:
        if tag is None:
            return morphs

        for morph in tag.mrph_list():
            if morph.bunrui in self.specific_parts:
                morphs.add(morph.midasi)

        return morphs
