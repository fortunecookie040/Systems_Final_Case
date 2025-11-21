from flask import Flask, request, send_file, render_template, abort
import io
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

@app.route("/")
def home():
    # Renders templates/index.html
    return render_template("index.html")

@app.route("/budget_plot")
def budget_plot():
    # Get query parameters: /budget_plot?budget=1000&spending=500
    budget_param = request.args.get("budget", type=float)
    spending_param = request.args.get("spending", type=float)

    if budget_param is None:
        abort(400, description="Please provide a 'budget' query parameter, e.g. /budget_plot?budget=1000")

    budget = float(budget_param)
    spending = float(spending_param) if spending_param is not None else None

    # --- Create date range for the current month ---
    today = date.today()
    start_of_month = today.replace(day=1)

    # First day of next month
    if start_of_month.month == 12:
        first_of_next_month = start_of_month.replace(year=start_of_month.year + 1, month=1)
    else:
        first_of_next_month = start_of_month.replace(month=start_of_month.month + 1)

    end_of_month = first_of_next_month - timedelta(days=1)

    dates = pd.date_range(start=start_of_month, end=end_of_month, freq="D")

    # Build DataFrame
    df = pd.DataFrame({"date": dates, "budget": [budget] * len(dates)})
    series_cols = ["budget"]

    if spending is not None:
        df["spending"] = [spending] * len(dates)
        series_cols.append("spending")

    # Long-form for seaborn
    plot_df = df.melt(id_vars="date", value_vars=series_cols,
                      var_name="type", value_name="amount")

    # --- Plot ---
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))

    sns.lineplot(data=plot_df, x="date", y="amount", hue="type", ax=ax, marker="o")

    ax.set_title(f"Monthly Budget View (Budget = {budget})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")

    # Y-axis max = 1.5 × max(budget, spending)
    ymax_source = budget
    if spending is not None:
        ymax_source = max(budget, spending)

    ax.set_ylim(0, ymax_source * 1.5)

    fig.autofmt_xdate()

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
