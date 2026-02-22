"""Tests for file comparison and synth detection."""
import pytest
from src.review_tool.comparator import compare_to_base


def test_polysynth_comparison(polysynth_file, base_file):
    """Test comparison detects p5.PolySynth in POLYSYNTH file."""
    result = compare_to_base(polysynth_file, base_file)
    
    assert result.p5_synth_references, "Should have synth references"
    assert "global" in result.p5_synth_references, "Should have global scope"
    assert "PolySynth" in result.p5_synth_references["global"], "Should detect PolySynth"


def test_oscillator_comparison(oscillator_file, base_file):
    """Test comparison detects p5.Oscillator in OSCILLATOR file."""
    result = compare_to_base(oscillator_file, base_file)
    
    assert result.p5_synth_references, "Should have synth references"
    assert "global" in result.p5_synth_references, "Should have global scope"
    assert "Oscillator" in result.p5_synth_references["global"], "Should detect Oscillator"


def test_polysynth_vs_oscillator(polysynth_file, oscillator_file, base_file):
    """Test that PolySynth and Oscillator are detected separately."""
    result_poly = compare_to_base(polysynth_file, base_file)
    result_osc = compare_to_base(oscillator_file, base_file)
    
    # PolySynth should have PolySynth, not Oscillator
    assert "PolySynth" in result_poly.p5_synth_references.get("global", [])
    assert "Oscillator" not in result_poly.p5_synth_references.get("global", [])
    
    # Oscillator should have Oscillator, not PolySynth
    assert "Oscillator" in result_osc.p5_synth_references.get("global", [])
    assert "PolySynth" not in result_osc.p5_synth_references.get("global", [])


def test_comparison_result_structure(polysynth_file, base_file):
    """Test that comparison result has expected structure."""
    result = compare_to_base(polysynth_file, base_file)
    
    assert hasattr(result, "p5_synth_references"), "Should have p5_synth_references attribute"
    assert isinstance(result.p5_synth_references, dict), "Should be a dict"
    assert hasattr(result, "overall_similarity"), "Should have overall_similarity"
    assert hasattr(result, "timing_changes"), "Should have timing_changes"
    assert hasattr(result, "color_changes"), "Should have color_changes"
    assert hasattr(result, "function_changes"), "Should have function_changes"


def test_polysynth_reported_as_change(polysynth_file, base_file):
    """Test that PolySynth presence is detected as a change from base."""
    result = compare_to_base(polysynth_file, base_file)
    
    # PolySynth should be reported (it's not in base file)
    assert result.p5_synth_references, "PolySynth should be reported since it's not in base file"
