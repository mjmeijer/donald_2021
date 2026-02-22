"""Tests for rendering logic in the TUI."""
import pytest
from src.review_tool.comparator import compare_to_base


def test_synth_rendering_logic_polysynth(polysynth_file, base_file):
    """Test that PolySynth rendering logic works correctly."""
    result = compare_to_base(polysynth_file, base_file)
    
    # Simulate rendering logic
    oscillator_scopes = []
    polysynth_scopes = []
    
    for scope, refs in result.p5_synth_references.items():
        if "Oscillator" in refs:
            oscillator_scopes.append(scope)
        if "PolySynth" in refs:
            polysynth_scopes.append(scope)
    
    # Assertions
    assert len(oscillator_scopes) == 0, "Should have no Oscillator scopes"
    assert len(polysynth_scopes) == 1, "Should have one PolySynth scope"
    assert "global" in polysynth_scopes, "PolySynth should be in global scope"


def test_synth_rendering_logic_oscillator(oscillator_file, base_file):
    """Test that Oscillator rendering logic works correctly."""
    result = compare_to_base(oscillator_file, base_file)
    
    # Simulate rendering logic
    oscillator_scopes = []
    polysynth_scopes = []
    
    for scope, refs in result.p5_synth_references.items():
        if "Oscillator" in refs:
            oscillator_scopes.append(scope)
        if "PolySynth" in refs:
            polysynth_scopes.append(scope)
    
    # Assertions
    assert len(oscillator_scopes) == 1, "Should have one Oscillator scope"
    assert len(polysynth_scopes) == 0, "Should have no PolySynth scopes"
    assert "global" in oscillator_scopes, "Oscillator should be in global scope"


def test_render_output_contains_polysynth(polysynth_file, base_file):
    """Test that rendering output includes PolySynth detection."""
    result = compare_to_base(polysynth_file, base_file)
    
    output = ""
    
    if result.p5_synth_references:
        oscillator_scopes = []
        polysynth_scopes = []
        
        for scope, refs in result.p5_synth_references.items():
            if "Oscillator" in refs:
                oscillator_scopes.append(scope)
            if "PolySynth" in refs:
                polysynth_scopes.append(scope)
        
        if polysynth_scopes:
            output += f"\n[bold magenta]🎹 p5.PolySynth Detected[/bold magenta]\n"
            if "global" in polysynth_scopes:
                output += f"  [global scope]\n"
    
    assert "p5.PolySynth Detected" in output, "Output should contain PolySynth detection"
    assert "global scope" in output, "Output should show global scope"


def test_render_output_contains_oscillator(oscillator_file, base_file):
    """Test that rendering output includes Oscillator detection."""
    result = compare_to_base(oscillator_file, base_file)
    
    output = ""
    
    if result.p5_synth_references:
        oscillator_scopes = []
        polysynth_scopes = []
        
        for scope, refs in result.p5_synth_references.items():
            if "Oscillator" in refs:
                oscillator_scopes.append(scope)
            if "PolySynth" in refs:
                polysynth_scopes.append(scope)
        
        if oscillator_scopes:
            output += f"\n[bold blue]🎺 p5.Oscillator Detected[/bold blue]\n"
            if "global" in oscillator_scopes:
                output += f"  [global scope]\n"
    
    assert "p5.Oscillator Detected" in output, "Output should contain Oscillator detection"
    assert "global scope" in output, "Output should show global scope"


def test_synth_sections_mutually_exclusive(polysynth_file, base_file):
    """Test that synth detection sections don't overlap."""
    result = compare_to_base(polysynth_file, base_file)
    
    oscillator_scopes = []
    polysynth_scopes = []
    
    for scope, refs in result.p5_synth_references.items():
        if "Oscillator" in refs:
            oscillator_scopes.append(scope)
        if "PolySynth" in refs:
            polysynth_scopes.append(scope)
    
    # Check that a scope isn't in both lists (mutually exclusive)
    overlap = set(oscillator_scopes) & set(polysynth_scopes)
    assert not overlap, "A scope should not have both Oscillator and PolySynth"
