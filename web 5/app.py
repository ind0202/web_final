from flask import Flask, render_template, request, jsonify, g, redirect
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 啟用所有路由的 CORS

# 資料庫連接設定（使用 Windows 認證）
DATABASE_CONNECTION_STRING = 'DRIVER={SQL Server};' \
                            'SERVER=LAPTOP-UIFPN5VA\\SQLSERVER2022;' \
                            'DATABASE=web;' \
                            'trusted_connection=yes'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pyodbc.connect(DATABASE_CONNECTION_STRING)
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 資料庫初始化
with app.app_context():
    get_db()

@app.route('/')
def home():
    return render_template('mainpage.html')

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        birthday = data.get('birthday')
        gender = data.get('gender')
        password = data.get('password')

        # 檢查用戶名是否已存在
        with get_db().cursor() as cursor:
            cursor.execute('SELECT * FROM Users WHERE Username = ?', (username,))
            existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'message': '該用戶名已經存在，請選擇其他用戶名。'})

        # 確保所有字段都有值，且不為空
        if not (username and email and birthday and gender and password):
            return jsonify({'message': '請填寫所有必填信息。'})

        # 存儲用戶數據
        with get_db().cursor() as cursor:
            cursor.execute('''
                INSERT INTO Users (Username, Email, Birthday, Gender, Password)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, birthday, gender, password))

        get_db().commit()  # 提交事務

        return jsonify({'message': '註冊成功'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': f'註冊失敗，請重試。錯誤訊息：{e}'})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # 使用資料庫游標
        with get_db().cursor() as cursor:
            cursor.execute('''
                SELECT * FROM Users
                WHERE Username = ? AND Password = ?
            ''', (username, password))

            result = cursor.fetchone()

        if result:
            # 登錄成功，返回 JSON 响應
            return jsonify({'message': '登入成功'})
        else:
            # 登錄失敗，返回 JSON 响應
            return jsonify({'message': '登入失敗，請檢查用戶名和密碼。'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': '登入失敗，請稍後再試。'})

@app.route('/register.html')
def register_page():
    return render_template('register.html')

# 靜態文件路由
@app.route('/style_login.css')
def style_login():
    return app.send_static_file('style_login.css')

@app.route('/style_addquestion.css')
def style_addquestion():
    return app.send_static_file('style_addquestion.css')

@app.route('/style_love.css')
def style_love():
    return app.send_static_file('style_love.css')

@app.route('/style_mainpage_nologin.css')
def style_mainpage_nologin():
    return app.send_static_file('style_mainpage_nologin.css')

@app.route('/style_mainpage.css')
def style_mainpage():
    return app.send_static_file('style_mainpage.css')

@app.route('/style_mainpage1.css')
def style_mainpage1():
    return app.send_static_file('style_mainpage1.css')

@app.route('/style_register.css')
def style_register():
    return app.send_static_file('style_register.css')

@app.route('/style_personal.css')
def style_personal():
    return app.send_static_file('style_personal.css')

# 頁面路由
@app.route('/mainpage1.html')
def my_mainpage1_page():
    return render_template('mainpage1.html')

@app.route('/mainpage2.html')
def my_mainpage2_page():
    return render_template('mainpage2.html')

@app.route('/mainpage3.html')
def my_mainpage3_page():
    return render_template('mainpage3.html')

@app.route('/mainpage.html')
def my_mainpage_page():
    return render_template('mainpage.html')

@app.route('/mainpage_nologin.html')
def my_mainpage_nologin_page():
    return render_template('mainpage_nologin.html')

@app.route('/love.html')
def my_love_page():
    return render_template('love.html')

@app.route('/homework.html')
def my_homework_page():
    return render_template('homework.html')

@app.route('/add_question.html')
def my_add_question_page():
    return render_template('add_question.html')

@app.route('/login.html')
def my_login_page():
    return render_template('login.html')

@app.route('/personal.html')
def my_personal_page():
    return render_template('personal.html')

@app.route('/travel.html')
def my_travel_page():
    return render_template('travel.html')

# 成功页面路由
@app.route('/success')
def success():
    return 'Login successful!'

if __name__ == '__main__':
    app.run(debug=True)
