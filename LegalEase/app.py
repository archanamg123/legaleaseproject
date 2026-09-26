import os
import requests
import streamlit as st

from dotenv import load_dotenv

from services.exporters import (
    format_txt,
    format_docx,
    format_pdf,
    format_html_preview,
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .preview-box {
        background-color: #111827;
        color: #f9fafb;
        padding: 30px;
        border-radius: 12px;
        max-height: 650px;
        overflow-y: auto;
        line-height: 1.7;
    }

    .preview-box h3 {
        color: #93c5fd;
        margin-top: 20px;
    }

    .preview-box p {
        color: #f3f4f6;
    }

    .warning-box {
        background-color: #fff7ed;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #f97316;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="warning-box">
    <b>Important:</b> LegalEase creates AI-assisted drafts.
    Always review generated documents with a qualified legal
    professional before using them for a real legal matter.
    </div>
    """,
    unsafe_allow_html=True,
)


st.write("")


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    language = st.selectbox(
        "Document Language",
        [
            "English",
            "Hindi",
            "Malayalam",
        ],
        index=0,
    )

    jurisdiction = st.text_input(
        "Jurisdiction",
        placeholder="Example: Kerala, India",
    )

    st.divider()

    st.subheader("Backend")

    st.code(
        BACKEND_URL,
        language="text"
    )

    st.caption(
        "Start FastAPI before generating a document."
    )


# ---------------------------------------------------------
# Input section
# ---------------------------------------------------------

st.header("📝 Create Your Document")

col1, col2 = st.columns(2)


with col1:

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Partnership Agreement",
            "Employment Offer Letter",
            "General Agreement",
            "Custom Legal Document",
        ],
    )


with col2:

    effective_date = st.date_input(
        "Effective Date"
    )


parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Example:\n"
        "Jane Doe (Service Provider)\n"
        "TechNova Inc. (Client)"
    ),
    height=120,
)


terms = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Enter each condition separated by a semicolon.\n\n"
        "Example:\n"
        "Payment must be made within 30 days; "
        "The provider must deliver the project by the agreed deadline; "
        "Confidential information must remain private; "
        "Either party may terminate with 15 days notice"
    ),
    height=180,
)


generate_button = st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# Generation
# ---------------------------------------------------------

if generate_button:

    if not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

        st.stop()

    if not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

        st.stop()

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": effective_date.isoformat(),
        "jurisdiction": jurisdiction,
        "language": language,
    }

    try:

        with st.spinner(
            "Generating your legal document..."
        ):

            response = requests.post(
                f"{BACKEND_URL}/generate",
                json=payload,
                timeout=120,
            )

        if response.status_code != 200:

            try:
                detail = response.json().get(
                    "detail",
                    "Unknown backend error."
                )

            except Exception:
                detail = response.text

            st.error(
                f"Generation failed: {detail}"
            )

        else:

            data = response.json()

            if not data.get("success"):

                st.error(
                    data.get(
                        "message",
                        "Document generation failed."
                    )
                )

            else:

                st.session_state["document"] = (
                    data["document"]
                )

                st.session_state["document_type"] = (
                    document_type
                )

                st.success(
                    "Document generated successfully!"
                )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI. "
            "Make sure the backend is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "The backend took too long to respond."
        )

    except Exception as exc:

        st.error(
            f"Unexpected error: {exc}"
        )


# ---------------------------------------------------------
# Document preview/editing
# ---------------------------------------------------------

if "document" in st.session_state:

    st.divider()

    st.header("📄 Generated Document")

    document = st.session_state["document"]

    edit_mode = st.toggle(
        "✏️ Edit Document",
        value=False,
    )

    if edit_mode:

        edited_document = st.text_area(
            "Edit your document",
            value=document,
            height=600,
        )

        st.session_state["document"] = (
            edited_document
        )

        document = edited_document

    else:

        preview_html = format_html_preview(
            document
        )

        st.markdown(
            f"""
            <div class="preview-box">
                {preview_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # Downloads
    # -----------------------------------------------------

    st.subheader("⬇️ Download")

    download_col1, download_col2, download_col3 = (
        st.columns(3)
    )

    doc_type = st.session_state.get(
        "document_type",
        "Legal Document"
    )

    safe_name = (
        doc_type.lower()
        .replace(" ", "_")
        .replace("/", "_")
    )


    with download_col1:

        txt_data = format_txt(document)

        st.download_button(
            label="📄 Download TXT",
            data=txt_data,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )


    with download_col2:

        docx_data = format_docx(
            document,
            doc_type,
        )

        st.download_button(
            label="📝 Download DOCX",
            data=docx_data,
            file_name=f"{safe_name}.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )


    with download_col3:

        pdf_data = format_pdf(
            document,
            doc_type,
        )

        st.download_button(
            label="📕 Download PDF",
            data=pdf_data,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "LegalEase • AI-assisted legal document drafting • "
    "Always review documents before legal use."
)