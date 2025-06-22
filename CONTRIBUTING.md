# Contributing to Custom Commands

Thanks for your interest in contributing!

## Ground Rules

- Be respectful and follow our [Code of Conduct](CODE_OF_CONDUCT.md)
- All contributions are welcome: bug reports, new features, improvements, docs
- Keep the tool simple and useful

## How to Contribute

1. **Fork the repo**
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes (write clear code and comments)
4. Commit (`git commit -m "Add: your change here"`)
5. Push (`git push origin feature/your-feature-name`)
6. Open a Pull Request (PR)

## Testing

- Run your commands locally
- Keep changes backwards compatible if possible
- Add comments to explain non-obvious logic

## Conventions

- Bash scripts: POSIX-compliant where possible
- Use `set -e` to fail fast on errors
- Keep command names short but descriptive
- Avoid hardcoding file paths or absolute dependencies

## Code Review Process

All PRs will be reviewed by maintainers. Be prepared to make changes if requested.

---
