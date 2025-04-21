import streamlit as st
import fitz  # PyMuPDF
import tempfile

st.set_page_config(page_title="PDF Flattener & Merger", page_icon="📄")
st.title("📄 PDF Flattener & Merger")
st.write("Upload multiple PDF files below to flatten (preserve visual signatures) and merge them into one.")

uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

    if st.button("🔁 Flatten & Merge PDFs"):
        with st.spinner("Processing..."):
            merged_pdf = fitz.open()

            for uploaded_file in uploaded_files:
                pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in pdf:
                    pix = page.get_pixmap(dpi=300)
                    img_rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
                    new_page = merged_pdf.new_page(width=page.rect.width, height=page.rect.height)
                    new_page.insert_image(img_rect, pixmap=pix)
                pdf.close()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                merged_pdf.save(tmp_file.name)
                merged_pdf.close()
                st.success("✅ Flattened and merged successfully!")
                with open(tmp_file.name, "rb") as f:
                    st.download_button("📥 Download Merged PDF", f.read(), file_name="flattened_merged.pdf")

else:
    st.info("Please upload one or more PDF files to get started.")
