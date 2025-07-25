# yaml2rst Test Suite

This directory contains a comprehensive test suite for the yaml2rst project. The test suite is designed to ensure code quality, reliability, and maintainability through various types of testing.

## Test Structure

```
tests/
├── README.md                    # This file
├── conftest.py                  # Shared pytest fixtures and configuration
├── unit/                        # Unit tests for individual components
│   ├── test_yaml2rst_main.py    # Tests for main module
│   ├── test_initializer.py      # Tests for initialization logic
│   ├── test_file_generator.py   # Tests for file generation
│   ├── test_base_generator.py   # Tests for base generator class
│   └── test_category_generator.py # Tests for category generator
├── integration/                 # Integration tests
│   └── test_e2e_generation.py   # End-to-end generation tests
├── functional/                  # Functional tests
│   └── test_cli.py              # CLI interface tests
└── performance/                 # Performance tests
    └── test_performance.py      # Performance and scalability tests
```

## Test Categories

### Unit Tests (`tests/unit/`)

Unit tests focus on testing individual components in isolation. They use extensive mocking to isolate the code under test and verify specific behaviors.

**Coverage includes:**
- Main module functionality (`test_yaml2rst_main.py`)
- Initialization and argument parsing (`test_initializer.py`)
- File generation logic (`test_file_generator.py`)
- Base generator class (`test_base_generator.py`)
- Content generators (`test_category_generator.py`)

### Integration Tests (`tests/integration/`)

Integration tests verify that multiple components work together correctly. They test the interaction between different parts of the system.

**Coverage includes:**
- End-to-end generation workflows
- Component integration
- Data flow between generators and file writers
- Multi-language support

### Functional Tests (`tests/functional/`)

Functional tests verify the system's behavior from a user's perspective, focusing on the command-line interface and user workflows.

**Coverage includes:**
- CLI argument parsing and validation
- Command execution workflows
- Error handling and user feedback
- Configuration management

### Performance Tests (`tests/performance/`)

Performance tests ensure the system performs well under various conditions and scales appropriately.

**Coverage includes:**
- Large dataset processing
- Memory usage optimization
- Scalability testing
- Concurrent operation simulation
- Memory leak detection

## Running Tests

### Prerequisites

Install test dependencies:

```bash
pip install pytest pytest-cov pytest-mock psutil
```

Optional dependencies for enhanced testing:
```bash
pip install pytest-xdist flake8  # For parallel execution and code style
```

### Basic Test Execution

Run all tests:
```bash
python run_tests.py
```

Run specific test categories:
```bash
python run_tests.py --type unit
python run_tests.py --type integration
python run_tests.py --type functional
python run_tests.py --type performance
```

### Advanced Options

Run with coverage reporting:
```bash
python run_tests.py --coverage
```

Run in verbose mode:
```bash
python run_tests.py --verbose
```

Skip slow tests (performance tests):
```bash
python run_tests.py --fast
```

Run tests in parallel:
```bash
python run_tests.py --parallel
```

### Direct pytest Usage

You can also run tests directly with pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_yaml2rst_main.py

# Run with coverage
pytest --cov=src/yaml2rst --cov-report=html

# Run specific test class or method
pytest tests/unit/test_file_generator.py::TestFileGenerator::test_initialization

# Run tests matching a pattern
pytest -k "test_generation"

# Run tests with specific markers
pytest -m "not slow"  # Skip slow tests
pytest -m "slow"      # Run only slow tests
```

## Test Configuration

### pytest.ini

The `pytest.ini` file in the project root contains pytest configuration:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    functional: marks tests as functional tests
    performance: marks tests as performance tests
addopts = 
    --strict-markers
    --tb=short
    -ra
```

### Fixtures

Common fixtures are defined in `conftest.py`:

- `temp_dir`: Provides a temporary directory for test files
- `mock_templates`: Provides mock template objects for testing
- Various other fixtures for common test setup

## Writing Tests

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`
- Use descriptive names that explain what is being tested

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
def test_example_functionality(self):
    # Arrange
    generator = SomeGenerator('ja')
    test_data = {'key': 'value'}
    
    # Act
    result = generator.process(test_data)
    
    # Assert
    assert result['processed'] is True
    assert result['key'] == 'value'
```

### Mocking Guidelines

- Mock external dependencies (file system, network, etc.)
- Use `unittest.mock.patch` for patching
- Mock at the appropriate level (not too high, not too low)
- Verify mock calls when behavior is important

### Test Categories and Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.slow
def test_large_dataset_processing(self):
    # Test that takes significant time
    pass

@pytest.mark.integration
def test_component_integration(self):
    # Test that verifies component interaction
    pass
```

## Coverage Goals

The test suite aims for high code coverage:

- **Minimum coverage**: 85%
- **Target coverage**: 90%+
- **Critical paths**: 100% coverage for core functionality

Coverage reports are generated in HTML format when using the `--coverage` option.

## Continuous Integration

The test suite is designed to run in CI environments:

- All tests should be deterministic
- No external dependencies (use mocking)
- Reasonable execution time (< 5 minutes for full suite)
- Clear failure reporting

## Performance Benchmarks

Performance tests establish benchmarks for:

- **Generation speed**: < 0.1s per item for typical content
- **Memory usage**: < 100MB increase for 1000 items
- **Scalability**: Linear scaling with dataset size
- **Memory leaks**: No significant memory growth over time

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure the `src` directory is in the Python path
2. **Mock failures**: Check that mocks match the actual interface
3. **Slow tests**: Use `--fast` to skip performance tests during development
4. **Coverage issues**: Check that all code paths are tested

### Debug Mode

Run tests with additional debugging:

```bash
pytest --pdb          # Drop into debugger on failure
pytest --lf           # Run only last failed tests
pytest --tb=long      # Show full tracebacks
pytest -s             # Don't capture output (show prints)
```

## Contributing

When adding new functionality:

1. Write tests first (TDD approach recommended)
2. Ensure all test categories are covered
3. Add appropriate markers for test categorization
4. Update this README if adding new test patterns
5. Maintain or improve coverage percentage

### Test Review Checklist

- [ ] Tests cover happy path and error cases
- [ ] Appropriate mocking is used
- [ ] Tests are deterministic and isolated
- [ ] Performance implications are considered
- [ ] Documentation is updated if needed

## Best Practices

1. **Keep tests simple and focused**: One concept per test
2. **Use descriptive test names**: Should explain what is being tested
3. **Mock external dependencies**: Tests should be isolated
4. **Test edge cases**: Not just the happy path
5. **Maintain test performance**: Tests should run quickly
6. **Use fixtures for common setup**: Avoid code duplication
7. **Test error conditions**: Verify proper error handling
8. **Keep tests maintainable**: Refactor tests when code changes

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)
