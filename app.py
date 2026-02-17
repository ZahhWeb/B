from flask import Flask, request,jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS images_backgrout_hero (filename TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS images_hero_logo (filename TEXT)")
conn.commit()
conn.close()
def init_db_hero():
  conn = sqlite3.connect("data_text_logo_hero.db")
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS text_hero_logo(
  id INTEGER PRIMARY KEY,
  content_logo_hero TEXT NOT NULL
  )
  """)
  conn.commit()
  conn.close()
init_db_hero()
@app.route("/upload_hero", methods=["POST"])
def upload():
    file = request.files["image"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT filename FROM images_backgrout_hero LIMIT 1")
    old = c.fetchone()
    if old:
        old_path = os.path.join(UPLOAD_FOLDER, old[0])
        if os.path.exists(old_path):
            os.remove(old_path)
        c.execute("DELETE FROM images_backgrout_hero")

    filename = "image.jpg"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    c.execute("INSERT INTO images_backgrout_hero VALUES (?)", (filename,))
    conn.commit()
    conn.close()

    return "Gambar diganti"

@app.route("/hero_image", methods=["GET"])
def hero_image():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT filename FROM images_backgrout_hero LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return send_from_directory(UPLOAD_FOLDER, row[0])
    return "Tidak ada gambar", 404

@app.route("/upload_hero_logo", methods=["POST"])
def upload_hero_logo():
    file = request.files["image"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT filename FROM images_hero_logo LIMIT 1")
    old = c.fetchone()
    if old:
        old_path = os.path.join(UPLOAD_FOLDER, old[0])
        if os.path.exists(old_path):
            os.remove(old_path)
        c.execute("DELETE FROM images_hero_logo")

    filename = "logo.jpg"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    c.execute("INSERT INTO images_hero_logo VALUES (?)", (filename,))
    conn.commit()
    conn.close()

    return "Logo diganti"

@app.route("/hero_image_logo", methods=["GET"])
def hero_image_logo():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT filename FROM images_hero_logo LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return send_from_directory(UPLOAD_FOLDER, row[0])
    return "Tidak ada logo", 404


@app.route("/save_text_logo_hero", methods=["POST"])
def save_text_logo_hero():
  data = request.json
  text_logo_hero1 = data.get("text","")
  if not text_logo_hero1:
    return jsonify({"error": "Text kosong"}), 400
  conn = sqlite3.connect("data_text_logo_hero.db")
  cursor = conn.cursor()
  
  cursor.execute("DELETE FROM text_hero_logo")
  
  cursor.execute("INSERT INTO text_hero_logo (id, content_logo_hero) VALUES (1, ?)", (text_logo_hero1,))
  conn.commit()
  conn.close()
  
  return jsonify({"message": "Text Berhasil di simpan?"})


@app.route("/kirim_text_logo_hero", methods=["GET"])
def kirim_text_logo_hero():
  conn = sqlite3.connect("data_text_logo_hero.db")
  cursor = conn.cursor()
  cursor.execute("SELECT content_logo_hero FROM text_hero_logo WHERE id=1")
  row = cursor.fetchone()
  conn.close()
  
  if row:
    return jsonify({"text": row[0]})
  else:
    return jsonify({"text": ""})
    
if __name__ == "__main__":
    app.run(debug=True)