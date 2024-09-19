import json
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

# Чтение данных из файла
with open('qust_expanded.txt', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Преобразование данных в DataFrame
df = pd.DataFrame(data)

# Подготовка данных: извлекаем ответы
answers = df['answer'].tolist()

# Инициализация модели SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Загрузка эмбеддингов вопросов из файла
question_embeddings = torch.load('question_embeddings.pt')

# Функция для поиска ответа с использованием порога схожести
def find_best_answer(question, model, question_embeddings, answers, threshold=0.7):
    question_embedding = model.encode(question, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(question_embedding, question_embeddings)[0]
    most_similar_index = similarities.argmax().item()
    similarity_score = similarities[most_similar_index].item()

    if similarity_score < threshold:
        return "Вопрос не найден, попробуйте переформулировать."
    return answers[most_similar_index], similarity_score

# Пример использования
new_question = "3 форма cut" 
answer, score = find_best_answer(new_question, model, question_embeddings, answers)

print(f"Ответ: {answer}")
print(f"Схожесть: {score}")