# 0x03. Unittests and Integration Tests

This project focuses on writing unit and integration tests in Python using `unittest`, `parameterized`, and `unittest.mock`.

## Learning Objectives

- Difference between unit and integration tests
- Common testing patterns: mocking, parametrizations, fixtures
- How to mock external dependencies (HTTP calls, methods, properties)
- How to use `parameterized` for data-driven tests
- How to parameterize test classes with fixtures

## Files

- `utils.py`: Contains `access_nested_map`, `get_json`, `memoize`
- `client.py`: Contains `GithubOrgClient`
- `test_utils.py`: Unit tests for `utils.py`
- `test_client.py`: Unit and integration tests for `client.py`
- `fixtures.py`: Test payloads for integration tests

## Requirements

- Python 3.7
- pycodestyle 2.5
- All files executable and properly shebanged
- Full documentation for modules, classes, and functions

## Usage

```bash
python3 -m unittest discover
