import os
from dotenv import load_dotenv

load_dotenv()


class GeminiDocumentGenerator:
    """
    Generates legal document drafts using Google Gemini.

    DEMO_MODE=true:
        Generates a local sample document without calling Gemini.

    DEMO_MODE=false:
        Uses the Gemini API.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.7-flash"
        ).strip()

        self.demo_mode = (
            os.getenv("DEMO_MODE", "true").strip().lower()
            in {"true", "1", "yes", "on"}
        )

        self.client = None

        if not self.demo_mode:
            if not self.api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY is missing. "
                    "Add it to your .env file or enable DEMO_MODE=true."
                )

            try:
                from google import genai

                self.client = genai.Client(
                    api_key=self.api_key
                )

            except ImportError as exc:
                raise RuntimeError(
                    "google-genai is not installed. "
                    "Run: pip install google-genai"
                ) from exc

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str = "",
        language: str = "English",
    ) -> str:

        document_type = document_type.strip()
        parties = parties.strip()
        terms = terms.strip()
        effective_date = effective_date.strip()
        jurisdiction = jurisdiction.strip()
        language = language.strip() or "English"

        if not document_type:
            raise ValueError("Document type is required.")

        if not parties:
            raise ValueError("Parties are required.")

        if not terms:
            raise ValueError("Terms and conditions are required.")

        if not effective_date:
            raise ValueError("Effective date is required.")

        if self.demo_mode:
            return self._demo_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                effective_date=effective_date,
                jurisdiction=jurisdiction,
                language=language,
            )

        prompt = self._build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
            jurisdiction=jurisdiction,
            language=language,
        )

        try:
            from google.genai import types

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are a legal document drafting assistant. "
                        "Create structured legal document drafts based "
                        "strictly on the information supplied by the user. "
                        "Do not invent names, dates, amounts, addresses, "
                        "laws, statutes, or obligations. "
                        "Use professional formatting and clear headings. "
                        "This is a drafting tool and not a substitute for "
                        "review by a qualified legal professional."
                    ),
                    max_output_tokens=5000,
                ),
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as exc:
            raise RuntimeError(
                f"Gemini generation failed: {exc}"
            ) from exc

    def _build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str,
        language: str,
    ) -> str:

        jurisdiction_text = (
            jurisdiction
            if jurisdiction
            else "Not specified"
        )

        return f"""
Create a professional draft of the following legal document.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

JURISDICTION:
{jurisdiction_text}

LANGUAGE:
{language}

TERMS AND CONDITIONS:
{terms}

Requirements:

1. Begin with a clear document title.
2. Identify the parties and effective date.
3. Organize the document using numbered sections.
4. Include only clauses reasonably supported by the supplied information.
5. Do not invent specific legal statutes or regulations.
6. Do not invent missing financial amounts or dates.
7. If important information is missing, use a clear placeholder such as:
   [INSERT INFORMATION]
8. Use professional legal-document language.
9. Include signature sections where appropriate.
10. Finish with a short notice stating that the document should be
    reviewed by an appropriately qualified legal professional before use.
11. Return only the document draft, without explaining your process.
"""

    def _demo_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str,
        language: str,
    ) -> str:

        term_list = [
            item.strip()
            for item in terms.split(";")
            if item.strip()
        ]

        lines = []

        lines.append(document_type.upper())
        lines.append("")
        lines.append(f"Effective Date: {effective_date}")
        lines.append(f"Language: {language}")

        if jurisdiction:
            lines.append(f"Jurisdiction: {jurisdiction}")

        lines.append("")
        lines.append("PARTIES")
        lines.append(parties)
        lines.append("")
        lines.append("AGREEMENT")
        lines.append("")

        lines.append(
            f"This {document_type} is entered into by the parties "
            f"identified above and is effective as of "
            f"{effective_date}."
        )

        lines.append("")
        lines.append("TERMS AND CONDITIONS")

        for index, term in enumerate(term_list, start=1):
            lines.append(f"{index}. {term}")

        lines.append("")
        lines.append("GENERAL PROVISIONS")
        lines.append(
            "The parties intend that this document accurately "
            "reflect the terms agreed between them."
        )

        lines.append("")
        lines.append("SIGNATURES")
        lines.append("")
        lines.append("Party 1: ______________________________")
        lines.append("Name: __________________________________")
        lines.append("Date: ___________________________________")
        lines.append("")
        lines.append("Party 2: ______________________________")
        lines.append("Name: __________________________________")
        lines.append("Date: ___________________________________")

        lines.append("")
        lines.append(
            "NOTICE: This draft is generated for informational and "
            "drafting purposes and should be reviewed by a qualified "
            "legal professional before use."
        )

        return "\n".join(lines)
