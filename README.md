# ADAPTbaby

ADAPTbaby is an experimental framework for testing and comparing various AI models, including Groq, OpenAI, Google, and Anthropic. It provides a user-friendly interface for testing models, visualizing performance metrics, and managing API keys.

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard](#dashboard)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/TeamADAPT/ADAPTbaby.git
   cd ADAPTbaby
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

4. Run the application:
   ```bash
   python adaptbaby_main.py
   ```

5. Open your browser and navigate to `http://localhost:8080` to access the ADAPTbaby dashboard.

## Features

- Multi-model testing: Compare responses from various AI models including Groq, OpenAI, Google, and Anthropic.
- Interactive dashboard: Visualize model usage, response times, and function relationships.
- API key management: Securely store and manage API keys for different AI services.
- Extensible architecture: Easily add new models or features to the framework.

## Installation

Detailed installation instructions can be found in the [Installation Guide](docs/installation.md).

## Usage

1. Navigate to the test models page.
2. Enter your prompt in the text area.
3. Click "Test Models" to send the prompt to all available AI models.
4. View the responses and performance metrics for each model.

For more detailed usage instructions, please refer to the [User Guide](docs/user_guide.md).

## Dashboard

The ADAPTbaby dashboard provides several visualizations and management tools:

- Model Usage Graph: Shows the frequency of use for each AI model.
- Response Time Graph: Displays the average response time for each model.
- Function Call Graph: Visualizes the relationships between different functions in the application.
- Recent Testing History: Lists the most recent model tests performed by the user.

To access the dashboard, navigate to `http://localhost:8080/dashboard` after starting the application.

## Contributing

We welcome contributions to ADAPTbaby! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get started.

## License

ADAPTbaby is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
