#!/usr/bin/env python3
import argparse
import logging
import os

from .logging_config import setup_logging
from .report_builder import build_report

logger = logging.getLogger(__name__)


def main():
    setup_logging()
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


if __name__ == "__main__":
    main()
