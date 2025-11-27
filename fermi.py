"""Fermi Calculator - Textual UI Application"""
from textual.app import App, ComposeResult
from textual.widgets import TextArea, Static, Header, Footer, Button
from textual.containers import Horizontal, Vertical
from fermi_engine import FermiEngine
from fermi_formatter import format_number


class FermiApp(App):
    """A Fermi estimation calculator with two-panel UI"""
    
    CSS_PATH = "fermi.tcss"
    BINDINGS = [
        ("ctrl+enter", "calculate", "Calculate"),
        ("ctrl+q", "quit", "Quit"),
    ]
    
    def __init__(self):
        super().__init__()
        self.engine = FermiEngine()
    
    def compose(self) -> ComposeResult:
        """Create the UI layout"""
        yield Header()
        with Horizontal(id="main"):
            with Vertical(id="input-panel"):
                yield Static("Model Definition", classes="panel-title")
                yield TextArea("", id="input")
                yield Button("Calculate", id="calc-btn", variant="primary")
            with Vertical(id="output-panel"):
                yield Static("Results", classes="panel-title")
                yield Static("", id="output")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "calc-btn":
            self.action_calculate()
    
    def action_calculate(self) -> None:
        """Execute the model and display results"""
        # Get input text
        input_widget = self.query_one("#input", TextArea)
        text = input_widget.text
        
        # Clear engine variables for fresh calculation
        self.engine.clear()
        
        # Execute model
        results = self.engine.execute_model(text)
        
        # Format output
        output_text = self.format_results(text, results)
        
        # Display
        output_widget = self.query_one("#output", Static)
        output_widget.update(output_text)
    
    def format_results(self, input_text: str, results: list) -> str:
        """
        Format results for display with => notation.
        
        Args:
            input_text: Original input text
            results: List of result dictionaries from engine
        
        Returns:
            Formatted string showing input lines with results
        """
        input_lines = input_text.split("\n")
        output_lines = []
        
        for line, result in zip(input_lines, results):
            # Add the input line
            output_lines.append(line)
            
            # Add the result on the next line with =>
            if result["type"] == "assignment":
                formatted_value = format_number(result["value"])
                output_lines.append(f"=> {formatted_value}")
            elif result["type"] == "error":
                output_lines.append(f"=> ERROR: {result['message']}")
            # Comments and empty lines don't get => lines
        
        return "\n".join(output_lines)


def main():
    """Run the Fermi Calculator application"""
    app = FermiApp()
    app.run()


if __name__ == "__main__":
    main()