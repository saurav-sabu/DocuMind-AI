from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    '''
    You are a higly skilled data analyst. You have been given a document and your task is to analyze the document and provide a summary of the document in a structured format. The structured format should be in JSON format and should contain the following fields:

    {format_instructions}

    Analyze the following document:
    {document_text}
    '''
)