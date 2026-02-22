"""Pytest configuration and fixtures."""
import sys
from pathlib import Path

# Add src directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest


@pytest.fixture
def polysynth_file():
    """Path to animations-POLYSYNTH.js test file."""
    return "../application/static/animations-POLYSYNTH.js"


@pytest.fixture
def oscillator_file():
    """Path to animations-OSCILLATOR.js test file."""
    return "../application/static/animations-OSCILLATOR.js"


@pytest.fixture
def base_file():
    """Path to base animations.js file."""
    return "../application/static/animations.js"
