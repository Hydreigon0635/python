import sqlite3

dbname = ('main.db') #データベース名を指定。拡張子は.db
conn = sqlite3.connect(dbname, isolation_level = None) #データベースを作成 isolation_level ： 自動コミット機能オン

cursor = conn.cursor() #カーソルオブジェクト作成

"""
・create table テーブル名（作成したいデータカラム）というSQL文でテーブルを宣言
※SQL命令は大文字でも小文字でもいい
・今回はtestテーブルに「id,name,date」カラム(列名称)を定義する※今回dateは生年月日という列
・「if not exists」はエラー防止の部分。すでに同じテーブルが作成されてるとエラーになる為
・カラム型は指定しなくても特には問題ない
※NULL, INTEGER(整数), REAL(浮動小数点), TEXT(文字列), BLOB(バイナリ)の5種類
"""

sql = """CREATE TABLE IF NOT EXISTS test(id, name, date)"""

cursor.execute(sql) #executeコマンドでSQL文を実行
conn.commit() #データベースにコミット（Excelでいう上書き保存。自動コミット設定なので本来は必要ない）

#データベース中のテーブル名を取得するSQL関数
sql = """SELECT NAME FROM SQLITE_MASTER WHERE TYPE = 'table'"""

for t in cursor.execute(sql): #for文で作成した全テーブルを確認していく
    print(t)


"""
レコードを追加する場合はinsert文を使う。
SQLインジェクションという不正SQL命令への脆弱性対策でpythonの場合は「？」を使用して記載するのが基本。
"""

sql = """INSERT INTO test VALUES(?, ?, ?)""" #?は後で値を受け取るよという意味

data = ((1, 'Shunri', 20040426)) #挿入するレコードを指定
cursor.execute(sql, data) #executeコマンドでSQL文を実行。複数同時に格納したい場合は"executemany"を使用する
conn.commit() #コミットする

"""
select 
* ですべてのデータを参照し、fromでどのテーブルからデータを呼ぶのか指定fetchallですべての行のデータを取り出す
fetchoneを使うと、テーブル内の全レコードを一行ずつ取り出す
"""
sql = """SELECT * FROM test"""
cursor.execute(sql)
print(cursor.fetchall()) #全レコード取り出し

"""
whereのあとに消したいデータの条件を書いて指定
このテーブルの1行目の要素はidなので例としてidが2のデータを指定
"""

cursor.execute('DELETE FROM test WHERE id = ?', (2, ))
conn.commit() #コミットする

"""
ALTER TABLE 変更前のテーブル名 RENAME TO 変更後のテーブル名
"""

sql = """ALTER TABLE test RENAME TO test1"""

conn.execute(sql)
conn.commit()

"""
DROP TABLE if exists 削除テーブル名
"""

sql = """DROP TABLE IF EXISTS test1"""

#作業完了したらDB接続を閉じる
conn.close()