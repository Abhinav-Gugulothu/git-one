import gradio as gr
from datetime import datetime


# -----------------------------
# Placeholder callbacks only
# -----------------------------
def fetch_placeholder(url):
    if not (url or "").strip():
        return "No URL entered."
    return "Fetched content preview will appear here (placeholder)."


def run_placeholder(
    text_input,
    file_input,
    fetched_preview,
    length_value,
    style_value,
    language_value,
    include_kp,
    include_actions,
):
    summary = (
        "Summary placeholder\n\n"
        f"- Length: {length_value}\n"
        f"- Style: {style_value}\n"
        f"- Language: {language_value}\n"
    )
    key_points = "Key points placeholder" if include_kp else "Key points disabled."
    action_items = "Action items placeholder" if include_actions else "Action items disabled."

    src_len = len((text_input or "").strip()) + len((fetched_preview or "").strip())
    out_len = len(summary)
    compression = 0 if src_len == 0 else max(0, int((1 - (out_len / src_len)) * 100))
    stats = (
        f"Original: {src_len} | Summary: {out_len} | "
        f"Compression: {compression}% | Updated: {datetime.now().strftime('%H:%M:%S')}"
    )
    return "Done", summary, key_points, action_items, stats


def set_status_ready():
    return "Ready"


def set_status_copy():
    return "Copied (placeholder)"


def set_status_download():
    return "Download triggered (placeholder)"


CUSTOM_CSS = """
.gradio-container {
  max-width: 1520px !important;
  margin: 0 auto !important;
}

.app-title h1,
.app-subtitle p {
  text-align: center !important;
  margin: 0;
}

.app-subtitle p {
  margin-top: 6px;
  margin-bottom: 12px;
  color: #555;
}

.panel {
  border: 1px solid #d9d9d9;
  border-radius: 12px;
  background: #fff;
  padding: 12px;
}

.panel h3 {
  margin: 0 0 10px 0;
}

.workspace-panel {
  min-height: 560px;
}

.action-panel {
  border: 1px solid #d9d9d9;
  border-radius: 12px;
  background: #fff;
  padding: 10px 12px;
}
"""


with gr.Blocks(
    title="Smart Summarizer",
    theme=gr.themes.Soft(),
    fill_width=False,
    css=CUSTOM_CSS,
) as demo:
    # Header (center aligned)
    with gr.Column(elem_classes=["app-title"]):
        gr.Markdown("# Smart Summarizer")
    with gr.Column(elem_classes=["app-subtitle"]):
        gr.Markdown("<p>Professional desktop summarization workspace</p>")

    status = gr.Textbox(label="Status", value="Ready", interactive=False)

    # Top row: full-width options
    with gr.Row():
        with gr.Column():
            with gr.Group(elem_classes=["panel"]):
                gr.Markdown("### Summarization Options")
                with gr.Row():
                    length_slider = gr.Slider(10, 100, value=40, step=5, label="Summary Length")
                    style_dd = gr.Dropdown(
                        ["Bullet Points", "Executive", "Simple", "Technical"],
                        value="Bullet Points",
                        label="Style",
                    )
                    language_dd = gr.Dropdown(
                        ["English", "Spanish", "French", "German"],
                        value="English",
                        label="Output Language",
                    )
                with gr.Row():
                    include_kp = gr.Checkbox(value=True, label="Include Key Points")
                    include_actions = gr.Checkbox(value=False, label="Include Action Items")

    # Middle row: left + right columns, equal height
    with gr.Row(equal_height=True):
        # Left column: input
        with gr.Column(scale=1, min_width=680):
            with gr.Group(elem_classes=["panel", "workspace-panel"]):
                gr.Markdown("### Input Panel")
                with gr.Tabs():
                    with gr.Tab("Text"):
                        text_input = gr.Textbox(
                            label="Input Text",
                            lines=20,
                            placeholder="Paste source text here...",
                        )
                    with gr.Tab("File"):
                        file_input = gr.File(
                            label="Upload Document",
                            file_types=[".txt", ".pdf", ".docx"],
                        )
                    with gr.Tab("URL"):
                        url_input = gr.Textbox(
                            label="Source URL",
                            placeholder="https://example.com/article",
                        )
                        fetch_btn = gr.Button("Fetch Content")
                        fetched_preview = gr.Textbox(
                            label="Fetched Preview",
                            lines=8,
                            interactive=False,
                        )

        # Right column: output
        with gr.Column(scale=1, min_width=680):
            with gr.Group(elem_classes=["panel", "workspace-panel"]):
                gr.Markdown("### Output Panel")
                with gr.Tabs():
                    with gr.Tab("Summary"):
                        summary_out = gr.Markdown("Summary will appear here.")
                    with gr.Tab("Key Points"):
                        key_points_out = gr.Markdown("Key points will appear here.")
                    with gr.Tab("Action Items"):
                        action_items_out = gr.Markdown("Action items will appear here.")

                stats_out = gr.Textbox(
                    label="Stats",
                    value="Original: - | Summary: - | Compression: - | Updated: -",
                    interactive=False,
                )

    # Bottom row: full-width actions
    with gr.Row():
        with gr.Column():
            with gr.Group(elem_classes=["action-panel"]):
                with gr.Row():
                    copy_btn = gr.Button("Copy")
                    download_btn = gr.Button("Download")
                    regenerate_btn = gr.Button("Regenerate")
                    generate_btn = gr.Button("Generate", variant="primary")

    # Event wiring
    fetch_btn.click(fetch_placeholder, inputs=[url_input], outputs=[fetched_preview])

    generate_btn.click(
        fn=lambda: "Summarizing...",
        inputs=[],
        outputs=[status],
    ).then(
        fn=run_placeholder,
        inputs=[
            text_input,
            file_input,
            fetched_preview,
            length_slider,
            style_dd,
            language_dd,
            include_kp,
            include_actions,
        ],
        outputs=[status, summary_out, key_points_out, action_items_out, stats_out],
    ).then(
        fn=set_status_ready,
        inputs=[],
        outputs=[status],
    )

    regenerate_btn.click(
        fn=lambda: "Regenerating...",
        inputs=[],
        outputs=[status],
    ).then(
        fn=run_placeholder,
        inputs=[
            text_input,
            file_input,
            fetched_preview,
            length_slider,
            style_dd,
            language_dd,
            include_kp,
            include_actions,
        ],
        outputs=[status, summary_out, key_points_out, action_items_out, stats_out],
    ).then(
        fn=set_status_ready,
        inputs=[],
        outputs=[status],
    )

    copy_btn.click(fn=set_status_copy, inputs=[], outputs=[status])
    download_btn.click(fn=set_status_download, inputs=[], outputs=[status])


if __name__ == "__main__":
    demo.launch()