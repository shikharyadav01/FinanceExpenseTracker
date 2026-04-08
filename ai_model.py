def predict_category(description: str) -> str:
    description = description.lower()

    rules = {
        "Food": ["pizza", "burger", "food", "restaurant", "coffee"],
        "Transport": ["uber", "bus", "train", "fuel", "ola"],
        "Utilities": ["electricity", "water", "internet", "bill"],
        "Rent": ["rent", "room", "flat"],
    }

    for category, keywords in rules.items():
        for word in keywords:
            if word in description:
                return category

    return "Others"