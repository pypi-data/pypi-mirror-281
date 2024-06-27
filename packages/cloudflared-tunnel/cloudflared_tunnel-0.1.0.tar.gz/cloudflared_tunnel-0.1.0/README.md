# Cloudflared Context Manager

Simple context manager to create a Cloudflared tunnel for a localhost port of choice.

Minimal example on how to use this package with Gradio:

```python
import gradio as gr
import cloudflared_tunnel

with gr.Blocks() as demo:
    with gr.Column():
        with gr.Row():
            input_text = gr.Textbox(lines=10, label="Input")
            output_text = gr.Textbox(lines=10, label="Output")
        submit_button = gr.Button(value="Echo")
    submit_button.click(lambda x: x, inputs=input_text, outputs=output_text)

if __name__ == "__main__":
    with cloudflared_tunnel.run() as port:
        demo.launch(show_api=False, server_port=port)
```

## Acknowledgements

This project is derived from [flask-cloudflared](https://github.com/UWUplus/flask-cloudflared), which in turn is based on [flask-ngrok](https://github.com/gstaff/flask-ngrok).
