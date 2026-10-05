import re
import unicodedata
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========================================
# CẤU HÌNH ĐƯỜNG DẪN ẢNH CỐ ĐỊNH
# ==========================================
CLASS_BG_URL = "/static/backgrounds/tap_the_lop.jpg"
BOYS_AVATAR_URL = "/static/avatars/cac_ban_nam.jpg" # Đảm bảo file ảnh này có trong folder static/avatars/


def format_display_name(text):
    """Chuẩn hóa định dạng tên hiển thị (Viết hoa chữ cái đầu)"""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text.title()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-card', methods=['POST'])
def get_card():
    data = request.get_json()
    input_name = data.get('name', '')
    
    if not input_name or not input_name.strip():
        return jsonify({'success': False, 'message': 'Vui lòng nhập tên!'}), 400

    display_name = format_display_name(input_name)

    # Nội dung lời chúc dài + Chữ ký xuống dòng ở cuối
    wishes = (
        f"Gửi tới {display_name} những lời chúc ấm áp và tuyệt vời nhất nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
        f"Chúc bạn luôn rạng rỡ, xinh đẹp, giữ trọn nụ cười tươi tắn trên môi và tràn đầy năng lượng tích cực. "
        f"Mong rằng chặng đường phía trước của bạn sẽ luôn ngập tràn niềm vui, thành công trong học tập và gặp thật nhiều may mắn, yêu thương trong cuộc sống! ✨💖\n\n"
        f"From: 22 Anh Tài K15 THPT Lê Hoàn 💫"
    )

    return jsonify({
        'success': True,
        'name': display_name,
        'image_url': BOYS_AVATAR_URL,
        'bg_url': CLASS_BG_URL,
        'wishes': wishes
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)