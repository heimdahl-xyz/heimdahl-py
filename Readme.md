# What is Heimdahl platform?

Heimdahl is a unified blockchain intelligence platform that provides seamless access to real-time and historical data
across multiple chains through an intuitive pattern-based query system.RetryClaude can make mistakes. 

More about it: https://heimdahl.gitbook.io/heimdahl
Website: https://heimdahl.xyz/

## Heimdahl Python SDK

A lightweight Python client for accessing Heimdahl's blockchain data platform. This SDK provides convenient access to
unified cross-chain blockchain data through a simple, Pythonic interface.

### Features

- Access unified blockchain data across Ethereum, Arbitrum, Solana, and more
- Retrieve token transfers and swaps with consistent data structures
- Query raw blockchain events for deeper analysis
- Simple pattern-based endpoints for intuitive filtering
- Clean Pythonic interface with standard data structures

### Installation

```bash
git clone git@github.com:heimdahl-xyz/heimdahl-py.git
```

### Quick Start

```python
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from client import Index


# Example usage
if __name__ == "__main__":
    # Initialize the client with your API key
    client = Index(api_key="pk_dc07ea43afeb807362e9b67201e6d07054f7292edb2c4bad")

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

```

### Core API Methods

#### Swaps

Get cross-chain swap data with consistent structure:

```python
# Basic usage
swaps = client.get_swaps(
    chain="ethereum",
    token1="USDC",
    token2="WETH",
    size_bucket="all"
)

# Size buckets
swaps = client.get_swaps(
    chain="ethereum",
    token1="USDC",
    token2="WETH",
    size_bucket="large"  # Options: micro, small, medium, large, whale, all
)

# Cross-chain search
swaps = client.search_swaps_by_token_pair(
    token1="USDC",
    token2="WETH",
    chain="all",  # Search across all chains
    limit=100
)
```

#### Transfers

Get token transfer data across chains:

```python
# Get transfers for a specific token
transfers = client.get_transfers(
    chain="arbitrum",
    token="USDC",
    page_size=10
)

# Filter by address
transfers = client.get_transfers(
    chain="ethereum",
    token="USDC", 
    from_address="0x123...",
    page_size=10
)

# Get transfers between specific addresses
transfers = client.get_transfers(
    chain="ethereum",
    token="USDC",
    from_address="0x123...",
    to_address="0x456...",
    page_size=10
)
```

#### Events

Get raw blockchain events:

```python
# Get Transfer events for a token contract
events = client.get_events(
    chain="arbitrum",
    token_address="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    event_name="Transfer"
)
```

### Pagination

Methods support pagination for retrieving large datasets:

```python
# Basic pagination
page1 = client.get_swaps(
    chain="ethereum",
    token1="USDC", 
    token2="WETH",
    page=0,
    page_size=10
)

page2 = client.get_swaps(
    chain="ethereum",
    token1="USDC", 
    token2="WETH",
    page=1,
    page_size=10
)

# Helper methods automatically handle pagination
all_transfers = client.get_token_transfers(
    token="USDC",
    chain="ethereum",
    limit=100  # Get up to 100 results across multiple pages
)
```

#### Data Format

All methods return Python lists of dictionaries with consistent keys:

#### Swap Data Example

```python
{
    "chain_name": "ethereum",
    "tx_hash": "0x8713e0df807c48d9396e5b017f73e896c4502f7d904328c5c556886744c328a4",
    "timestamp": 1741969405,
    "token1_address": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
    "token1_symbol": "USDC",
    "token1_decimals": 6,
    "token2_address": "0xE0554a476A092703abdB3Ef35c80e0D76d32939F",
    "token2_symbol": "WETH",
    "token2_decimals": 18,
    "token1_sender": "0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C",
    "token2_sender": "0xE0554a476A092703abdB3Ef35c80e0D76d32939F",
    "token1_amount": 7309553024,
    "token2_amount": 3794441433022390000,
    "price_token1_in_token2": 1926384463,
    "price_token2_in_token1": 519107176671927460000000000
}
```

#### Transfer Data Example

```python
{
    "timestamp": 1742068605,
    "from_address": "0x51C72848c68a965f66FA7a88855F9f7784502a7F",
    "to_address": "0x7fCDC35463E3770c2fB992716Cd070B63540b947",
    "amount": 187911700,
    "token_address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "symbol": "USDC",
    "chain": "arbitrum",
    "network": "mainnet",
    "tx_hash": "0x81bc3bc4546ecb80b6cf653f560c2e9047f4e65361c044ffc14556a454cd4196",
    "decimals": 6,
    "position": 316050372
}
```

### Error Handling

The SDK uses standard Python exceptions. API errors will raise a `requests.exceptions.HTTPError` with the appropriate
status code and message.

```python
try:
    swaps = client.get_swaps(chain="ethereum", token1="INVALID_TOKEN")
except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")
```

### Requirements

- Python 3.6+
- requests

### License

MIT
