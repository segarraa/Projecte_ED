# -*- coding: utf-8 -*-
"""
ImageData.py : metadades de les imatges (Func3)
"""

import os
import cfg

CAMPS = ["Prompt", "Model", "Seed", "CFG_Scale", "Steps",
         "Sampler", "Generated", "Created_Date"]


class ImageData:

    def __init__(self):
        # diccionari uuid -> diccionari amb el path i les metadades
        self.imatges = {}

    def add_image(self, uuid: str, file: str):
        # si l'arxiu no existeix no l'afegeixo
        if uuid is None or file is None:
            return
        if not os.path.isfile(self._path_real(file)):
            return
        # només guardo el path, les metadades queden buides (None)
        dades = {"file": file, "width": None, "height": None}
        for camp in CAMPS:
            dades[camp] = None
        self.imatges[uuid] = dades

    def remove_image(self, uuid: str):
        if uuid in self.imatges:
            del self.imatges[uuid]

    def _path_real(self, file: str) -> str:
        if os.path.isfile(file):
            return file
        path = os.path.join(cfg.ROOT_DIR, file)
        if os.path.isfile(path):
            return path
        # per si ve amb "../" davant
        net = file
        while net.startswith("../"):
            net = net[3:]
        return os.path.join(cfg.ROOT_DIR, net)

    def load_metadata(self, uuid: str):
        if uuid not in self.imatges:
            return

        dades = self.imatges[uuid]
        path = self._path_real(dades["file"])

        if not os.path.isfile(path):
            return
        meta = cfg.read_png_metadata(path)
        if meta is None:
            meta = {}

        # si un camp no hi és, queda None
        for camp in CAMPS:
            valor = meta.get(camp)
            dades[camp] = str(valor) if valor is not None else None

        dades["width"], dades["height"] = self._llegir_dimensions(path)

    def _llegir_dimensions(self, path: str):
        # les dimensions estan al chunk IHDR
        try:
            with open(path, "rb") as f:
                cap = f.read(24)
            amplada = int.from_bytes(cap[16:20], "big")
            alcada = int.from_bytes(cap[20:24], "big")
            return amplada, alcada
        except Exception:
            return None, None

    def _get(self, uuid: str, camp: str) -> str:
        # si la imatge no existeix retorno None
        if uuid not in self.imatges:
            return None
        return self.imatges[uuid][camp]

    def get_prompt(self, uuid: str) -> str:
        return self._get(uuid, "Prompt")

    def get_model(self, uuid: str) -> str:
        return self._get(uuid, "Model")

    def get_seed(self, uuid: str) -> str:
        return self._get(uuid, "Seed")

    def get_cfg_scale(self, uuid: str) -> str:
        return self._get(uuid, "CFG_Scale")

    def get_steps(self, uuid: str) -> str:
        return self._get(uuid, "Steps")

    def get_sampler(self, uuid: str) -> str:
        return self._get(uuid, "Sampler")

    def get_generated(self, uuid: str) -> str:
        return self._get(uuid, "Generated")

    def get_created_date(self, uuid: str) -> str:
        return self._get(uuid, "Created_Date")

    def get_filename(self, uuid: str) -> str:
        if uuid not in self.imatges:
            return None
        return self.imatges[uuid]["file"]

    def get_dimensions(self, uuid: str) -> tuple:
        if uuid not in self.imatges:
            return None
        dades = self.imatges[uuid]
        if dades["width"] is None:
            return None
        return (dades["width"], dades["height"])

    def get_uuids(self) -> list:
        return list(self.imatges.keys())

    def __len__(self):
        return len(self.imatges)

    def __str__(self):
        return f"ImageData: {len(self.imatges)} imatges"
