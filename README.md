# ADAPTbaby

ADAPTbaby is an extension of the BabyAGI project, focusing on building a self-improving AI agent with a user-friendly GUI. The project aims to create a system that can adapt and learn from interactions, gradually expanding its capabilities.

## Features

- Enhanced AI agent with memory capabilities and conversation history support
- Multiple LLM model support with user-selectable options (OpenAI models, GitHub Models)
- Interactive and visually appealing chat interface with markdown support
- Task processing workflow (analysis, planning, execution, summarization)
- Detailed task information display with download functionality
- Function relationship visualization (standard, Mermaid, and 3D graphs)
- Responsive design for various screen sizes
- Debug mode for advanced users

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- OpenAI API key
- GitHub Models API key (for Azure AI models)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/ADAPTbaby.git
   cd ADAPTbaby
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OpenAI_PROJECT_API_KEY=your_openai_api_key_here
   TeamADAPT_GitHub_FINE_GRAINED_PAT=your_github_models_api_key_here
   GITHUB_MODELS_ENDPOINT=your_github_models_endpoint_here
   ```

## Running the Application

1. Ensure you're in the project directory and your virtual environment is activated.

2. Run the application:
   ```
   python adaptbaby_main.py
   ```

3. Open a web browser and navigate to `http://localhost:8080/adaptbaby` to access the ADAPTbaby dashboard.

## Usage

1. Select an LLM model from the dropdown menu (OpenAI or GitHub Models).
2. Enter your task or question in the input box and click "Send" or press Enter.
3. View the AI's response in the chat interface.
4. Toggle debug mode to see detailed task information.
5. Use the download button to save task details as a markdown file.
6. Navigate through different sections using the top navigation bar.

## Available Models

- OpenAI Models: GPT-4o, GPT-4o Mini, GPT-3.5 Turbo, GPT-3.5 Turbo 16k
- GitHub Models: AI21 Jumbo Instruct, Cohere Command R, Cohere Command R Plus, Meta Llama 3 (70B and 8B Instruct), Mixtral Large, Mistral Small, Phi-3 Medium Instruct 12B

## Testing

To run tests for the application, use the following command:
```
python -m unittest discover tests
```

## Contributing

Contributions to ADAPTbaby are welcome! Please refer to the `CONTRIBUTING.md` file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- OpenAI for providing the GPT models
- GitHub for providing access to various AI models
- The BabyAGI project for the initial inspiration

## Contact

For any questions or feedback, please open an issue on the GitHub repository or contact the project maintainers.

## Recent Updates

As of the latest commit:
- Updated `adaptbaby_main.py` with multi-model support, including GitHub Models
- Integrated multiple LLM providers (OpenAI and GitHub Models via Azure AI)
- Updated model selection logic and implemented `langchain_completion` function to handle different model types
- Enhanced `adaptbaby_agent` to use the new completion function
- Added support for various GitHub Models (AI21, Cohere, Meta Llama, Mixtral, Mistral, Phi)
- Improved error handling and logging for better debugging and monitoring

Current Development Status:
- The project now supports a wide range of models from both OpenAI and GitHub
- Updates include changes to dashboard components, templates, function packs, and examples
- The project is actively being developed with ongoing improvements to various aspects of the system

Next Steps:
- Continue testing and refining the multi-model support implementation
- Optimize performance for handling multiple users and tasks simultaneously
- Implement user authentication and session management
- Develop comprehensive unit tests to ensure system reliability
- Explore advanced features of GitHub Models and how they can be leveraged in the project

For a detailed progress log, please refer to the `BABES_ADAPTbaby_Progress.md` file in the project root.
