"""Utility functions for animation file parsing and discovery."""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple


def find_animation_files(directory: str) -> List[str]:
    """
    Find all animation-*.js files in a directory (excluding animations.js).
    
    Args:
        directory: Path to search for animation files
        
    Returns:
        List of matching file paths sorted alphabetically
    """
    anim_dir = Path(directory)
    if not anim_dir.exists():
        return []
    
    files = sorted([
        str(f) for f in anim_dir.glob("animations-*.js")
        if f.name != "animations.js"
    ])
    return files


def read_file(filepath: str) -> str:
    """Read a JavaScript file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: Could not read file: {e}"


def extract_id(content: str) -> str:
    """Extract the 'id' variable from JavaScript content."""
    match = re.search(r"var\s+id\s*=\s*['\"]([^'\"]+)['\"]", content)
    return match.group(1) if match else "NOT_FOUND"


def extract_timings(content: str) -> Dict[str, int]:
    """
    Extract timing variables (T0-T7) from JavaScript content.
    
    Returns:
        Dictionary mapping timing names to values (or -1 if not found)
    """
    timings = {}
    for i in range(8):
        # Pattern: var T<i>_NAME = <number>;
        pattern = rf"var\s+T{i}_\w+\s*=\s*(\d+)"
        match = re.search(pattern, content)
        key = f"T{i}"
        timings[key] = int(match.group(1)) if match else -1
    return timings


def extract_color_arrays(content: str) -> Dict[str, List[str]]:
    """
    Extract color arrays from JavaScript content.
    
    Returns:
        Dictionary mapping array names to their color entries
    """
    color_arrays = {}
    array_pattern = r"var\s+(\w+Colors)\s*=\s*new\s+Array\(([\s\S]*?)\);"
    
    for match in re.finditer(array_pattern, content):
        array_name = match.group(1)
        array_content = match.group(2)
        
        # Extract color entries (quoted strings)
        colors = re.findall(r"['\"]([^'\"]+)['\"]", array_content)
        color_arrays[array_name] = colors
    
    return color_arrays


def extract_functions(content: str) -> Dict[str, str]:
    """
    Extract function definitions from JavaScript content.
    
    Returns:
        Dictionary mapping function names to their body content
    """
    functions = {}
    function_pattern = r"function\s+(\w+)\s*\((.*?)\)\s*\{([\s\S]*?)\n\}"
    
    for match in re.finditer(function_pattern, content):
        func_name = match.group(1)
        func_body = match.group(3).strip()
        functions[func_name] = func_body
    
    return functions


def get_required_functions() -> List[str]:
    """Return list of required function names."""
    return [
        "showIdle",
        "showPrepare",
        "showTestStep",
        "showDecay",
        "showCountdown",
        "showTimeout",
        "showSuccess",
        "showFailure"
    ]


def get_required_color_arrays() -> List[str]:
    """Return list of required color array names."""
    return [
        "idleColors",
        "prepColors",
        "blokColors",
        "decayColors",
        "countColors",
        "timeoutColors",
        "successColors",
        "failColors"
    ]


def get_required_timings() -> List[str]:
    """Return list of required timing variable names."""
    return [f"T{i}" for i in range(8)]
