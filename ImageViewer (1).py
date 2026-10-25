# -*- coding: utf-8 -*-
"""
ImageViewer.py : visualitzar imatges i les seves metadades (Func4)
"""

import os
import cfg


class ImageViewer:

    def __init__(self, image_data):
        self.data = image_data

    def print_image(self, uuid: str):
        d = self.data
        prompt = d.get_prompt(uuid)
        if prompt is not None and len(prompt) > 100:
            prompt = prompt[:100] + "..."
        dimensions = d.get_dimensions(uuid)
        if dimensions is None:
            dimensions = (None, None)
        amplada, alcada = dimensions

        print("-" * 50)
        print(f" UUID:       {uuid}")
        print(f" Arxiu:      {d.get_filename(uuid)}")
        print(f" Dimensions: {amplada}x{alcada}")
        print(f" Prompt:     {prompt}")
        print(f" Model:      {d.get_model(uuid)}")
        print(f" Seed:       {d.get_seed(uuid)}")
        print(f" CFG Scale:  {d.get_cfg_scale(uuid)}")
        print(f" Steps:      {d.get_steps(uuid)}")
        print(f" Sampler:    {d.get_sampler(uuid)}")
        print(f" Generated:  {d.get_generated(uuid)}")
        print(f" Created:    {d.get_created_date(uuid)}")
        print("-" * 50)

    def show_file(self, file: str):
        path = file
        if not os.path.isfile(path):
            path = os.path.join(cfg.ROOT_DIR, file)
        try:
            from PIL import Image
            img = Image.open(path)
            img.show()
        except Exception as e:
            print(f"No es pot mostrar la imatge {file}: {e}")

    def show_image(self, uuid: str, mode: int):
        # 0: metadades, 1: metadades + imatge, 2: només imatge
        if mode == 0 or mode == 1:
            self.print_image(uuid)
        if mode == 1 or mode == 2:
            self.show_file(self.data.get_filename(uuid))

    def __str__(self):
        return f"ImageViewer ({len(self.data)} imatges)"
