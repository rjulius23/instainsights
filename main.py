#!/usr/bin/env python3
"""
Instagram Profile Statistics Viewer

A desktop application for looking up Instagram profile statistics
through HikerAPI with CSV export capabilities.

Usage:
    python main.py --api-key YOUR_API_KEY
"""
import argparse
import sys
import tkinter as tk
from typing import Optional

from src.infrastructure.api.hiker_api_client import HikerApiClient
from src.infrastructure.export.csv_exporter import CsvExporter
from src.application.profile_service import ProfileService
from src.presentation.main_window import MainWindow


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Instagram Profile Statistics Viewer"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="HikerAPI authentication key"
    )
    return parser.parse_args()


def main() -> None:
    """Application entry point."""
    args = parse_arguments()
    
    # Initialize dependencies
    api_client = HikerApiClient(api_key=args.api_key)
    csv_exporter = CsvExporter()
    profile_service = ProfileService(api_client=api_client)
    
    # Start the UI
    root = tk.Tk()
    root.title("Instagram Profile Statistics")
    root.geometry("800x600")
    
    app = MainWindow(
        master=root,
        profile_service=profile_service,
        exporter=csv_exporter
    )
    
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
