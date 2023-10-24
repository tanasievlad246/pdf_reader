from abc import ABC, abstractmethod


class PdfParserAbstract(ABC):

    @abstractmethod
    def retrieve_text(self):
        pass

    @abstractmethod
    def __dict__(self):
        pass

    @abstractmethod
    def parse_data(self):
        pass
