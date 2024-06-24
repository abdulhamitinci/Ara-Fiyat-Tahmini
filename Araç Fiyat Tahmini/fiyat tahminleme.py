import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Excel dosyasını oku
df = pd.read_excel('output.xlsx')

# Eksik verileri doldur (varsa)
df.fillna(method='ffill', inplace=True)

# Bağımsız değişkenler (X) ve bağımlı değişken (y) olarak veriyi ayır
X = df[['Yıl', 'Kilometre']]  # Bağımsız değişkenler
y = df['Fiyat']  # Bağımlı değişken

# Veriyi eğitim ve test setlerine böle
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli oluştur
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Modeli eğit
model.fit(X_train, y_train)

# Model performansını değerlendir
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Tahmin yapmak için kullanıcıdan girdileri al
arac_yil = int(input("Araç Yılı: "))
arac_km = int(input("Araç Kilometresi: "))

# Kullanıcının girdilerini modele uygun formata getir
arac_verisi = [[arac_yil, arac_km]]

# Modeli kullanarak fiyat tahmini yap
tahmin_edilen_fiyat = model.predict(arac_verisi)
print("Tahmin Edilen Fiyat:", tahmin_edilen_fiyat[0])
