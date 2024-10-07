# ADAPTbaby

ADAPTbaby is an extension of the BabyAGI project, focusing on building a self-improving AI agent with a user-friendly GUI. The project aims to create a system that can adapt and learn from interactions, gradually expanding its capabilities.

## Features

- Enhanced AI agent with memory capabilities and conversation history support
- Multiple LLM model support with user-selectable options (OpenAI, Anthropic, Gemini, and Hugging Face models)
- Interactive and visually appealing chat interface with markdown support
- Task processing workflow (analysis, planning, execution, summarization)
- Detailed task information display with download functionality
- Function relationship visualization (standard, Mermaid, and 3D graphs)
- Responsive design for various screen sizes
- Debug mode for advanced users

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- API keys for:
  - OpenAI
  - Anthropic
  - Google (for Gemini models)
  - Hugging Face

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
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   HF_ACCESS_API_TOKEN=your_huggingface_access_token_here
   ```

## Running the Application

1. Ensure you're in the project directory and your virtual environment is activated.

2. Run the application:
   ```
   python adaptbaby_main.py
   ```

3. Open a web browser and navigate to `http://localhost:8080/adaptbaby` to access the ADAPTbaby dashboard.

## Usage

1. Select an LLM model from the dropdown menu (OpenAI, Anthropic, Gemini, or Hugging Face).
2. Enter your task or question in the input box and click "Send" or press Enter.
3. View the AI's response in the chat interface.
4. Toggle debug mode to see detailed task information.
5. Use the download button to save task details as a markdown file.
6. Navigate through different sections using the top navigation bar.

## Available Models

- OpenAI Models: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo, GPT-3.5 Turbo 16k, and more
- Anthropic Models: Claude 2.1, Claude Instant 1.2, Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
- Gemini Models: Gemini Pro, Gemini Pro Vision, Gemini 1.5 Pro (various versions)
- Hugging Face Models: DistilBERT (for sentiment analysis), GPT-2, and other models available through the Hugging Face API

## Documentation

For detailed information on specific aspects of the project, please refer to the following documents:

- [GitHub Integration Challenges](github_challenges.md): Outlines the challenges encountered while integrating GitHub models and the solutions attempted.
- [Hugging Face Installation Guide](huggingface_installation.md): Provides step-by-step instructions for installing and setting up Hugging Face models in the project.

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
- Anthropic for the Claude models
- Google for the Gemini models
- Hugging Face for their extensive model library and APIs
- The BabyAGI project for the initial inspiration

## Contact

For any questions or feedback, please open an issue on the GitHub repository or contact the project maintainers.

## Recent Updates

As of the latest commit:
- Updated `adaptbaby_main.py` with expanded multi-model support, including OpenAI, Anthropic, Gemini, and Hugging Face models
- Integrated multiple LLM providers and implemented `langchain_completion` function to handle different model types
- Enhanced `adaptbaby_agent` to use the new completion function
- Successfully tested integration with various models from different providers
- Improved error handling and logging for better debugging and monitoring

Current Development Status:
- The project now supports a wide range of models from OpenAI, Anthropic, Google (Gemini), and Hugging Face
- Updates include changes to dashboard components, templates, function packs, and examples
- The project is actively being developed with ongoing improvements to various aspects of the system

Next Steps:
- Implement error handling for cases where specific models might not be available or API keys are missing
- Optimize the model selection process in the user interface
- Develop unit tests for each model integration to ensure ongoing reliability
- Consider implementing a caching mechanism for frequently used models to improve performance
- Continue refining the multi-model support implementation
- Implement user authentication and session management
- Develop a visual representation of the agent's knowledge graph

For a detailed progress log, please refer to the `BABES_ADAPTbaby_Progress.md` file in the project root.
