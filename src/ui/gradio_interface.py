import gradio as gr

class JournalUI:
    def __init__(self, chat_handler):
        """Initialize the journal UI with the given chat handler function."""
        self.chat_handler = chat_handler
    
    def create_interface(self):
        """Create and return the Gradio interface."""
        with gr.Blocks(theme=gr.themes.Soft(primary_hue="teal")) as demo:
            gr.Markdown("""
            # 🌿 Inner Mirror: Reflective Journaling Agent
            
            Welcome to Inner Mirror, your personal reflective journaling companion. Share your thoughts, and I'll help you process them with empathy and insight.
            
            
            """)
            
            with gr.Row():
                with gr.Column(scale=4):
                    chatbot = gr.Chatbot(
                        height=500, 
                        type="messages", 
                        value=[
                            {"role": "assistant", "content": "Hello there! 😊 I'm Mirror, here to reflect on your thoughts and provide insights."}
                        ],
                        show_label=False
                    )
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            show_label=False, 
                            placeholder="Write your thoughts and press Enter…",
                            container=False,
                            scale=9
                        )
                        send_button = gr.Button("Send", scale=1)
                    
                    gr.Markdown("""
                    ### 💭 How to get the most out of journaling
                    
                    - Be honest with yourself
                    - There are no right or wrong entries
                    - Write regularly, even if briefly
                    - Reflect on patterns in your thoughts and feelings
                    """)
                
                with gr.Column(scale=1):
                    gr.Markdown("### 🎬 Tool Examples")
                    
                    example_queries = [
                        "I'm feeling anxious today. Can you help me?",
                        "Find me a video about mindfulness meditation",
                        "What are some trending videos in education?",
                        "I had a great day today! Everything went well."
                    ]
                    
                    gr.Examples(
                        examples=example_queries,
                        inputs=msg
                    )
            
            state = gr.State([])

            msg.submit(self.chat_handler, [msg, state], [msg, chatbot])
            send_button.click(self.chat_handler, [msg, state], [msg, chatbot])
            
            return demo 