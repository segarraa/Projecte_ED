# -*- coding: utf-8 -*-
"""
ImageID.py : generació i gestió dels UUID de les imatges (Func2)
"""

import cfg


class ImageID:

    def __init__(self):
        # diccionari uuid -> path de l'arxiu
        self.uuids = {}

    def generate_uuid(self, file: str) -> str:
        uuid = str(cfg.get_uuid(file))

        # si ja existeix, l'arxiu nou no es fa servir
        if uuid in self.uuids:
            print(f"AVÍS: UUID repetit, l'arxiu {file} no s'utilitzarà")
            return None

        self.uuids[uuid] = file
        return uuid

    def get_uuid(self, file: str) -> str:
        # només el retorna si està generat i actiu
        uuid = str(cfg.get_uuid(file))
        if uuid in self.uuids:
            return uuid
        return None

    def remove_uuid(self, uuid: str):
        if uuid in self.uuids:
            del self.uuids[uuid]

    def get_file(self, uuid: str) -> str:
        return self.uuids.get(uuid)

    def __len__(self):
        return len(self.uuids)

    def __str__(self):
        return f"ImageID: {len(self.uuids)} UUIDs"
