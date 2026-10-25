# -*- coding: utf-8 -*-
"""
ImageFiles.py : llistat dels arxius PNG de la col·lecció (Func1)
"""

import os


class ImageFiles:

    def __init__(self):
        # llistes de paths
        self.actuals = []
        self.anteriors = []

    def reload_fs(self, path: str):
        # guardo l'estat d'abans per poder comparar
        self.anteriors = self.actuals
        self.actuals = []

        if not os.path.isdir(path):
            return

        for carpeta, subcarpetes, fitxers in os.walk(path):
            for nom in fitxers:
                if nom.lower().endswith(".png"):
                    complet = os.path.join(carpeta, nom).replace(os.sep, "/")
                    self.actuals.append(complet)

    def files_added(self) -> list:
        # els que hi són ara i abans no
        anteriors = set(self.anteriors)
        return [f for f in self.actuals if f not in anteriors]

    def files_removed(self) -> list:
        # els que hi eren abans i ara no
        actuals = set(self.actuals)
        return [f for f in self.anteriors if f not in actuals]

    def __len__(self):
        return len(self.actuals)

    def __str__(self):
        return f"ImageFiles: {len(self.actuals)} arxius"
