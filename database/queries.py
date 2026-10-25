from database.db import get_db
from datetime import datetime

def get_user_by_id(user_id):
    """
    Fetches a user's profile details by their ID.
    """
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if not row:
            return None

        # Format created_at (YYYY-MM-DD HH:MM:SS) to "Month YYYY"
        created_date = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
        member_since = created_date.strftime('%B %Y')

        return {
            "name": row['name'],
            "email": row['email'],
            "member_since": member_since,
            "initials": "".join([n[0].upper() for n in row['name'].split()])
        }
    finally:
        conn.close()

def get_recent_transactions(user_id, limit=10):

    """
    Fetches the most recent transactions for a given user.
    """
    conn = get_db()
    try:
        cursor = conn.execute(
            "SELECT date, description, category, amount FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        # Convert sqlite3.Row objects to dictionaries
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_summary_stats(user_id):
    """
    Fetches total spent, transaction count, and the top spending category for a user.
    """
    conn = get_db()
    try:
        # Total Spent
        res_total = conn.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,)).fetchone()
        total_spent = res_total[0] if res_total[0] is not None else 0.0

        # Transaction Count
        res_count = conn.execute("SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user_id,)).fetchone()
        count = res_count[0] if res_count[0] is not None else 0

        # Top Category
        res_cat = conn.execute(
            "SELECT category FROM expenses WHERE user_id = ? GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1",
            (user_id,)
        ).fetchone()
        top_category = res_cat[0] if res_cat and res_cat[0] else "—"

        return {
            "total_spent": total_spent,
            "count": count,
            "top_category": top_category
        }
    finally:
        conn.close()

def get_category_breakdown(user_id):
    """
    Calculates the spending breakdown by category for a given user.
    """
    conn = get_db()
    try:
        cursor = conn.execute(
            "SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category ORDER BY total DESC",
            (user_id,)
        )
        rows = cursor.fetchall()

        if not rows:
            return []

        # Calculate total spending
        total_spending = sum(row['total'] for row in rows)

        if total_spending == 0:
            return [{"name": row['category'], "amount": row['total'], "percent": 0} for row in rows]

        breakdown = []
        sum_percents = 0

        for i, row in enumerate(rows):
            # Round percentage to nearest integer
            percent = round((row['total'] / total_spending) * 100)
            breakdown.append({
                "name": row['category'],
                "amount": row['total'],
                "percent": percent
            })
            sum_percents += percent

        # Adjust the largest category to ensure sum is exactly 100%
        diff = 100 - sum_percents
        if diff != 0:
            breakdown[0]["percent"] += diff

        return breakdown
    finally:
        conn.close()
