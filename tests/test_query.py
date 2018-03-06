# -*- coding: utf-8 -*-
import unittest
from .context import QueryParser


class TestQueryParser(unittest.TestCase):

    def setUp(self):
        self.query_parser = QueryParser()

    def test_drop_morph(self):
        test = '東京にある美味しいカレーが食べたいです'
        expected = ['カレー']

        self.query_parser.drop_morph(test)

        actual = self.query_parser.words

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()