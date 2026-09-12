"""Render a PDF page to PNG for local mockup and QA inspection."""

import argparse
from pathlib import Path

import pypdfium2 as pdfium


def render_page(pdf_path: Path, output_path: Path, page_number: int, scale: float) -> None:
    """Render one 1-based PDF page to a PNG image."""
    document = pdfium.PdfDocument(str(pdf_path))
    if page_number < 1 or page_number > len(document):
        raise ValueError(
            f"Page {page_number} is outside the document range 1-{len(document)}"
        )

    page = document[page_number - 1]
    image = page.render(scale=scale).to_pil()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="PDF file to render")
    parser.add_argument("output", type=Path, help="Destination PNG file")
    parser.add_argument("--page", type=int, default=1, help="1-based page number")
    parser.add_argument("--scale", type=float, default=1.5, help="Render scale")
    args = parser.parse_args()
    render_page(args.pdf.resolve(), args.output.resolve(), args.page, args.scale)
    print(f"Rendered page {args.page} to {args.output.resolve()}")


if __name__ == "__main__":
    main()
