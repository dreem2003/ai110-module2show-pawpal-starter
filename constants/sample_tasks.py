from models.priority import Priority

# Each entry is a dict ready to pass as kwargs to Task(...)
SAMPLE_TASKS: list[dict] = [
    {
        "title": "Morning walk",
        "duration_minutes": 30,
        "priority": Priority.HIGH,
        "category": "exercise",
    },
    {
        "title": "Breakfast feeding",
        "duration_minutes": 10,
        "priority": Priority.HIGH,
        "category": "feeding",
    },
    {
        "title": "Evening walk",
        "duration_minutes": 30,
        "priority": Priority.HIGH,
        "category": "exercise",
    },
    {
        "title": "Dinner feeding",
        "duration_minutes": 10,
        "priority": Priority.HIGH,
        "category": "feeding",
    },
    {
        "title": "Brushing / grooming",
        "duration_minutes": 15,
        "priority": Priority.MEDIUM,
        "category": "grooming",
    },
    {
        "title": "Playtime",
        "duration_minutes": 20,
        "priority": Priority.MEDIUM,
        "category": "enrichment",
    },
    {
        "title": "Training session",
        "duration_minutes": 15,
        "priority": Priority.MEDIUM,
        "category": "training",
    },
    {
        "title": "Vet medication",
        "duration_minutes": 5,
        "priority": Priority.HIGH,
        "category": "health",
    },
    {
        "title": "Litter box / cleanup",
        "duration_minutes": 10,
        "priority": Priority.LOW,
        "category": "hygiene",
    },
    {
        "title": "Socialisation / cuddle time",
        "duration_minutes": 20,
        "priority": Priority.LOW,
        "category": "enrichment",
    },
]
