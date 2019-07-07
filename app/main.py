from flask import *
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
import os, sys, binascii

# 設定ファイルをインポート
from variable import *

app = Flask(__name__)

# HTTP security header
Talisman(app)

# データベースの初期設定
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# session情報をデータベースへ格納する
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY"] = db
Session(app)


# ユーザーからの購入履歴データベース
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    item_num = db.Column(db.Integer)
    item_dlv = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, item_id, item_num):
        self.user_id = user_id
        self.item_id = item_id
        self.item_num = item_num
        self.item_dlv = False


# ユーザーへの給付履歴データベース
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    prize_name = db.Column(db.String(720))
    prize_money = db.Column(db.Integer)

    def __init__(self, user_id, prize_name, prize_money):
        self.user_id = user_id
        self.prize_name = prize_name
        self.prize_money = prize_money


# データベースを作成
# もしdbファイルがない場合は自動で作成される
db.create_all()


@app.route("/")
def index():
    # 管理者のページ
    if session.get("state_admin"):
        # 未配達品リストの作成
        undlv_list = []
        db_undlv_list = db.session.query(Purchase).filter_by(item_dlv=False)
        for du in db_undlv_list:
            # ユーザー名とユーザーidの照会
            for pu in pwd_user:
                if pu.get("id") == du.user_id:
                    du_user_name: str = pu.get("name")
            # 品物名と品物idの照会
            for il in item_list:
                if il.get("id") == du.item_id:
                    du_item_name: str = il.get("name")
            undlv_list.append(
                {
                    "id": du.id,
                    "user_name": du_user_name,
                    "item_name": du_item_name,
                    "item_num": du.item_num,
                }
            )

        # 購入履歴リストの作成
        log_purchase = []
        db_purchase = db.session.query(Purchase)
        for dp in db_purchase:
            # ユーザー名とユーザーidの照会
            for pu in pwd_user:
                if pu.get("id") == dp.user_id:
                    dp_user_name: str = pu.get("name")
            # 品物名と品物idの照会
            for il in item_list:
                if il.get("id") == dp.item_id:
                    dp_item_name: str = il.get("name")
            log_purchase.append(
                {
                    "id": dp.id,
                    "user_name": dp_user_name,
                    "item_name": dp_item_name,
                    "item_num": dp.item_num,
                }
            )

        # 給付履歴リストの作成
        log_income = []
        db_income = db.session.query(Income)
        for di in db_income:
            # ユーザー名とユーザーidの照会
            for pu in pwd_user:
                if pu.get("id") == di.user_id:
                    di_user_name: str = pu.get("name")
            log_income.append(
                {
                    "id": di.id,
                    "user_name": di_user_name,
                    "prize_name": di.prize_name,
                    "prize_money": di.prize_money,
                }
            )

        # 各班の残金リストの作成
        user_rest = []
        for pu in pwd_user:
            db_income = db.session.query(Income).filter_by(user_id=pu.get("id"))
            sc_income: int = sc_init
            for di in db_income:
                sc_income += di.prize_money
            db_purchase = db.session.query(Purchase).filter_by(user_id=pu.get("id"))
            sc_spend: int = 0
            for dp in db_purchase:
                for il in item_list:
                    if il.get("id") == dp.item_id:
                        sc_spend += il.get("price") * dp.item_num
            sc_rest: int = sc_income - sc_spend
            user_rest.append(
                {
                    "user_id": pu.get("id"),
                    "user_name": pu.get("name"),
                    "sc_rest": sc_rest,
                }
            )

        # admin.html を表示する
        return render_template(
            "admin.html",
            app_name=app_name,
            undlv_list=undlv_list,
            log_purchase=log_purchase,
            log_income=log_income,
            user_list=pwd_user,
            user_rest=user_rest,
        )

    # ユーザーのページ
    elif session.get("state_user"):
        # 給付履歴リスト・給付金合計値の作成
        db_income = db.session.query(Income).filter_by(user_id=session["user_id"])
        log_income = db_income
        sc_income: int = sc_init
        for di in db_income:
            sc_income += di.prize_money

        # 購入履歴リスト・支払金合計値の作成
        db_purchase = db.session.query(Purchase).filter_by(user_id=session["user_id"])
        log_purchase = []
        sc_spend: int = 0
        for dp in db_purchase:
            for il in item_list:
                if il.get("id") == dp.item_id:
                    log_purchase.append(
                        {
                            "name": il.get("name"),
                            "num": dp.item_num,
                            "prc": il.get("price"),
                            "spd": il.get("price") * dp.item_num,
                            "dlv": dp.item_dlv,
                        }
                    )
                    sc_spend += il.get("price") * dp.item_num

        # 残金算出
        sc_rest: int = sc_income - sc_spend

        # user.html を表示する
        return render_template(
            "user.html",
            app_name=app_name,
            item_list=item_list,
            sc_init=sc_init,
            sc_spend=sc_spend,
            sc_income=sc_income,
            sc_rest=sc_rest,
            log_purchase=log_purchase,
            log_income=log_income,
        )

    # 管理者・ユーザーでないときログインページへ飛ばす
    else:
        return render_template("login.html", app_name=app_name)


