import matplotlib.pyplot as plt

class Plotter:
    @staticmethod
    def plot_sentiment_distribution(positive_count, negative_count):
        if positive_count == 0 and negative_count == 0:
            raise ValueError("Нет данных для построения диаграммы.")
        labels = ['Положительные', 'Негативные']
        sizes = [positive_count, negative_count]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.pie(sizes, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        fig.canvas.manager.set_window_title("Диаграмма")
        plt.title("Статистика отзывов", fontsize=20, weight='bold')
        ax.legend(labels=labels, loc="center right", fontsize=10, title="Тональность")
        plt.tight_layout()
        plt.show()
