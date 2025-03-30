import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from client import HeimdahlClient


# Example usage
if __name__ == "__main__":
    # Initialize the client with your API key
    client = HeimdahlClient(api_key="pk_dc07ea43afeb807362e9b67201e6d07054f7292edb2c4bad")

    try:
        # Example 2: Get transfers for a specific address
        transfers = client.get_transfers(
            chain="arbitrum",
            token="USDC",
            from_address="0x51C72848c68a965f66FA7a88855F9f7784502a7F",
            page_size=5
        )

        print(f"\nFound {len(transfers)} USDC transfers from the address on Arbitrum")

        # Example 3: Get Transfer events for a token
        events = client.get_events(
            chain="arbitrum",
            token_address="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            event_name="Transfer"
        )

        print(f"\nFound {len(events)} Transfer events for the token on Arbitrum")
        if events:
            print("\nFirst event:")
            print(events["events"][0])

    finally:
        # Close the client
        client.close()
