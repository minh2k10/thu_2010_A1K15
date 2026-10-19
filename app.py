import re
import random
import unicodedata
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========================================
# CẤU HÌNH ĐƯỜNG DẪN ẢNH ĐỘC QUYỀN
# ==========================================
CHAM_AVATAR_URL = "/static/avatars/bao_cham.jpg"
CHAM_BG_URL = "/static/backgrounds/cham_bg.jpg"  # Hoặc dùng lại CLASS_BG_URL nếu muốn

def remove_accents(input_str):
    """Hàm loại bỏ dấu tiếng Việt để so sánh tên linh hoạt"""
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()

# ==========================================
# DANH SÁCH 30 LỜI CHÚC DÀNH RIÊNG CHO BẢO CHÂM
# ==========================================
# ==========================================
# DANH SÁCH 30 LỜI CHÚC DÀNH RIÊNG BẢO CHÂM TỪ ĐẮC VIỆT DŨNG
# ==========================================
WISH_TEMPLATES = [
    # 1
    "Gửi tới {name} những lời chúc ấm áp và tuyệt vời nhất nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
    "Chúc Châm luôn rạng rỡ, xinh đẹp, giữ trọn nụ cười tươi tắn trên môi và tràn đầy năng lượng tích cực. "
    "Mong rằng chặng đường phía trước của em sẽ luôn ngập tràn niềm vui, thành công trong học tập và gặp thật nhiều may mắn, yêu thương trong cuộc sống! ✨💖\n\n"
    "From: Đắc Việt Dũng 💫",

    # 2
    "Gửi tới {name} - cô gái vô cùng đáng yêu và đặc biệt nhất của Dũng!\n\n"
    "Nhân ngày 20/10, chúc Châm luôn giữ vững phong độ xinh đẹp, tự tin và tỏa sáng theo cách của riêng mình. "
    "Cảm ơn em vì đã luôn đồng hành, sẻ chia và mang đến nhiều kỉ niệm ngọt ngào cho anh. Chúc em một ngày tràn ngập hoa, quà và niềm vui trọn vẹn nhất! 🌸✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 3
    "Chúc mừng ngày Phụ nữ Việt Nam 20/10 gửi tới Bảo Châm!\n\n"
    "Cảm ơn sự xuất hiện của em đã giúp cuộc sống của Dũng luôn ấm áp và ngập tràn niềm vui. "
    "Chúc Châm ngày hôm nay nhận được thật nhiều tình yêu thương, ngọt ngào và quà cáp. Hãy luôn giữ vững nụ cười rạng rỡ, học giỏi và luôn hạnh phúc em nhé! 💕🌷\n\n"
    "From: Đắc Việt Dũng 💫",

    # 4
    "Gửi em - cô gái xinh xắn {name} nhân ngày 20/10!\n\n"
    "Chúc Châm ngày càng rạng rỡ, học tập đạt thật nhiều điểm số cao và luôn đạt được những mục tiêu mình mơ ước. "
    "Cảm ơn em đã luôn dịu dàng, đáng yêu và đồng hành cùng anh. Mong mọi điều bình an và hạnh phúc nhất sẽ luôn mỉm cười với em! ✨💝\n\n"
    "From: Đắc Việt Dũng 💫",

    # 5
    "Chúc mừng {name} nhân ngày 20/10 thật nhiều niềm vui và ý nghĩa!\n\n"
    "Cảm ơn Châm vì đã luôn mang tới năng lượng tích cực và sự ấm áp cho Dũng. "
    "Chúc em luôn xinh tươi như những bông hoa mùa xuân, luôn kiên cường, tự tin bước đi trên con đường tương lai và luôn là cô gái hạnh phúc nhất bên anh! 🌹💫\n\n"
    "From: Đắc Việt Dũng 💫",

    # 6
    "Gửi Bảo Châm nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
    "Chúc em có một ngày kỉ niệm thật ngọt ngào bên gia đình, bạn bè và người yêu thương em. "
    "Mong rằng hành trình sắp tới của Châm sẽ toàn là cơ hội tốt, đi đến đâu tỏa sáng đến đó và luôn nhận được sự trân trọng, yêu mến từ mọi người! ✨💖\n\n"
    "From: Đắc Việt Dũng 💫",

    # 7
    "Gửi tới {name} xinh đẹp và tràn đầy nhiệt huyết!\n\n"
    "Cảm ơn vì sự đồng hành tuyệt vời của Châm cùng anh trong suốt thời gian qua. "
    "Nhân ngày 20/10, chúc em luôn giữ được tâm hồn trẻ trung, nụ cười rạng rỡ, vượt qua mọi kỳ thi thật dễ dàng và luôn thành công trên mọi chặng đường! 🎀🌺\n\n"
    "From: Đắc Việt Dũng 💫",

    # 8
    "Gửi Bảo Châm - cô gái vô cùng đặc biệt duy nhất của anh!\n\n"
    "Chúc Châm ngày 20/10 ngập tràn trong sự cưng chiều, nhận được vô số món quà đáng yêu và luôn ngập tràn tiếng cười. "
    "Cảm ơn em đã luôn là một phần quan trọng không thể thiếu của anh. Chúc em luôn xinh xắn, may mắn và gặt hái nhiều kết quả cao! 💖🌟\n\n"
    "From: Đắc Việt Dũng 💫",

    # 9
    "Chúc mừng ngày 20/10 ngọt ngào gửi tới Bảo Châm!\n\n"
    "Cảm ơn Châm vì những khoảnh khắc đáng nhớ và sự dễ thương em mang lại cho cuộc sống của anh. "
    "Mong rằng em luôn tự tin vào bản thân, theo đuổi đam mê một cách trọn vẹn và luôn cảm nhận được tình yêu chân thành từ anh. Chúc em ngày hôm nay thật hạnh phúc! 🌷✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 10
    "Thân gửi {name} nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
    "Chúc Châm có một ngày ngọt ngào, tràn đầy niềm vui và nhiều sự bất ngờ. "
    "Hãy luôn là một cô gái xinh đẹp, mạnh mẽ, tự tin và vững vàng bước qua mọi thử thách nhé. Cảm ơn em vì đã luôn dịu dàng và đáng yêu! ✨💖\n\n"
    "From: Đắc Việt Dũng 💫",

    # 11
    "Gửi đến Bảo Châm những lời chúc chân thành nhất ngày 20/10!\n\n"
    "Cảm ơn Châm vì đã luôn làm cho thế giới của anh trở nên tuyệt vời hơn. "
    "Chúc em tuổi mới ngày càng xinh đẹp, sắc sảo, học tập thăng tiến và mỗi ngày trôi qua đều là một ngày ngập tràn niềm vui cùng những điều tuyệt vời nhất! 🌸⭐\n\n"
    "From: Đắc Việt Dũng 💫",

    # 12
    "Gửi Bảo Châm thân mến của anh!\n\n"
    "Nhân ngày 20/10, chúc em luôn tràn ngập sức sống, xinh đẹp rạng ngời và giữ được sự vui vẻ hồn nhiên. "
    "Cảm ơn sự hiện diện đáng quý của Châm trong cuộc đời Dũng. Mong em luôn bình an, may mắn và vạn sự như ý! 💫💕\n\n"
    "From: Đắc Việt Dũng 💫",

    # 13
    "Chúc mừng ngày 20/10 thật nhiều niềm vui gửi tới {name}!\n\n"
    "Chúc Châm hôm nay sẽ nhận được thật nhiều hoa, quà và vô vàn lời chúc ý nghĩa. "
    "Cảm ơn em vì đã luôn dịu dàng, lắng nghe và ở bên cạnh anh. Chúc chặng đường tương lai của em sẽ luôn rải đầy hoa hồng và may mắn! 🌹✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 14
    "Gửi Bảo Châm - cô gái vô cùng cá tính và đáng yêu!\n\n"
    "Nhân ngày Phụ nữ Việt Nam, chúc em lúc nào cũng rạng rỡ, tràn đầy năng lượng tích cực và luôn tỏa sáng. "
    "Cảm ơn Châm đã mang lại nhiều nụ cười cho anh. Chúc em đạt được mọi ước mơ và gặt hái thật nhiều thành công nhé! 💖✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 15
    "Chúc mừng 20/10 ngọt ngào gửi tới {name}!\n\n"
    "Cảm ơn vì Châm đã luôn là một mảnh ghép dịu dàng, đáng mến nhất của anh. "
    "Chúc em ngày hôm nay và cả 364 ngày còn lại trong năm luôn xinh đẹp, an yên, không có lo âu vướng bận và thi cử đạt thành tích xuất sắc! 🌷💖\n\n"
    "From: Đắc Việt Dũng 💫",

    # 16
    "Thân gửi Bảo Châm nhân ngày Phụ nữ Việt Nam!\n\n"
    "Chúc Châm luôn vững tin vào bản thân, xinh đẹp mỗi ngày và luôn gặp những cơ hội rộng mở trên đường đời. "
    "Cảm ơn em đã gắn bó và đóng góp nhiều kỷ niệm đẹp cho thanh xuân của anh. Chúc bé có một ngày 20/10 thật trọn vẹn! 🌟✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 17
    "Gửi Bảo Châm xinh đẹp của anh!\n\n"
    "Chúc Châm ngày 20/10 thật nhiều hoa thơm, quà đẹp và những lời chúc yêu thương nhất. "
    "Cảm ơn em vì đã luôn tinh tế, mang lại không khí ấm áp cho anh. Mong rằng chặng đường học tập của em luôn đạt điểm tuyệt đối! 🌸💖\n\n"
    "From: Đắc Việt Dũng 💫",

    # 18
    "Chúc mừng {name} nhân ngày 20/10!\n\n"
    "Cảm ơn sự chân thành và tình cảm ấm áp em luôn dành cho Dũng. "
    "Chúc Châm luôn giữ được sự vui tươi, thông minh, ngày càng xinh đẹp và chinh phục được mọi đỉnh cao học tập mà em mơ ước! ✨💥\n\n"
    "From: Đắc Việt Dũng 💫",

    # 19
    "Gửi tới Bảo Châm - bông hoa tươi thắm nhất của cuộc đời anh!\n\n"
    "Nhân ngày Phụ nữ Việt Nam 20/10, chúc em luôn rực rỡ, may mắn và hạnh phúc. "
    "Cảm ơn vì Châm đã luôn mang sự tích cực đến bên anh. Mong rằng mọi dự định sắp tới của em đều diễn ra thuận lợi! 🌷💫\n\n"
    "From: Đắc Việt Dũng 💫",

    # 20
    "Chúc mừng Bảo Châm nhân ngày kỉ niệm 20/10!\n\n"
    "Mong Châm luôn tràn đầy sức sống, nụ cười luôn thường trực trên môi và luôn cảm nhận được tình yêu thương từ anh. "
    "Cảm ơn em đã luôn đồng hành cùng Dũng, chúc em luôn gặt hái được những điều tuyệt vời nhất! 💕✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 21
    "Thân gửi Bảo Châm xinh xắn!\n\n"
    "Nhân ngày 20/10, chúc em không chỉ hôm nay mà ngày nào cũng là một ngày ngập tràn niềm vui và bình an. "
    "Cảm ơn sự hiền lành, dễ thương của Châm. Chúc em thi cử luôn suôn sẻ và gặt hái thật nhiều hoa điểm 10! 🌸🌟\n\n"
    "From: Đắc Việt Dũng 💫",

    # 22
    "Gửi tới {name} - cô gái thông minh và đáng yêu!\n\n"
    "Nhân ngày 20/10, chúc Châm lúc nào cũng trẻ trung, tự tin và vững bước với ước mơ của mình. "
    "Cảm ơn Châm vì đã cùng tạo nên một thời thanh xuân thật đẹp với anh. Chúc em có một ngày ngọt ngào tràn đầy bất ngờ! 💖✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 23
    "Chúc mừng {name} nhân ngày Phụ nữ Việt Nam!\n\n"
    "Cảm ơn nụ cười và năng lượng đáng yêu của em dành cho anh mỗi ngày. "
    "Chúc Châm 20/10 nhận thật nhiều quà, luôn xinh đẹp như công chúa và gặt hái thành công rực rỡ! 🌹💫\n\n"
    "From: Đắc Việt Dũng 💫",

    # 24
    "Gửi Bảo Châm thân thương!\n\n"
    "Chúc Châm ngày 20/10 thật nhiều niềm vui, luôn tự tin tỏa sáng và đạt được mọi mong ước. "
    "Cảm ơn em đã cùng đồng hành, vun đắp tình cảm giữa hai đứa thêm gắn kết. Mong em luôn bình an và luôn nở nụ cười rạng rỡ! 🌷✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 25
    "Chúc mừng Bảo Châm nhân dịp đặc biệt 20/10!\n\n"
    "Cảm ơn em vì đã luôn lắng nghe, chia sẻ và tô điểm cho cuộc sống của anh thêm nhiều sắc màu. "
    "Chúc Châm luôn xinh đẹp, duyên dáng, giữ trọn ngọn lửa đam mê và vượt qua mọi kì thi một cách xuất sắc nhất! 💕💫\n\n"
    "From: Đắc Việt Dũng 💫",

    # 26
    "Gửi người thương Bảo Châm vô cùng dễ mến!\n\n"
    "Chúc Châm ngày Phụ nữ Việt Nam tràn ngập tiếng cười, nhận được những bất ngờ ngọt ngào nhất. "
    "Cảm ơn em vì đã là một phần tuyệt vời trong đời anh. Mong tương lai sẽ mang đến cho em vô vàn may mắn! ✨🌸\n\n"
    "From: Đắc Việt Dũng 💫",

    # 27
    "Thân gửi {name} nhân ngày 20/10!\n\n"
    "Chúc Châm luôn giữ được sự lạc quan, rạng rỡ và nét cuốn hút rất riêng của mình. "
    "Cảm ơn tình cảm thầm lặng nhưng tuyệt vời em dành cho Dũng. Chúc em luôn vui vẻ, học giỏi và gặp toàn điều tốt lành! 💖🌟\n\n"
    "From: Đắc Việt Dũng 💫",

    # 28
    "Gửi tới Bảo Châm lời chúc 20/10 ngọt ngào nhất!\n\n"
    "Chúc em xinh đẹp rạng ngời, lúc nào cũng tràn đầy niềm tin và động lực phấn đấu. "
    "Cảm ơn Châm đã cùng anh đi qua những tháng ngày đẹp đẽ. Chúc em luôn là cô gái hạnh phúc và thành công! 🌺✨\n\n"
    "From: Đắc Việt Dũng 💫",

    # 29
    "Chúc mừng ngày Phụ nữ Việt Nam gửi tới Bảo Châm!\n\n"
    "Mong rằng ngày hôm nay của Châm sẽ ngập tràn quà tặng, sự quan tâm và tình yêu thương từ anh. "
    "Cảm ơn em vì sự dễ thương và ấm áp. Chúc em luôn may mắn, học tập xuất sắc và luôn tỏa sáng! 🌸💖\n\n"
    "From: Đắc Việt Dũng 💫",

    # 30
    "Gửi Bảo Châm - mảnh ghép rực rỡ nhất của đời anh!\n\n"
    "Nhân ngày 20/10, chúc em có một ngày ngập tràn nụ cười, luôn xinh đẹp, thông minh và tràn đầy kiêu hãnh. "
    "Cảm ơn em vì đã cùng anh tạo nên vô vàn kỉ niệm thanh xuân tuyệt đẹp. Chúc mọi ước mơ của Châm đều trở thành hiện thực! ✨💫\n\n"
    "From: Đắc Việt Dũng 💫"
]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-card', methods=['POST'])
def get_card():
    data = request.get_json()
    input_name = data.get('name', '').strip()
    
    if not input_name:
        return jsonify({'success': False, 'message': 'Vui lòng nhập tên của bạn nhé!'}), 400

    clean_name = remove_accents(input_name)

    # ĐIỀU KIỆN ĐỘC QUYỀN: Chỉ chấp nhận các tên gọi của Nguyễn Bảo Châm
    allowed_names = ["nguyen bao cham", "bao cham", "cham", "nguyen cham"]
    
    is_cham = any(name in clean_name for name in allowed_names)

    if is_cham:
        display_name = "Nguyễn Bảo Châm"
        random_template = random.choice(WISH_TEMPLATES)
        wishes = random_template.format(name=display_name)

        return jsonify({
            'success': True,
            'name': display_name,
            'image_url': CHAM_AVATAR_URL,  # Ảnh đại diện của Bảo Châm
            'bg_url': CHAM_BG_URL,          # Ảnh nền riêng của Bảo Châm
            'wishes': wishes
        })
    else:
        # Nếu nhập tên người khác sẽ từ chối nhẹ nhàng
        return jsonify({
            'success': False,
            'message': 'ko phải vợ dũng! 💕'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)