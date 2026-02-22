"""Comparison module for analyzing changes in student submissions."""

import difflib
from typing import Dict, List, Tuple
from .utils import (
    read_file,
    extract_id,
    extract_timings,
    extract_color_arrays,
    extract_functions
)


class ComparisonResult:
    """Result of comparing a student file to the base file."""
    
    def __init__(self, student_file: str, base_file: str):
        self.student_file = student_file
        self.base_file = base_file
        self.overall_similarity = 0.0
        self.timing_similarity = 0.0
        self.color_similarity = 0.0
        self.function_similarity = 0.0
        self.timing_changes: Dict[str, Tuple[int, int]] = {}  # name -> (base, student)
        self.color_changes: Dict[str, Tuple[List, List]] = {}  # name -> (base, student)
        self.function_changes: List[str] = []
        self.id_changed = False
        self.student_id = ""
        self.base_id = ""
    
    def __str__(self) -> str:
        result = f"Similarity Score: {self.overall_similarity:.1f}%\n"
        result += f"  Timing:    {self.timing_similarity:.1f}%\n"
        result += f"  Colors:    {self.color_similarity:.1f}%\n"
        result += f"  Functions: {self.function_similarity:.1f}%\n"
        
        if self.id_changed:
            result += f"\nID Changed: '{self.base_id}' → '{self.student_id}'\n"
        
        if self.timing_changes:
            result += f"\nTiming Changes ({len(self.timing_changes)}):\n"
            for name, (base_val, student_val) in self.timing_changes.items():
                result += f"  {name}: {base_val} → {student_val}\n"
        
        if self.color_changes:
            result += f"\nColor Changes ({len(self.color_changes)}):\n"
            for name, (base_colors, student_colors) in self.color_changes.items():
                if len(base_colors) == len(student_colors):
                    diffs = [i for i in range(len(base_colors)) 
                            if base_colors[i] != student_colors[i]]
                    result += f"  {name}: {len(diffs)} colors changed\n"
                else:
                    result += f"  {name}: array size {len(base_colors)} → {len(student_colors)}\n"
        
        if self.function_changes:
            result += f"\nFunctions with Changes ({len(self.function_changes)}):\n"
            for func_name in self.function_changes:
                result += f"  {func_name}()\n"
        
        return result


def compare_to_base(student_file: str, base_file: str) -> ComparisonResult:
    """
    Compare a student animation file to the base template.
    
    Args:
        student_file: Path to student submission
        base_file: Path to base template
        
    Returns:
        ComparisonResult with similarity scores and changes
    """
    result = ComparisonResult(student_file, base_file)
    
    # Read files
    student_content = read_file(student_file)
    base_content = read_file(base_file)
    
    if student_content.startswith("ERROR:") or base_content.startswith("ERROR:"):
        result.overall_similarity = 0.0
        return result
    
    # Compare IDs
    result.student_id = extract_id(student_content) or "UNKNOWN"
    result.base_id = extract_id(base_content) or "UNKNOWN"
    result.id_changed = result.student_id != result.base_id
    
    # Compare timings
    student_timings = extract_timings(student_content)
    base_timings = extract_timings(base_content)
    
    timing_total = len(base_timings)
    timing_matches = 0
    for key in base_timings:
        if student_timings[key] == base_timings[key]:
            timing_matches += 1
        else:
            if base_timings[key] > 0 and student_timings[key] > 0:
                result.timing_changes[key] = (base_timings[key], student_timings[key])
    
    result.timing_similarity = (timing_matches / timing_total * 100) if timing_total > 0 else 0
    
    # Compare color arrays
    student_colors = extract_color_arrays(student_content)
    base_colors = extract_color_arrays(base_content)
    
    color_total = len(base_colors)
    color_matches = 0
    
    for array_name in base_colors:
        if array_name in student_colors:
            if student_colors[array_name] == base_colors[array_name]:
                color_matches += 1
            else:
                result.color_changes[array_name] = (
                    base_colors[array_name],
                    student_colors[array_name]
                )
        else:
            result.color_changes[array_name] = (base_colors[array_name], [])
    
    result.color_similarity = (color_matches / color_total * 100) if color_total > 0 else 0
    
    # Compare functions
    student_functions = extract_functions(student_content)
    base_functions = extract_functions(base_content)
    
    function_total = len(base_functions)
    function_matches = 0
    
    for func_name in base_functions:
        if func_name in student_functions:
            # Use difflib to compare function bodies
            base_body = base_functions[func_name]
            student_body = student_functions[func_name]
            
            matcher = difflib.SequenceMatcher(None, base_body, student_body)
            similarity = matcher.ratio()
            
            if similarity >= 0.95:  # Allow minor whitespace differences
                function_matches += 1
            else:
                result.function_changes.append(func_name)
        else:
            result.function_changes.append(func_name)
    
    result.function_similarity = (function_matches / function_total * 100) if function_total > 0 else 0
    
    # Calculate overall similarity as weighted average
    # Weight: 30% timings, 40% colors, 30% functions
    result.overall_similarity = (
        result.timing_similarity * 0.3 +
        result.color_similarity * 0.4 +
        result.function_similarity * 0.3
    )
    
    return result


def compare_multiple_files(base_file: str, student_files: List[str]) -> Dict[str, ComparisonResult]:
    """
    Compare multiple student files to base file.
    
    Args:
        base_file: Path to base template
        student_files: List of student file paths
        
    Returns:
        Dictionary mapping student file paths to ComparisonResult objects
    """
    results = {}
    for student_file in student_files:
        results[student_file] = compare_to_base(student_file, base_file)
    return results


def get_similarity_color(similarity: float) -> str:
    """
    Get a color code for a similarity score.
    
    Args:
        similarity: Similarity percentage (0-100)
        
    Returns:
        Color name for textual UI
    """
    if similarity >= 95:
        return "green"
    elif similarity >= 80:
        return "yellow"
    elif similarity >= 50:
        return "yellow"
    else:
        return "red"
