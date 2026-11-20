import csv
import json
import time
import random
from datetime import datetime


def ask_ai_mock(review_text):
    time.sleep(random.uniform(0.1, 1.5))

    bad_words = ["ужас", "плохо", "разбит", "кошмар", "негатив"]
    if any(word in review_text.lower() for word in bad_words):
        return {"label": "NEGATIVE", "score": round(random.uniform(0.85, 0.999), 3)}
    else:
        return {"label": "POSITIVE", "score": round(random.uniform(0.7, 0.999), 3)}

def process_reviews():
    try:
        with open("reviews.csv", "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        with open("reviews.csv", "w", encoding="utf-8") as f:
            f.write("review\n")
            f.write("Отличный товар, все супер!\n")
            f.write("Ужасный сервис, никогда больше\n")
            f.write("Нормально, но доставка долгая.\n")
            f.write("Куртка пришла с браком, ужас.\n")
            f.write("Спасибо, все понравилось.\n")
    
    reviews_data = []
    with open("reviews.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reviews_data = list(reader)

    all_results = []

    print(f"Начинаем обработку {len(reviews_data)} отзывов...\n")
    
    for item in reviews_data:
        review_text = item.get("review", "").strip()
        if not review_text:
            continue

        start_time = time.time()
        ai_result = ask_ai_mock(review_text)
        end_time = time.time()

        final_time = end_time - start_time

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "review": review_text,
            "sentiment": ai_result["label"],
            "score": ai_result["score"],
            "final_sec": round(final_time, 4)
        }
        all_results.append(log_entry)

        print(f"Обработан отзыв: '{review_text[:30]}...' -> {log_entry['sentiment']} ({log_entry['final_sec']} сек)")
    
    with open("support_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print("\nЛоги сохранены в support_results.json")

    print("\n" + "="*40)
    print("Статистика работы поддержки")

    total_processed = len(all_results)
    if total_processed == 0:
        print("Нет данных для анализа.")
        return
    
    print(f"Обработано: {total_processed} отзывов")

    negatives = [r for r in all_results if r["sentiment"] == "NEGATIVE"]
    neg_count = len(negatives)
    neg_percent = (neg_count / total_processed) * 100
    print(f"Негативных: {neg_count} ({neg_percent:.0f}%)")

    avg_time = sum(r["final_sec"] for r in all_results) / total_processed
    print(f"Среднее время: {avg_time:.2f} сек")

    if negatives:
        worst_review = min(negatives, key=lambda x: x["score"])
        print(f"Самый негативный: '{worst_review['review']}' ({worst_review['sentiment']}, {worst_review['score']})")
    else:
        print("Самый негативный: Нет негативных отзывов.")

if __name__ == "__main__":
    process_reviews()