import requests
from typing import Dict, List, Optional, Union, Any
from urllib.parse import quote


class HeimdahlClient:
    """
    Python SDK for the Heimdahl blockchain data platform.

    Provides access to cross-chain swap, transfer, and event data with a unified interface.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.heimdahl.xyz/v1"):
        """
        Initialize the Heimdahl client.

        Args:
            api_key: Your Heimdahl API key
            base_url: API base URL (defaults to production)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        Make a request to the Heimdahl API.

        Args:
            endpoint: API endpoint to call
            params: Query parameters to include

        Returns:
            API response parsed as JSON
        """
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_swaps(self,
                  chain: str = "all",
                  network: str = "mainnet",
                  token1: str = None,
                  token2: str = None,
                  size_bucket: str = "all",
                  page: int = 0,
                  page_size: int = 10) -> List[Dict]:
        """
        Get cross-chain swap data using the unified pattern.

        Pattern: {chain}.{network}.{token1}.{token2}.{size_bucket}

        Args:
            chain: Blockchain name (ethereum, arbitrum, solana, etc.) or "all"
            network: Network (mainnet, testnet)
            token1: First token address or symbol
            token2: Second token address or symbol
            size_bucket: Size category (micro, small, medium, large, whale, all)
            page: Page number for pagination
            page_size: Number of results per page

        Returns:
            List of swap dictionaries
        """
        # Build the pattern-based URL
        pattern_parts = [chain, network]

        if token1:
            pattern_parts.append(token1)
            if token2:
                pattern_parts.append(token2)
                pattern_parts.append(size_bucket)
            else:
                pattern_parts.append("all")  # Default if token2 not specified
                pattern_parts.append(size_bucket)

        # URL-encode each part if needed
        encoded_parts = [quote(str(part)) for part in pattern_parts]
        pattern = ".".join(encoded_parts)

        # Make the request
        endpoint = f"swaps/list/{pattern}"
        params = {
            "page": page,
            "pageSize": page_size
        }

        return self._make_request(endpoint, params)

    def get_transfers(self,
                     chain: str = "all",
                     network: str = "mainnet",
                     token: str = None,
                     from_address: str = None,
                     to_address: str = None,
                     page: int = 0,
                     page_size: int = 10) -> List[Dict]:
        """
        Get token transfer data across chains.

        Pattern: {chain}.{network}.{token}.{from}.{to}.all

        Args:
            chain: Blockchain name (ethereum, arbitrum, solana, etc.) or "all"
            network: Network (mainnet, testnet)
            token: Token address or symbol
            from_address: Filter by sender address
            to_address: Filter by recipient address
            page: Page number for pagination
            page_size: Number of results per page

        Returns:
            List of transfer dictionaries
        """
        # Build the pattern-based URL
        pattern_parts = [chain, network]

        if token:
            pattern_parts.append(token)
            if from_address:
                pattern_parts.append(from_address)
                if to_address:
                    pattern_parts.append(to_address)
                else:
                    pattern_parts.append("all")  # Default if to_address not specified
            else:
                pattern_parts.append("all")  # Default if from_address not specified
                if to_address:
                    pattern_parts.append(to_address)
                else:
                    pattern_parts.append("all")  # Default if to_address not specified

        pattern_parts.append("all")  # Final part of the pattern

        # URL-encode each part if needed
        encoded_parts = [quote(str(part)) for part in pattern_parts]
        pattern = ".".join(encoded_parts)

        # Make the request
        endpoint = f"transfers/list/{pattern}"
        params = {
            "page": page,
            "pageSize": page_size
        }

        return self._make_request(endpoint, params)

    def get_events(self,
                  chain: str,
                  token_address: str,
                  event_name: str) -> List[Dict]:
        """
        Get raw blockchain events for a specific token and event type.

        Pattern: /v1/{chain}/events/{token_address}/{event_name}

        Args:
            chain: Blockchain name (ethereum, arbitrum, solana, etc.)
            token_address: Contract address
            event_name: Event name (e.g., "Transfer")

        Returns:
            List of event dictionaries
        """
        # Make the request
        endpoint = f"{chain}/events/{token_address}/{event_name}"

        return self._make_request(endpoint)

    def search_swaps_by_token_pair(self,
                                   token1: str,
                                   token2: str,
                                   chain: str = "all",
                                   network: str = "mainnet",
                                   size_bucket: str = "all",
                                   limit: int = 100) -> List[Dict]:
        """
        Search for swaps between a specific token pair.

        Args:
            token1: First token symbol or address
            token2: Second token symbol or address
            chain: Blockchain name or "all"
            network: Network (mainnet, testnet)
            size_bucket: Size category
            limit: Maximum number of results to return

        Returns:
            List of matching swaps
        """
        results = []
        page = 0
        page_size = min(100, limit)

        while len(results) < limit:
            swaps = self.get_swaps(
                chain=chain,
                network=network,
                token1=token1,
                token2=token2,
                size_bucket=size_bucket,
                page=page,
                page_size=page_size
            )

            if not swaps:
                break

            results.extend(swaps)
            if len(swaps) < page_size:
                break

            page += 1

        return results[:limit]

    def get_token_transfers(self,
                           token: str,
                           from_address: Optional[str] = None,
                           to_address: Optional[str] = None,
                           chain: str = "all",
                           network: str = "mainnet",
                           limit: int = 100) -> List[Dict]:
        """
        Get all transfers for a specific token, optionally filtered by address.

        Args:
            token: Token symbol or address
            from_address: Optional sender address
            to_address: Optional recipient address
            chain: Blockchain name or "all"
            network: Network (mainnet, testnet)
            limit: Maximum number of results

        Returns:
            List of matching transfers
        """
        results = []
        page = 0
        page_size = min(100, limit)

        while len(results) < limit:
            transfers = self.get_transfers(
                chain=chain,
                network=network,
                token=token,
                from_address=from_address,
                to_address=to_address,
                page=page,
                page_size=page_size
            )

            if not transfers:
                break

            results.extend(transfers)
            if len(transfers) < page_size:
                break

            page += 1

        return results[:limit]

    def close(self):
        """Close the session."""
        self.session.close()


# Example usage
if __name__ == "__main__":
    # Initialize the client with your API key
    client = HeimdahlClient(api_key="pk_dc07ea43afeb807362e9b67201e6d07054f7292edb2c4bad")

    try:
        # Example 1: Get USDC/WETH swaps on Ethereum
        swaps = client.get_swaps(
            chain="ethereum",
            token1="USDC",
            token2="WETH",
            size_bucket="all",
            page_size=5
        )

        print(f"Found {len(swaps)} USDC/WETH swaps on Ethereum")
        if swaps:
            print("\nFirst swap:")
            for key, value in swaps[0].items():
                print(f"{key}: {value}")

        # Example 2: Get transfers for a specific address
        transfers = client.get_transfers(
            chain="arbitrum",
            token="USDC",
            from_address="0x51C72848c68a965f66FA7a88855F9f7784502a7F",
            page_size=5
        )

        print(f"\nFound {len(transfers)} USDC transfers from the address on Arbitrum")
        if transfers:
            print("\nFirst transfer:")
            for key, value in transfers[0].items():
                print(f"{key}: {value}")

            # Calculate total amount
            if "decimals" in transfers[0]:
                decimals = transfers[0]["decimals"]
                total = sum(transfer["amount"] for transfer in transfers) / (10 ** decimals)
                print(f"\nTotal amount: {total:.2f} USDC")
            else:
                total = sum(transfer["amount"] for transfer in transfers)
                print(f"\nTotal raw amount: {total}")

        # Example 3: Get Transfer events for a token
        events = client.get_events(
            chain="arbitrum",
            token_address="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            event_name="Transfer"
        )

        print(f"\nFound {len(events)} Transfer events for the token on Arbitrum")
        print(events["events"])
        if events:
            print("\nFirst event:")
            print(events["events"][0])

    finally:
        # Close the client
        client.close()
