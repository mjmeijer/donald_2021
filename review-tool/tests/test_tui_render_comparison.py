"""Tests for _render_comparison method in TUI."""
import pytest
from src.review_tool.comparator import compare_to_base
from src.review_tool.tui import ValidationPanel


def test_render_comparison_polysynth_detection(polysynth_file, base_file):
    """Test that _render_comparison correctly renders PolySynth detection from animations-POLYSYNTH.js."""
    # Create a ValidationPanel instance
    panel = ValidationPanel(base_file)
    
    # Perform comparison
    comp_result = compare_to_base(polysynth_file, base_file)
    
    # Render the comparison
    output = panel._render_comparison(comp_result)
    
    # Assertions
    assert "🎹 p5.PolySynth Detected" in output, "Should display PolySynth detection header"
    assert "[bold magenta]" in output, "Should use magenta color for PolySynth"
    assert "[global scope]" in output, "Should show global scope for PolySynth"
    
    # Should NOT show Oscillator
    assert "🎺 p5.Oscillator Detected" not in output, "Should not show Oscillator detection"
    assert "[bold blue]" not in output or "Oscillator" not in output, "Should not mention Oscillator"


def test_render_comparison_oscillator_detection(oscillator_file, base_file):
    """Test that _render_comparison correctly renders Oscillator detection from animations-OSCILLATOR.js."""
    # Create a ValidationPanel instance
    panel = ValidationPanel(base_file)
    
    # Perform comparison
    comp_result = compare_to_base(oscillator_file, base_file)
    
    # Render the comparison
    output = panel._render_comparison(comp_result)
    
    # Assertions
    assert "🎺 p5.Oscillator Detected" in output, "Should display Oscillator detection header"
    assert "[bold blue]" in output, "Should use blue color for Oscillator"
    assert "[global scope]" in output, "Should show global scope for Oscillator"
    
    # Should NOT show PolySynth
    assert "🎹 p5.PolySynth Detected" not in output, "Should not show PolySynth detection"
    assert "PolySynth" not in output, "Should not mention PolySynth"


def test_render_comparison_polysynth_full_output(polysynth_file, base_file):
    """Test the complete output format when rendering PolySynth detection."""
    panel = ValidationPanel(base_file)
    comp_result = compare_to_base(polysynth_file, base_file)
    output = panel._render_comparison(comp_result)
    
    # Check that all major sections are present
    assert "SIMILARITY ANALYSIS" in output, "Should have similarity analysis header"
    assert "Overall Similarity:" in output, "Should show similarity scores"
    assert "🔄 CHANGES DETECTED" in output, "Should have changes section"
    
    # Check PolySynth section specifically
    assert "🎹 p5.PolySynth Detected" in output, "Should show PolySynth detection"
    
    # Verify it's not showing "No changes detected" message
    assert "No changes detected from base" not in output, "Should not show 'no changes' when synth is detected"


def test_render_comparison_synth_references_structure(polysynth_file, base_file):
    """Test that synth references are properly extracted and structured."""
    comp_result = compare_to_base(polysynth_file, base_file)
    
    # Verify the comparison result has synth references
    assert comp_result.p5_synth_references, "Should have p5_synth_references populated"
    assert "global" in comp_result.p5_synth_references, "Should have global scope"
    assert "PolySynth" in comp_result.p5_synth_references["global"], "Should detect PolySynth in global scope"
    
    # Now test rendering
    panel = ValidationPanel(base_file)
    output = panel._render_comparison(comp_result)
    
    # Verify rendering matches the structure
    assert "PolySynth" in output, "Rendered output should mention PolySynth"


def test_render_comparison_no_synth_in_base(base_file):
    """Test that base file does not have synth references."""
    # Compare base to itself
    comp_result = compare_to_base(base_file, base_file)
    
    # Base file should not have synth references
    assert not comp_result.p5_synth_references or len(comp_result.p5_synth_references) == 0, \
        "Base file should not have synth references"
    
    panel = ValidationPanel(base_file)
    output = panel._render_comparison(comp_result)
    
    # Should show "No changes detected" since comparing to itself
    assert "No changes detected from base" in output, "Should show no changes when comparing base to itself"
    assert "PolySynth" not in output, "Should not show PolySynth"
    assert "Oscillator" not in output, "Should not show Oscillator"


def test_render_comparison_polysynth_mutually_exclusive(polysynth_file, oscillator_file, base_file):
    """Test that PolySynth and Oscillator are rendered separately and not together."""
    # Test PolySynth file
    panel = ValidationPanel(base_file)
    comp_poly = compare_to_base(polysynth_file, base_file)
    output_poly = panel._render_comparison(comp_poly)
    
    # Test Oscillator file
    comp_osc = compare_to_base(oscillator_file, base_file)
    output_osc = panel._render_comparison(comp_osc)
    
    # PolySynth file should only have PolySynth
    assert "PolySynth" in output_poly, "PolySynth file should show PolySynth"
    assert "Oscillator" not in output_poly, "PolySynth file should not show Oscillator"
    
    # Oscillator file should only have Oscillator
    assert "Oscillator" in output_osc, "Oscillator file should show Oscillator"
    assert "PolySynth" not in output_osc, "Oscillator file should not show PolySynth"
