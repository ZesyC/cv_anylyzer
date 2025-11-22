# Contributing to CV Analyzer

Thank you for considering contributing to CV Analyzer! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, Node version, etc.)

**Bug Report Template**:

```markdown
**Description**: Brief description of the bug

**Steps to Reproduce**:

1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happens

**Environment**:

- OS: [e.g., macOS 13.0]
- Python: [e.g., 3.10.5]
- Node: [e.g., 18.0.0]
- Browser: [e.g., Chrome 120]

**Additional Context**: Any other relevant information
```

### Suggesting Features

Feature suggestions are welcome! Please:

1. Check if the feature has already been suggested
2. Provide a clear use case
3. Explain why this feature would be useful
4. Consider implementation complexity

**Feature Request Template**:

```markdown
**Feature Description**: Brief description

**Use Case**: Why this feature is needed

**Proposed Solution**: How it should work

**Alternatives Considered**: Other approaches you've thought about

**Additional Context**: Screenshots, mockups, etc.
```

### Pull Request Process

1. **Fork the repository** and create your branch from `develop`:

   ```bash
   git checkout -b feature/my-feature develop
   ```

2. **Make your changes**:

   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**:

   ```bash
   # Backend
   cd backend
   pytest

   # Frontend
   cd frontend
   npm test
   ```

4. **Commit your changes** following commit conventions:

   ```bash
   git commit -m "feat: add keyword extraction feature"
   ```

5. **Push to your fork**:

   ```bash
   git push origin feature/my-feature
   ```

6. **Create a Pull Request**:
   - Use a clear, descriptive title
   - Reference related issues
   - Describe what changed and why
   - Include screenshots for UI changes

**Pull Request Template**:

```markdown
## Description

Brief description of changes

## Related Issues

Closes #123

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)

[Add screenshots]

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
```

## Development Setup

See [Development Guide](docs/development.md) for detailed setup instructions.

**Quick Start**:

```bash
# Clone and setup
git clone <your-fork>
cd cv-analyzer
scripts/setup.sh

# Start development
scripts/dev.sh
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Maximum line length: 88 characters
- Use type hints
- Write docstrings for public functions

**Example**:

```python
def process_cv(file_path: str, options: dict) -> dict:
    """
    Process CV file and return analysis results.

    Args:
        file_path: Path to the CV file
        options: Processing options

    Returns:
        Dictionary containing analysis results

    Raises:
        ValueError: If file format is unsupported
    """
    pass
```

### TypeScript Style Guide

- Follow [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Use 2 spaces for indentation
- Prefer functional components
- Use explicit type annotations
- Avoid `any` type

**Example**:

```typescript
interface AnalysisOptions {
  includeKeywords: boolean;
  generateSuggestions: boolean;
}

export const analyzeCV = async (
  file: File,
  options: AnalysisOptions
): Promise<AnalysisResult> => {
  // Implementation
};
```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

**Format**: `<type>(<scope>): <subject>`

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, missing semi-colons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Examples**:

```bash
feat(backend): add PDF text extraction service
fix(frontend): resolve file upload validation bug
docs: update API reference with new endpoints
refactor(backend): simplify error handling logic
test(frontend): add unit tests for FileUpload component
```

**Scope** (optional): Package or component affected (backend, frontend, api, ui, etc.)

## Testing Requirements

### Backend Tests

- Write tests for all new services and endpoints
- Maintain minimum 80% code coverage
- Use pytest fixtures for test data
- Mock external API calls

**Example**:

```python
def test_extract_text_from_pdf(sample_pdf_path):
    """Test PDF text extraction."""
    result = extract_text_from_pdf(sample_pdf_path)
    assert result is not None
    assert len(result) > 100
    assert "experience" in result.lower()
```

### Frontend Tests

- Write tests for new components
- Test user interactions
- Test API integration
- Maintain minimum 70% code coverage

**Example**:

```typescript
test("FileUpload shows validation error for invalid file", async () => {
  const { getByTestId } = render(<FileUpload />);
  const input = getByTestId("file-input");

  // Upload invalid file
  fireEvent.change(input, { target: { files: [invalidFile] } });

  await waitFor(() => {
    expect(getByText("Invalid file format")).toBeInTheDocument();
  });
});
```

## Documentation

When adding features:

1. Update relevant documentation in `/docs`
2. Add inline code comments for complex logic
3. Update API reference if endpoints changed
4. Add examples for new functionality
5. Update README if user-facing changes

## Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Urgent production fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

## Review Process

All submissions require review. We use GitHub pull requests for this purpose:

1. **Automated Checks**: CI/CD will run tests and linting
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, maintainers will merge

**Review Criteria**:

- Code quality and style
- Test coverage
- Documentation completeness
- Performance impact
- Breaking changes (if any)

## Release Process

Releases are managed by maintainers:

1. Create release branch from `develop`
2. Update version numbers
3. Update CHANGELOG.md
4. Merge to `main`
5. Tag release
6. Deploy to production

## Getting Help

- **Documentation**: Check [docs/](docs/)
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions for questions
- **Contact**: Reach out to maintainers

## Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to CV Analyzer! 
