"""
Este script entrena un modelo de Red Neuronal Convolucional (CNN) para la clasificación de imágenes de animales.
Utiliza data augmentation simple (reflejo horizontal, escala de grises) para expandir el dataset.
El modelo entrenado y los nombres de las clases se guardan al finalizar el entrenamiento.

Versiones anteriores con modelos SVM se han eliminado para mayor claridad.
"""
import os
import json
import numpy as np
from PIL import Image, ImageOps
from sklearn.model_selection import train_test_split
import tensorflow as tf

from keras import layers, models

# Funcion para cargar y generar variaciones de imágenes
# --- Constantes de Configuración ---
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_SCRIPT_DIR, "data")
IMAGE_SIZE = (128, 128)
MAX_IMAGES_PER_CLASS = 400
TEST_SPLIT_SIZE = 0.2
VALIDATION_SPLIT_SIZE = 0.2
RANDOM_STATE = 42
EPOCHS = 15
BATCH_SIZE = 32
MODEL_FILENAME = os.path.join(_SCRIPT_DIR, "modelo_cnn_entrenado.h5")
CLASS_NAMES_FILENAME = os.path.join(_SCRIPT_DIR, "class_names.json")

# --- Funciones Auxiliares ---
def load_images_with_augmentation(data_dir, size, max_images_per_class):
    """
    Carga imágenes desde directorios, aplica data augmentation y las prepara para el modelo.

    Args:
        data_dir (str): Ruta al directorio principal que contiene las subcarpetas de clases.
        size (tuple): Tupla (ancho, alto) para redimensionar las imágenes.
        max_images_per_class (int): Número máximo de imágenes originales a cargar por clase.

    Returns:
        tuple: Una tupla conteniendo (array de imágenes, array de etiquetas, lista de nombres de clases).
    """
    images = []
    labels = []
    class_names = []

    for label, class_name in enumerate(os.listdir(data_dir)):
        class_folder = os.path.join(data_dir, class_name)
        if os.path.isdir(class_folder):
            class_names.append(class_name)
            image_count = 0
            for img_file in os.listdir(class_folder):
                if image_count >= MAX_IMAGES_PER_CLASS:
                    break
                img_path = os.path.join(class_folder, img_file)
                try:
                    # Cargar y redimensionar imagen
                    img = Image.open(img_path).convert("RGB").resize(size)

                    # Imagen original
                    images.append(np.array(img))
                    labels.append(label)

                    # Reflejo horizontal
                    reflected_img = ImageOps.mirror(img)
                    images.append(np.array(reflected_img))
                    labels.append(label)

                    # Escala de grises
                    grayscale_img = img.convert("L").convert("RGB")
                    images.append(np.array(grayscale_img))
                    labels.append(label)

                    image_count += 1
                except Exception as e:
                    print(f"Error al procesar la imagen {img_path}: {e}")
    return np.array(images), np.array(labels), class_names

def build_cnn_model(input_shape, num_classes):
    """
    Construye y compila el modelo de Red Neuronal Convolucional (CNN).

    Args:
        input_shape (tuple): La forma de las imágenes de entrada (alto, ancho, canales).
        num_classes (int): El número de clases de salida.


    Returns:
        tensorflow.keras.Model: El modelo CNN compilado.
    """
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
    return model

def main():
    """Función principal para cargar datos, entrenar y evaluar el modelo."""
    # 1. Cargar y preprocesar datos
    print("Cargando y aumentando imágenes...")
    X, y, class_names = load_images_with_augmentation(DATA_DIR, IMAGE_SIZE, MAX_IMAGES_PER_CLASS)
    X = X / 255.0  # Normalización
    y = tf.keras.utils.to_categorical(y, num_classes=len(class_names))  # One-hot encoding

    print(f"Forma de X: {X.shape}, Forma de y: {y.shape}")
    print(f"Clases encontradas ({len(class_names)}): {class_names}")

    # 2. Dividir el dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SPLIT_SIZE, random_state=RANDOM_STATE
    )

    # 3. Construir y entrenar el modelo
    print("\nConstruyendo el modelo CNN...")
    model = build_cnn_model(input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3), num_classes=len(class_names))
    model.summary()

    print("\nIniciando entrenamiento...")
    history = model.fit(
        X_train, y_train,
        validation_split=VALIDATION_SPLIT_SIZE,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE
    )

    # 4. Evaluación
    print("\nEvaluando el modelo con el conjunto de prueba...")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
    print(f"Precisión en el conjunto de prueba (Test Accuracy): {test_acc:.4f}")

    # 5. Guardar el modelo y los nombres de las clases
    model.save(MODEL_FILENAME)
    print(f"Modelo CNN guardado en: {MODEL_FILENAME}")

    with open(CLASS_NAMES_FILENAME, 'w') as f:
        json.dump(class_names, f)
    print(f"Nombres de las clases guardados en: {CLASS_NAMES_FILENAME}")

if __name__ == "__main__":
    main()
