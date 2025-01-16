# from backend.app.chatbot.rag.bot import get_answer
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.agent.reactagent import answer as react_answer
# import gradio as gr
# from reactagent import answer
# if __name__ == "__main__":
#     def main():
#         print("Type 'exit' to end the conversation.")
#         while True:
#             query = input("Enter your question: ")
#             if query.lower() == 'exit':
#                 print("Ending the conversation. Goodbye!")
#                 break
#             answer = get_answer(query)
#             print(f"Answer: {answer}")
#     main()
#     # demo = gr.ChatInterface(fn=get_answer, theme=gr.themes.Soft(), title="BOT")
#     # demo.launch(share=False)

app = Flask(__name__)

CORS(app)

@app.route('/')
def home():
    return 'Hello, world!'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    question = data['question']
    answer = react_answer(question)
    return jsonify({"response": answer})

    # data = request.get_json()
    # query = data.get('question', '').strip()
    # mode = data.get('mode', 'rag')  # Default to 'rag' if mode not specified

    # if not query:
    #     return jsonify({"error": "No query provided"}), 400

    # try:
    #     if mode.lower() == 'react':  # Use ReactAgent for specific queries
    #         response = react_answer(query)
    #     else:  # Default to RAG-based retrieval
    #         response = get_answer(query)

    #     return jsonify({"response": response}), 200
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)