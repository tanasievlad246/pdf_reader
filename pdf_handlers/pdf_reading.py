from .abstract_class import PdfParserAbstract
import fitz
import re


class PdfParser(PdfParserAbstract):
    def __init__(self, filepath, search_terms=None):
        self.filepath = filepath
        self.data = None
        self.search_terms = search_terms

    def retrieve_text(self):
        document = fitz.open(self.filepath)
        document_pages = [document.load_page(page_nr).getText('blocks')
                          for page_nr in range(document.page_count)]

        document_blocks = []
        for page in document_pages:
            document_blocks += page

        setattr(self, 'data', document_blocks)

    def __dict__(self):
        return

    def parse_data(self):
        for block in self.data:
            string = block[4]
            for term in self.search_terms:
                match = re.search(term[0], string)
                if match:
                    print(self.data[self.data.index(block)+term[1]][4])

