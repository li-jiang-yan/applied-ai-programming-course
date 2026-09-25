import gradio as gr
from backend import predict

def submit(text, threshold, display, count):
    return predict(text, threshold, display), count + 1, str(count + 1)

with gr.Blocks() as demo:
    gr.Markdown("# Review desk\nA tiny teaching model. Review predictions before using them.")
    count = gr.State(0)
    review = gr.Textbox(label="Course review", placeholder="The explanations were clear", lines=3)
    threshold = gr.Slider(0.5, 0.95, value=0.6, step=0.05, label="Human-review threshold")
    display = gr.Dropdown(["Detailed", "Label only"], value="Detailed", label="Output format")
    run = gr.Button("Analyse review", variant="primary")
    result = gr.Textbox(label="Prediction")
    total = gr.Textbox(label="Requests in this session", value="0")
    run.click(submit, [review, threshold, display, count], [result, count, total])
    threshold.change(lambda: "Threshold changed. Select Analyse review to update.", outputs=result)

if __name__ == "__main__":
    demo.queue().launch()
