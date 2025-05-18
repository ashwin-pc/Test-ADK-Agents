import os
from opensearchpy import OpenSearch, RequestsHttpConnection
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import sys
import json
from typing import Optional

# Add the parent directory to sys.path to allow importing from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_models import SMART_MODEL

def connect_to_opensearch() -> OpenSearch:
    """
    Creates and returns an OpenSearch client using environment variables.
    
    Required environment variables:
    - OPENSEARCH_HOST: The hostname or IP of the OpenSearch cluster
    - OPENSEARCH_PORT: The port of the OpenSearch cluster (default: 9200)
    - OPENSEARCH_USERNAME: The username for OpenSearch authentication (optional)
    - OPENSEARCH_PASSWORD: The password for OpenSearch authentication (optional)
    - OPENSEARCH_USE_SSL: Whether to use SSL for connections (default: 'True')
    
    Returns:
        OpenSearch client instance
    """
    host = os.getenv('OPENSEARCH_HOST')
    port = int(os.getenv('OPENSEARCH_PORT', '9200'))
    use_ssl = os.getenv('OPENSEARCH_USE_SSL', 'True').lower() == 'true'
    username = os.getenv('OPENSEARCH_USERNAME')
    password = os.getenv('OPENSEARCH_PASSWORD')
    
    if not host:
        raise ValueError("OPENSEARCH_HOST environment variable must be set")
    
    http_auth = None
    if username and password:
        http_auth = (username, password)
    
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=http_auth,
        use_ssl=use_ssl,
        verify_certs=False,  # For development only. In production, set to True
        connection_class=RequestsHttpConnection,
        timeout=60
    )
    
    return client

def create_index(index_name: str, mapping: Optional[dict] = None) -> dict:
    """
    Creates an index in OpenSearch with optional mapping.
    
    Args:
        index_name (str): The name of the index to create
        mapping (dict, optional): JSON mapping for the index schema
    
    Returns:
        dict: status and result or error message
    """
    try:
        client = connect_to_opensearch()
        
        # Check if index already exists
        if client.indices.exists(index=index_name):
            return {
                "status": "error",
                "error_message": f"Index '{index_name}' already exists."
            }
        
        # Create index with or without mapping
        create_response = client.indices.create(
            index=index_name,
            body=mapping if mapping else {}
        )
        
        return {
            "status": "success",
            "result": f"Index '{index_name}' created successfully.",
            "response": create_response
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to create index: {str(e)}"
        }

def index_document(index_name: str, document: dict, doc_id: Optional[str] = None) -> dict:
    """
    Indexes a document into OpenSearch.
    
    Args:
        index_name (str): The index to add the document to
        document (dict): The document to index
        doc_id (Optional[str], optional): Document ID, will be generated if not provided
    
    Returns:
        dict: status and result or error message
    """
    try:
        client = connect_to_opensearch()
        
        # Check if index exists
        if not client.indices.exists(index=index_name):
            return {
                "status": "error",
                "error_message": f"Index '{index_name}' does not exist."
            }
            
        # Index document with or without specified ID
        if doc_id:
            response = client.index(
                index=index_name,
                id=doc_id,
                body=document,
                refresh=True  # Make document immediately available for search
            )
        else:
            response = client.index(
                index=index_name,
                body=document,
                refresh=True
            )
            
        return {
            "status": "success",
            "result": f"Document indexed successfully.",
            "response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to index document: {str(e)}"
        }

def search_documents(index_name: str, query: dict) -> dict:
    """
    Searches for documents in an OpenSearch index.
    
    Args:
        index_name (str): The index to search in
        query (dict): OpenSearch query DSL
    
    Returns:
        dict: status and search results or error message
    """
    try:
        client = connect_to_opensearch()
        
        # Check if index exists
        if not client.indices.exists(index=index_name):
            return {
                "status": "error",
                "error_message": f"Index '{index_name}' does not exist."
            }
        
        # Perform search
        response = client.search(
            index=index_name,
            body=query
        )
        
        # Extract and format search results
        hits = response.get("hits", {}).get("hits", [])
        results = []
        
        for hit in hits:
            result = {
                "id": hit.get("_id"),
                "score": hit.get("_score"),
                "document": hit.get("_source")
            }
            results.append(result)
        
        return {
            "status": "success",
            "total_hits": response.get("hits", {}).get("total", {}).get("value", 0),
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Search failed: {str(e)}"
        }

def delete_document(index_name: str, doc_id: str) -> dict:
    """
    Deletes a document from an OpenSearch index.
    
    Args:
        index_name (str): The index containing the document
        doc_id (str): The ID of the document to delete
        
    Returns:
        dict: status and result or error message
    """
    try:
        client = connect_to_opensearch()
        
        # Check if index exists
        if not client.indices.exists(index=index_name):
            return {
                "status": "error",
                "error_message": f"Index '{index_name}' does not exist."
            }
            
        # Check if document exists
        if not client.exists(index=index_name, id=doc_id):
            return {
                "status": "error",
                "error_message": f"Document with ID '{doc_id}' does not exist in index '{index_name}'."
            }
            
        # Delete the document
        response = client.delete(
            index=index_name,
            id=doc_id,
            refresh=True
        )
        
        return {
            "status": "success",
            "result": f"Document with ID '{doc_id}' deleted successfully.",
            "response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to delete document: {str(e)}"
        }

def parse_query_string(query_string: str) -> dict:
    """
    Parses a simple query string into OpenSearch query DSL.
    
    Args:
        query_string (str): The search query string
        
    Returns:
        dict: OpenSearch query DSL
    """
    return {
        "query": {
            "multi_match": {
                "query": query_string,
                "fields": ["*"],
                "fuzziness": "AUTO"
            }
        }
    }

def simple_search(index_name: str, query_string: str) -> dict:
    """
    Performs a simple search using a query string.
    
    Args:
        index_name (str): The index to search in
        query_string (str): Simple text query
        
    Returns:
        dict: status and search results or error message
    """
    query = parse_query_string(query_string)
    return search_documents(index_name, query)

# Create the OpenSearch agent
opensearch_agent = LlmAgent(
    name="opensearch_agent",
    model=LiteLlm(model=SMART_MODEL),
    description="Agent to interact with OpenSearch for indexing and searching data",
    instruction=(
        "You are a helpful agent who can interact with OpenSearch to index, "
        "search, and manage documents. You can create indices, add documents, "
        "search for information, and delete documents."
    ),
    tools=[
        create_index, 
        index_document, 
        search_documents,
        simple_search,
        delete_document
    ],
)

root_agent = opensearch_agent