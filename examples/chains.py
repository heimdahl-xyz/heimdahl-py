import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from client import HeimdahlClient

if __name__ == "__main__":
    client = HeimdahlClient(api_key="pk_dc07ea43afeb807362e9b67201e6d07054f7292edb2c4bad")

    try:
        chains = client.get_chains()
        for c in chains:
          print("chain ", c["chain_name"])

    finally:
        # Close the client
        client.close()
