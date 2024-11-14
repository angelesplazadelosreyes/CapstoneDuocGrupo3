import joblib
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier

# Datos de ejemplo (puedes reemplazar esto con tu dataset real)
X = np.random.rand(100, 15)  # 100 ejemplos, 15 características
y = np.random.randint(2, size=100)  # Etiquetas binarias (0 o 1)

# Modelo
model = RandomForestClassifier()

# Validación cruzada
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf)
print("Accuracy promedio:", scores.mean())

# Entrenamiento final
model.fit(X, y)

# Guardar el modelo
joblib.dump(model, 'apps/core/trained_model.pkl')
print("Modelo guardado exitosamente en 'apps/core/trained_model.pkl'")
