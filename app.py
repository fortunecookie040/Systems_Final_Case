from flask import Flask, request, send_file, render_template, abort
import io
from datetime import date, timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__, template_folder="template")

# In-memory store: YYYY-MM-DD -> spending value
SPENDING_DATA = {}  # e.g. {"2025-11-29": 35.0}


@app.route("/")
def home():
    # Renders template/index.html
    return render_template("index.html")


@app.route("/budget_plot")
def budget_plot():
    """
    Monthly budget model.

    Query params:
      - budget: total budget for the month (e.g. 1000)
      - spending: amount spent on this one date
      - date: YYYY-MM-DD (the date this spending applies to)
      - view: "week" or "month" (default "month")

    Behavior:
      - Store/overwrite spending for that specific date in SPENDING_DATA.
      - Build a daily time series for either:
          * the week containing that date (view=week), OR
          * the whole month of that date (view=month / default).
      - For each day:
          * daily_spend = SPENDING_DATA.get(day, 0)
          * cumulative_spend = sum of all previous daily_spend from month start
          * remaining = max(0, budget - cumulative_spend)
      - Plot:
          * line for remaining budget
          * line for daily spending
    """
    # --- read query params ---
    budget_param = request.args.get("budget", type=float)
    spending_param = request.args.get("spending", type=float)
    date_str = request.args.get("date", type=str)
    view = request.args.get("view", default="month")  # "week" or "month"

    if budget_param is None:
        abort(400, description="Please provide 'budget', e.g. ?budget=1000")
    if spending_param is None:
        abort(400, description="Please provide 'spending', e.g. ?spending=50")
    if date_str is None:
        abort(400, description="Please provide 'date', e.g. ?date=2025-11-29")

    monthly_budget = float(budget_param)
    spending = float(spending_param)

    # --- parse focus date ---
    try:
        focus_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        abort(400, description="Invalid 'date'. Use YYYY-MM-DD, e.g. 2025-11-29")

    # --- store/update this date's spending ---
    iso_key = focus_date.isoformat()
    SPENDING_DATA[iso_key] = spending

    # --- determine month start (for cumulative) ---
    month_start = focus_date.replace(day=1)

    # --- choose display range (week vs month) ---
    if view == "week":
        # Monday–Sunday of that week
        start = focus_date - timedelta(days=focus_date.weekday())
        end = start + timedelta(days=6)
        title_range = f"Week of {start.isoformat()} – {end.isoformat()}"
    else:
        # whole month of focus_date
        start = month_start
        if start.month == 12:
            first_next = start.replace(year=start.year + 1, month=1)
        else:
            first_next = start.replace(month=start.month + 1)
        end = first_next - timedelta(days=1)
        title_range = f"Month of {start.strftime('%Y-%m')}"

    # --- build daily time series ---
    # We need cumulative spend from the *month start* for remaining.
    all_dates_for_cumulative = pd.date_range(start=month_start, end=end, freq="D")

    cumulative_spend_by_day = {}
    running_total = 0.0

    for d in all_dates_for_cumulative:
        iso = d.date().isoformat()
        daily_spend = float(SPENDING_DATA.get(iso, 0.0))
        running_total += daily_spend
        cumulative_spend_by_day[iso] = running_total

    # Now build records only for the display range
    display_dates = pd.date_range(start=start, end=end, freq="D")
    records = []
    max_daily_spend = 0.0
    max_remaining = 0.0

    for d in display_dates:
        iso = d.date().isoformat()
        daily_spend = float(SPENDING_DATA.get(iso, 0.0))
        cum_spend = cumulative_spend_by_day.get(iso, 0.0)
        remaining = max(0.0, monthly_budget - cum_spend)

        max_daily_spend = max(max_daily_spend, daily_spend)
        max_remaining = max(max_remaining, remaining)

        # daily spending series
        records.append({
            "date": d,
            "type": "daily_spending",
            "amount": daily_spend,
        })
        # remaining budget series
        records.append({
            "date": d,
            "type": "remaining_budget",
            "amount": remaining,
        })

    plot_df = pd.DataFrame.from_records(records)

    # --- plot ---
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(9, 4.5))

    sns.lineplot(
        data=plot_df,
        x="date",
        y="amount",
        hue="type",
        ax=ax,
        marker="o"
    )

    ax.set_title(f"Monthly Budget Tracker ({title_range})\nTotal monthly budget = {monthly_budget:.0f}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")

    # y-axis: big enough for both spending and remaining
    ymax_source = max(monthly_budget, max_daily_spend, max_remaining, 1.0)
    ax.set_ylim(0, ymax_source * 1.1)
    ymin_source = -monthly_budget
    ax.set_ylim(ymin_source, ymax_source * 1.1)


    fig.autofmt_xdate()

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return send_file(buf, mimetype="image/png")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
