"""Review tool for student animation submissions."""

import sys
import os
from pathlib import Path
from .tui import run_tui
from .validator import validate_animation_file
from .comparator import compare_to_base
from .utils import find_animation_files


def main() -> None:
    """Main entry point for the review tool."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Review student JavaScript animation submissions for Donald 2021",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  review-tool                    # Use current directory
  review-tool /path/to/static/   # Use specific directory
  review-tool --validate         # Validate files without TUI
        """
    )
    
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory containing animation files (default: current directory)"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation only (no TUI)"
    )
    
    parser.add_argument(
        "--base",
        default=None,
        help="Path to base animations.js file"
    )
    
    args = parser.parse_args()
    
    # Resolve directory
    anim_dir = os.path.abspath(args.directory)
    if not os.path.isdir(anim_dir):
        print(f"Error: Directory not found: {anim_dir}")
        sys.exit(1)
    
    # Find or validate base file
    if args.base:
        base_file = os.path.abspath(args.base)
    else:
        base_file = os.path.join(anim_dir, "animations.js")
    
    if not os.path.exists(base_file):
        print(f"Error: Base file not found: {base_file}")
        print("Use --base to specify the base animations.js file")
        sys.exit(1)
    
    # Find animation files
    animation_files = find_animation_files(anim_dir)
    
    if not animation_files:
        print(f"No animation-*.js files found in {anim_dir}")
        sys.exit(1)
    
    if args.validate:
        # Validation mode - print results to console
        print(f"Found {len(animation_files)} animation file(s)\n")
        print(f"Base file: {base_file}\n")
        
        for filepath in sorted(animation_files):
            filename = os.path.basename(filepath)
            print(f"\n{'='*60}")
            print(f"File: {filename}")
            print('='*60)
            
            # Validation
            val_result = validate_animation_file(filepath)
            print(val_result)
            
            # Comparison
            comp_result = compare_to_base(filepath, base_file)
            print(f"Similarity: {comp_result.overall_similarity:.1f}%")
            print(f"  Timings:    {comp_result.timing_similarity:.1f}%")
            print(f"  Colors:     {comp_result.color_similarity:.1f}%")
            print(f"  Functions:  {comp_result.function_similarity:.1f}%")
            
            if comp_result.timing_changes:
                print(f"\nTiming Changes ({len(comp_result.timing_changes)}):")
                for name, (base, student) in sorted(comp_result.timing_changes.items()):
                    print(f"  {name}: {base} → {student}")
    else:
        # TUI mode
        print(f"Starting review tool for {anim_dir}")
        print(f"Found {len(animation_files)} animation file(s)")
        run_tui(anim_dir)
