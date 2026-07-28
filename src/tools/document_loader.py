"""Loading and chunking of the local knowledge base file."""

from pathlib import Path


def split_into_chunks(text: str) -> list[str]:
    """Split raw knowledge base text into paragraph chunks.

    Paragraphs are separated by one or more blank lines. Empty results are
    discarded so that trailing or repeated blank lines do not produce chunks.

    Args:
        text: Raw contents of the knowledge base file.

    Returns:
        Paragraph chunks with surrounding whitespace removed.
    """
    paragraphs = text.split("\n\n")
    return [stripped for paragraph in paragraphs if (stripped := paragraph.strip())]


def load_chunks(path: Path) -> list[str]:
    """Read the knowledge base file and split it into paragraph chunks.

    Args:
        path: Path to the knowledge base text file.

    Returns:
        Paragraph chunks from the file.

    Raises:
        FileNotFoundError: If the knowledge base file does not exist.
        ValueError: If the file exists but contains no usable text.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Knowledge base file not found: {path}")

    chunks = split_into_chunks(path.read_text(encoding="utf-8"))
    if not chunks:
        raise ValueError(f"Knowledge base file is empty: {path}")
    return chunks
