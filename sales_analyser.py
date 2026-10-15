import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

st.set_page_config(page_title="Customer Sales Analyser", layout="wide")
st.title("📊 Customer Sales Analyser")
st.markdown("Upload a CSV file with your sales data to get instant insights.")

# ── File Upload ───────────────────────────────────────
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Raw Data")
    st.dataframe(df)

    # ── Column Selection ──────────────────────────────
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.error("No numeric columns found in your CSV.")
    else:
        col = st.selectbox("Select column to analyse", numeric_cols)
        data = df[col].dropna().values

        st.markdown("---")
        st.subheader(f"📈 Analysis for: **{col}**")

        # ── Central Tendency ──────────────────────────
        mean   = np.mean(data)
        median = np.median(data)
        mode   = stats.mode(data, keepdims=True).mode[0]
        variance = np.var(data)
        std_dev  = np.std(data)
        skewness = stats.skew(data)

        col1, col2, col3 = st.columns(3)
        col1.metric("Mean",   f"{mean:,.2f}")
        col1.metric("Median", f"{median:,.2f}")
        col1.metric("Mode",   f"{mode:,.2f}")
        col2.metric("Std Dev",  f"{std_dev:,.2f}")
        col2.metric("Variance", f"{variance:,.2f}")
        col2.metric("Skewness", f"{skewness:.2f}")
        col3.metric("Min",   f"{np.min(data):,.2f}")
        col3.metric("Max",   f"{np.max(data):,.2f}")
        col3.metric("Range", f"{np.max(data) - np.min(data):,.2f}")

        # ── Distribution Type ─────────────────────────
        st.markdown("---")
        if skewness > 0.5:
            dist_type = "📈 Right Skewed — Mean > Median, long tail on right"
        elif skewness < -0.5:
            dist_type = "📉 Left Skewed — Mean < Median, long tail on left"
        else:
            dist_type = "🔔 Approximately Normal — Mean ≈ Median"
        st.info(f"**Distribution:** {dist_type}")

        # ── Typical Range ─────────────────────────────
        lower = mean - std_dev
        upper = mean + std_dev
        inside = np.sum((data >= lower) & (data <= upper))
        st.info(f"**Typical Range (Mean ± 1 SD):** {lower:,.2f} to {upper:,.2f} — {inside} of {len(data)} values ({inside/len(data)*100:.0f}%)")

        # ── Outliers ──────────────────────────────────
        st.markdown("---")
        st.subheader("🚨 Outlier Detection (beyond Mean ± 2 SD)")
        outliers = data[(data < mean - 2*std_dev) | (data > mean + 2*std_dev)]
        if len(outliers) > 0:
            st.warning(f"Found {len(outliers)} outlier(s): {', '.join([f'{o:,.0f}' for o in outliers])}")
        else:
            st.success("No outliers detected.")

        # ── Histogram ─────────────────────────────────
        st.markdown("---")
        st.subheader("📊 Distribution Chart")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(data, bins=20, color='steelblue', edgecolor='white')
        ax.axvline(mean,   color='red',    linestyle='--', label=f'Mean {mean:,.0f}')
        ax.axvline(median, color='green',  linestyle='--', label=f'Median {median:,.0f}')
        ax.axvline(lower,  color='orange', linestyle=':',  label=f'Mean - 1 SD')
        ax.axvline(upper,  color='orange', linestyle=':',  label=f'Mean + 1 SD')
        ax.set_xlabel(col)
        ax.set_ylabel('Count')
        ax.legend()
        st.pyplot(fig)

        # ── Correlation ───────────────────────────────
        st.markdown("---")
        st.subheader("🔗 Correlation with Other Columns")
        other_cols = [c for c in numeric_cols if c != col]
        if other_cols:
            corr_col = st.selectbox("Compare with", other_cols)
            data2 = df[corr_col].dropna().values
            min_len = min(len(data), len(data2))
            r, p = stats.pearsonr(data[:min_len], data2[:min_len])
            st.metric("Pearson r", f"{r:.2f}")
            if abs(r) > 0.7:
                st.success("Strong correlation")
            elif abs(r) > 0.3:
                st.info("Moderate correlation")
            else:
                st.warning("Weak or no correlation")

            fig2, ax2 = plt.subplots(figsize=(6, 4))
            ax2.scatter(data[:min_len], data2[:min_len], color='steelblue', alpha=0.6)
            ax2.set_xlabel(col)
            ax2.set_ylabel(corr_col)
            ax2.set_title(f'{col} vs {corr_col} (r={r:.2f})')
            st.pyplot(fig2)
        else:
            st.info("Need at least 2 numeric columns for correlation.")

        # ── Sampling ──────────────────────────────────
        st.markdown("---")
        st.subheader("🎲 Random Sampling")
        max_sample = min(100, len(data))
        default = min(5, max_sample)
        sample_size = st.slider("Sample size", min_value=1,
                        max_value=max_sample, value=default)
        sample = np.random.choice(data, size=sample_size, replace=False)
        s1, s2 = st.columns(2)
        s1.metric("Sample Mean", f"{np.mean(sample):,.2f}")
        s2.metric("Population Mean", f"{mean:,.2f}")
        s1.metric("Sample SD", f"{np.std(sample):,.2f}")
        s2.metric("Population SD", f"{std_dev:,.2f}")
        st.caption(f"Sampling error: {abs(np.mean(sample) - mean):,.2f}")

else:
    st.info("👆 Upload a CSV file to get started.")
    st.markdown("**Expected format:** Any CSV with at least one numeric column.")
    st.markdown("**Example columns:** Sales, Revenue, Purchases, Salary, Score")