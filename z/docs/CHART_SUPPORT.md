# Chart and Diagram Support

The frontend supports rendering interactive charts and diagrams within chat messages using Plotly.js and Mermaid.

## Supported Visualizations

1. **Plotly Charts** - Interactive data visualizations
   - Line charts, bar charts, pie charts, scatter plots
   - 3D plots, heatmaps, contour plots
   - Statistical charts (box plots, histograms, etc.)
   - Financial charts (candlestick, OHLC)
   - And many more...

2. **Mermaid Diagrams** - Static diagrams and flowcharts
   - Flowcharts
   - Sequence diagrams
   - Class diagrams
   - State diagrams
   - ER diagrams
   - Gantt charts
   - And more...

## How It Works

The engine sends chart/diagram data as markdown code blocks with special language tags:
- ````plotly` for Plotly charts (with JSON data)
- ````mermaid` for Mermaid diagrams (with mermaid syntax)

The frontend automatically detects these code blocks and renders them as interactive visualizations instead of plain code.

## Using Plotly Charts

### Import the utilities

```python
from app.utils.chart_formatter import format_plotly_chart, PlotlyTemplates
```

### Method 1: Use pre-built templates (easiest)

```python
# Simple line chart
chart = PlotlyTemplates.line_chart(
    x=[1, 2, 3, 4, 5],
    y=[10, 15, 13, 17, 20],
    title="Sales Over Time",
    x_label="Month",
    y_label="Sales ($)",
    series_name="Revenue"
)

# Bar chart
chart = PlotlyTemplates.bar_chart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    values=[100, 150, 130, 180],
    title="Quarterly Revenue",
    x_label="Quarter",
    y_label="Revenue ($M)"
)

# Pie chart
chart = PlotlyTemplates.pie_chart(
    labels=["Product A", "Product B", "Product C"],
    values=[30, 45, 25],
    title="Market Share"
)

# Multi-line chart
chart = PlotlyTemplates.multi_line_chart(
    x=[1, 2, 3, 4],
    series=[
        {"y": [10, 15, 13, 17], "name": "Product A"},
        {"y": [16, 12, 14, 18], "name": "Product B"},
        {"y": [8, 11, 10, 13], "name": "Product C"}
    ],
    title="Product Comparison"
)
```

### Method 2: Custom charts with full control

```python
# Custom plotly chart with full configuration
chart = format_plotly_chart(
    data=[
        {
            "x": [1, 2, 3, 4],
            "y": [10, 15, 13, 17],
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Series 1",
            "line": {"color": "rgb(55, 128, 191)", "width": 3},
            "marker": {"size": 8}
        },
        {
            "x": [1, 2, 3, 4],
            "y": [16, 12, 14, 18],
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Series 2",
            "line": {"color": "rgb(255, 127, 14)", "width": 3},
            "marker": {"size": 8}
        }
    ],
    layout={
        "title": "Custom Multi-Series Chart",
        "xaxis": {
            "title": "X Axis Label",
            "showgrid": True,
            "zeroline": True
        },
        "yaxis": {
            "title": "Y Axis Label",
            "showgrid": True,
            "zeroline": True
        },
        "hovermode": "closest",
        "showlegend": True,
        "legend": {"x": 0, "y": 1}
    },
    config={
        "displayModeBar": True,
        "displaylogo": False
    }
)
```

### Using charts in responses

```python
from app.utils.chart_formatter import PlotlyTemplates

async def process(message: str, context: dict | None = None) -> tuple[str, dict]:
    # Generate some data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales = [45000, 52000, 48000, 61000, 58000, 67000]

    # Create chart
    chart = PlotlyTemplates.line_chart(
        x=months,
        y=sales,
        title="Monthly Sales Performance",
        x_label="Month",
        y_label="Sales ($)",
        series_name="Sales"
    )

    # Include chart in response
    response = f"""Here's your sales performance analysis:

{chart}

**Key Insights:**
- Total sales: ${sum(sales):,}
- Average monthly sales: ${sum(sales) // len(sales):,}
- Best month: {months[sales.index(max(sales))]} (${max(sales):,})
- Growth trend: Positive
"""

    return response, {"chart_included": True}
```

## Using Mermaid Diagrams

### Import the utilities

```python
from app.utils.chart_formatter import format_mermaid_diagram, MermaidTemplates
```

### Method 1: Use pre-built templates

