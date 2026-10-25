# -*- coding: utf-8 -*-
"""
Gallery.py : galeries d'imatges en JSON (Func5 i Func7)
"""

import json
import os
import cfg


class Gallery:

    def __init__(self, image_id, image_viewer):
        self.ids = image_id
        self.viewer = image_viewer
        self.nom = ""
        self.descripcio = ""
        self.data = ""
        self.imatges = []   # llista d'UUIDs en ordre

    def load_file(self, file: str):
        self.nom = ""
        self.descripcio = ""
        self.data = ""
        self.imatges = []

        try:
            with open(file, "r", encoding="utf-8") as f:
                galeria = json.load(f)
        except Exception as e:
            print(f"No es pot llegir la galeria {file}: {e}")
            return

        if not isinstance(galeria, dict):
            print(f"La galeria {file} no té el format correcte")
            return

        self.nom = galeria.get("gallery_name", "")
        self.descripcio = galeria.get("description", "")
        self.data = galeria.get("created_date", "")

        imatges = galeria.get("images", [])
        if not isinstance(imatges, list):
            return

        # només afegeixo les imatges que existeixen a la col·lecció
        for path in imatges:
            if not isinstance(path, str):
                continue
            uuid = self._buscar_uuid(path)
            if uuid is None:
                print(f"AVÍS: la imatge {path} no és a la col·lecció")
            else:
                self.imatges.append(uuid)

    def _buscar_uuid(self, path: str) -> str:
        # provo el path tal qual i el path canonic
        path = path.replace("\\", "/")
        uuid = self.ids.get_uuid(path)
        if uuid is None:
            uuid = self.ids.get_uuid(cfg.get_canonical_pathfile(path))
        if uuid is None and "/" in path:
            uuid = self.ids.get_uuid(path.split("/", 1)[1])
        return uuid

    def show(self):
        print(f"\nGaleria: {self.nom}")
        print(f"Descripció: {self.descripcio}")
        print(f"Data: {self.data}")
        print(f"Imatges: {len(self.imatges)}")
        for uuid in self.imatges:
            self.viewer.show_image(uuid, cfg.DISPLAY_MODE)

    def add_image_at_end(self, uuid: str):
        self.imatges.append(uuid)

    def remove_first_image(self):
        if self.imatges:
            self.imatges.pop(0)

    def remove_last_image(self):
        if self.imatges:
            self.imatges.pop()

    def __len__(self):
        return len(self.imatges)

    def __str__(self):
        return f"Gallery '{self.nom}': {len(self.imatges)} imatges"
