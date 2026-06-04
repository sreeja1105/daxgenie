# Contributing to DAXGenie

Thanks for your interest in contributing! Contributions that improve documentation, add example prompts, fix bugs, or enhance tests are especially welcome.

## How to file issues
- Please open an issue in this repository describing the bug, feature request, or documentation change.
- Include reproduction steps, expected vs actual behaviour, and any relevant logs or screenshots.

## Development setup
1. Fork the repo and create a feature branch.
2. Set up a virtual environment and install dev dependencies:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Run the app locally for manual testing:

```bash
streamlit run app.py
```

4. Run tests:

```bash
pytest -q
```

## Coding style
- Keep functions small and focused.
- Follow PEP8; line length up to 120 chars is acceptable for this project.
- Add unit tests for new behavior where practical.

## Pull requests
- Open a pull request against the `main` branch with a clear title and description.
- Link related issues and include screenshots or GIFs for UI changes.
- CI will run tests and linter; ensure they pass before requesting review.

## License
By contributing you agree that your contributions will be licensed under the project's MIT license.

Thank you — contributions make this project better for Power BI analysts everywhere!