```python
# Flowchart
diagram = MermaidTemplates.flowchart('''
    A[User Request] --> B{Valid?}
    B -->|Yes| C[Process Request]
    B -->|No| D[Return Error]
    C --> E[Send Response]
''')

# Sequence diagram
diagram = MermaidTemplates.sequence_diagram('''
    participant User
    participant Backend
    participant Engine
    User->>Backend: Send Message
    Backend->>Engine: Process Request
    Engine-->>Backend: Return Response
    Backend-->>User: Display Message
''')
```

### Method 2: Custom diagrams

```python
# Any mermaid diagram type
diagram = format_mermaid_diagram('''
graph LR
    A[Client] --> B[Load Balancer]
    B --> C[Server 1]
    B --> D[Server 2]
    B --> E[Server 3]
    C --> F[Database]
    D --> F
    E --> F
''')
```

## Complete Example: Processor with Charts

```python
from app.utils.chart_formatter import PlotlyTemplates, MermaidTemplates

class MessageProcessor:
    async def process(
        self,
        message: str,
        context: dict | None = None,
        tracking: Optional[TrackingMetadata] = None,
    ) -> tuple[str, dict]:
        # Detect if user wants a chart
        if "show chart" in message.lower() or "visualize" in message.lower():
            # Generate sample data
            chart = PlotlyTemplates.bar_chart(
                categories=["A", "B", "C", "D"],
                values=[23, 45, 67, 34],
                title="Sample Data Visualization"
            )

            response = f"Here's your data visualization:\n\n{chart}"
            metadata = {"chart_type": "bar", "chart_included": True}

            return response, metadata

        # Detect if user wants a diagram
        elif "show flow" in message.lower() or "diagram" in message.lower():
            diagram = MermaidTemplates.flowchart('''
                A[Start] --> B[Process Data]
                B --> C{Success?}
                C -->|Yes| D[Save Results]
                C -->|No| E[Handle Error]
                D --> F[End]
                E --> F
            ''')

            response = f"Here's the process flow:\n\n{diagram}"
            metadata = {"diagram_type": "flowchart", "diagram_included": True}

            return response, metadata

        # Regular LLM processing
        else:
            # ... existing LLM logic ...
            pass
```

## Chart Types Reference

### Plotly Chart Types

Common chart types (set via `type` field in data):

- `scatter` - Scatter plot / line chart (with `mode: "markers"` or `mode: "lines"`)
- `bar` - Bar chart
- `pie` - Pie chart
- `histogram` - Histogram
- `box` - Box plot
- `heatmap` - Heatmap
- `contour` - Contour plot
- `scatter3d` - 3D scatter plot
- `surface` - 3D surface plot
- `candlestick` - Candlestick chart (financial)

See [Plotly documentation](https://plotly.com/javascript/) for all available chart types and options.

### Mermaid Diagram Types

Common diagram types:

- `graph` / `flowchart` - Flowcharts
- `sequenceDiagram` - Sequence diagrams
- `classDiagram` - Class diagrams
- `stateDiagram` - State diagrams
- `erDiagram` - Entity-relationship diagrams
- `gantt` - Gantt charts
- `pie` - Pie charts
- `gitGraph` - Git graphs

See [Mermaid documentation](https://mermaid.js.org/) for all available diagram types and syntax.

## Best Practices

1. **Use templates for simple charts** - They handle common cases and reduce code
2. **Validate data** - Ensure data arrays are not empty before creating charts
3. **Add context** - Include text explanation along with the visualization
4. **Keep it focused** - Don't overload charts with too much data
5. **Use appropriate chart types** - Match the chart type to the data and message
6. **Test rendering** - Verify charts render correctly in the UI
7. **Handle errors** - Wrap chart generation in try-catch blocks

## Error Handling

The frontend will display error messages if:
- JSON is malformed in plotly blocks
- Mermaid syntax is invalid
- Chart data is missing required fields

Always validate data before creating charts:

```python
def create_safe_chart(x, y, title):
    try:
        if not x or not y or len(x) != len(y):
            return "Error: Invalid chart data"

        chart = PlotlyTemplates.line_chart(x, y, title)
        return chart
    except Exception as e:
        logger.error(f"Chart generation failed: {e}")
        return "Error: Could not generate chart"
```

## Performance Considerations

- **Plotly.js bundle size**: ~6MB (1.8MB gzipped) - already included in frontend
- **Data size limits**: Keep chart data under 10,000 points for good performance
- **Multiple charts**: Can include multiple charts in one message
- **Caching**: Frontend caches Plotly library for faster subsequent loads

## Future Enhancements

Potential future additions:
- D3.js support for custom visualizations
- Chart.js for lightweight charts
- Export charts as images
- Interactive data exploration
- Real-time data updates
