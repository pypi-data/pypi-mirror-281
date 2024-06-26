import os
import cv2
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import save_model


# Function to load and preprocess images
def load_images(main_folder):
    data = []
    labels = []

    for folder_name in os.listdir(main_folder):
        label = folder_name  # Use folder name as label
        for filename in os.listdir(os.path.join(main_folder, folder_name)):
            img = cv2.imread(os.path.join(main_folder, folder_name, filename))
            img = cv2.resize(img, (128, 128))  # Resize to a fixed size
            img = img / 255.0  # Normalize pixel values
            data.append(img)
            labels.append(label)

    return np.array(data), np.array(labels)


def cnn_model_training():
    main_folder = 'training_data'
    try:
        train_data, train_labels = load_images(main_folder)
    except Exception as e:
        print(f"Error loading images: {e}")
        exit()

    print(train_labels)
    print(train_data)

    # Label Encoding
    try:
        label_encoder = LabelEncoder()
        train_labels_encoded = label_encoder.fit_transform(train_labels)
        joblib.dump(label_encoder, "label_encoder_biller_backup.pkl")
    except Exception as e:
        print(f"Error encoding labels: {e}")
        exit()

    # Split data into training and validation sets
    try:
        train_data, val_data, train_labels_encoded, val_labels_encoded = train_test_split(train_data,
                                                                                          train_labels_encoded,
                                                                                          test_size=0.2,
                                                                                          random_state=42)
    except Exception as e:
        print(f"Error splitting data: {e}")
        exit()

    # Define CNN model
    model = models.Sequential([
        layers.Conv2D(128, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(len(set(train_labels_encoded)))  # Number of unique encoded labels
    ])

    # Compile the model
    try:
        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
    except Exception as e:
        print(f"Error compiling model: {e}")
        exit()

    # Train the model
    try:
        model.fit(train_data, train_labels_encoded, epochs=10, validation_data=(val_data, val_labels_encoded))
    except Exception as e:
        print(f"Error training model: {e}")
        exit()

    try:
        save_model(model, 'login_page_model_backup.h5')
    except Exception as e:
        print(f"Error saving model: {e}")
        exit()
