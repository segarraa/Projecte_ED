# -*- coding: utf-8 -*-
"""
SearchMetadata.py : cerques per metadades (Func6)
"""


class SearchMetadata:

    def __init__(self, image_data):
        self.data = image_data

    def _cerca(self, getter, sub: str) -> list:
        resultat = []
        if sub is None:
            return resultat
        sub = str(sub)
        for uuid in self.data.get_uuids():
            valor = getter(uuid)
            if valor is not None and str(valor).find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def prompt(self, sub: str) -> list:
        return self._cerca(self.data.get_prompt, sub)

    def model(self, sub: str) -> list:
        return self._cerca(self.data.get_model, sub)

    def seed(self, sub: str) -> list:
        return self._cerca(self.data.get_seed, sub)

    def cfg_scale(self, sub: str) -> list:
        return self._cerca(self.data.get_cfg_scale, sub)

    def steps(self, sub: str) -> list:
        return self._cerca(self.data.get_steps, sub)

    def sampler(self, sub: str) -> list:
        return self._cerca(self.data.get_sampler, sub)

    def date(self, sub: str) -> list:
        return self._cerca(self.data.get_created_date, sub)

    def generated(self, sub: str) -> list:
        return self._cerca(self.data.get_generated, sub)

    def dimensions(self, width: int, height: int) -> list:
        resultat = []
        try:
            buscat = (int(width), int(height))
        except (TypeError, ValueError):
            return resultat
        for uuid in self.data.get_uuids():
            if self.data.get_dimensions(uuid) == buscat:
                resultat.append(uuid)
        return resultat

    def and_operator(self, list1: list, list2: list) -> list:
        # els que són a les dues llistes
        list1 = list1 or []
        segona = set(list2 or [])
        resultat = []
        for uuid in list1:
            if uuid in segona and uuid not in resultat:
                resultat.append(uuid)
        return resultat

    def or_operator(self, list1: list, list2: list) -> list:
        # els d'alguna de les dues, sense repetir
        resultat = []
        for uuid in (list1 or []) + (list2 or []):
            if uuid not in resultat:
                resultat.append(uuid)
        return resultat

    def __str__(self):
        return f"SearchMetadata ({len(self.data)} imatges)"
