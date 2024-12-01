import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split

def load_dataset_from_xlsx(folder_path):
    texts, sentiments = [], []

    for file_name in os.listdir(folder_path):
        if not file_name.endswith('.xlsx'):
            continue

        file_path = os.path.join(folder_path, file_name)
        try:
            df = pd.read_excel(file_path)
            
            df = df.dropna(subset=["Описание"])

            for _, row in df.iterrows():
                text = row["Описание"]
                stars = row["Звезды"]

                if stars <= 3:
                    label = 0
                else:
                    label = 1
                
                texts.append(text.strip())
                sentiments.append(label)

        except Exception as e:
            print(f"Ошибка при обработке файла {file_name}: {e}")

    print(f"Загружено {len(texts)} отзывов.")
    return texts, np.array(sentiments)

def preprocess_texts(texts, max_words=20000, max_len=200):
    tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)

    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=max_len)

    with open("../model/tokenizer.json", "w", encoding="utf-8") as f:
        f.write(tokenizer.to_json())

    return padded_sequences, tokenizer

def create_model(max_words=20000, max_len=200, embedding_dim=256):
    model = Sequential([
        Embedding(max_words, embedding_dim, input_length=max_len),
        LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.3),
        LSTM(64, dropout=0.3, recurrent_dropout=0.3),
        Dense(64, activation="relu"),
        Dropout(0.5),
        Dense(2, activation="softmax")
    ])

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model

def plot_training_history(history):
    plt.figure(figsize=(12, 6))

    # График потерь
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Обучающая выборка')
    plt.plot(history.history['val_loss'], label='Валидационная выборка')
    plt.title('Потери во время обучения')
    plt.xlabel('Эпохи')
    plt.ylabel('Потери')
    plt.legend()

    # График точности
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Обучающая выборка')
    plt.plot(history.history['val_accuracy'], label='Валидационная выборка')
    plt.title('Точность во время обучения')
    plt.xlabel('Эпохи')
    plt.ylabel('Точность')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    data_folder = "../dataset/wb_shirts_dataset"
    max_words = 20000
    max_len = 200
    embedding_dim = 256

    print("Загружаем датасет...")
    texts, sentiments = load_dataset_from_xlsx(data_folder)

    if len(texts) == 0:
        print("Ошибка: нет данных для обучения.")
        return

    print("Токенизируем текст...")
    padded_sequences, tokenizer = preprocess_texts(texts, max_words, max_len)

    X_train, X_val, y_train, y_val = train_test_split(padded_sequences, sentiments, test_size=0.2, random_state=42)

    print("Создаём модель...")
    model = create_model(max_words, max_len, embedding_dim)

    print("Обучаем модель...")
    history = model.fit(X_train, y_train, epochs=15, batch_size=256, validation_data=(X_val, y_val))

    model.save("../model/sentiment_model.h5")

    print("Обучение завершено и модель сохранена.")

    plot_training_history(history)

if __name__ == "__main__":
    main()
