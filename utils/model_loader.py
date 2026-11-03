from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from utils.config_loader import load_config
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

from dotenv import load_dotenv
import os
import sys

logger = CustomLogger().get_logger(__name__)

class ModelLoader:

    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        logger.info("Configuration Loaded Successfully",config_keys=list(self.config.keys()))

    def _validate_env(self):
        required_variables = ["GOOGLE_API_KEY","GROQ_API_KEY"]
        self.api_key = {key:os.getenv(key) for key in required_variables}
        missing = [k for k, v in self.api_key.items() if not v]
        if missing:
            logger.error("Missing environment variables",missing_vars=missing)
            raise DocumentPortalException("Missing environment variables",sys)

        logger.info("Environment variables validated")

    def load_embedding(self):
        try:
            logger.info("Loading Embedding Model")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)
        
        except Exception as e:
            logger.error("Error loading embedding model",error=str(e))
            raise DocumentPortalException("Failed to load embedding model",sys)
    
    def load_llm(self):
        try:
            logger.info("Loading LLM Model")
            llm_block = self.config["llm"]
            provider_key = os.getenv("LLM_PROVIDER","google")
            if provider_key not in llm_block:
                logger.error("LLM provider not found in config",provider=provider_key)
                raise DocumentPortalException(f"LLM provider '{provider_key}' not found in config",sys)
            
            llm_config = llm_block[provider_key]
            provider = llm_config.get("provider")
            model_name = llm_config.get("model_name")
            temperature = llm_config.get("temperature",0.2)
            if provider == "google":
                return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
            elif provider == "groq":
                return ChatGroq(model=model_name, temperature=temperature)
                
        except Exception as e:
            logger.error("Error loading LLM model",error=str(e))
            raise DocumentPortalException("Failed to load LLM model",sys)

if __name__ == "__main__":
    model_loader = ModelLoader()
    embedding_model = model_loader.load_embedding()
    llm_model = model_loader.load_llm()
    result = llm_model.invoke("Hi")
    print(result)
    logger.info("Models loaded successfully",embedding_model=str(embedding_model),llm_model=str(llm_model))