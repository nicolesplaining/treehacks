# Scrapybara Python Template

A template project for quickly getting started with the Scrapybara SDK and Act SDK for AI-powered desktop and browser automation.

## Prerequisites

- Python 3.8 or higher
- Poetry (Python package manager: https://python-poetry.org/docs/)
- A Scrapybara API key (https://scrapybara.com/dashboard)

## Setup

1. Clone this repository:

```bash
git clone https://github.com/Scrapybara/scrapybara-python-template.git
cd scrapybara-python-template
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Then edit `.env` with your API keys:

```bash
SCRAPYBARA_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_api_key_here  # Optional
```

## Project Structure

```
.
├── .env                 # Environment variables
├── pyproject.toml      # Poetry dependencies and project config
├── main.py            # Main script with Scrapybara setup
├── .cursorrules        # Cursor rules for working with the Scrapybara SDK
└── README.md          # This file
```

## Usage

Run the template script:

```bash
poetry run python main.py
```

The script will:

1. Initialize a Scrapybara client
2. Start a new instance
3. Launch a browser
4. Use the Act SDK to navigate to scrapybara.com
5. Print the agent's observations
6. Clean up resources automatically

## Customization

### Modifying the Agent's Task

Edit the `prompt` parameter in `main.py` to give the agent different instructions:

```python
prompt="Your custom instructions here"
```

### Adding More Tools

You can add more custom tools by defining them as shown in https://docs.scrapybara.com/tools#define-custom-tools

```python
tools=[
    ComputerTool(instance),
    BashTool(instance),
    EditTool(instance),
    BrowserTool(instance),
    YourNewTool(instance)
]
```

### Error Handling

The template includes basic error handling with automatic cleanup:

- Catches and prints any exceptions
- Ensures instance cleanup via `finally` block
- Stops the browser and instance properly

## Advanced Usage

### Environment Variables

Add additional environment variables to `.env` as needed:

```bash
SCRAPYBARA_API_KEY=your_key
ANTHROPIC_API_KEY=your_key  # If using your own Anthropic key
```

### Custom Model Configuration

Modify the model initialization to use your own API key:

```python
model=Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

## Cursor Rules

We've included a `.cursorrules` file that contains instructions for working with the Scrapybara SDK.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT

## Support

For Scrapybara SDK issues:

- Visit the [Scrapybara documentation](https://docs.scrapybara.com)
- Join the [Discord community](https://discord.gg/s4bPUVFXqA)
- Contact hello@scrapybara.com

For template project issues:

- Open an issue in this repository
