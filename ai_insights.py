def generate_insights(expenses):
    if not expenses:
        return ["No expenses to analyze."]

    insights = []

    # 1. Total spending
    total = sum(e.amount for e in expenses)

    # 2. Category-wise totals
    category_totals = {}
    for e in expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount

    # 3. Highest category
    top_category = max(category_totals, key=category_totals.get)
    percentage = (category_totals[top_category] / total) * 100

    insights.append(f"📊 You spent {percentage:.1f}% on {top_category}.")

    # 4. Average expense
    avg = total / len(expenses)
    insights.append(f"📉 Your average expense is ₹{avg:.2f}.")

    # 5. Total transactions
    insights.append(f"🔢 You made {len(expenses)} transactions.")

    # 6. Spending trend (simple)
    if len(expenses) >= 2:
        first_half = expenses[:len(expenses)//2]
        second_half = expenses[len(expenses)//2:]

        sum1 = sum(e.amount for e in first_half)
        sum2 = sum(e.amount for e in second_half)

        if sum1 > 0:
            change = ((sum2 - sum1) / sum1) * 100

            if change > 0:
                insights.append(f"📈 Your spending increased by {change:.1f}%.")
            else:
                insights.append(f"📉 Your spending decreased by {abs(change):.1f}%.")

    return insights