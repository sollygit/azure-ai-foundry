from dotenv import load_dotenv
import os
import json
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential

def main():
    """Create a Content Understanding analyzer for extracting content from documents."""
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get the travel content schema
        with open("travel_content_analyzer.json", "r") as file:
            schema_json = json.load(file)
        
        card_schema = json.dumps(schema_json)

        # Get config settings
        load_dotenv()
        endpoint = os.getenv('CONTENT_UNDERSTANDING_ENDPOINT')
        key = os.getenv('CONTENT_UNDERSTANDING_KEY')
        analyzer_name = os.getenv('CONTENT_UNDERSTANDING_ANALYZER_NAME')

        # Create the analyzer
        create_analyzer (card_schema, analyzer_name, endpoint, key)
        
        print("\n")

    except Exception as ex:
        print(f"Error: {ex}")

def create_analyzer (schema, analyzer, endpoint, key):
    # Create a Content Understanding analyzer
    print(f"Creating {analyzer}")

    # Create the Content Understanding client
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Parse the schema JSON into a ContentAnalyzer object
    analyzer_definition = json.loads(schema)

    # Create the analyzer using the SDK (long-running operation)
    poller = client.begin_create_analyzer(
        analyzer_id=analyzer,
        resource=analyzer_definition,
        allow_replace=True
    )

    # Wait for the operation to complete
    result = poller.result()
    print(f"Analyzer '{analyzer}' created successfully.")
    print(f"Status: {result['status'] if isinstance(result, dict) else 'Succeeded'}")


if __name__ == "__main__":
    main()
