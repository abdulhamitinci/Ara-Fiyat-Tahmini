import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Excel dosyasını oku
df = pd.read_excel('output.xlsx')

# Verileri hazırla
X = df[['Yıl', 'Kilometre']]  # Bağımsız değişkenler
y = df['Fiyat']  # Bağımlı değişken

# Verileri eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli oluştur ve eğit
model = LinearRegression()
model.fit(X_train, y_train)

# Modeli değerlendir
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Ortalama Kare Hata (MSE):", mse)
print("R-kare (R2):", r2)
