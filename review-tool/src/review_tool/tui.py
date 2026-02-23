"""Textual TUI for reviewing student animation submissions."""

from pathlib import Path
import os
from textual.app import ComposeResult, App
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Static, Button
from textual.reactive import reactive
from textual.message import Message

from .utils import find_animation_files
from .validator import validate_animation_file, ValidationResult
from .comparator import compare_to_base, ComparisonResult, get_similarity_color


class FileSelectedMessage(Message):
    """Message sent when a file is selected in the tree."""
    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath


class ValidationPanel(VerticalScroll):
    """Right panel showing validation results with scrolling."""
    
    validation_result = reactive(None)
    comparison_result = reactive(None)
    selected_file = reactive(None)
    
    def __init__(self, base_file: str, **kwargs):
        super().__init__(**kwargs)
        self.base_file = base_file
        self.content_widget = None
    
    def on_mount(self):
        """Initialize the content widget when mounted."""
        self.content_widget = Static("")
        self.mount(self.content_widget)
    
    def watch_validation_result(self, new_value):
        """Update display when validation result changes."""
        self._update_display()
    
    def watch_comparison_result(self, new_value):
        """Update display when comparison result changes."""
        self._update_display()
    
    def watch_selected_file(self, new_value):
        """Update display when selected file changes."""
        self._update_display()
    
    def _update_display(self):
        """Update the content widget with current results."""
        if not self.content_widget:
            return
            
        if not self.selected_file:
            self.content_widget.update("[dim]👈 Select a file on the left to see details[/dim]")
            return
        
        if not self.validation_result:
            self.content_widget.update("[dim]Loading...[/dim]")
            return
        
        # Get just the filename for display
        filename = Path(self.selected_file).name
        output = f"[bold magenta]{filename}[/bold magenta]\n"
        output += "═" * 50 + "\n\n"
        
        result = self.validation_result
        
        if isinstance(result, ValidationResult):
            output += self._render_validation(result)
        
        if self.comparison_result:
            output += self._render_comparison(self.comparison_result)
        
        self.content_widget.update(output)
    
    def _render_validation(self, result: ValidationResult) -> str:
        """Render validation results."""
        status = "✓ VALID" if result.is_valid else "✗ INVALID"
        color = "green" if result.is_valid else "red"
        
        output = f"[bold {color}]{status}[/bold {color}]\n"
        output += "─" * 50 + "\n\n"
        
        if result.errors:
            output += "[bold red]❌ ERRORS:[/bold red]\n"
            for err in result.errors:
                output += f"  ✗ {err}\n"
            output += "\n"
        
        if result.warnings:
            output += "[bold yellow]⚠️  WARNINGS:[/bold yellow]\n"
            for warn in result.warnings:
                output += f"  ⚠ {warn}\n"
            output += "\n"
        
        if not result.errors and not result.warnings:
            output += "[green]✓ All validation checks passed![/green]\n\n"
        
        return output
    
    def _render_comparison(self, comp: ComparisonResult) -> str:
        """Render comparison results."""
        output = "[bold cyan]📊 SIMILARITY ANALYSIS[/bold cyan]\n"
        output += "─" * 50 + "\n\n"
        
        # Overall similarity - BIG and PROMINENT
        overall_color = get_similarity_color(comp.overall_similarity)
        output += f"[bold {overall_color}]Overall Similarity: {comp.overall_similarity:5.1f}%[/bold {overall_color}]\n\n"
        
        # Component breakdown
        output += "[bold]Component Scores:[/bold]\n"
        timing_color = get_similarity_color(comp.timing_similarity)
        color_color = get_similarity_color(comp.color_similarity)
        func_color = get_similarity_color(comp.function_similarity)
        
        output += f"  • Timing Variables: [{timing_color}]{comp.timing_similarity:5.1f}%[/{timing_color}]\n"
        output += f"  • Color Arrays:     [{color_color}]{comp.color_similarity:5.1f}%[/{color_color}]\n"
        output += f"  • Functions:        [{func_color}]{comp.function_similarity:5.1f}%[/{func_color}]\n"
        
        # ID info
        if comp.id_changed:
            output += f"\n[bold cyan]ID:[/bold cyan] '{comp.base_id}' → '{comp.student_id}'\n"
        
        # Detected changes section
        output += "\n[bold yellow]🔄 CHANGES DETECTED[/bold yellow]\n"
        output += "─" * 50 + "\n"
        
        if comp.timing_changes:
            output += f"\n[bold]Timing Changes ({len(comp.timing_changes)}):[/bold]\n"
            for name, (base_val, student_val) in sorted(comp.timing_changes.items()):
                diff = student_val - base_val
                sign = "+" if diff > 0 else ""
                output += f"  {name}: {base_val} → {student_val}  ({sign}{diff})\n"
        
        if comp.color_arrays_added:
            output += f"\n[bold green]✚ Color Arrays Added ({len(comp.color_arrays_added)}):[/bold green]\n"
            for name in sorted(comp.color_arrays_added.keys()):
                colors = comp.color_arrays_added[name]
                output += f"  + {name} ({len(colors)} colors)\n"
        
        if comp.color_arrays_removed:
            output += f"\n[bold red]✖ Color Arrays Removed ({len(comp.color_arrays_removed)}):[/bold red]\n"
            for name in sorted(comp.color_arrays_removed.keys()):
                colors = comp.color_arrays_removed[name]
                output += f"  - {name} ({len(colors)} colors)\n"
        
        if comp.color_changes:
            output += f"\n[bold yellow]⟳ Color Arrays Modified ({len(comp.color_changes)}):[/bold yellow]\n"
            for name in sorted(comp.color_changes.keys()):
                base_colors, student_colors = comp.color_changes[name]
                if len(base_colors) != len(student_colors):
                    output += f"  {name}: {len(base_colors)} → {len(student_colors)} colors\n"
                else:
                    diffs = sum(1 for i in range(len(base_colors)) 
                               if base_colors[i] != student_colors[i])
                    if diffs > 0:
                        output += f"  {name}: {diffs}/{len(base_colors)} colors changed\n"
        
        if comp.function_changes:
            output += f"\n[bold]Modified Functions ({len(comp.function_changes)}):[/bold]\n"
            for func_name in sorted(comp.function_changes):
                output += f"  • {func_name}()\n"
        
        # Separate reporting for p5.Oscillator and p5.PolySynth
        if comp.p5_synth_references:
            # Separate refs by type
            oscillator_scopes = []
            polysynth_scopes = []
            
            for scope, refs in comp.p5_synth_references.items():
                if "Oscillator" in refs:
                    oscillator_scopes.append(scope)
                if "PolySynth" in refs:
                    polysynth_scopes.append(scope)
            
            # Report p5.Oscillator usage
            if oscillator_scopes:
                output += f"\n[bold blue]🎺 p5.Oscillator Detected[/bold blue]\n"
                if "global" in oscillator_scopes:
                    output += f"  [global scope]\n"
                for scope in sorted(oscillator_scopes):
                    if scope != "global":
                        output += f"  • {scope}()\n"
            
            # Report p5.PolySynth usage
            if polysynth_scopes:
                output += f"\n[bold magenta]🎹 p5.PolySynth Detected[/bold magenta]\n"
                if "global" in polysynth_scopes:
                    output += f"  [global scope]\n"
                for scope in sorted(polysynth_scopes):
                    if scope != "global":
                        output += f"  • {scope}()\n"
        
        if not comp.timing_changes and not comp.color_arrays_added and not comp.color_arrays_removed and not comp.color_changes and not comp.function_changes and not comp.p5_synth_references:
            output += "[dim]No changes detected from base[/dim]\n"
        
        return output
    
    def update_file(self, filepath: str):
        """Update the display for a selected file."""
        self.selected_file = filepath
        val_result = validate_animation_file(filepath)
        comp_result = compare_to_base(filepath, self.base_file)
        
        self.validation_result = val_result
        self.comparison_result = comp_result


