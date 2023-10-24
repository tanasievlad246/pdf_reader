from .abstract_class import PdfParserAbstract
import os
from google.cloud import documentai_v1 as documentai
from projects.pdf_reader.util.codes import LOCATION, PROJECT_ID, PROCESSOR_ID
import pandas as pd


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'util/dandsltd-dev-e0c5251c5ebd.json'


class DocumentAi(PdfParserAbstract):
    def __init__(self, filepath, search_terms=None):
        self.filepath = filepath
        self.search_terms = search_terms
        self.data = None

    def retrieve_text(self):
        client = documentai.DocumentProcessorServiceClient()

        name = f"projects/{PROJECT_ID}/locations/{LOCATION}" \
               f"/processors/{PROCESSOR_ID}"

        # Read the file into memory
        with open(self.filepath, "rb") as image:
            image_content = image.read()

        document = {"content": image_content, "mime_type": "application/pdf"}

        # Configure the process request
        request = {"name": name, "raw_document": document}

        result = client.process_document(request)
        document = result.document
        setattr(self, 'data', document.entities)

    def __dict__(
            self) -> dict[str:str]:
        return {key.type_: key.mention_text for key in self.data}

    def __repr__(
            self) -> list[str]:
        return [entity.type_ for entity in self.data]

    def parse_data(
            self) -> dict[str: str]:
        data = {key.type_: key.mention_text for key in self.data}
        relevant_data = {key: value for (key, value) in data.items()
                         if key in self.search_terms}
        return relevant_data
