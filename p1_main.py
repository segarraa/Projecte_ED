# -*- coding: utf-8 -*-
"""
p1_main.py : proves de la primera part de la pràctica
"""

import json
import cfg
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata


def main():
    # creo els objectes
    files = ImageFiles()
    ids = ImageID()
    data = ImageData()
    viewer = ImageViewer(data)
    cerca = SearchMetadata(data)
    galeries = []   # llista de galeries creades

    # Func1 + Func2 + Func3: llegeixo el disc i carrego les imatges
    files.reload_fs(cfg.ROOT_DIR)
    for f in files.files_added():
        canonic = cfg.get_canonical_pathfile(f)
        uuid = ids.generate_uuid(canonic)
        if uuid is not None:
            data.add_image(uuid, canonic)
            data.load_metadata(uuid)
    print(files, "|", ids, "|", data)

    # Func4: mostro una imatge
    uuids = data.get_uuids()
    if uuids:
        viewer.show_image(uuids[0], 0)

    # Func6: cerques
    r1 = cerca.prompt("city")
    r2 = cerca.model("SD")
    print("prompt 'city':", len(r1))
    print("model 'SD':", len(r2))
    print("AND:", len(cerca.and_operator(r1, r2)))
    print("OR:", len(cerca.or_operator(r1, r2)))

    # Func7: galeria a partir d'una cerca
    g = Gallery(ids, viewer)
    g.nom = "Ciutats"
    for uuid in r1:
        g.add_image_at_end(uuid)
    galeries.append(g)
    print(g)

    # Func5: guardo la galeria en JSON i la torno a carregar
    contingut = {
        "gallery_name": "Ciutats",
        "description": "Imatges amb 'city' al prompt",
        "created_date": "2026-10-25",
        "images": [cfg.ROOT_DIR + "/" + ids.get_file(u) for u in r1[:3]],
    }
    with open("galeria_prova.json", "w", encoding="utf-8") as f:
        json.dump(contingut, f, indent=2)

    g2 = Gallery(ids, viewer)
    g2.load_file("galeria_prova.json")
    galeries.append(g2)
    g2.show()


if __name__ == "__main__":
    main()
