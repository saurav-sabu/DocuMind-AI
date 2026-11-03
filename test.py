import os
from pathlib import Path
from src.document_analyzer.data_ingestion import DocumentHandler
from src.document_analyzer.data_analysis import DocumentAnalyzer

pdf_path = r"data\document_analysis\attention_is_all_you_need.pdf"

class DummyFile:

    def __init__(self,file_path):
        self.name = Path(file_path)
        self._file_path = file_path

    def getbuffer(self):
        return open(self._file_path,"rb").read()

dummy_pdf = DummyFile(pdf_path)
handler = DocumentHandler()
saved_path = handler.save_pdf(dummy_pdf)
print(saved_path)
content = handler.read_pdf(saved_path)

analyzer = DocumentAnalyzer()
analysis_result = analyzer.analyze_document(content)

for key,value in analysis_result.items():
    print(f"{key}:{value}")