# 注文処理
@app.route("/order", methods=["POST"])
def order():
    # ユーザーか確認
    if session.get("state_user"):
        order_user_id: int = int(session["user_id"])
        order_item_id: int = int(request.form["item_id"])
        order_item_num: int = int(request.form["item_num"])

        # 購入数を確認して購入履歴データベースに追加する
        if 0 < order_item_num and order_item_num < 6:
            history = Purchase(order_user_id, order_item_id, order_item_num)
            db.session.add(history)
            db.session.commit()

    return redirect("/")


# 配達完了処理
@app.route("/dlv/<int:req_id>")
def dlv(req_id):
    # 管理者か確認
    if session.get("state_admin"):
        db_req = db.session.query(Purchase).filter_by(id=req_id).first()
        # 購入履歴データベースの配達状況値を書き換える
        if not db_req.item_dlv:
            db_req.item_dlv = True
            db.session.add(db_req)
            db.session.commit()

    return redirect("/")


# 給付処理
@app.route("/prize", methods=["POST"])
def prize():
    # 管理者か確認
    if session.get("state_admin"):
        user_id: int = int(request.form["user_id"])
        prize_name: str = str(request.form["prize_name"])
        prize_money: int = int(request.form["prize_money"])

        # 給付履歴データベースに追加
        log = Income(user_id, prize_name, prize_money)
        db.session.add(log)
        db.session.commit()

    return redirect("/")


# ログイン処理
@app.route("/login", methods=["POST"])
def login():
    # 管理者か確認しsession値を書き込む
    for pa in pwd_admin:
        if request.form["username"] == pa.get("name"):
            if request.form["password"] == pa.get("password"):
                session["state_admin"]: bool = True
                session["state_user"]: bool = False
                session["login_name"]: str = pa.get("name")
                return redirect("/")

    # ユーザーか確認しsession値を書き込む
    for pu in pwd_user:
        if request.form["username"] == pu.get("name"):
            if request.form["password"] == pu.get("password"):
                session["state_admin"]: bool = False
                session["state_user"]: bool = True
                session["user_id"]: int = pu.get("id")
                session["login_name"]: str = pu.get("name")
                return redirect("/")

    return render_template("login.html", mis_login=1)


# ログアウト処理
# 各session値を空にしてトップページへリダイレクト
@app.route("/logout")
def logout():
    session["state_admin"]: bool = False
    session["state_user"]: bool = False
    session["user_id"]: int = None
    session["login_name"]: str = None
    return redirect("/")


if __name__ == "__main__":
    app.secret_key = binascii.hexlify(os.urandom(32))
    app.run(debug=True)
