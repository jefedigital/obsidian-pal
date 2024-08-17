# YourPal - Obsidian Search Plugin

YourPal is a Python-based assistant for [Obsidian](https://obsidian.md/) that provides powerful and efficient utilities to aid in knowledge management and research.

## Modules

### 1. Natural Language Search
YourPal uses the [BM25S](https://huggingface.co/blog/xhluca/bm25s) algorithm to index and search your notes, offering more relevant results than Obsidian's built-in search.

### 2. More to come ..

## Installation

1. Download the latest release from the GitHub repository.
2. Extract the ZIP file into your Obsidian plugins folder: `<vault>/.obsidian/plugins/`
3. Restart Obsidian and enable the YourPal plugin in the settings.

## Backend Setup

The YourPal plugin requires a Python backend to function. Follow these steps to set up the backend:

1. Ensure you have Python 3.7+ installed on your system.
2. Navigate to the `backend` directory in the project.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```
   uvicorn main:app --reload
   ```

## Configuration

1. Open Obsidian Settings and navigate to the YourPal plugin settings.
2. Set the Backend URL (default is `http://localhost:8000`).
3. Click "Test Connection" to ensure the plugin can communicate with the backend.

## Usage

1. Click the YourPal icon in the Obsidian ribbon or use the command "Open YourPal Search".
2. In the YourPal search view, click "Index Vault" to create or update the search index.
3. Enter your search query in the input field and press Enter.
4. Click on any search result to open the corresponding file.


## Development

To set up the development environment:

1. Clone the repository.
2. Install dependencies for both the plugin and the backend:
   ```
   npm install
   cd backend && pip install -r requirements.txt
   ```
3. Use `npm run dev` to watch for changes and build the plugin.
4. Start the backend server with `uvicorn main:app --reload` in the `backend` directory.

## Contributing

Contributions are welcome! Please feel free to submit a PR.

## License

This project is licensed under the MIT License.

## Support

If you encounter any issues or have questions, please file an issue on this GitHub repo.

