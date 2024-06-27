import csv
import json
import logging
import os
from typing import Any, Dict, List

import pandas as pd
import requests
import yaml
from covalent import CovalentClient

logger = logging.getLogger(__name__)


class TokenQuotesFetcher:
    def __init__(self, api_key):
        self.client = CovalentClient(api_key)
        logger.info("Covalent client initialized")

    def get_token_balances(self, chain_id, address, quote_currency):
        try:
            response = self.client.balance_service.get_token_balances_for_wallet_address(
                chain_id, address, quote_currency=quote_currency
            )

            # Check if the response indicates an error
            if hasattr(response, "error") and response.error:
                if response.error_code == 401:
                    logger.error("Invalid API key")
                    raise ValueError("Invalid API key. Please check your Covalent API key.")
                else:
                    logger.error(f"API error: {response.error_message}")
                    raise ValueError(f"API error: {response.error_message}")

            return response
        except requests.RequestException as e:
            logger.error(f"Network error when connecting to Covalent API: {str(e)}")
            raise ConnectionError(f"Network error when connecting to Covalent API: {str(e)}") from e
        except ValueError as e:  # noqa: F841
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}") from e

    @staticmethod
    def process_response(response) -> Dict[str, Any]:
        return {
            **response.__dict__,
            "items": [
                {
                    **item.__dict__,
                    "logo_urls": item.logo_urls.__dict__ if item.logo_urls else None,
                    "protocol_metadata": (item.protocol_metadata.__dict__ if item.protocol_metadata else None),
                }
                for item in response.data.items
                if item.balance != 0
            ],
        }


def load_wallets(input_source: str) -> List[Dict[str, str]]:
    if os.path.isfile(input_source):
        _, ext = os.path.splitext(input_source)
        with open(input_source, "r") as f:
            if ext == ".json":
                logger.info(f"Loading wallets from JSON file: {input_source}")
                data = json.load(f)
                return data["wallets"]
            elif ext in [".yaml", ".yml"]:
                logger.info(f"Loading wallets from YAML file: {input_source}")
                data = yaml.safe_load(f)
                return data["wallets"]
            elif ext == ".csv":
                logger.info(f"Loading wallets from CSV file: {input_source}")
                reader = csv.DictReader(f)
                return [{"address": row["address"], "chain_id": row["chain_id"]} for row in reader]
            else:
                raise ValueError(f"Unsupported file type: {ext}")
    else:
        try:
            data = json.loads(input_source)
            logger.info(f"Loaded wallets from a JSON string: {input_source}")
            return data["wallets"]
        except json.JSONDecodeError:
            logger.info(f"Assuming input is a single wallet address: {input_source} and chain_id: eth-mainnet")
            pass
        return [{"address": input_source, "chain_id": "eth-mainnet"}]  # Default to Ethereum mainnet


def fetch_token_balances(wallets: List[Dict[str, str]], api_key: str, quote_currency: str) -> List[Dict]:
    fetcher = TokenQuotesFetcher(api_key)
    results = []
    for wallet in wallets:
        logger.info(f"Fetching token balances for {wallet['address']} on {wallet['chain_id']}")
        try:
            response = fetcher.get_token_balances(wallet["chain_id"], wallet["address"], quote_currency)
            response.address = wallet["address"]
            response.chain_id = wallet["chain_id"]
            response.nickname = wallet.get("nickname")
            response.quote_currency = quote_currency
            response.provider = wallet.get("provider")
            processed = fetcher.process_response(response)
            results.append(processed)
        except Exception as e:
            logger.error(f"Error fetching balances for {wallet['address']}: {str(e)}")
    return results


def extract_data(file_path: str) -> List[Dict]:
    extracted_data = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                json_data = json.loads(line)
                address = json_data.get("address")
                chain_id = json_data.get("chain_id")
                nickname = json_data.get("nickname")
                provider = json_data.get("provider")
                quote_currency = json_data.get("quote_currency")
                for item in json_data.get("items", []):
                    extracted_item = {
                        "address": address,
                        "chain_id": chain_id,
                        "nickname": nickname,
                        "provider": provider,
                        "contract_name": item.get("contract_name"),
                        "contract_display_name": item.get("contract_display_name"),
                        "contract_ticker_symbol": item.get("contract_ticker_symbol"),
                        "contract_address": item.get("contract_address"),
                        "balance": float(item.get("balance")) / pow(10, item.get("contract_decimals")),
                        "quote_rate": item.get("quote_rate"),
                        "quote": item.get("quote"),
                        "quote_currency": quote_currency,
                        "last_transferred_at": item.get("last_transferred_at"),
                    }
                    extracted_data.append(extracted_item)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line}")
    return extracted_data


def save_to_jsonlines(data_list: List[Dict], path: str) -> str:
    logger.info(f"Saving temp token balances to {path}")
    with open(path, "w") as f:
        for item in data_list:
            f.write(json.dumps(item, default=str) + "\n")
    return path


def save_to_csv(data: List[Dict], output_file: str):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    logger.info(f"Token balances saved to {output_file}")


def build_report(
    input_source: str,
    output_file: str,
    quote_currency: str,
    api_key: str,
    jsonl_output: str = "/tmp/token_balances.jsonl",
):
    wallets = load_wallets(input_source)
    results = fetch_token_balances(wallets, api_key, quote_currency)
    save_to_jsonlines(results, jsonl_output)
    data = extract_data(jsonl_output)
    save_to_csv(data, output_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch token balances for wallets")
    parser.add_argument("input", help="Path to input file (YAML, JSON, CSV) or a single wallet address")
    parser.add_argument("-o", "--output", default="token_quotes.csv", help="Path to output file (CSV)")
    parser.add_argument("--currency", default="usd", help="Quote currency (default: usd)")
    parser.add_argument(
        "--api-key",
        help="Covalent API key (or set COVALENT_API_KEY environment variable)",
    )
    parser.add_argument(
        "--jsonl_output",
        default="/tmp/token_balances.jsonl",
        help="Path to output JSON Lines file",
    )

    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("COVALENT_API_KEY")
    if not api_key:
        raise ValueError("Covalent API key must be provided via --api-key " "or COVALENT_API_KEY environment variable")

    build_report(args.input, args.output, args.currency, api_key, args.jsonl_output)
