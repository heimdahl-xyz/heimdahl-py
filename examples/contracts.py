import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from client import HeimdahlClient


# Example usage
if __name__ == "__main__":
    # Initialize the client with your API key
    client = HeimdahlClient(api_key="pk_dc07ea43afeb807362e9b67201e6d07054f7292edb2c4bad")

    try:
        contracts = client.get_contracts()
        for c in contracts:
          print("contract ", c["contract_name"])
          print("address ", c["contract_address"])
          print("events ", c["events"])

    finally:
        # Close the client
        client.close()
