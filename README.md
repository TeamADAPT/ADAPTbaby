# ADAPTbaby

ADAPTbaby is an extension of the BabyAGI project, focusing on building a self-improving AI agent with a user-friendly GUI. The project aims to create a system that can adapt and learn from interactions, gradually expanding its capabilities.

## Features

- Enhanced AI agent with memory capabilities and conversation history support
- Multiple LLM model support with user-selectable options (GPT-4o, GPT-3.5 Turbo, etc.)
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

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OpenAI_PROJECT_API_KEY=your_api_key_here
   ```

## Running the Application

1. Ensure you're in the project directory and your virtual environment is activated.

2. Run the application:
   ```
   python adaptbaby_main.py
   ```

3. Open a web browser and navigate to `http://localhost:8080/adaptbaby` to access the ADAPTbaby dashboard.

## Usage

1. Select an LLM model from the dropdown menu.
2. Enter your task or question in the input box and click "Send" or press Enter.
3. View the AI's response in the chat interface.
4. Toggle debug mode to see detailed task information.
5. Use the download button to save task details as a markdown file.
6. Navigate through different sections using the top navigation bar.

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
- The BabyAGI project for the initial inspiration

## Contact

For any questions or feedback, please open an issue on the GitHub repository or contact the project maintainers.

## Recent Updates

As of the latest commit (886ab90):
- Updated `adaptbaby_main.py` with multi-model support
- Integrated multiple LLM providers (OpenAI, Azure AI, Google Gemini, Anthropic)
- Updated model selection logic and implemented `langchain_completion` function
- Enhanced `adaptbaby_agent` to use the new completion function

Current Development Status:
- Many files across the project have been modified and are pending staging and commit
- Updates include changes to dashboard components, templates, function packs, and examples
- The project is actively being developed with ongoing improvements to various aspects of the system

Next Steps:
- Review and stage modified files
- Commit changes with descriptive commit messages
- Update documentation to reflect all recent changes and new features
- Continue testing and refining the multi-model support implementation
