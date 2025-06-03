# Print Pricing Calculator

A modern, responsive web application for calculating print product prices based on various options and quantities.

## Features

- Dark mode interface
- Real-time price calculations
- Mobile-friendly design
- Support for multiple product types:
  - Carbonless Forms
  - Cut Sheet
  - Digital Color
  - Letterhead
  - Card Stock
  - Scratch Pads

## Usage

Visit: https://athanmonk.github.io/pricing-tool

Select your product type and options to see instant price calculations.

## Development

The project consists of:
- Python script for processing CSV pricing data
- React-based web interface
- JSON-based data storage

## Local Development

1. Clone the repository
2. Run the Python script to generate pricing data:
   ```bash
   python3 generate_pricing_data.py
   ```
3. Serve the files using a local web server:
   ```bash
   python3 -m http.server 8000
   ```
4. Open http://localhost:8000 in your browser
