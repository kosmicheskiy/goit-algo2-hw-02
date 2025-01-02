from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Перетворення вхідних даних у об'єкти PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]
    max_volume, max_items = constraints["max_volume"], constraints["max_items"]

    # Сортування за пріоритетом і часом друку
    jobs.sort(key=lambda job: (job.priority, job.print_time))

    print_order, total_time = [], 0

    while jobs:
        current_volume, current_batch, current_time = 0, [], 0

        for job in jobs[:]:
            if current_volume + job.volume <= max_volume and len(current_batch) < max_items:
                current_batch.append(job.id)
                current_volume += job.volume
                current_time = max(current_time, job.print_time)

        jobs = [job for job in jobs if job.id not in current_batch]
        print_order.extend(current_batch)
        total_time += current_time

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    for i, (test_jobs, desc) in enumerate([
        (test1_jobs, "однаковий пріоритет"),
        (test2_jobs, "різні пріоритети"),
        (test3_jobs, "перевищення обмежень")
    ], 1):
        print(f"Тест {i} ({desc}):")
        result = optimize_printing(test_jobs, constraints)
        print(f"Порядок друку: {result['print_order']}")
        print(f"Загальний час: {result['total_time']} хвилин\n")

if __name__ == "__main__":
    test_printing_optimization()
