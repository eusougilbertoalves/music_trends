from datetime import datetime
from fpdf import FPDF

def generate_markdown_report(insights: str) -> str:
    """
    Generates a Markdown report from the provided insights.

    Args:
        insights (str): The insights text.

    Returns:
        str: The Markdown formatted report.
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    report = f"# Music Trends Report - {current_date}\n\n"
    report += "## Trends Insights:\n\n"
    report += insights
    return report

def save_markdown_report(content: str, path: str):
    """
    Saves the Markdown report to a file.

    Args:
        content (str): The Markdown content.
        path (str): The file path to save the report.
    """
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def convert_markdown_to_pdf(markdown_path: str, pdf_path: str):
    """
    Converts a Markdown file to PDF.

    Args:
        markdown_path (str): Path to the Markdown file.
        pdf_path (str): Path to save the PDF file.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    with open(markdown_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Replace unsupported characters (e.g., em dash) with a hyphen
            sanitized_line = line.replace("\u2014", "-")
            # You can also add additional replacements if necessary
            pdf.multi_cell(0, 10, sanitized_line)
    pdf.output(pdf_path)