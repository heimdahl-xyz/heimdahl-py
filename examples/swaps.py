import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from client import HeimdahlClient


# Example usage
if __name__ == "__main__":
    # Initialize the client with your API key
    client = HeimdahlClient(api_key="pk_dc07ea43afeb807362e9b67201e6d07054f7292edb2c4bad")

    try:
        swaps = client.get_swaps(
            chain="ethereum",
            token1="USDC",
            token2="WETH",
            size_bucket="all",
            page_size=5
        )

        print(str(len(swaps["swaps"])) + " swaps found")
        for e in swaps["swaps"]:
            print(e["token1_symbol"])
            print(e["token2_symbol"])
            print(e["token1_amount"])
            print(e["token2_amount"])

    finally:
        # Close the client
        client.close()
