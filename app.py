# İlk olarak Flask framework'ü ve gerekli modülleri içe aktaracağız.
# JSON dosyası ile çalışmak için json modülünü kullanacağız.
# Flask uygulamasını ve API endpoint'lerini oluşturacağız.

from flask import Flask, jsonify, request, render_template
import json
import os
from flask_cors import CORS
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')
# Flask uygulamasını başlatıyoruz
app = Flask(__name__)

CORS(app)
# JSON dosyasının yolunu belirliyoruz
DATA_FILE = os.path.join(app.static_folder, 'data.json')

# JSON dosyasından veri okuyan bir fonksiyon
def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)
    
read_data()

# JSON dosyasına veri yazan bir fonksiyon
def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Tüm kullanıcıları listeleme endpoint'i
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(read_data())

# Yeni bir kullanıcı ekleme endpoint'i
@app.route('/api/users', methods=['POST'])
def add_user():
    data = read_data()
    if data:
        # Mevcut en yüksek ID'yi bul ve 1 artırarak yeni kullanıcı için kullan
        new_id = max(item['id'] for item in data) + 1
        print (new_id)
    else:
        # Hiç kullanıcı yoksa, ID'yi 1 olarak ayarla
        new_id = 1
    new_user = request.json
    print (new_user)
    new_user['id'] = new_id
    print (new_user) # Yeni kullanıcının ID'sini ayarla
    data.append(new_user)
    write_data(data)
    return jsonify(new_user), 201


# Kullanıcı güncelleme endpoint'i
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = read_data()
    user = next((item for item in data if item['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_update = request.json
    for key, value in user_update.items():
        user[key] = value
    write_data(data)
    return jsonify(user)

# Kullanıcı silme endpoint'i
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    data = read_data()
    user = next((item for item in data if item['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data.remove(user)
    write_data(data)
    return jsonify({'success': True}), 204

# Frontend için ana sayfa route'u
@app.route('/')
def index():
    return render_template('index.html', users=read_data())


@app.route('/ikikereiki')
def naber():
    degisken= 2*2
    return str(degisken)


#data.json'daki verileri okuyup, cinsiyetlerine göre pie chart oluşturan ve onu html olarak döndüren route, numpy ve matplotlib kullanılarak
@app.route('/cinsiyet')
def cinsiyet():
    # remove existing png file if exists
    if os.path.exists('static/cinsiyet.png'):
        os.remove('static/cinsiyet.png')
    data = read_data()
    cinsiyetler = [0, 0]
    for user in data:
        if user['cinsiyet'] == "Erkek":
            cinsiyetler[0] += 1
        else:
            cinsiyetler[1] += 1
    labels = 'Erkek', 'Kadın'
    sizes = cinsiyetler
    colors = ['blue', 'green']
    explode = (0, 0.1)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('static/cinsiyet.png')
    return render_template('cinsiyet.html')

# Flask uygulamasını başlatma
if __name__ == '__main__':
    
    
    #app.run(debug=True)
    # set port 8080
    app.run(host='127.0.0.1', port=8080, debug=True)



# Bu kod parçası, Flask uygulamasının temel yapısını ve CRUD işlevlerini nasıl gerçekleştireceğimizi göstermektedir.
