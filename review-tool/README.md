# Donald 2021 - Animation Review Tool

A Python tool for reviewing and analyzing student JavaScript animation submissions for the Donald 2021 memory testing application.

## Features

### Preflight Validation
- **Missing Functions**: Detects if student submissions lack required functions (`showIdle`, `showPrepare`, etc.)
- **Missing Variables**: Checks for all required timing variables (T0-T7) and color arrays
- **ID Validation**: Ensures students have changed the default `YOUR_GROUP` ID
- **Structure Checks**: Validates proper array sizes and required function calls

### Similarity Analysis
- **Overall Similarity Score**: 0-100% comparison to the base template
- **Component Breakdown**: Separate scores for:
  - **Timings**: Did the student modify timing parameters?
  - **Colors**: Did the student change color schemes?
  - **Functions**: Did the student modify animation logic?
- **Change Detection**: Identifies specific modifications made


### Sound Detection
- **p5.Oscillator Detection**: Automatically detects use of `p5.Oscillator()` for tone generation
- **p5.PolySynth Detection**: Automatically detects use of `p5.PolySynth()` for polyphonic synthesis
- **Scope Tracking**: Shows whether sound objects are used globally or within specific functions
- **Visual Indicators**: 🎺 for Oscillator, 🎹 for PolySynth in the UI

### Two Modes of Operation

#### 1. Validation Mode (CLI)
```bash
review-tool /path/to/static/ --validate
```
Outputs a detailed report of all files with validation results and similarity scores.

#### 2. Interactive TUI Mode
```bash
review-tool /path/to/static/
```
Launches a textual user interface with:
- **Left Panel**: File browser showing all animation-*.js files (scrollable)
- **Right Panel**: Detailed validation and comparison results for selected file (scrollable)
- **Navigation**: Use arrow keys to select files, scroll with mouse or arrow keys, `r` to refresh, `q` to quit
- **Auto-scroll**: Right panel automatically scrolls when content exceeds viewport height

## Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage Examples

### Validate all files in a directory
```bash
review-tool /path/to/animations/ --validate
```

### Use default base file (animations.js in same directory)
```bash
review-tool /path/to/animations/
```

### Specify a custom base file
```bash
review-tool /path/to/animations/ --base /path/to/animations.js
```

### Use current directory
```bash
review-tool
```

## Output Format

### Validation Results
- ✓ VALID: File passes all checks
- ✗ INVALID: File has errors that should be fixed
- ⚠ WARNINGS: Non-fatal issues (e.g., unusual values)

### Similarity Scoring
```
Overall:    72.5%
  Timings:    37.5%
  Colors:     87.5%
  Functions:  87.5%
```

- **100%**: Identical to base
- **90-100%**: Minimal changes (likely just data tweaks)
- **70-90%**: Good modifications (timings/colors updated)
- **50-70%**: Significant changes (logic may be modified)
- **<50%**: Major changes or structural problems

## Architecture

### Modules

- **[utils.py](src/review_tool/utils.py)**: File discovery and parsing
  - `find_animation_files()`: Locate animation-*.js files
  - `extract_id()`, `extract_timings()`, `extract_color_arrays()`, `extract_functions()`
  - `extract_p5_synth_references()`: Detect p5.Oscillator and p5.PolySynth usage
   
- **[validator.py](src/review_tool/validator.py)**: Submission validation
  - `validate_animation_file()`: Run all validation checks
  - `ValidationResult`: Class holding validation status and error messages
  
- **[comparator.py](src/review_tool/comparator.py)**: Similarity analysis
  - `compare_to_base()`: Calculate similarity scores
  - `ComparisonResult`: Class holding comparison metrics and changes detected
  
- **[tui.py](src/review_tool/tui.py)**: Textual user interface
  - `ReviewApp`: Main application class
  - `FileBrowser`: Scrollable widget for file selection
  - `ValidationPanel`: Scrollable display area for results with reactive updates
  
- **[__init__.py](src/review_tool/__init__.py)**: CLI entry point

## What Makes a Valid Submission?

Required elements:
1. **Modified ID**: Not 'YOUR_GROUP'
2. **All 8 Timing Variables**: T0_IDLE through T7_INCORRECT
3. **All 8 Functions**: showIdle, showPrepare, showTestStep, showDecay, showCountdown, showTimeout, showSuccess, showFailure
4. **All 8 Color Arrays**: idleColors, prepColors, blokColors, decayColors, countColors, timeoutColors, successColors, failColors
5. **Proper Structure**: Functions contain showButtons() and showLeds() calls

## Common Student Mistakes Detected

- ✗ Submitting unmodified template (ID still 'YOUR_GROUP')
- ✗ Missing functions or color arrays entirely
- ✗ Broken function structure
- ✗ Incorrect file (wrong JavaScript submitted)

## Example Output

```
============================================================
File: animations-0.js
============================================================
✓ VALID

Similarity: 72.5%
  Timings:    37.5%
  Colors:     87.5%
  Functions:  87.5%

Timing Changes (5):
  T0: 20 → 10
  T1: 120 → 60
  T2: 40 → 20
  T3: 120 → 60
  T4: 360 → 240
```

## Development

### Running Tests
```bash
pytest
```

Run specific test suites:
```bash
pytest tests/test_extraction.py     # Sound detection tests
pytest tests/test_comparison.py     # Comparison logic tests
pytest tests/test_tui_render_comparison.py  # UI rendering tests
```

### Building
```bash
uv build
```
