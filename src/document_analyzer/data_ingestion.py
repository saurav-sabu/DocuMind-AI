import sys
import os
import pymupdf
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from pathlib import Path
from io import BytesIO

logger = CustomLogger().get_logger(__name__)

class DocumentHandler:

    def __init__(self,data_dir=None,session_id=None):

        try:
            self.data_dir = data_dir or os.getenv("DATA_STORAGE_PATH",os.path.join(os.getcwd(),"data","document_analysis"))
            self.session_id = session_id or f"session_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{uuid.uuid4().hex[:8]}"
            self.session_path = os.path.join(self.data_dir,self.session_id)
            os.makedirs(self.session_path,exist_ok=True)
            logger.info("PDF Handler initialized",session_id=self.session_id,session_path=self.session_path)

        except Exception as e:
            logger.error(f"Error initialization DocumentHandler: {e}")
            raise DocumentPortalException(e,sys)

    def save_pdf(self,uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)
            if not filename.lower().endswith(".pdf"):
                raise DocumentPortalException("Invalid file type...")

            save_path = os.path.join(self.session_path,filename)

            with open(save_path,"wb") as f:
                f.write(uploaded_file.getbuffer())

            logger.info("PDF Saved Successfully",file=filename,save_path=save_path,session_id=self.session_id)
            return save_path
        
        except Exception as e:
            logger.error(f"Error Saving PDF: {e}")
            raise DocumentPortalException(e,sys)
  

    def read_pdf(self,pdf_path):
        try:
            text_chunks = []
            with pymupdf.open(pdf_path) as doc:
                for page_num, page in enumerate(doc,start=1):
                    text_chunks.append(f"\n---Page {page_num} ---\n{page.get_text()}")
            text = "\n".join(text_chunks)
            logger.info("PDF read Successfully",pdf_path=pdf_path,pages=len(text_chunks),session_id=self.session_id)
            return text
                
        except Exception as e:
            logger.error(f"Error Reading PDF: {e}")
            raise DocumentPortalException(e,sys)

if __name__ == "__main__":
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
    print(content[:500])
