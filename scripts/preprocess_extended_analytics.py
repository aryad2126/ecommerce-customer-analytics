"""
preprocess_extended_analytics.py
Generates clean, aggregated data marts for the E-Commerce Intelligence Dashboard.
Covers:
1. Product & Category Mart: category translations, sales, quantities, average prices.
2. Delivery & Logistics Mart: delivery duration, estimated vs actual delays, late delivery flags.
3. Customer Retention & Cohort Mart: first purchase cohort, returning purchase periods, frequency distribution.
4. Reviews & Satisfaction Mart: review ratings, score by category, delivery delay vs review score correlation.
5. Seller Performance Mart: seller revenue, order volume, distinct items, state distribution.
6. Sales Forecasting Series: monthly chronological aggregates for order count and item revenue.
"""

from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "olist"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MARTS_DIR = PROCESSED_DIR / "marts"
MARTS_DIR.mkdir(parents=True, exist_ok=True)

def run_pipeline():
    print("=" * 60)
    print("STARTING EXTENDED ANALYTICS PIPELINE")
    print("=" * 60)

    # 1. Load raw datasets
    print("Loading raw Olist datasets...")
    orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
    order_items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
    payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
    reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")
    products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
    sellers = pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv")
    customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
    cat_trans = pd.read_csv(RAW_DIR / "product_category_name_translation.csv")

    # Date parsing
    for col in [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col], errors="coerce")

    if "review_creation_date" in reviews.columns:
        reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"], errors="coerce")

    print(f"Loaded: orders={len(orders):,}, items={len(order_items):,}, products={len(products):,}, reviews={len(reviews):,}")

    # Build Category Translation Map
    cat_map = dict(zip(cat_trans["product_category_name"], cat_trans["product_category_name_english"]))
    # Default translation formatter
    def translate_cat(cat):
        if pd.isna(cat):
            return "Uncategorized"
        eng = cat_map.get(cat, cat.replace("_", " ").title())
        return eng.replace("_", " ").title()

    products["category_english"] = products["product_category_name"].apply(translate_cat)

    # -------------------------------------------------------------
    # MART 1: Product & Category Summary
    # -------------------------------------------------------------
    print("\n[1/6] Building Category & Product Mart...")
    # Join items with products & orders (for status filtering)
    items_enriched = order_items.merge(
        products[["product_id", "category_english", "product_photos_qty", "product_weight_g"]],
        on="product_id",
        how="left"
    ).merge(
        orders[["order_id", "order_status", "order_purchase_timestamp"]],
        on="order_id",
        how="left"
    )

    # Aggregate by Category (Delivered & All)
    cat_delivered = items_enriched[items_enriched["order_status"] == "delivered"]

    cat_stats = cat_delivered.groupby("category_english").agg(
        revenue=("price", "sum"),
        total_freight=("freight_value", "sum"),
        units_sold=("order_item_id", "count"),
        orders_count=("order_id", "nunique"),
        distinct_products=("product_id", "nunique"),
        avg_item_price=("price", "mean"),
        avg_freight=("freight_value", "mean"),
    ).reset_index()

    # Join average review score per category if available
    item_reviews = cat_delivered.merge(
        reviews[["order_id", "review_score"]],
        on="order_id",
        how="inner"
    )
    cat_review_stats = item_reviews.groupby("category_english").agg(
        avg_review_score=("review_score", "mean"),
        review_count=("review_score", "count")
    ).reset_index()

    cat_summary = cat_stats.merge(cat_review_stats, on="category_english", how="left")
    cat_summary = cat_summary.sort_values("revenue", ascending=False)
    cat_summary.to_csv(MARTS_DIR / "category_summary.csv", index=False)
    print(f"Saved category_summary.csv ({len(cat_summary)} categories)")

    # Top products mart
    prod_stats = cat_delivered.groupby(["product_id", "category_english"]).agg(
        revenue=("price", "sum"),
        units_sold=("order_item_id", "count"),
        orders_count=("order_id", "nunique"),
        avg_price=("price", "mean")
    ).reset_index().sort_values("revenue", ascending=False).head(500)
    prod_stats.to_csv(MARTS_DIR / "top_products.csv", index=False)
    print(f"Saved top_products.csv ({len(prod_stats)} products)")

    # -------------------------------------------------------------
    # MART 2: Delivery & Logistics Mart
    # -------------------------------------------------------------
    print("\n[2/6] Building Delivery & Logistics Mart...")
    # Only orders that have actual customer delivery timestamp
    delivered_orders = orders[
        orders["order_status"].eq("delivered") &
        orders["order_delivered_customer_date"].notna() &
        orders["order_purchase_timestamp"].notna() &
        orders["order_estimated_delivery_date"].notna()
    ].copy()

    # Join customer state
    delivered_orders = delivered_orders.merge(
        customers[["customer_id", "customer_state", "customer_city"]],
        on="customer_id",
        how="left"
    )

    # Calculate delivery duration in days
    delivered_orders["delivery_duration_days"] = (
        delivered_orders["order_delivered_customer_date"] - delivered_orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400.0

    # Calculate delivery delay vs estimate in days (positive = late, negative = early)
    delivered_orders["delivery_delay_days"] = (
        delivered_orders["order_delivered_customer_date"] - delivered_orders["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400.0

    # Filter out anomalous negative duration if any
    delivered_orders = delivered_orders[delivered_orders["delivery_duration_days"] >= 0].copy()
    delivered_orders["is_late"] = delivered_orders["delivery_delay_days"] > 0
    delivered_orders["days_early_or_late"] = delivered_orders["delivery_delay_days"]

    delivery_export = delivered_orders[[
        "order_id", "customer_id", "customer_state", "customer_city",
        "order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date",
        "delivery_duration_days", "delivery_delay_days", "is_late"
    ]]
    delivery_export.to_csv(MARTS_DIR / "delivery_orders.csv", index=False)
    print(f"Saved delivery_orders.csv ({len(delivery_export):,} delivered orders)")

    # State delivery aggregate
    state_delivery = delivery_export.groupby("customer_state").agg(
        orders_count=("order_id", "count"),
        avg_delivery_days=("delivery_duration_days", "mean"),
        median_delivery_days=("delivery_duration_days", "median"),
        late_orders_count=("is_late", "sum"),
        avg_delay_days=("delivery_delay_days", "mean"),
    ).reset_index()
    state_delivery["on_time_rate"] = (1 - state_delivery["late_orders_count"] / state_delivery["orders_count"]) * 100
    state_delivery["late_rate"] = (state_delivery["late_orders_count"] / state_delivery["orders_count"]) * 100
    state_delivery.to_csv(MARTS_DIR / "state_delivery_summary.csv", index=False)
    print(f"Saved state_delivery_summary.csv ({len(state_delivery)} states)")

    # -------------------------------------------------------------
    # MART 3: Customer Retention & Cohort Mart
    # -------------------------------------------------------------
    print("\n[3/6] Building Customer Retention & Cohort Mart...")
    # Link orders to customer_unique_id
    cust_orders = orders.dropna(subset=["order_purchase_timestamp"]).merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="inner"
    )

    # Identify first purchase date per unique customer
    first_purchases = cust_orders.groupby("customer_unique_id")["order_purchase_timestamp"].min().reset_index()
    first_purchases.rename(columns={"order_purchase_timestamp": "first_purchase_date"}, inplace=True)
    first_purchases["cohort_month"] = first_purchases["first_purchase_date"].dt.to_period("M").astype(str)

    cust_orders = cust_orders.merge(first_purchases, on="customer_unique_id", how="left")
    cust_orders["order_month"] = cust_orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

    # Monthly new vs returning customer counts
    monthly_retention = []
    all_months = sorted(cust_orders["order_month"].unique())
    seen_customers = set()

    for m in all_months:
        m_orders = cust_orders[cust_orders["order_month"] == m]
        m_custs = set(m_orders["customer_unique_id"].dropna().unique())
        new_custs = m_custs - seen_customers
        returning_custs = m_custs & seen_customers
        seen_customers.update(m_custs)

        monthly_retention.append({
            "order_month": m,
            "total_customers": len(m_custs),
            "new_customers": len(new_custs),
            "returning_customers": len(returning_custs),
            "returning_ratio": (len(returning_custs) / len(m_custs) * 100) if m_custs else 0
        })

    retention_df = pd.DataFrame(monthly_retention)
    retention_df.to_csv(MARTS_DIR / "monthly_retention.csv", index=False)
    print(f"Saved monthly_retention.csv ({len(retention_df)} months)")

    # Customer order frequency distribution
    cust_order_counts = cust_orders.groupby("customer_unique_id")["order_id"].nunique()
    freq_bins = pd.cut(
        cust_order_counts,
        bins=[0, 1, 2, 3, 4, 100],
        labels=["1 order", "2 orders", "3 orders", "4 orders", "5+ orders"]
    ).value_counts().reset_index()
    freq_bins.columns = ["frequency_tier", "customer_count"]
    freq_bins.to_csv(MARTS_DIR / "customer_frequency_distribution.csv", index=False)
    print("Saved customer_frequency_distribution.csv")

    # Cohort retention matrix (cohort month vs period difference 0 to 12 months)
    # Filter cohorts with at least some activity
    cust_orders["cohort_period"] = (
        (cust_orders["order_purchase_timestamp"].dt.year - cust_orders["first_purchase_date"].dt.year) * 12 +
        (cust_orders["order_purchase_timestamp"].dt.month - cust_orders["first_purchase_date"].dt.month)
    )
    cohort_group = cust_orders.groupby(["cohort_month", "cohort_period"])["customer_unique_id"].nunique().reset_index()
    cohort_pivot = cohort_group.pivot(index="cohort_month", columns="cohort_period", values="customer_unique_id")
    # Retention rate as percentage of cohort size at period 0
    cohort_size = cohort_pivot.iloc[:, 0]
    cohort_retention = cohort_pivot.divide(cohort_size, axis=0) * 100
    cohort_retention.to_csv(MARTS_DIR / "cohort_retention_matrix.csv")
    print("Saved cohort_retention_matrix.csv")

    # -------------------------------------------------------------
    # MART 4: Reviews & Satisfaction Mart
    # -------------------------------------------------------------
    print("\n[4/6] Building Reviews & Satisfaction Mart...")
    # Clean review scores and join with orders to get delivery delay
    rev_joined = reviews.dropna(subset=["review_score"]).merge(
        delivered_orders[["order_id", "order_purchase_timestamp", "delivery_delay_days", "delivery_duration_days", "customer_state"]],
        on="order_id",
        how="inner"
    )

    rev_joined["is_delayed"] = rev_joined["delivery_delay_days"] > 0
    rev_delay_summary = rev_joined.groupby("is_delayed").agg(
        avg_score=("review_score", "mean"),
        count=("review_id", "count")
    ).reset_index()

    # Delay bins: Early (<= -3d), On-time (-3d to 0d), 1-3d late, 4-7d late, >7d late
    rev_joined["delay_bracket"] = pd.cut(
        rev_joined["delivery_delay_days"],
        bins=[-999, -3, 0, 3, 7, 999],
        labels=["Early (3+ days)", "On-Time (0-3d early)", "Slightly Late (1-3 days)", "Late (4-7 days)", "Severely Late (>7 days)"]
    )
    delay_impact = rev_joined.groupby("delay_bracket", observed=False).agg(
        avg_score=("review_score", "mean"),
        review_count=("review_id", "count"),
        pct_negative=("review_score", lambda s: (s <= 2).mean() * 100)
    ).reset_index()
    delay_impact.to_csv(MARTS_DIR / "review_delay_impact.csv", index=False)
    print("Saved review_delay_impact.csv")

    # Overall review score distribution
    score_dist = reviews["review_score"].value_counts().sort_index().reset_index()
    score_dist.columns = ["review_score", "count"]
    score_dist["percentage"] = score_dist["count"] / score_dist["count"].sum() * 100
    score_dist.to_csv(MARTS_DIR / "review_score_distribution.csv", index=False)
    print("Saved review_score_distribution.csv")

    # Monthly review score trend
    rev_joined["month"] = rev_joined["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly_rev = rev_joined.groupby("month").agg(
        avg_score=("review_score", "mean"),
        review_count=("review_id", "count")
    ).reset_index().sort_values("month")
    monthly_rev = monthly_rev[monthly_rev["review_count"] >= 30]
    monthly_rev.to_csv(MARTS_DIR / "review_monthly_trend.csv", index=False)
    print("Saved review_monthly_trend.csv")

    # State review scores
    state_rev = rev_joined.groupby("customer_state").agg(
        avg_score=("review_score", "mean"),
        review_count=("review_id", "count")
    ).reset_index().sort_values("review_count", ascending=False)
    state_rev.to_csv(MARTS_DIR / "review_state_scores.csv", index=False)
    print("Saved review_state_scores.csv")

    # -------------------------------------------------------------
    # MART 5: Seller Performance Mart
    # -------------------------------------------------------------
    print("\n[5/6] Building Seller Performance Mart...")
    seller_items = order_items.merge(
        orders[["order_id", "order_status", "order_purchase_timestamp"]],
        on="order_id",
        how="inner"
    ).merge(
        sellers,
        on="seller_id",
        how="left"
    )

    # Deliveries and revenue per seller
    delivered_seller_items = seller_items[seller_items["order_status"] == "delivered"]
    seller_summary = delivered_seller_items.groupby(["seller_id", "seller_state", "seller_city"]).agg(
        total_revenue=("price", "sum"),
        total_freight=("freight_value", "sum"),
        items_sold=("order_item_id", "count"),
        orders_fulfilled=("order_id", "nunique"),
        distinct_products=("product_id", "nunique")
    ).reset_index()

    # Seller review scores
    seller_reviews = delivered_seller_items.merge(
        reviews[["order_id", "review_score"]],
        on="order_id",
        how="inner"
    ).groupby("seller_id")["review_score"].agg(
        avg_review_score="mean",
        total_reviews="count"
    ).reset_index()

    seller_summary = seller_summary.merge(seller_reviews, on="seller_id", how="left")
    seller_summary = seller_summary.sort_values("total_revenue", ascending=False)
    seller_summary.to_csv(MARTS_DIR / "seller_summary.csv", index=False)
    print(f"Saved seller_summary.csv ({len(seller_summary):,} sellers)")

    # -------------------------------------------------------------
    # MART 6: Chronological Series for Sales Forecasting
    # -------------------------------------------------------------
    print("\n[6/6] Building Chronological Forecasting Series...")
    # Daily and monthly aggregations across the core timeline (2017-01 to 2018-08)
    orders_clean = orders.dropna(subset=["order_purchase_timestamp"]).copy()
    delivered_clean = orders_clean[orders_clean["order_status"] == "delivered"].merge(
        order_items.groupby("order_id")["price"].sum().reset_index(name="item_revenue"),
        on="order_id",
        how="left"
    )
    delivered_clean["item_revenue"] = delivered_clean["item_revenue"].fillna(0)

    delivered_clean["month_str"] = delivered_clean["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly_series = delivered_clean.groupby("month_str").agg(
        orders_count=("order_id", "nunique"),
        item_revenue=("item_revenue", "sum")
    ).reset_index().sort_values("month_str")

    # Filter out partial trailing months if any
    monthly_series = monthly_series[monthly_series["orders_count"] > 20]
    monthly_series.to_csv(MARTS_DIR / "monthly_forecast_series.csv", index=False)
    print(f"Saved monthly_forecast_series.csv ({len(monthly_series)} periods)")

    print("\n" + "=" * 60)
    print("ALL EXTENDED ANALYTICS MARTS CREATED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
