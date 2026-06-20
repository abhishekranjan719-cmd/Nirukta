#!/usr/bin/env python3
"""
Generate human-readable Markdown reports from MS SQL Schema Analysis JSON

Usage:
    python generate_schema_report.py <input_json> <output_md>
    python generate_schema_report.py analysis.json report.md
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def format_number(num: int) -> str:
    """Format number with commas"""
    return f"{num:,}"


def generate_executive_summary(data: dict[str, Any]) -> str:
    """Generate executive summary section"""
    lines = [
        "# Database Schema Analysis Report",
        "",
        f"**Database:** `{data.get('database', 'N/A')}`  ",
        f"**Schema:** `{data.get('schema', 'N/A')}`  ",
        f"**Analyzed:** {data.get('analyzed_at', 'N/A')}  ",
        f"**Analyzer Version:** {data.get('analyzer_version', 'N/A')}  ",
        "",
        "## Executive Summary",
        "",
        f"- **Tables:** {data.get('table_count', 0)}",
        f"- **Total Rows:** {format_number(data.get('total_rows', 0))}",
        f"- **High Cardinality Threshold:** {data.get('high_cardinality_threshold', 200)}",
        "",
    ]

    # Add overall assessment if available
    llm = data.get("llm_analysis", {})
    if "schema_assessment" in llm:
        assessment = llm["schema_assessment"]
        lines.extend(
            [
                "### Overall Assessment",
                "",
                f"- **Quality:** {assessment.get('overall_quality', 'N/A').title()}",
                f"- **Normalization:** {assessment.get('normalization_level', 'N/A')}",
                f"- **NL2SQL Suitability:** {assessment.get('suitability_for_nl2sql', 'N/A').title()}",
                "",
            ]
        )

        if "summary" in assessment:
            lines.extend([f"**Summary:** {assessment['summary']}", ""])

    return "\n".join(lines)


def generate_data_quality_issues(data: dict[str, Any]) -> str:
    """Generate data quality issues section"""
    lines = ["## 🚨 Data Quality Issues (NL2SQL Risks)", ""]

    llm = data.get("llm_analysis", {})
    failure_patterns = llm.get("nl2sql_failure_patterns", {})
    detected_issues = failure_patterns.get("detected_data_quality_issues", {})

    if not detected_issues:
        lines.append("*No data quality issues detected.*\n")
        return "\n".join(lines)

    # Table Selection Risks
    table_risks = detected_issues.get("wrong_table_selection_risks", [])
    if table_risks:
        lines.extend([f"### ❌ Wrong Table Selection Risks ({len(table_risks)} issues)", ""])
        for i, risk in enumerate(table_risks, 1):
            if "tables" in risk:
                lines.append(f"{i}. **Similar Tables:** `{risk['tables'][0]}` ↔️ `{risk['tables'][1]}`")
                lines.append(f"   - *Issue:* {risk['issue']}")
            elif "table" in risk:
                lines.append(f"{i}. **Table:** `{risk['table']}`")
                lines.append(f"   - *Issue:* {risk['issue']}")
                if "recommendation" in risk:
                    lines.append(f"   - *Fix:* {risk['recommendation']}")
            lines.append("")

    # Column Selection Risks
    column_risks = detected_issues.get("wrong_column_selection_risks", [])
    if column_risks:
        lines.extend([f"### ❌ Wrong Column Selection Risks ({len(column_risks)} issues)", ""])
        for i, risk in enumerate(column_risks, 1):
            lines.append(f"{i}. **Column:** `{risk['column']}`")
            lines.append(f"   - *Found in tables:* {', '.join([f'`{t}`' for t in risk.get('tables', [])])}")
            lines.append(f"   - *Issue:* {risk['issue']}")
            lines.append(f"   - *Risk:* {risk.get('risk', 'N/A')}")
            lines.append("")

    # Filter Condition Risks
    filter_risks = detected_issues.get("wrong_filter_condition_risks", [])
    if filter_risks:
        lines.extend([f"### ❌ Wrong Filter Condition Risks ({len(filter_risks)} issues)", ""])
        for i, risk in enumerate(filter_risks, 1):
            if "column" in risk:
                lines.append(f"{i}. **Column:** `{risk.get('table', 'N/A')}.{risk['column']}`")
                lines.append(f"   - *Issue:* {risk['issue']}")
                if "data_type" in risk:
                    lines.append(f"   - *Current Type:* `{risk['data_type']}`")
                if "wrong_example" in risk:
                    lines.append(f"   - ❌ *Wrong:* `{risk['wrong_example']}`")
                if "correct_example" in risk:
                    lines.append(f"   - ✅ *Correct:* `{risk['correct_example']}`")
                if "recommendation" in risk:
                    lines.append(f"   - *Fix:* {risk['recommendation']}")
                lines.append("")

    # Join Condition Risks
    join_risks = detected_issues.get("wrong_join_condition_risks", [])
    if join_risks:
        lines.extend([f"### ❌ Wrong Join Condition Risks ({len(join_risks)} issues)", ""])
        for i, risk in enumerate(join_risks[:10], 1):  # Limit to first 10
            lines.append(f"{i}. **Column:** `{risk.get('table', 'N/A')}.{risk.get('column', 'N/A')}`")
            lines.append(f"   - *Issue:* {risk['issue']}")
            if "potential_references" in risk:
                lines.append(
                    f"   - *Potential References:* {', '.join([f'`{t}`' for t in risk['potential_references']])}"
                )
            if "recommendation" in risk:
                lines.append(f"   - *Fix:* {risk['recommendation']}")
            lines.append("")

    # Aggregation Risks
    agg_risks = detected_issues.get("wrong_aggregation_risks", [])
    if agg_risks:
        lines.extend([f"### ❌ Wrong Aggregation Risks ({len(agg_risks)} issues)", ""])
        for i, risk in enumerate(agg_risks, 1):
            if "columns" in risk:
                lines.append(f"{i}. **Multi-level Columns:** {', '.join([f'`{c}`' for c in risk.get('columns', [])])}")
                lines.append(f"   - *Tables:* {', '.join([f'`{t}`' for t in risk.get('tables', [])])}")
            else:
                lines.append(f"{i}. **Column:** `{risk.get('table', 'N/A')}.{risk.get('column', 'N/A')}`")
            lines.append(f"   - *Issue:* {risk['issue']}")
            lines.append(f"   - *Risk:* {risk.get('risk', 'N/A')}")
            if "recommendation" in risk:
                lines.append(f"   - *Fix:* {risk['recommendation']}")
            lines.append("")

    return "\n".join(lines)


def generate_recommendations(data: dict[str, Any]) -> str:
    """Generate recommendations section"""
    lines = ["## 💡 Recommendations", ""]

    llm = data.get("llm_analysis", {})
    recommendations = llm.get("recommendations", {})

    if not recommendations:
        lines.append("*No recommendations available.*\n")
        return "\n".join(lines)

    # Data Types
    data_types = recommendations.get("data_types", [])
    if data_types:
        lines.extend(["### Data Type Improvements", ""])
        for i, rec in enumerate(data_types, 1):
            lines.append(f"{i}. **`{rec.get('table', 'N/A')}.{rec.get('column', 'N/A')}`**")
            lines.append(f"   - Current: `{rec.get('current_type', 'N/A')}`")
            lines.append(f"   - Suggested: `{rec.get('suggested_type', 'N/A')}`")
            lines.append(f"   - Reason: {rec.get('reason', 'N/A')}")
            lines.append("")

    # Naming Conventions
    naming = recommendations.get("naming_conventions", [])
    if naming:
        lines.extend(["### Naming Convention Improvements", ""])
        for i, rec in enumerate(naming, 1):
            lines.append(f"{i}. **Category:** {rec.get('category', 'N/A').title()}")
            lines.append(f"   - Issue: {rec.get('issue', 'N/A')}")
            lines.append(f"   - Suggestion: {rec.get('suggestion', 'N/A')}")
            if "examples" in rec:
                lines.append(f"   - Examples: {rec['examples']}")
            lines.append("")

    # Normalization
    normalization = recommendations.get("normalization", [])
    if normalization:
        lines.extend(["### Normalization Improvements", ""])
        for i, rec in enumerate(normalization, 1):
            lines.append(f"{i}. **Table:** `{rec.get('table', 'N/A')}`")
            lines.append(f"   - Issue: {rec.get('issue', 'N/A')}")
            lines.append(f"   - Recommendation: {rec.get('recommendation', 'N/A')}")
            lines.append(f"   - Benefit: {rec.get('benefit', 'N/A')}")
            lines.append("")

    # Constraints
    constraints = recommendations.get("constraints", [])
    if constraints:
        lines.extend(["### Constraint Improvements", ""])
        for i, rec in enumerate(constraints, 1):
            lines.append(f"{i}. **`{rec.get('table', 'N/A')}`** - {rec.get('constraint_type', 'N/A')}")
            lines.append(f"   - Recommendation: {rec.get('recommendation', 'N/A')}")
            lines.append(f"   - Benefit: {rec.get('benefit', 'N/A')}")
            lines.append("")

    # Indexes
    indexes = recommendations.get("indexes", [])
    if indexes:
        lines.extend(["### Index Recommendations", ""])
        for i, rec in enumerate(indexes, 1):
            cols = ", ".join([f"`{c}`" for c in rec.get("columns", [])])
            lines.append(f"{i}. **Table:** `{rec.get('table', 'N/A')}`")
            lines.append(f"   - Columns: {cols}")
            lines.append(f"   - Type: {rec.get('index_type', 'N/A')}")
            lines.append(f"   - Reason: {rec.get('reason', 'N/A')}")
            lines.append("")

    return "\n".join(lines)


def generate_table_details(data: dict[str, Any]) -> str:
    """Generate table details section"""
    lines = ["## 📊 Table Details", ""]

    tables = data.get("tables", [])
    if not tables:
        lines.append("*No tables found.*\n")
        return "\n".join(lines)

    llm = data.get("llm_analysis", {})
    table_descriptions = llm.get("table_descriptions", {})
    column_descriptions = llm.get("column_descriptions", {})

    for table in tables:
        table_name = table["table_name"]
        lines.extend([f"### {table_name}", ""])

        # Basic stats
        lines.extend(
            [
                f"**Rows:** {format_number(table.get('row_count', 0))}  ",
                f"**Columns:** {len(table.get('columns', []))}  ",
                f"**Primary Keys:** {', '.join([f'`{pk}`' for pk in table.get('primary_keys', [])]) or '*None*'}  ",
                "",
            ]
        )

        # Table description from LLM
        if table_name in table_descriptions:
            desc = table_descriptions[table_name]
            if "purpose" in desc:
                lines.extend([f"**Purpose:** {desc['purpose']}", ""])
            if desc.get("business_questions"):
                lines.extend(["**Business Questions:**", ""])
                for q in desc["business_questions"]:
                    lines.append(f"- {q}")
                lines.append("")

        # Foreign keys
        if table.get("foreign_keys"):
            lines.extend(["**Foreign Keys:**", ""])
            for fk in table["foreign_keys"][:5]:  # Limit to 5
                ref_table = fk.get("referenced_table", "N/A")
                ref_col = fk.get("referenced_column", "N/A")
                lines.append(f"- `{fk.get('column_name', 'N/A')}` → `{ref_table}.{ref_col}`")
            if len(table.get("foreign_keys", [])) > 5:
                lines.append(f"- *(... and {len(table['foreign_keys']) - 5} more)*")
            lines.append("")

        # Key columns
        lines.extend(["**Key Columns:**", ""])

        for col in table.get("columns", [])[:10]:  # Show first 10 columns
            col_name = col["column_name"]
            data_type = col["full_data_type"]
            nullable = "NULL" if col["is_nullable"] else "NOT NULL"
            distinct = format_number(col.get("distinct_count", 0))

            col_line = f"- **`{col_name}`** ({data_type}, {nullable}) - {distinct} distinct values"

            # Add warnings
            warnings = []
            if col.get("is_high_cardinality"):
                warnings.append("⚠️ HIGH CARDINALITY")
            if col.get("null_percentage", 0) > 50:
                warnings.append(f"⚠️ {col.get('null_percentage', 0):.1f}% NULL")

            if warnings:
                col_line += f" {' '.join(warnings)}"

            lines.append(col_line)

            # Add column description if available
            if table_name in column_descriptions:
                col_descs = column_descriptions[table_name]
                if col_name in col_descs:
                    col_desc = col_descs[col_name]
                    if "description" in col_desc:
                        lines.append(f"  - *{col_desc['description']}*")

        if len(table.get("columns", [])) > 10:
            lines.append(f"- *(... and {len(table['columns']) - 10} more columns)*")

        lines.extend(["", "---", ""])

    return "\n".join(lines)


def generate_schema_description(data: dict[str, Any]) -> str:
    """Generate schema description section"""
    lines = ["## 📝 Schema Description", ""]

    llm = data.get("llm_analysis", {})
    schema_desc = llm.get("schema_description", "")

    if schema_desc:
        lines.extend([schema_desc, ""])
    else:
        lines.append("*No schema description available.*\n")

    # Table relationships overview
    if "table_relationships_overview" in llm:
        rel_overview = llm["table_relationships_overview"]
        lines.extend(["### Table Relationships", ""])

        if rel_overview.get("central_tables"):
            central = ", ".join([f"`{t}`" for t in rel_overview["central_tables"]])
            lines.append(f"**Central/Fact Tables:** {central}  ")

        if rel_overview.get("lookup_tables"):
            lookup = ", ".join([f"`{t}`" for t in rel_overview["lookup_tables"]])
            lines.append(f"**Lookup/Dimension Tables:** {lookup}  ")

        if "relationship_summary" in rel_overview:
            lines.extend(["", rel_overview["relationship_summary"], ""])

    return "\n".join(lines)


def generate_markdown_report(input_json_path: str, output_md_path: str) -> None:
    """Generate a comprehensive markdown report from schema analysis JSON"""

    # Load JSON data
    print(f"📖 Reading {input_json_path}...")
    with open(input_json_path, encoding="utf-8") as f:
        data = json.load(f)

    print("📝 Generating markdown report...")

    # Generate sections
    sections = [
        generate_executive_summary(data),
        generate_schema_description(data),
        generate_data_quality_issues(data),
        generate_recommendations(data),
        generate_table_details(data),
    ]

    # Combine all sections
    report = "\n".join(sections)

    # Add footer
    report += f"\n\n---\n\n*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    # Write to file
    output_path = Path(output_md_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Report saved to {output_md_path}")
    print(f"   Size: {len(report):,} characters")


def main():
    """Main entry point"""
    if len(sys.argv) != 3:
        print("Usage: python generate_schema_report.py <input_json> <output_md>")
        print("Example: python generate_schema_report.py analysis.json report.md")
        sys.exit(1)

    input_json = sys.argv[1]
    output_md = sys.argv[2]

    if not Path(input_json).exists():
        print(f"❌ Error: Input file not found: {input_json}")
        sys.exit(1)

    try:
        generate_markdown_report(input_json, output_md)
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
