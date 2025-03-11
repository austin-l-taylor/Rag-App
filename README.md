# McKenney's AI RAG Application

This is a Streamlit application that allows you to chat with OpenAI's GPT models and provides the functionality to upload a PDF document and ask questions about its content.

## Features

- **Chat with GPT Models**: Interact with OpenAI's GPT models (`gpt-4o-mini` and `gpt-4o`) directly through the app.
- **Temperature Control**: Adjust the randomness and creativity of the AI's responses using the temperature slider.
- **PDF Chat**: Upload a PDF document and ask questions about its content. The app processes the document and provides answers based on the content.
- **Chat History Export**: Export your chat history as a CSV file for future reference.

## Installation

### Prerequisites

- Python 3.7 or higher
- [OpenAI API Key](https://platform.openai.com/account/api-keys)

### Create a Virtual Environment

```bash
python -m venv venv
# Activate the virtual environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Keeper Environment

```SECRET_ID``` Should point to a Keeper UID container your API key:

```bash  
# Configuration
SECRET_ID = "6VKizQ3fK7fSPq41w8E5zg"

Keeper.authorize()
secret = Keeper.client.get_secrets([SECRET_ID])[0]
secret = secret.custom_field("Secret", field_type=None, value=None)
api_key = secret[0]
```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your default web browser.

### How to Use the App

1. **Select the Model**: Choose between `gpt-4o-mini` and `gpt-4o` from the sidebar.
   - **gpt-4o-mini**: A smaller model that is faster and cheaper to use.
   - **gpt-4o**: A larger model that is more accurate and can generate more detailed responses.
2. **Adjust Temperature**: Use the slider to control the randomness of the AI's responses.
   - A higher temperature results in more creative and unpredictable responses.
   - A lower temperature makes the responses more focused and deterministic.
3. **PDF Chat (Optional)**:
   - Toggle the **PDF Chat** option in the sidebar.
   - Upload a PDF document using the file uploader.
   - Once uploaded, the app will process the PDF (this may take a few moments).
   - You can now ask questions about the content of the PDF.
4. **Start Chatting**: Type your message in the input box at the bottom of the app and press Enter.
5. **Export Chat History**: Click the **Download Chat Log** button to export your chat history as a CSV file.

## Docker Instructions

### Building and Pushing a New Docker Image Version

To create a new version of your Docker image and push it to your Docker repository, follow these steps:

1. **Build the Docker Image**: Navigate to the directory containing your `Dockerfile` and run the following command to build the image. Replace `v1.1` with your desired version tag.

    ```sh
    docker build -t atay95/streamlit-app:v1.1 .
    ```

2. **Tag the Docker Image**: Tag the Docker image with the repository name. Replace `v1.1` with your desired version tag.

    ```sh
    docker tag atay95/streamlit-app:v1.1 atay95/streamlit-app:v1.1
    ```

3. **Log in to Docker Hub**: Log in to your Docker Hub account if you haven't already:

    ```sh
    docker login
    ```

4. **Push the Docker Image**: Push the tagged image to your Docker repository:

    ```sh
    docker push atay95/streamlit-app:v1.1
    ```

### Example Commands

Here is a summary of the commands:

#### Step 1: Build and Tag the Docker image
```sh
docker build -t atay95/streamlit-app:v1.1 .
```

#### Step 2: Log in to Docker Hub
```sh
docker login
```

#### Step 3: Push the Docker image to the repository
```sh
docker push atay95/streamlit-app:v1.1
```

### Notes

- **Resetting the App**: Refresh the page if you wish to reset the chat history or switch to a different PDF.
- **Need Help?**: Click on the **Need help?** expander within the app for additional information.

## Troubleshooting

- **Error Messages**: If you encounter errors, they will be displayed within the app. Check the terminal for detailed logs.
- **PDF Processing Issues**: Ensure that the PDF file is not corrupted and is in a readable format.
- **API Key Issues**: Make sure your OpenAI API key is valid and properly set in the environment variables.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for providing an easy way to build web apps in Python.
- [OpenAI](https://openai.com/) for the GPT models.
- [LangChain](https://github.com/hwchase17/langchain) for making it easier to work with language models.

## Contact

For questions or feedback, please open an issue in the repository or reach out to one of the contributors.