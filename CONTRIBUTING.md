# Contributing to MCP Bug Bounty Agent

We welcome contributions from the security research community!

## Development Setup

```bash
git clone https://github.com/your-org/mcp-bugbounty-agent.git
cd mcp-bugbounty-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Code Style

- Use Black for code formatting: `black src/`
- Use flake8 for linting: `flake8 src/`
- Follow PEP 8 guidelines
- Add type hints where possible

## Testing

```bash
pytest tests/ -v
python examples/demo_script.py
```

## Security Guidelines

- Only contribute features for authorized testing
- Follow responsible disclosure practices
- Document security implications of changes
- Test thoroughly in isolated environments

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation
7. Submit pull request

## Issue Reporting

- Use GitHub issues for bug reports
- Include reproduction steps
- Provide environment details
- For security issues, email security@bugbounty-agent.com