class FileBrowser(VerticalScroll):
    """Button list widget for browsing animation files."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_buttons = {}
    
    def populate_files(self, files: list):
        """Populate the button list with file list."""
        # Remove all existing children using remove_children which handles cleanup properly
        self.remove_children()
        self.file_buttons = {}
        
        # Add buttons for each file - no IDs needed
        for filepath in files:
            filename = Path(filepath).name
            button = Button(f"📄 {filename}")
            self.file_buttons[button] = filepath
            self.mount(button)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press - update file when clicked."""
        if event.button in self.file_buttons:
            filepath = self.file_buttons[event.button]
            self.post_message(FileSelectedMessage(filepath))


class ReviewApp(App):
    """Main textual application for reviewing submissions."""
    
    TITLE = "Donald 2021 - Animation Review Tool"
    CSS = """
    Screen {
        layout: horizontal;
    }
    
    FileBrowser {
        width: 40;
        border: solid $primary;
        background: $panel;
        padding: 1;
    }
    
    FileBrowser Button {
        width: 100%;
        margin-bottom: 1;
    }
    
    ValidationPanel {
        width: 1fr;
        border: solid $primary;
        background: $boost;
        overflow-y: auto;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]
    
    def __init__(self, animation_dir: str, base_file: str, **kwargs):
        super().__init__(**kwargs)
        self.animation_dir = animation_dir
        self.base_file = base_file
        self.animation_files = []
        self.file_browser = None
        self.validation_panel = None
    
    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        
        with Horizontal():
            # Left sidebar with file list
            self.file_browser = FileBrowser()
            yield self.file_browser
            
            # Right panel with validation/comparison results
            self.validation_panel = ValidationPanel(self.base_file)
            yield self.validation_panel
        
        yield Footer()
    
    def on_mount(self):
        """Load files when app starts."""
        self.animation_files = find_animation_files(self.animation_dir)
        
        # Populate the tree with files
        self.file_browser.populate_files(self.animation_files)
        
        if self.animation_files:
            # Auto-select and display first file
            self.validation_panel.update_file(self.animation_files[0])
    
    def on_file_selected_message(self, message: FileSelectedMessage) -> None:
        """Handle file selection from the tree widget."""
        if message and message.filepath:
            self.validation_panel.update_file(message.filepath)
    
    def action_refresh(self):
        """Refresh the file list."""
        self.animation_files = find_animation_files(self.animation_dir)
        self.file_browser.populate_files(self.animation_files)
        
        if self.animation_files:
            self.validation_panel.update_file(self.animation_files[0])


def run_tui(animation_dir: str):
    """Run the textual TUI application."""
    # Construct base file path
    base_file = os.path.join(animation_dir, "animations.js")
    
    if not os.path.exists(base_file):
        print(f"Error: Base file not found: {base_file}")
        return
    
    files = find_animation_files(animation_dir)
    if not files:
        print(f"No animation-*.js files found in {animation_dir}")
        return
    
    app = ReviewApp(animation_dir, base_file)
    app.run()
