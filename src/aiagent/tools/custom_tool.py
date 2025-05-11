from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."


class ExportMarkdownPDF(BaseTool):
    name: str = Field(default="ExportMarkdownPDF", description="Nom de l'outil")
    description: str = Field(default="Convertit un texte Markdown en PDF")

    def _run(self, markdown_text: str, output_path: Optional[str] = "report.pdf") -> str:
        import markdown
        from weasyprint import HTML

        html_content = markdown.markdown(markdown_text)

        HTML(string=html_content).write_pdf(output_path)

        return f"PDF généré à : {output_path}"