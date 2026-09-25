import gradio as gr
from private_qa import build_engine, answer

engine = build_engine()
demo = gr.Interface(
    fn=lambda question: answer(engine, question),
    inputs=gr.Textbox(label="Ask about the fictional course", lines=3),
    outputs=gr.Textbox(label="Answer and retrieved filenames", lines=8),
    title="Course helpdesk",
    description="Practice data only. Retrieved text is sent to a hosted model.",
    examples=[["When can I request a refund?"], ["What laptop do I need?"]],
)
if __name__ == "__main__":
    demo.launch()
