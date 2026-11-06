import sys
from pathlib import Path
import pymupdf
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
import uuid

logger = CustomLogger().get_logger(__name__)

class DocumentCompare:

    def __init__(self,base_dir:str="data\\document_compare"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True,exist_ok=True)
        self.session_id = f"compare_{uuid.uuid4().hex[:8]}"
        

    def delete_existing_files(self):
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        logger.info("File deleted",path=str(file))
                logger.info("Directory Cleaned",directory=str(self.base_dir))
        except Exception as e:
            logger.error(f"Error deleting existing file: {e}")
            raise DocumentPortalException(e,sys)

    def save_uploaded_files(self,reference_file,actual_file):
        try:
            self.delete_existing_files()
            logger.info("Existing file deleted successfully")
            ref_path = self.base_dir / reference_file.name
            act_path = self.base_dir / actual_file.name

            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF Files are allowed")

            with open(ref_path,"wb") as f:
                f.write(reference_file.getbuffer())

            with open(act_path,"wb") as f:
                f.write(actual_file.getbuffer())

            return ref_path,act_path

        except Exception as e:
            logger.error(f"Error saving uploaded file: {e}")
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
            logger.error(f"Error reading PDF: {e}")
            raise DocumentPortalException(e,sys)

    def combined_documents(self):
        try:
            content_dict = {}
            doc_parts = []
            for file in self.base_dir.iterdir():
                if file.is_file() and file.suffix == ".pdf":
                    content = self.read_pdf(file)
                    content_dict[file.name] = content
                    doc_parts.append(f"\n--- Document: {file.name} ---\n{content}")

            combined_text = "\n".join(doc_parts)
            logger.info("Documents Combined Successfully",documents=list(content_dict.keys()),session_id=self.session_id)
            return combined_text
        
        except Exception as e:
            logger.error(f"Error combining docs: {e}")
            raise DocumentPortalException(e,sys)