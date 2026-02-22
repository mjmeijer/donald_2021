"""Validation module for student animation submissions."""

from typing import Dict, List, Tuple
from .utils import (
    read_file,
    extract_id,
    extract_timings,
    extract_color_arrays,
    extract_functions,
    get_required_functions,
    get_required_color_arrays,
    get_required_timings
)


class ValidationResult:
    """Result of validating an animation file."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def add_error(self, message: str):
        """Add an error and mark as invalid."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Add a warning (non-fatal)."""
        self.warnings.append(message)
    
    def __str__(self) -> str:
        status = "✓ VALID" if self.is_valid else "✗ INVALID"
        result = f"{status}\n"
        
        if self.errors:
            result += "\nErrors:\n"
            for err in self.errors:
                result += f"  ✗ {err}\n"
        
        if self.warnings:
            result += "\nWarnings:\n"
            for warn in self.warnings:
                result += f"  ⚠ {warn}\n"
        
        return result


def validate_animation_file(filepath: str) -> ValidationResult:
    """
    Validate a student animation submission.
    
    Checks for:
    - Valid ID (not 'YOUR_GROUP')
    - All required timing variables (T0-T7)
    - All required functions
    - All required color arrays
    - Proper array sizes (12 elements for most arrays)
    
    Args:
        filepath: Path to the animation file
        
    Returns:
        ValidationResult object with details
    """
    result = ValidationResult(filepath)
    
    # Read file
    content = read_file(filepath)
    if content.startswith("ERROR:"):
        result.add_error(f"Could not read file: {content}")
        return result
    
    # Check ID
    student_id = extract_id(content)
    if student_id == "NOT_FOUND":
        result.add_error("Missing 'id' variable")
    elif student_id == "YOUR_GROUP":
        result.add_error("ID is still 'YOUR_GROUP' - appears to be unmodified template")
    
    # Check timing variables
    timings = extract_timings(content)
    missing_timings = []
    for timing_name in get_required_timings():
        if timings[timing_name] == -1:
            missing_timings.append(timing_name)
    
    if missing_timings:
        result.add_error(f"Missing timing variables: {', '.join(missing_timings)}")
    
    # Check for invalid timing values  
    for timing_name, value in timings.items():
        if value > 0 and value < 10:
            result.add_warning(f"{timing_name} value {value} seems too low (typically ≥20)")
    
    # Check functions
    functions = extract_functions(content)
    missing_functions = []
    for func_name in get_required_functions():
        if func_name not in functions:
            missing_functions.append(func_name)
    
    if missing_functions:
        result.add_error(f"Missing functions: {', '.join(missing_functions)}")
    
    # Check color arrays
    color_arrays = extract_color_arrays(content)
    missing_arrays = []
    undersized_arrays = []
    
    for array_name in get_required_color_arrays():
        if array_name not in color_arrays:
            missing_arrays.append(array_name)
        else:
            # Most arrays should have 12 colors, but colorblind variants might differ
            if len(color_arrays[array_name]) != 12:
                # Only warn if dramatically different
                if len(color_arrays[array_name]) < 8:
                    undersized_arrays.append(f"{array_name} ({len(color_arrays[array_name])} colors)")
    
    if missing_arrays:
        result.add_error(f"Missing color arrays: {', '.join(missing_arrays)}")
    
    if undersized_arrays:
        result.add_warning(f"Arrays with fewer than 8 colors: {', '.join(undersized_arrays)}")
    
    # Check for showButtons and showLeds calls in functions
    critical_calls = ["showButtons", "showLeds"]
    if functions:
        # Check key functions have the necessary calls
        key_functions = ["showIdle", "showPrepare", "showDecay", "showCountdown", "showTimeout"]
        for func_name in key_functions:
            if func_name in functions:
                func_body = functions[func_name]
                if "showLeds" not in func_body:
                    result.add_warning(f"{func_name}() missing showLeds() call")
    
    return result


def validate_multiple_files(filepaths: List[str]) -> Dict[str, ValidationResult]:
    """
    Validate multiple animation files.
    
    Args:
        filepaths: List of file paths to validate
        
    Returns:
        Dictionary mapping filepaths to ValidationResult objects
    """
    results = {}
    for filepath in filepaths:
        results[filepath] = validate_animation_file(filepath)
    return results
