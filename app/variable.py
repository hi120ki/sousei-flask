# 変数値の設定ファイル

# アプリ名
app_name: str = "創成実験 2020"

# 創成コインの初期分配値
sc_init: int = 25000

# 管理者ユーザー
pwd_admin: list = [
    {"id": 0, "name": "admin0", "password": "vdceos"},
    {"id": 1, "name": "admin1", "password": "ajwoeq"},
    {"id": 2, "name": "admin2", "password": "lbsjcx"},
    {"id": 3, "name": "admin3", "password": "ileapl"},
]

# 一般ユーザー
pwd_user: list = [
    {"id": 0, "name": "team0", "password": "niwxwl"},
    {"id": 1, "name": "team9", "password": "xtdpip"},
    {"id": 2, "name": "team10", "password": "hovgul"},
    {"id": 3, "name": "team11", "password": "cwwnmm"},
    {"id": 4, "name": "team12", "password": "wlcunr"},
    {"id": 5, "name": "team14", "password": "xcizkb"},
    {"id": 6, "name": "team15", "password": "xxnojt"},
    {"id": 7, "name": "team16", "password": "nghoeh"},
]

# 品物リスト
item_list: list = [
    {"id": 0, "name": "ミニ四駆", "price": 4000, "description": "2期の走行テストで必要となります"},
    {"id": 1, "name": "風力モーターセット", "price": 3000, "description": "風力発電に必要なモーター・ギアのセット"},
    {"id": 2, "name": "コンデンサ", "price": 1000, "description": "複数用いて効率を調べる必要があります"},
    {"id": 3, "name": "太陽光パネル", "price": 3000, "description": "1期では1枚、2期では2枚まで使用できます"},
    {"id": 4, "name": "プリント基板", "price": 1000, "description": "ミニ四駆を走らせるときに使うことができます"},
    {"id": 5, "name": "アルミホイル", "price": 2000, "description": "市販のアルミホイル1本"},
    {"id": 6, "name": "リッツ線", "price": 1000, "description": "回路を組むための銅線1m"},
    {"id": 7, "name": "プロペラ", "price": 1000, "description": "風力発電に必要です。羽の形や枚数を工夫してください"},
    {"id": 8, "name": "単三電池", "price": 500, "description": "最終実験で使用できる単三電池です"},
    {"id": 9, "name": "単三電池ボックス", "price": 1000, "description": "最終実験で使用できる単三電池ボックスです"},
]
