from langchain_core.prompts import ChatPromptTemplate

document_analysis_prompt = ChatPromptTemplate.from_template(
    '''
    You are a higly skilled data analyst. You have been given a document and your task is to analyze the document and provide a summary of the document in a structured format. The structured format should be in JSON format and should contain the following fields:

    {format_instructions}

    Analyze the following document:
    {document_text}
    '''
)

document_comparison_prompt = ChatPromptTemplate.from_template(
    '''
    You will be provided with content from two documents. Your task is to compare the two documents and identify any changes made between the two documents. The changes should be provided:
    1. Compare the contents in two pdfs
    2. Identify any changes made between the two documents and note the page number where the change occurred.
    3. Provide a summary of the changes made in a structured format in page wise comparison. The structured format should be in JSON format
    4. If any page does not have any changes, it should have a note indicating no changes.

    Input Documents:
    {combined_document_text}

    Your response should be in the following structured format:
    {format_instructions}
    '''
)




PROMPT_REGISTRY = {
    "document_analysis":document_analysis_prompt,
    "document_comparison":document_comparison_prompt
}