from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import db, string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    # ログイン判定
    if db.login(user_name, password):
        session['user'] = True      # session にキー：'user', バリュー:True を追加
        session.permanent = True    # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=5)   # session の有効期限を 1 分に設定
        return redirect(url_for('mypage'))
    else :
        error = 'ユーザ名またはパスワードが違います。'
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)

@app.route('/mypage', methods=['GET'])
def mypage():
    # session にキー：'user' があるか判定
    if 'user' in session:
        return render_template('mypage.html')   # session があれば mypage.html を表示
    else :
        return redirect(url_for('index'))   # session がなければログイン画面にリダイレクト

@app.route('/logout')
def logout():
    session.pop('user', None)   # session の破棄
    return redirect(url_for('index'))   # ログイン画面にリダイレクト

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error, user_name=user_name, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)

    count = db.insert_user(user_name, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)
    
@app.route('/list')
def list():
    book_list = db.select_all_books()
    return render_template('list.html', books=book_list)

@app.route('/register_library')
def register_library():
    return render_template('register_library.html')
    
@app.route('/register_library_exe', methods=['POST'])
def register_library_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
   
    
    db.insert_book(title, author, isbn)
    
    book_list=db.select_all_books()
    
    return render_template('list.html', books=book_list)


@app.route('/delete')
def delete_library():
    return render_template('delete_library.html')

@app.route('/delete_library_exe', methods=['POST'])
def delete_library_exe():
    isbn = request.form.get('isbn')
    
    db.delete_book(isbn)  # この行の引用符を削除します
    
    book_list = db.select_all_books()
    
    return render_template('list.html', books=book_list)

@app.route('/search')
def search_library():
    return render_template('search_library.html')

@app.route('/search_library_exe', methods=['POST'])
def search_library_exe():
    title = request.form.get('title')

    search_results = db.search_book(title)  # Assign the search results to a variable
    
    book_list = db.select_all_books()
 
    return render_template('list.html', books=search_results)  # Use the search results variable

@app.route('/update')
def update_library():
    return render_template('update_library.html')

@app.route('/update_library_exe', methods=['POST'])
def update_library_exe():
    title = request.form.get('title')
    isbn = request.form.get('isbn')

    db.update_book(title, isbn)
 
    book_list = db.select_all_books()
    return render_template('list.html', books=book_list)

if __name__ == '__main__':
    app.run(debug=True)