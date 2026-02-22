# Tests

Test suite for the review-tool using pytest.

## Test Structure

- **test_extraction.py** - Tests for p5 synth reference extraction from JavaScript files
  - Validates that p5.PolySynth and p5.Oscillator are correctly extracted
  - Tests data structure validation

- **test_comparison.py** - Tests for file comparison logic
  - Validates that synth references are detected during file comparison
  - Tests that references are properly separated (PolySynth vs Oscillator)

- **test_rendering.py** - Tests for TUI rendering logic
  - Validates that synth detection renders correctly in the UI
  - Tests that rendering sections don't overlap

- **conftest.py** - Pytest configuration and shared fixtures
  - Provides file path fixtures for test files

## Running Tests

### Run all tests
```bash
uv run pytest tests/ -v
```

### Run specific test file
```bash
uv run pytest tests/test_extraction.py -v
```

### Run specific test
```bash
uv run pytest tests/test_extraction.py::test_polysynth_extraction -v
```

### Run with coverage
```bash
uv run pytest tests/ --cov=src/review_tool
```

## Test Results

All 14 tests currently pass, validating:
- ✅ p5.PolySynth extraction from POLYSYNTH file
- ✅ p5.Oscillator extraction from OSCILLATOR file
- ✅ Comparison detection of synth references
- ✅ Rendering logic for separate synth type reporting
- ✅ Data structure validation across all modules

## Adding Tests

To add new tests:

1. Create a test file in the `tests/` directory following the `test_*.py` naming convention
2. Define test functions prefixed with `test_`
3. Use pytest fixtures from `conftest.py` as needed
4. Use assertions to validate behavior

Example:
```python
def test_my_feature(polysynth_file):
    """Test description."""
    content = read_file(polysynth_file)
    assert len(content) > 0, "File should have content"
```
