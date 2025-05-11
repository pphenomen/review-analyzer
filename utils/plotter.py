import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    @staticmethod
    def pie_sentiment_plot(sentiment_counts):
        """
        Круговая диаграмма распределения отзывов
        """
        filtered = {k: v for k, v in sentiment_counts.items() if v > 0}

        if not filtered:
            raise ValueError("Нет данных для построения диаграммы.")

        labels = list(filtered.keys())
        sizes = list(filtered.values())

        colors = ['#66b3b7', '#d3d3d3', '#ff6f61']
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.pie(sizes, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        fig.canvas.manager.set_window_title("Диаграмма")
        plt.title("Распределение тональностей отзывов", fontsize=20, weight='bold')
        ax.legend(labels=labels, loc="center right", fontsize=10, title="Тональность")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def histogram_rating_plot(reviews):
        """
        Гистограмма распределения оценок.
        reviews: список кортежей (текст, тональность, звезды)
        """
        if not reviews:
            raise ValueError("Нет данных для построения гистограммы оценок.")
        
        stars = [r[2] for r in reviews]
        counts = {}
        for star in stars:
            counts[star] = counts.get(star, 0) + 1
        
        # сортируем по звёздам
        stars_sorted = sorted(counts.keys())
        counts_sorted = [counts[s] for s in stars_sorted]

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(stars_sorted, counts_sorted, color='skyblue', edgecolor='black')
        ax.set_xlabel("Оценки (звёзды)", fontsize=12)
        ax.set_ylabel("Количество отзывов", fontsize=12)
        ax.set_title("Распределение оценок", fontsize=16, weight='bold')
        ax.set_xticks(stars_sorted)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        fig.canvas.manager.set_window_title("Гистограмма распределения оценок")
        
        # подписи над столбцами
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height, str(height), ha='center', va='bottom')

        plt.tight_layout()
        plt.show()