from flask import Flask, render_template , request,  redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perserta.db'
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + "\static\media/"
ALLOWED_EXTENSIONS = { 'pdf', 'png', 'jpg', 'jpeg'}

db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Model
class Peserta(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nama = db.Column(db.String(50))
  alamat = db.Column(db.String(50))
  gender = db.Column(db.String(10))
  umur = db.Column(db.Integer())
  photo = db.Column(db.String(100))
  
  

  def __repr__(self):
    return self.nama
  
def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/tambah_peserta/')
def semua_pendaftar():
    return  render_template("tambah_peserta.html")

@app.route("/tambah_peserta/save", methods=['POST'])
def save_peserta():
    if request.method == 'POST':
        #membuat objek peserta
       f_nama =request.form.get("nama")
       f_alamat =request.form.get("alamat")
       f_gender =request.form.get("gender")
       f_umur =request.form.get("umur")
       photo = request.files['Photo']
       print(photo.filename)

       if photo.filename== '':
           flash("Photo tidak boleh kosong")
       if photo and allowed_file(photo.filename):
          filename= secure_filename(photo.filename)

          #sytnyax unutuk upload image
          photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

          
        #menginsten objeck dan memberikan attribute

          f_photo = os.path.join('static\media', filename)
          p = Peserta(nama=f_nama, alamat=f_alamat,gender=f_gender, umur=f_umur, photo=f_photo)
       
          db.session.add(p)
          db.session.commit()
          return redirect('/list_pendaftaran')
    return redirect('/tambah_peserta')






    
       
    
@app.route("/list_pendaftaran/<id>/delete")
def delete_pendafar(id):
    obj = Peserta.query.filter_by(id=id).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect('/list_pendaftaran')




@app.route("/home/<nama>")
def home(nama):
    nama = (nama)
    return{ render_template("home.html", nama=nama)}

@app.route("/list_img")
def semuaphoto():
    return render_template("load_image.html")
if "__main__" ==__name__:
     app.run(debug= True,port =2000)
