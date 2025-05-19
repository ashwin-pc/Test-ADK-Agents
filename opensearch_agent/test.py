import os
import sys
from dotenv import load_dotenv
from opensearchpy import OpenSearch, RequestsHttpConnection
import requests
import json
import socket
import time

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.END}\n")

def print_section(message):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{message}{Colors.END}")
    print(f"{Colors.BLUE}{'-' * 40}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.CYAN}{message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def check_environment():
    """Check required environment variables for OpenSearch."""
    required_vars = ['OPENSEARCH_HOST']
    optional_vars = [
        'OPENSEARCH_PORT',
        'OPENSEARCH_USERNAME',
        'OPENSEARCH_PASSWORD',
        'OPENSEARCH_USE_SSL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print_error(f"Missing required environment variables: {', '.join(missing_vars)}")
        print_info("Please ensure your .env file contains all required variables")
        return False
    
    print_success("All required environment variables are set")
    
    # Print environment configuration
    print_section("Environment Configuration")
    print_info(f"OpenSearch Host: {os.getenv('OPENSEARCH_HOST')}")
    print_info(f"OpenSearch Port: {os.getenv('OPENSEARCH_PORT', '9200')}")
    
    if os.getenv('OPENSEARCH_USERNAME'):
        print_info("OpenSearch Authentication: Enabled")
    else:
        print_warning("OpenSearch Authentication: Not configured")
    
    use_ssl = os.getenv('OPENSEARCH_USE_SSL', 'True').lower() == 'true'
    print_info(f"OpenSearch SSL: {'Enabled' if use_ssl else 'Disabled'}")
    
    return True

def test_network_connectivity():
    """Test basic network connectivity to the OpenSearch host and port."""
    host = os.getenv('OPENSEARCH_HOST')
    port_str = os.getenv('OPENSEARCH_PORT')
    
    print_section("Testing Network Connectivity")
    
    # Test DNS resolution
    try:
        print_info(f"DNS Resolution: Resolving {host}...")
        ip_address = socket.gethostbyname(host)
        print_success(f"Successfully resolved {host} to {ip_address}")
    except socket.gaierror as e:
        print_error(f"DNS resolution failed: {str(e)}")
        print_info("Troubleshooting:")
        print_info("1. Check if the hostname is correct")
        print_info("2. Check if DNS is working properly")
        print_info("3. Try using an IP address instead of hostname")
        return False
    
    # Test port connectivity if port is provided
    if port_str:
        try:
            port = int(port_str)
            print_info(f"Port Connectivity: Testing connection to {host}:{port}...")
            start_time = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            s.close()
            end_time = time.time()
            print_success(f"Successfully connected to {host}:{port} in {end_time - start_time:.2f} seconds")
        except (socket.timeout, socket.error) as e:
            print_error(f"Connection to {host}:{port} failed: {str(e)}")
            print_info("Troubleshooting:")
            print_info("1. Check if the OpenSearch service is running")
            print_info("2. Check if there's a firewall blocking the connection")
            print_info("3. Verify the port number is correct")
            print_info("4. Check if you need to connect through a VPN or proxy")
            return False
    else:
        print_info("Port not specified in environment variables, skipping port connectivity test")
        print_info("Using default port 9200 for OpenSearch client connection")
    
    return True

def get_opensearch_client():
    """Create and return an OpenSearch client."""
    try:
        # Already imported at the top of the file
        pass
    except ImportError:
        print_error("OpenSearch Python client not installed")
        print_info("Install it with: pip install opensearch-py")
        return None
    
    host = os.getenv('OPENSEARCH_HOST')
    port_str = os.getenv('OPENSEARCH_PORT')
    port = int(port_str) if port_str else 9200
    
    use_ssl = os.getenv('OPENSEARCH_USE_SSL', 'True').lower() == 'true'
    username = os.getenv('OPENSEARCH_USERNAME')
    password = os.getenv('OPENSEARCH_PASSWORD')
    
    http_auth = None
    if username and password:
        http_auth = (username, password)
    
    try:
        print_info(f"Connecting to OpenSearch at {host}:{port} (SSL: {'Enabled' if use_ssl else 'Disabled'})")
        
        connection_params = {
            'hosts': [{'host': host}],
            'http_auth': http_auth,
            'use_ssl': use_ssl,
            # 'verify_certs': False,  # For development only. In production, set to True
            'connection_class': RequestsHttpConnection,
            'timeout': 30
        }
        
        # Add port only if specified
        if port_str:
            connection_params['hosts'][0]['port'] = port
            
        client = OpenSearch(**connection_params)
        return client
    except Exception as e:
        print_error(f"Failed to create OpenSearch client: {str(e)}")
        return None

def test_cluster_health(client):
    """Test basic cluster health."""
    print_section("Testing Cluster Health")
    
    try:
        health = client.cluster.health()
        status = health.get('status')
        
        if status == 'green':
            print_success(f"Cluster health is {status} - All shards are allocated")
        elif status == 'yellow':
            print_warning(f"Cluster health is {status} - All primary shards are allocated but some replicas are not")
        else:
            print_error(f"Cluster health is {status} - Some primary shards are not allocated")
        
        print_info(f"Cluster name: {health.get('cluster_name')}")
        print_info(f"Number of nodes: {health.get('number_of_nodes')}")
        print_info(f"Active shards: {health.get('active_shards')}")
        
        return True
    except Exception as e:
        print_error(f"Failed to check cluster health: {str(e)}")
        print_info("This might be due to connectivity issues or insufficient permissions")
        return False

def test_index_permissions(client):
    """Test index creation and deletion permissions."""
    print_section("Testing Index Permissions")
    
    test_index = "test_permissions_" + str(int(time.time()))
    
    # Test index creation
    try:
        print_info(f"Creating test index '{test_index}'...")
        create_response = client.indices.create(index=test_index)
        
        if create_response.get('acknowledged', False):
            print_success(f"Successfully created index '{test_index}'")
        else:
            print_warning(f"Index creation was not acknowledged: {create_response}")
    except Exception as e:
        print_error(f"Failed to create index: {str(e)}")
        print_info("This might indicate you don't have index creation permissions")
        return False
    
    # Test index deletion
    try:
        print_info(f"Deleting test index '{test_index}'...")
        delete_response = client.indices.delete(index=test_index)
        
        if delete_response.get('acknowledged', False):
            print_success(f"Successfully deleted index '{test_index}'")
        else:
            print_warning(f"Index deletion was not acknowledged: {delete_response}")
    except Exception as e:
        print_error(f"Failed to delete index: {str(e)}")
        print_info("This might indicate you don't have index deletion permissions")
        print_warning(f"The test index '{test_index}' might still exist and should be cleaned up manually")
        return False
    
    return True

def test_document_operations(client):
    """Test document CRUD operations."""
    print_section("Testing Document Operations")
    
    test_index = "test_docs_" + str(int(time.time()))
    test_doc = {
        "title": "Test Document",
        "content": "This is a test document to check OpenSearch permissions.",
        "tags": ["test", "permissions"],
        "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }
    
    # Create test index
    try:
        client.indices.create(index=test_index)
        print_success(f"Created test index '{test_index}'")
    except Exception as e:
        print_error(f"Failed to create index for document testing: {str(e)}")
        return False
    
    # Index a document
    try:
        print_info("Testing document indexing...")
        index_result = client.index(
            index=test_index,
            body=test_doc,
            refresh=True,
            id="test-doc-1"
        )
        print_success("Successfully indexed test document")
    except Exception as e:
        print_error(f"Failed to index document: {str(e)}")
        print_info("This might indicate you don't have document write permissions")
        # Try to clean up
        try:
            client.indices.delete(index=test_index)
        except:
            pass
        return False
    
    # Read a document
    try:
        print_info("Testing document retrieval...")
        get_result = client.get(index=test_index, id="test-doc-1")
        if get_result.get('found', False):
            print_success("Successfully retrieved test document")
        else:
            print_warning("Document retrieval did not return 'found: true'")
    except Exception as e:
        print_error(f"Failed to retrieve document: {str(e)}")
        print_info("This might indicate you don't have document read permissions")
        # Try to clean up
        try:
            client.indices.delete(index=test_index)
        except:
            pass
        return False
    
    # Search for documents
    try:
        print_info("Testing document search...")
        search_result = client.search(
            index=test_index,
            body={"query": {"match": {"content": "test"}}}
        )
        hits = search_result.get('hits', {}).get('hits', [])
        if hits:
            print_success(f"Search successful, found {len(hits)} documents")
        else:
            print_warning("Search did not return any results (expected 1)")
    except Exception as e:
        print_error(f"Failed to search documents: {str(e)}")
        print_info("This might indicate you don't have search permissions")
        # Try to clean up
        try:
            client.indices.delete(index=test_index)
        except:
            pass
        return False
    
    # Delete the document
    try:
        print_info("Testing document deletion...")
        delete_result = client.delete(
            index=test_index,
            id="test-doc-1",
            refresh=True
        )
        print_success("Successfully deleted test document")
    except Exception as e:
        print_error(f"Failed to delete document: {str(e)}")
        print_info("This might indicate you don't have document deletion permissions")
        
    # Delete the test index
    try:
        client.indices.delete(index=test_index)
        print_success(f"Cleaned up test index '{test_index}'")
    except Exception as e:
        print_error(f"Failed to clean up test index: {str(e)}")
        print_warning(f"The test index '{test_index}' might still exist and should be cleaned up manually")
    
    return True

def print_debug_tips():
    """Print helpful debugging tips."""
    print_section("Debugging Tips")
    
    print_info("If you encountered connection issues:")
    print_info("1. Verify your OpenSearch cluster is running and accessible")
    print_info("2. Check that your network allows connections to the host and port")
    print_info("3. Confirm that your authentication credentials are correct")
    print_info("4. Verify SSL settings match your cluster configuration")
    print_info("5. Check if your OpenSearch cluster uses fine-grained access control")
    print_info("")
    print_info("Common curl commands for troubleshooting:")
    
    host = os.getenv('OPENSEARCH_HOST')
    port = os.getenv('OPENSEARCH_PORT', '9200')
    use_ssl = os.getenv('OPENSEARCH_USE_SSL', 'True').lower() == 'true'
    protocol = "https" if use_ssl else "http"
    auth_part = ""
    if os.getenv('OPENSEARCH_USERNAME') and os.getenv('OPENSEARCH_PASSWORD'):
        auth_part = f"-u {os.getenv('OPENSEARCH_USERNAME')}:{os.getenv('OPENSEARCH_PASSWORD')} "
    
    print_info(f"  Basic connection test:")
    print_info(f"    curl {auth_part}-{'k ' if use_ssl else ''}{protocol}://{host}:{port}")
    
    print_info(f"  Check cluster health:")
    print_info(f"    curl {auth_part}-{'k ' if use_ssl else ''}{protocol}://{host}:{port}/_cluster/health?pretty")
    
    print_info(f"  List indices:")
    print_info(f"    curl {auth_part}-{'k ' if use_ssl else ''}{protocol}://{host}:{port}/_cat/indices?v")

def main():
    print_header("OpenSearch Connection Test")
    
    # Load environment variables from .env file
    print_section("Environment Setup")
    loaded_env = load_dotenv(override=True)
    
    if loaded_env:
        print_success("Loaded .env file successfully")
    else:
        print_warning(".env file not found. Using existing environment variables")
    
    # Check environment
    if not check_environment():
        print_debug_tips()
        return
    
    # Test network connectivity
    if not test_network_connectivity():
        print_debug_tips()
        return
    
    # Create OpenSearch client
    client = get_opensearch_client()
    if not client:
        print_debug_tips()
        return
    
    # Test cluster health
    if not test_cluster_health(client):
        print_debug_tips()
        return
    
    # Test permissions
    test_index_permissions(client)
    test_document_operations(client)
    
    print_header("OpenSearch Connection Test Complete")

if __name__ == "__main__":
    main()