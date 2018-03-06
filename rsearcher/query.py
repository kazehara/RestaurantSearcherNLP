# -*- coding: utf-8 -*-
import re
from typing import List, Optional

from pyknp import Jumanpp, Bunsetsu

__all__ = ['QueryParser']


class QueryParser:

    def __init__(self, specific_parts: Optional[List[str]]=None, specific_domains: Optional[List[str]]=None):
        self.juman: Jumanpp = Jumanpp()
        if specific_parts is None:
            specific_parts: List[str] = ['普通名詞']
        if specific_domains is None:
            specific_domains: List[str] = ['料理・食事']
        self.specific_parts: List[str] = specific_parts
        self.specific_domains: List[str] = specific_domains

        self.words: Optional[List[str]] = None

    def drop_morph(self, query: str) -> None:
        self.words: List[str] = []
        morphed_query: Bunsetsu = self.juman.analysis(query)

        for morph in morphed_query.mrph_list():
            if morph.bunrui in self.specific_parts:
                # 固有名詞はドメイン解析無用
                if morph.bunrui == '固有名詞':
                    self.words.append(morph.midasi)
                    continue

                domain_candidates: List[str] = re.findall(r'ドメイン:.*$', morph.imis)

                domain: str = ''
                if len(domain_candidates) > 0:
                    domain: str = domain_candidates[0].replace('ドメイン:', '')
                if domain in self.specific_domains or len(domain_candidates) == 0:
                    self.words.append(morph.midasi)




