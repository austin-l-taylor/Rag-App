# AI RAG Application

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

### Create a Virtual Environment (Optional but Recommended)

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

### Set Up Environment Variables

Create a `.env` file in the root directory of the project and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key
```

Alternatively, you can set the environment variable in your shell:

- **Windows**

  ```bash
  set OPENAI_API_KEY=your_openai_api_key
  ```

### Setup API Key

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

Make sure you have set the `OPENAI_API_KEY` environment variable as instructed above.

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

For questions or feedback, please open an issue in the repository.
