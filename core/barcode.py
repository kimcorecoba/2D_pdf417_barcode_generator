print("BARCODE.PY LOADED")

import os

import pdf417gen
from PIL import Image
from core.encoder import AAMVAEncoder


class BarcodeGenerator:

    def generate(self, fields, header=None):
        print("generate signature:", header)

        data = ""

        encoder = AAMVAEncoder()

        data = encoder.encode(fields, header)
        payload = data
        print("\n===== AAMVA PAYLOAD =====")
        print(data)
        print("=========================\n")

        codes = pdf417gen.encode(data)
        image = pdf417gen.render_image(codes)

        os.makedirs("output", exist_ok=True)

        image.save("output/barcode.png")

        return {
            "image": image,
            "payload": payload,
        }