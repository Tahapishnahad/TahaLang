# diagnostics.py

from dataclasses import dataclass

@dataclass(frozen=True)
class SourceFile:
    """
    Represents a source file, including its name and content.

    Attributes:
        name: Name of the file.
        content: File's content as a str.
    """

    name: str
    content: str

    def get_line(self, line_number: int) -> str | None:
        lines = self.content.split("\n")

        if line_number < 1 or line_number > len(lines):
            return None

        return lines[line_number-1]

s = SourceFile(
    "pp",
    """let s = 2\nlet r = 2"""
)

print(s.get_line(-1))