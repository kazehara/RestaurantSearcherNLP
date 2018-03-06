# -*- coding: utf-8 -*-
import unittest
from .context import Analyst, Word2VecModel


TEST_SENTENCE = '東京近辺で美味しいカレーが食べられるお店です'


class TestAnalyst(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.word2vec = Word2VecModel('models/word2vec.gensim.model')

    def setUp(self):
        self.analyst = Analyst(self.word2vec)

    def test_parse(self):
        expected_candidates = ['東京近辺で美味しいカレーが食べられるお店です']
        expected_morph_sets = [(set(), {'近辺', '店', 'カレー'})]

        self.analyst.parse(TEST_SENTENCE)

        actual_candidates = self.analyst.candidates
        actual_morph_sets = self.analyst.morph_sets

        self.assertEqual(expected_candidates, actual_candidates)
        self.assertEqual(expected_morph_sets, actual_morph_sets)

    def test_calc_query_base_score(self):
        self.analyst.parse(TEST_SENTENCE)

        actual = self.analyst.calc_query_base_score(['カレー', 'パスタ'])

        self.assertEqual(len(actual), min(len(self.analyst.candidates), len(self.analyst.morph_sets)))
        self.assertLessEqual(sum(actual) / len(actual), 1)

    def test_calc_candidate_score(self):
        self.analyst.parse(TEST_SENTENCE)

        actual = self.analyst.calc_candidate_score()

        self.assertEqual(len(actual), len(self.analyst.candidates))
        self.assertLessEqual(sum(actual) / len(actual), 1)

    def test_most_significant_candidates(self):
        scores = [0.9, 0.2, 0.5, 0.4, 0.8, 0.6, 0.1]
        candidates = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        expected = ['a', 'e', 'f']
        actual = self.analyst.most_significant_candidates(scores, candidates)

        self.assertEqual(expected, actual)

    def test_append_morphs(self):
        # Already tested by analyst.parse
        pass


if __name__ == '__main__':
    unittest.main()
