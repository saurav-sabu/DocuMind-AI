import os
import sys
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain_classic.output_parsers import OutputFixingParser
from logger.custom_logger import CustomLogger
from prompts.prompt_library import PROMPT_REGISTRY

logger = CustomLogger().get_logger(__name__)

class DocumentAnalyzer:

    def __init__(self):
        try:
            self.llm = ModelLoader().load_llm()
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser,llm=self.llm)
            self.prompt = PROMPT_REGISTRY.get("document_analysis")

        except Exception as e:
            logger.error(f"Error Initialization Document Analyzer: {e}")
            raise DocumentPortalException(e,sys)

    def analyze_document(self,document_text:str):
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            logger.info("Analysis Chain intialzied")

            response = chain.invoke({
                "format_instructions":self.parser.get_format_instructions(),
                "document_text":document_text
            })

            logger.info("Analysis chain Successful",keys=list(response.keys()))
            return response
        
        except Exception as e:
            logger.error(f"Error in analysis chain: {e}")
            raise DocumentPortalException(e,sys)