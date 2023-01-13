from flask import Flask
list_pendaftar = []
app = Flask(__name__)

@app.route("/")
def welcom_To_Itec():
  return{
         "message" : "Welcom to itec mataram"       
  }


@app.route("/pendaftaran")
def semua_pendaftaran():
     return {
      "pendaftaran :" : list_pendaftar
     }

@app.route('/tambah_peserta/<nama>')
def tambah_peserta(nama):
    list_pendaftar.append(nama)
    return{
      "mesaage": f"list pendaftaran berhasil di update: {list_pendaftar}"
    }
app.route("/delete/<nama>")
def delete_peserta(nama):
                
   list_pendaftar.remove(nama)
   return{
      "mesaage" : f"peserta berhasil di hapus : {nama}"
   }
if "__main__" ==__name__:
     app.run(debug= True,port =2000)
