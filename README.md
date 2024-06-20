# Demo

This project includes:

- Shell scripts for setting up the NVIDIA Docker container
- Python code for the Gradio frontend
- TODO: Vector database for RAG
- TODO: Remove the keys and put the IP addresses, etc., in environment variables

## Setup

1. Make sure you can pull images from the NGC Catalog [NGC Catalog](https://catalog.ngc.nvidia.com/). Follow the instructions [here](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html#ngc-authentication).

2. Once you have the Docker image, you should be able to start the server (check you have all the necessary api keys etc.) :
   ```sh
   ./nim_server.sh

3. The frontend uses Gradio:
   ```sh
   python3 ./chat.py

   
