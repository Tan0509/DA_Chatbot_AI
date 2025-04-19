from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI
from utils import save_history_to_file


load_dotenv()

app = Flask(__name__)

print("🔑 DEBUG KEY:", os.getenv("OPENROUTER_API_KEY"))  # 👈 In thử

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        completion = client.chat.completions.create(
            model="google/gemma-3-27b-it:free",
            messages=[
                # Không dùng system ở đây nữa!
                {"role": "user", "content": user_message}
            ]
        )

        if completion and completion.choices:
            reply = completion.choices[0].message.content
            # ✅ Lưu lại hội thoại
            save_history_to_file(user_message, reply)
            
            return jsonify({"reply": reply})
        else:
            print("❌ DEBUG - Không có phản hồi từ AI:")
            print(completion)
            return jsonify({"reply": "Không có phản hồi từ AI."})

    except Exception as e:
        print("❌ DEBUG - Lỗi khi gọi OpenRouter:", e)
        return jsonify({"reply": f"Bot: Lỗi khi gọi AI: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
