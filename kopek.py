from flask import Flask, request
from werkzeug.utils import secure_filename as sf
import os
import datetime
import shutil

app = Flask(__name__)

kontrolForm = """
<form action="kontrolEt" method="post">
Kimlik no: <input type="text" name="kimlik" size="6"><br><br>
Köpek Adı:<input type="text" name="dogsname"><br><br>
<input type="submit" value="Kontrol Et">
</form>
<br>
"""

kontrolOnayla = """
<center>
<br>
<form action="kontrolOK" method="post">
<input type="hidden" name="kimne" value="vvkimnevv">
<input style="padding: 1%; font-size: 300%;" type="submit" value="Onayla">
</form>
</center>
"""

kayitForm = """
<style>
td{
    padding: 4%;
}
table{
}
</style>
<form action="kaydet" method="post">
<table>
<tr><td>Kimlik no:</td><td><input type="text" name="kimlik" size="6"></td></tr>
<tr><td>İsim Soyisim:</td><td><input type="text" name="namesurname"></td></tr>
<tr><td>Telefon:</td><td><input type="tel" name="tel"></td></tr>
<tr><td>Köpek Adı:</td><td><input type="text" name="dogsname"></td></tr>
<tr><td>Köpek Yaşı:</td><td><input type="text" name="dogsage" size="2"></td></tr>
<tr><td>Köpek Fotoğrafı:</td><td><input type="file" name="photo"></td></tr>
<tr><td>Kontrol Tarihi:</td><td><input type="date" name="controldate"></td></tr>
<tr><td><input type="submit" value="Kaydet"></td></tr>
</table>
</form>
"""

kopekSilFormu = """
<form action="sil" method="post">
Kimlik no: <input type="text" name="kimlik" size="6"><br><br>
Köpek Adı:<input type="text" name="dogsname"><br><br>
<input type="submit" value="Kaydı Sil">
</form>
"""

girisHTML = """
<style>
.buton{
padding: 2%;
font-size: 300%;
background: #ecd91d;
border-radius: 50% 50%;
display: block;
width: 20%;
}
a{
    text-decoration: none;
    color: white;
}
</style>
<center>
<a href="/kontrol" class="buton">Kontrol</a><br>
<a href="/kayit" class="buton">Yeni Kayıt</a><br>
<a href="/kopekSil" class="buton">Kayıt Sil :(</a><br>
<a href="/kayitlar" class="buton">Kayıtlı Canlar</a><br>
</center>
"""

tableStyle = """
<style>
td{
padding: 1%;
}
table{
    width: 100%;
}
th, td{
    border-bottom: 1px solid;
    text-align: center;
}
tr:hover {background-color: #f5e548;} 
tr:nth-child(even) {background-color: #fff699;}  
</style>
"""

scrpt = """
<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("liste");
  switching = true;
  dir = "asc";
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>
"""

def rowData(gelenData):
    return "<td>" + str(gelenData) + "</td>"


@app.route('/')
def anasayfa():
    return girisHTML


@app.route('/kontrol', methods=['POST', 'GET'])
def kontrol():
  return kontrolForm

@app.route('/kontrolEt', methods=['POST', 'GET'])
def kontrolEt():
  try:
    securename = sf(request.form.get('kimlik') + str(request.form.get('dogsname'))).lower()
    kayitOku = open(securename + '/doginfo.txt', 'r')
    kb = dict(eval(kayitOku.read()))
    kayitOku.close()
    kayitHead = """<table id="liste"><tr><th>Kimlik</th><th>İsim Soyisim</th><th>Telefon Numarası</th><th>Köpek Adı</th><th>Köpek Yaşı</th><th>Son Kontrol Tarihi</th></tr>"""
    kayit = kayitHead + '<tr>' + rowData(kb.get('kimlik')) + rowData(kb.get('namesurname')) + rowData(kb.get('tel')) +rowData(kb.get('dogsname')) + rowData(kb.get('dogsage')) + rowData(kb.get('controldate')) + '</tr>'
    kopekFoto = """<br><center><img src="{}"></img></center>""".format("https://www.syfy.com/sites/syfy/files/styles/1200x680_hero/public/2017/10/duckhuntdog.jpg")
    return tableStyle + scrpt +  kayit + '</table>' + kopekFoto + kontrolOnayla.replace("vvkimnevv", securename)
  except:
    return "Kayıt Bulunamadı"

@app.route('/kontrolOK', methods=['POST', 'GET'])
def kontrolOK():
  dir = request.form.get('kimne')
  kayitOku = open(dir + '/doginfo.txt', 'r')
  kb = dict(eval(kayitOku.read()))
  kayitOku.close()
  kb['controldate'] = datetime.date.today()
  kayitGuncelle = open(dir + "/doginfo.txt", 'w')
  kayitGuncelle.write(str(kb))
  kayitGuncelle.close()
  return "bak bakayım"  


@app.route('/kaydet', methods=['POST', 'GET'])
def kaydet():
    try:
        if str(request.form.get('kimlik')).isnumeric:
            securename = sf(request.form.get('kimlik') + str(request.form.get('dogsname')) )
            os.mkdir(securename.lower())
            newDog = open(securename.lower() + "/doginfo.txt", 'w')
            newDog.write(str(request.form.to_dict()))
            newDog.close()
            return "<strong>{}</strong> adlı köpek, <strong>{}</strong> kimlik kartı numaralı <strong>{}</strong> üzerine kaydedildi.".format(request.form.get('dogsname'), request.form.get('kimlik'), request.form.get('namesurname'))
        else:
            return "Kimlik numarası rakamlardan oluşmalıdır."        
    except:
        return "Köpek kayıtlı"


@app.route('/kopekSil')
def kopekSilForm():
    return kopekSilFormu

@app.route('/sil', methods = ['POST'])
def sil():
    try:
        securename = sf(request.form.get('kimlik') + str(request.form.get('dogsname')) )
        shutil.rmtree(securename.lower())
        return "<strong>{}</strong> kimlik numaralı vatandaşa ait <strong>{}</strong> isimli köpeğin kaydı silindi.".format(request.form.get('kimlik'), request.form.get('dogsname'))
    except:
        return "Kayıt bulunamadı"


@app.route('/kayit')
def kayitSayfasi():
    return kayitForm







@app.route("/kayitlar")
def kayitliKopekler():
    kayit = """<table id="liste"><tr><th onclick="sortTable(0)">Kimlik</th><th onclick="sortTable(1)">İsim Soyisim</th><th onclick="sortTable(2)">Telefon Numarası</th><th onclick="sortTable(3)">Köpek Adı</th><th onclick="sortTable(4)">Köpek Yaşı</th><th onclick="sortTable(5)">Son Kontrol Tarihi</th></tr>"""
    for pat in os.listdir(os.path.curdir):
        if pat[0].isnumeric():
            kayitOku = open(pat + '/doginfo.txt', 'r')
            kb = dict(eval(kayitOku.read()))
            kayitOku.close()
            kayit = kayit + '<tr>' + rowData(kb.get('kimlik')) + rowData(kb.get('namesurname')) + rowData(kb.get('tel')) +rowData(kb.get('dogsname')) + rowData(kb.get('dogsage')) + rowData(kb.get('controldate')) + '</tr>'
    return tableStyle + scrpt +  kayit + '</table>'






if __name__ == '__main__':
    app.run()
