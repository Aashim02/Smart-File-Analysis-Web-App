import io
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def summarize_text(text: str, sentence_count: int = 2) -> str:
    """Create a short summary from the first few sentences."""
    normalized = " ".join(text.split())
    if not normalized:
        return "No content available"

    sentences = [s.strip() for s in normalized.split(".") if s.strip()]
    if not sentences:
        return normalized[:180]

    summary = ". ".join(sentences[:sentence_count]).strip()
    if summary and not summary.endswith("."):
        summary += "."
    return summary or "No summary available"


def analyze_folder(folder: Path) -> Tuple[List[List[str]], int, int, List[str]]:
    """Analyze files in a folder and summarize .txt files."""
    rows: List[List[str]] = []
    txt_count = 0
    other_count = 0
    errors: List[str] = []

    try:
        files = sorted(folder.iterdir(), key=lambda p: p.name.lower())
    except OSError as exc:
        raise RuntimeError(f"Unable to access folder: {exc}") from exc

    for file_path in files:
        if not file_path.is_file():
            other_count += 1
            continue

        if file_path.suffix.lower() != ".txt":
            other_count += 1
            continue

        txt_count += 1
        try:
            content = file_path.read_text(encoding="utf-8")
            summary = summarize_text(content)
            rows.append([file_path.name, str(file_path), summary])
        except UnicodeDecodeError:
            errors.append(f"{file_path.name}: not UTF-8 encoded")
        except OSError as exc:
            errors.append(f"{file_path.name}: {exc}")

    return rows, txt_count, other_count, errors


def analyze_uploaded_files(uploaded_files) -> Tuple[List[List[str]], int, int, List[str]]:
    """Analyze uploaded files and summarize .txt files."""
    rows: List[List[str]] = []
    txt_count = 0
    other_count = 0
    errors: List[str] = []

    for file in uploaded_files:
        file_name = file.name
        if not file_name.lower().endswith(".txt"):
            other_count += 1
            continue

        txt_count += 1
        try:
            content = file.getvalue().decode("utf-8")
            summary = summarize_text(content)
            rows.append([file_name, "uploaded", summary])
        except UnicodeDecodeError:
            errors.append(f"{file_name}: not UTF-8 encoded")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{file_name}: {exc}")

    return rows, txt_count, other_count, errors


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to Excel bytes for download and optional save."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Summary")
    return buffer.getvalue()


def main() -> None:
    st.set_page_config(page_title="Smart File Analysis Web App", layout="wide")

    st.title("Smart File Analysis Web App")
    st.caption("Analyze folder files, summarize .txt content, view graph, and export Excel")

    mode = st.radio(
        "Input mode",
        ["Local folder path", "Upload files"],
        horizontal=True,
    )

    default_data_folder = Path(__file__).resolve().parent / "data"
    default_path = str(default_data_folder) if default_data_folder.is_dir() else ""

    folder_input = ""
    uploaded_files = []
    save_to_folder = False

    if mode == "Local folder path":
        folder_input = st.text_input("Folder path", value=default_path, placeholder="E:/path/to/folder")
        save_to_folder = st.checkbox("Also save output.xlsx in selected folder", value=True)
    else:
        uploaded_files = st.file_uploader(
            "Upload files (.txt preferred)",
            type=None,
            accept_multiple_files=True,
        )

    run_clicked = st.button("Analyze Files", type="primary", use_container_width=True)

    if not run_clicked:
        st.info("Enter a folder path and click Analyze Files.")
        return

    folder = None
    with st.spinner("Analyzing files..."):
        if mode == "Local folder path":
            folder = Path(folder_input.strip().strip('"').strip("'"))
            if not folder_input.strip():
                st.error("Please enter a folder path.")
                return

            if not folder.exists() or not folder.is_dir():
                st.error("Invalid folder path.")
                return

            try:
                rows, txt_count, other_count, errors = analyze_folder(folder)
            except RuntimeError as exc:
                st.error(str(exc))
                return
        else:
            if not uploaded_files:
                st.error("Please upload at least one file.")
                return

            rows, txt_count, other_count, errors = analyze_uploaded_files(uploaded_files)

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("TXT files", txt_count)
    metric2.metric("Other files", other_count)
    metric3.metric("Summaries generated", len(rows))

    st.subheader("File Analysis")
    fig, axis = plt.subplots(figsize=(7, 4))
    bars = axis.bar(["TXT Files", "Other Files"], [txt_count, other_count], color=["#2EA043", "#8B949E"])
    axis.set_ylabel("Count")
    axis.set_title("File Distribution")
    for bar, value in zip(bars, [txt_count, other_count]):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 0.02, str(value), ha="center", va="bottom")
    st.pyplot(fig)

    if errors:
        with st.expander("Read errors"):
            for item in errors:
                st.warning(item)

    if not rows:
        st.warning("No .txt files found to summarize.")
        return

    df = pd.DataFrame(rows, columns=["File Name", "File Path", "Summary"])
    st.subheader("Processed Data")
    st.dataframe(df, use_container_width=True)

    excel_bytes = dataframe_to_excel_bytes(df)

    if mode == "Local folder path" and save_to_folder and folder is not None:
        output_file = folder / "output.xlsx"
        try:
            output_file.write_bytes(excel_bytes)
            st.success(f"Excel file saved at: {output_file}")
        except OSError as exc:
            st.error(f"Could not save output.xlsx in folder: {exc}")

    st.download_button(
        label="Download Excel",
        data=excel_bytes,
        file_name="output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
