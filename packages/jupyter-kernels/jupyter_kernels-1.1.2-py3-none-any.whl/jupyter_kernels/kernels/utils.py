from rich.console import Console
from rich.table import Table


def new_kernel_table(title="Jupyter Kernel"):
    table = Table(title=title)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Server name", style="magenta", no_wrap=True)
    table.add_column("Environment", style="green", no_wrap=True)
    return table


def add_kernel_to_table(table, kernel):
    table.add_row(
        kernel["kernel_given_name"],
        kernel["jupyter_pod_name"],
        kernel["environment_name"],
    )


def display_kernels(kernels: list) -> None:
    """Display a list of kernels in the console."""
    table = new_kernel_table(title="Jupyter Kernels")
    for kernel in kernels:
        add_kernel_to_table(table, kernel)
    console = Console()
    console.print(table)
