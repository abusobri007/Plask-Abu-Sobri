from flask import Flask, render_template , request,  redirect 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perserta.db'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Model
class Peserta(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nama = db.Column(db.String(50))
  alamat = db.Column(db.String(50))
  gender = db.Column(db.String(10))
  umur = db.Column(db.Integer())

  def __repr__(self):
    return self.nama
  

def welcom_To_Itec():
  return{
         "message" : "Welcom to itec mataram"       
  }


@app.route("/list_pendaftaran")
def semua_pendaftaran():
    list_peserta = Peserta.query.all()
    return render_template("list_pendaftaran.html",  tgl = "Tabel Peserta", lp=list_peserta)
     

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
       #menginsten objeck dan memberikan atribut

       p = Peserta(nama=f_nama, alamat=f_alamat,gender=f_gender, umur=f_umur)
       db.session.add(p)
       db.session.commit()
       return redirect('/list_pendaftaran')

@app.route("/list_pendaftaran/<id>/edit")
def edit_peserta(id):
    obj = Peserta.query.filter_by(id=id).first()
    return render_template("edit_peserta.html",obj=obj)

@app.route("/list_pendaftaran/<id>/update", methods=['POST'])
def update_peserta(id):
    obj = Peserta.query.filter_by(id=id).first()#data from db
 #data from cline server
    f_nama = request.form.get("nama")
    f_alamat = request.form.get("alamat")
    f_gender = request.form.get("gender")
    f_umur = request.form.get("umur")

    #data form db whiht data from cline server
    obj.nama=f_nama
    obj.alamat=f_alamat
    obj.gender=f_gender
    obj.umur=f_umur

    #save perubahan data ke db

    db.session.add(obj)
    db.session.commit()
    return redirect('/list_pendaftaran')




    
       
    
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
if "__main__" ==__name__:
     app.run(debug= True,port =2000)
