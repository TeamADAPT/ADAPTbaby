# ADAPTbaby

ADAPTbaby is an experimental framework for a self-building autonomous agent, inspired by the BabyAGI concept. It combines AI model testing capabilities with the ability to generate and execute new functions based on user input.

## Features

- Multi-model testing: Compare responses from various AI models including Groq, OpenAI, Google, and Anthropic.
- Interactive dashboard: Visualize model usage, response times, and function relationships.
- Self-building capability: Generate and execute new functions based on user prompts.
- API key management: Securely store and manage API keys for different AI services.
- Extensible architecture: Easily add new models or features to the framework.

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

## Self-Building Autonomous Agent

ADAPTbaby implements a self-building autonomous agent concept. The `/self_build` endpoint allows users to input prompts that generate new Python functions. These functions are then executed within the application, demonstrating the system's ability to extend its own capabilities.

To use this feature:

1. Send a POST request to `/self_build` with a JSON payload containing a `prompt` field.
2. The system will generate a Python function based on the prompt using the Groq model.
3. The generated function will be executed, and the result will be returned.

This feature showcases the potential for creating an AI system that can expand its own functionality based on user input and needs.

## Contributing

We welcome contributions to ADAPTbaby! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get started.

## License

ADAPTbaby is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
