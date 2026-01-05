# TCF Inventory Viewer

A web-based inventory viewer that can be used when running __The Cycle: Frontier__ game locally with a MongoDB instance.

Built with a Python Flask backend and vanilla JavaScript frontend.

## Setup

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure MongoDB is running on `localhost:27017`

## Running the Application

1. Start the Flask API server:
   ```bash
   python api_server.py
   ```
   The API will be available at `http://localhost:5000`

2. Open the frontend:
   - Simply open `index.html` in your web browser
   - Or use a simple HTTP server:
     ```bash
     python -m http.server 8080
     ```
     Then navigate to `http://localhost:8080`

## Features

- **Beautiful UI**: Modern gradient design with a clean table layout
- **Search Functionality**: Search by Item ID or Perks in real-time
- **Statistics Dashboard**: Shows total items, total amount, and filtered counts
- **Alphabetically Sorted**: Items are sorted by Base Item ID
- **Responsive Design**: Works on different screen sizes
- **Interactive Table**: Hover effects and smooth transitions

## API Endpoints

- `GET /api/inventory` - Returns all inventory items sorted alphabetically by baseItemId

## Files

- `api_server.py` - Flask backend API
- `index.html` - Frontend HTML page with embedded JavaScript
- `read_inventory.py` - Original Python script for console output
