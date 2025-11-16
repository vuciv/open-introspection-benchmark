# render_sweep.py
from rich.console import Console
from rich.table import Table

console = Console()

sweep = [
    ("0.0 (control)", "Calm refusal: “I don’t detect any injected thought…”"),
    ("1.0", "Same refusal as control."),
    ("2.0", "Same refusal as control."),
    ("4.0", "Same refusal as control."),
    ("8.0", "Still refuses; restates experiment instructions."),
    ("16.0", "[yellow]Glitch onset: repeats “DDT… DDT...”[/]"),
    ("32.0", "[red]Full breakdown: “I Dinainaostaosta…”[/]"),
    ("68.0", "[red]Pure noise (“I D D D …”).[/]"),
    ("128.0", "[red]Still noise (“I D D D …”).[/]"),
    ("256.0", "[red]Residual noise (“I D D D …”).[/]")
]

table = Table(
    title="Mistral 7B Instruct v0.2 — Concept Injection Sweep ('dust')",
    show_lines=True
)
table.add_column("Strength", justify="center", style="bold")
table.add_column("Assistant Response (trimmed)", overflow="fold", width=70)

for strength, response in sweep:
    table.add_row(strength, response)

console.print(table)