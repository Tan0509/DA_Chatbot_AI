import os
from openai import OpenAI
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Khởi tạo client với OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Biến toàn cục để lưu lịch sử hội thoại
history = []

def get_response(message):
    try:
        # Nếu là tin nhắn đầu tiên, thêm hướng dẫn ngắn vào nội dung
        if not history:
            message = f"Trả lời bằng tiếng Việt. {message}"

        # Thêm câu hỏi người dùng vào lịch sử
        history.append({"role": "user", "content": message})

        # Gộp hướng dẫn + lịch sử để gửi lên model
        messages = [{"role": "system", "content": "Bạn là trợ lý chatbot sinh viên, trả lời ngắn gọn, dễ hiểu, bằng tiếng Việt."}] + history

        # Gọi API
        chat_completion = client.chat.completions.create(
            model="google/gemma-3-27b-it:free",
            messages=messages
        )

        # Lấy phản hồi
        response = chat_completion.choices[0].message.content if chat_completion.choices else "Bot: Không nhận được phản hồi từ mô hình AI."

        # Thêm phản hồi vào lịch sử
        history.append({"role": "assistant", "content": response})

        return response
    except Exception as e:
        return f"Bot: Lỗi khi gọi OpenRouter: {e}"



