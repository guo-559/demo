# Demo

This project includes:

- Shell scripts for setting up the NVIDIA Docker container
- A simple Gradio frontend
- Some RAG examples
- TODO: Remove the keys and put the IP addresses, etc., in environment variables

## Setup

1. Make sure you can pull images from the [NGC Catalog](https://catalog.ngc.nvidia.com/). Follow the instructions [here](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html#ngc-authentication).

2. Once you have the Docker image, you should be able to start the server (check you have all the necessary api keys etc.) :
   ```sh
   ./nim_server.sh

3. The frontend uses Gradio:
   ```sh
   python3 ./chat.py

4. For the code in the elastic folder, it uses the NVIDIA NIM image for generation, but the elastic database needs to be intialized. There's an example environment file here which is needed (rename the extension to .env)
