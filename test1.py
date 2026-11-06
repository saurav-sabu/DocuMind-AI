import io
from pathlib import Path
from src.document_comparison.data_ingestion import DocumentCompare
from src.document_comparison.document_compare import DocumentCompareLLM

def load_fake_uplaoded_file(file_path):
    return io.BytesIO(file_path.read_bytes())

def test_compare_document():

    class FakeUpload:

        def __init__(self, file_path):
            self.file_path = file_path
            self.name = Path(file_path).name

        def getbuffer(self):
            return Path(self.file_path).read_bytes()

    comparator = DocumentCompare()
    ref_upload = FakeUpload("data/sample_pdfs/long_report_v1.pdf")
    act_upload = FakeUpload("data/sample_pdfs/long_report_v2.pdf")

    ref_file, act_file = comparator.save_uploaded_files(ref_upload,act_upload)
    combined_text = comparator.combined_documents()
    print(combined_text[:1000])

    llm_compare = DocumentCompareLLM()
    compare_df = llm_compare.compare_docs(combined_text)
    print(compare_df.head())

if __name__ == "__main__":
    test_compare_document()