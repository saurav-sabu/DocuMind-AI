import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompts.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_classic.output_parsers import OutputFixingParser

load_dotenv()

logger = CustomLogger().get_logger(__name__)

class DocumentCompareLLM:

    def __init__(self):
        self.llm = ModelLoader().load_llm()
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser,llm=self.llm)
        self.prompt = PROMPT_REGISTRY.get("document_comparison")
        self.chain = self.prompt | self.llm | self.parser


    def compare_docs(self,combined_document_text:str):
        try:
            inputs = {
                "combined_document_text":combined_document_text,
                "format_instructions":self.parser.get_format_instructions()
            }
            logger.info("Start Document Comparison")
            response = self.chain.invoke(inputs)
            logger.info("Document Comparison Completed")
            return self._format_response(response)
        except Exception as e:
            logger.error("Error in compare documentation: {e}")
            raise DocumentPortalException(e,sys)

    def _format_response(self,response):
        try:
            df = pd.DataFrame(response)
            logger.info("Response Formatted into DataFrame",dataframe=df)
            return df
        except Exception as e:
            logger.error("Error formatting in dataframe: {e}")
            raise DocumentPortalException(e,sys)