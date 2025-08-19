# Simple File Share

A minimal, easy-to-use file sharing web server built with Python and Flask. Upload and download files from any device on your network.

## Features
- **Upload files** via a simple web interface
- **Download files** from a searchable list
- **Automatic file renaming** to avoid overwrites
- **Human-readable file sizes and timestamps**
- **No database required**

## Getting Started

### Prerequisites
- Python 3.9 or newer
- Flask (`pip install flask`)

### Running the Server
1. Install Flask:
   ```bash
   pip install flask
   ```
2. Start the server:
   - On Windows, double-click `start.bat` _or_ run:
     ```bash
     python server.py
     ```
   - By default, the server runs on [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage
- **Upload:** Go to `/` and select files to upload.
- **Download:** Go to `/downloads.html` to see and download uploaded files.

## File Structure
- `server.py` — Main Flask server
- `public/` — Static HTML pages
- `uploads/` — Uploaded files
- `start.bat` — Windows start script

## Security Notes
- Filenames are sanitized, but this is a minimal demo. For production, add authentication and HTTPS.

## License
MIT
