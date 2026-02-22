"""Tests for p5 synth reference extraction."""
import pytest
from src.review_tool.utils import read_file, extract_functions, extract_p5_synth_references


def test_polysynth_extraction(polysynth_file):
    """Test that p5.PolySynth is extracted from POLYSYNTH file."""
    content = read_file(polysynth_file)
    
    assert "p5.PolySynth" in content, "p5.PolySynth should be in file content"
    
    functions = extract_functions(content)
    synth_refs = extract_p5_synth_references(content, functions)
    
    assert synth_refs, "Should have synth references"
    assert "global" in synth_refs, "Should have global scope references"
    assert "PolySynth" in synth_refs["global"], "Should detect PolySynth"


def test_oscillator_extraction(oscillator_file):
    """Test that p5.Oscillator is extracted from OSCILLATOR file."""
    content = read_file(oscillator_file)
    
    assert "p5.Oscillator" in content, "p5.Oscillator should be in file content"
    
    functions = extract_functions(content)
    synth_refs = extract_p5_synth_references(content, functions)
    
    assert synth_refs, "Should have synth references"
    assert "global" in synth_refs, "Should have global scope references"
    assert "Oscillator" in synth_refs["global"], "Should detect Oscillator"


def test_base_file_no_synth(base_file):
    """Test that base file has no synth references."""
    content = read_file(base_file)
    
    assert "p5.PolySynth" not in content, "Base file should not have PolySynth"
    assert "p5.Oscillator" not in content, "Base file should not have Oscillator"
    
    functions = extract_functions(content)
    synth_refs = extract_p5_synth_references(content, functions)
    
    assert not synth_refs, "Base file should have no synth references"


def test_extraction_returns_list(polysynth_file):
    """Test that extract_p5_synth_references returns correct data structure."""
    content = read_file(polysynth_file)
    functions = extract_functions(content)
    synth_refs = extract_p5_synth_references(content, functions)
    
    assert isinstance(synth_refs, dict), "Should return a dict"
    for scope, refs in synth_refs.items():
        assert isinstance(scope, str), "Scope should be a string"
        assert isinstance(refs, list), "References should be a list"
        for ref in refs:
            assert isinstance(ref, str), "Each reference should be a string"
