# OpenSearch Agent

This agent provides capabilities to interact with OpenSearch clusters for document indexing, searching, and management using a simple API.

## Features

- **Create Indices**: Set up new indices with optional mappings for data structure.
- **Index Documents**: Add documents to OpenSearch with automatic or specified IDs.
- **Search Documents**: Run sophisticated searches with full OpenSearch Query DSL support.
- **Simple Search**: Use simplified text queries for quick document searches.
- **Delete Documents**: Remove documents from indices.
- **Execute OpenSearch API**: Access any OpenSearch API endpoint directly for advanced operations.

## Requirements

- OpenSearch cluster (self-hosted or managed service)
- Python with dependencies in `requirements.txt`
- Environment variables for OpenSearch connection

## Environment Configuration

Set the following environment variables in your `.env` file:

```
OPENSEARCH_HOST=your-opensearch-host
OPENSEARCH_PORT=9200
OPENSEARCH_USERNAME=your-username  # Optional
OPENSEARCH_PASSWORD=your-password  # Optional
OPENSEARCH_USE_SSL=True  # Default: True
```

## Usage

```python
from opensearch_agent.agent import opensearch_agent

# Create a new index
result = opensearch_agent.tools.create_index(
    index_name="my_documents",
    mapping={
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "tags": {"type": "keyword"}
            }
        }
    }
)

# Add a document
result = opensearch_agent.tools.index_document(
    index_name="my_documents",
    document={
        "title": "Sample Document",
        "content": "This is a sample document for testing",
        "tags": ["sample", "test"]
    },
    doc_id="doc1"  # Optional
)

# Perform a simple search
result = opensearch_agent.tools.simple_search(
    index_name="my_documents",
    query_string="sample document"
)

# Advanced search with DSL
result = opensearch_agent.tools.search_documents(
    index_name="my_documents",
    query={
        "query": {
            "bool": {
                "must": {"match": {"content": "sample"}},
                "filter": {"term": {"tags": "test"}}
            }
        }
    }
)

# Delete a document
result = opensearch_agent.tools.delete_document(
    index_name="my_documents",
    doc_id="doc1"
)

# Execute direct OpenSearch API call
result = opensearch_agent.tools.execute_opensearch_api(
    method="GET",
    endpoint_path="/_cat/indices",
    params={"v": True, "format": "json"}
)
```

## Testing

To test the OpenSearch Agent, run the included test script:

```bash
python test.py
```

The test will verify:
1. Environment variable configuration
2. Network connectivity to your OpenSearch cluster
3. Authentication and permissions
4. Basic operations like index creation, document indexing, searching, and deletion