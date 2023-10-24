from .abstract_class import PdfParserAbstract
from PIL import Image, ImageStat
import pytesseract
import io
import fitz
import pandas as pd
from dataclasses import dataclass

RESOLUTION = (1224, 1584)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class ImageReader(PdfParserAbstract):
    def __init__(self, filepath, coordinates):
        self.filepath = filepath
        self.data = None
        self.coordinates = coordinates
        self.pages = None

    def retrieve_text(self):
        self.pages = self.pdf_to_images()
        self.parse_data()

    def __dict__(self):
        return {x: pytesseract.image_to_string(
            self.pages[0].crop(self.coordinates[x]))
            for x in self.coordinates}

    def parse_data(self):
        pass
        # for x in self.coordinates:
        #     print(f'{x}: ', pytesseract.image_to_string(
        #         self.pages[0].crop(self.coordinates[x])))

    def pdf_to_images(self
                      ) -> list[Image]:

        zoom = 3  # zoom - higher resolution and processing time.
        matrix = fitz.Matrix(zoom, zoom)  # Maintains image quality

        document = fitz.open(self.filepath)
        pages = [page for page in document]
        image_pages = []
        for page in pages:
            pix = page.getPixmap(
                matrix=matrix,
                colorspace='csGRAY',
                )  # broken into pixel map
            data = pix.getImageData('.png')
            image = Image.open(io.BytesIO(data))  # opening
            image = image.resize(RESOLUTION, Image.ANTIALIAS)
            image_pages.append(image)

        return image_pages
