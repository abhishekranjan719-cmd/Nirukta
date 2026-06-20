"""
Utility functions for formatting chart data for frontend rendering.

Supports:
- Plotly charts (interactive visualizations)
- Mermaid diagrams (flowcharts, sequence diagrams, etc.)
"""

import json
from typing import Any


def format_plotly_chart(
    data: list[dict[str, Any]],
    layout: dict[str, Any] | None = None,
    config: dict[str, Any] | None = None,
) -> str:
    """
    Format plotly chart data as a markdown code block for frontend rendering.

    The frontend will automatically detect and render this as an interactive chart.

    Args:
        data: List of plotly traces (data to plot)
        layout: Optional layout configuration (title, axes, etc.)
        config: Optional plotly config (display options)

    Returns:
        Formatted markdown string with plotly JSON

    Example:
        ```python
        # Simple line chart
        chart = format_plotly_chart(
            data=[
                {"x": [1, 2, 3, 4], "y": [10, 15, 13, 17], "type": "scatter", "mode": "lines+markers", "name": "Series 1"}
            ],
            layout={"title": "Sample Line Chart", "xaxis": {"title": "X Axis"}, "yaxis": {"title": "Y Axis"}},
        )
        ```
    """
    chart_data = {"data": data}

    if layout:
        chart_data["layout"] = layout

    if config:
        chart_data["config"] = config

    json_str = json.dumps(chart_data, indent=2)
    return f"```plotly\n{json_str}\n```"


def format_mermaid_diagram(diagram: str) -> str:
    """
    Format mermaid diagram as a markdown code block for frontend rendering.

    The frontend will automatically detect and render this as a diagram.

    Args:
        diagram: Mermaid diagram syntax

    Returns:
        Formatted markdown string with mermaid diagram

    Example:
        ```python
        # Simple flowchart
        diagram = format_mermaid_diagram('''
        graph TD
            A[Start] --> B{Decision}
            B -->|Yes| C[Do Something]
            B -->|No| D[Do Something Else]
            C --> E[End]
            D --> E
        ''')
        ```
    """
    return f"```mermaid\n{diagram.strip()}\n```"


# Common plotly chart templates
class PlotlyTemplates:
    """Pre-built plotly chart templates for common use cases."""

    @staticmethod
    def line_chart(
        x: list[Any],
        y: list[Any],
        title: str = "Line Chart",
        x_label: str = "X",
        y_label: str = "Y",
        series_name: str = "Data",
    ) -> str:
        """Create a simple line chart."""
        return format_plotly_chart(
            data=[
                {
                    "x": x,
                    "y": y,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": series_name,
                }
            ],
            layout={
                "title": title,
                "xaxis": {"title": x_label},
                "yaxis": {"title": y_label},
            },
        )

    @staticmethod
    def bar_chart(
        categories: list[str],
        values: list[float],
        title: str = "Bar Chart",
        x_label: str = "Category",
        y_label: str = "Value",
    ) -> str:
        """Create a simple bar chart."""
        return format_plotly_chart(
            data=[{"x": categories, "y": values, "type": "bar"}],
            layout={
                "title": title,
                "xaxis": {"title": x_label},
                "yaxis": {"title": y_label},
            },
        )

    @staticmethod
    def pie_chart(labels: list[str], values: list[float], title: str = "Pie Chart") -> str:
        """Create a simple pie chart."""
        return format_plotly_chart(
            data=[{"labels": labels, "values": values, "type": "pie"}],
            layout={"title": title},
        )

    @staticmethod
    def scatter_plot(
        x: list[Any],
        y: list[Any],
        title: str = "Scatter Plot",
        x_label: str = "X",
        y_label: str = "Y",
    ) -> str:
        """Create a simple scatter plot."""
        return format_plotly_chart(
            data=[{"x": x, "y": y, "type": "scatter", "mode": "markers"}],
            layout={
                "title": title,
                "xaxis": {"title": x_label},
                "yaxis": {"title": y_label},
            },
        )

    @staticmethod
    def multi_line_chart(
        x: list[Any],
        series: list[dict[str, Any]],
        title: str = "Multi-Line Chart",
        x_label: str = "X",
        y_label: str = "Y",
    ) -> str:
        """
        Create a multi-line chart.

        Args:
            x: Common x-axis values
            series: List of series, each with 'y' and 'name' keys
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label

        Example:
            ```python
            chart = PlotlyTemplates.multi_line_chart(
                x=[1, 2, 3, 4],
                series=[{"y": [10, 15, 13, 17], "name": "Series 1"}, {"y": [16, 12, 14, 18], "name": "Series 2"}],
                title="Comparison",
            )
            ```
        """
        data = []
        for s in series:
            data.append(
                {
                    "x": x,
                    "y": s["y"],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": s["name"],
                }
            )

        return format_plotly_chart(
            data=data,
            layout={
                "title": title,
                "xaxis": {"title": x_label},
                "yaxis": {"title": y_label},
            },
        )


# Common mermaid diagram templates
class MermaidTemplates:
    """Pre-built mermaid diagram templates for common use cases."""

    @staticmethod
    def flowchart(steps: str) -> str:
        """
        Create a flowchart diagram.

        Args:
            steps: Mermaid flowchart syntax

        Example:
            ```python
            diagram = MermaidTemplates.flowchart('''
            A[Start] --> B{Decision}
            B -->|Yes| C[Action 1]
            B -->|No| D[Action 2]
            ''')
            ```
        """
        return format_mermaid_diagram(f"graph TD\n{steps}")

    @staticmethod
    def sequence_diagram(interactions: str) -> str:
        """
        Create a sequence diagram.

        Args:
            interactions: Mermaid sequence diagram syntax

        Example:
            ```python
            diagram = MermaidTemplates.sequence_diagram('''
            Alice->>Bob: Hello Bob!
            Bob->>Alice: Hi Alice!
            ''')
            ```
        """
        return format_mermaid_diagram(f"sequenceDiagram\n{interactions}")
