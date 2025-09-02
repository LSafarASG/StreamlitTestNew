# frontend.py
from __future__ import annotations
import os
import streamlit as st
from equityui import NativeBarChart, PlotlyBarChart
import time

st.set_page_config(page_title="Equity Dashboard", layout="wide")
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("Equity Allocations")

# Performance testing section
st.header("Performance Testing - 2 Widgets")
st.write("Test the rendering speed of PlotlyBarChart widgets.")

# Show Plotly status
from equityui import PLOTLY_LOADED
if PLOTLY_LOADED:
    st.success("✅ Plotly is pre-loaded and ready")
else:
    st.error("❌ Plotly failed to load")

# Button to generate new random data
if st.button("🔄 Generate New Random Data", type="primary"):
    # Clear cache to force fresh data
    PlotlyBarChart.clear_cache()
    st.success("Cache cleared! New data will be generated.")
    st.rerun()

# Display two PlotlyBarChart widgets for testing
col1, col2 = st.columns(2)

with col1:
    st.subheader("Widget 1 - Random Data")
    start_time = time.time()
    chart1 = PlotlyBarChart(endpoint="/random-test-data", title="Random Data Set 1")
    chart1.render(backend_url, cache_key=f"widget1_{int(time.time())}", profile_performance=True)
    render_time1 = time.time() - start_time
    st.caption(f"Total render time: {render_time1:.3f}s")

with col2:
    st.subheader("Widget 2 - Random Data")
    start_time = time.time()
    chart2 = PlotlyBarChart(endpoint="/random-test-data", title="Random Data Set 2")
    chart2.render(backend_url, cache_key=f"widget2_{int(time.time())}")
    render_time2 = time.time() - start_time
    st.caption(f"Render time: {render_time2:.3f}s")

# Performance metrics
st.subheader("Performance Metrics")
col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
with col_metrics1:
    st.metric("Widget 1 Render Time", f"{render_time1:.3f}s")
with col_metrics2:
    st.metric("Widget 2 Render Time", f"{render_time2:.3f}s")
with col_metrics3:
    speedup = render_time1 / render_time2 if render_time2 > 0 else 0
    st.metric("Speedup Factor", f"{speedup:.1f}x")

# Performance insights
st.subheader("Performance Insights")
if render_time1 > render_time2 * 10:
    st.success(f"🎯 **Major Performance Gain**: Widget 2 is {speedup:.1f}x faster than Widget 1")
    st.write("This confirms data caching is working.")
elif render_time1 > render_time2 * 2:
    st.info(f"📈 **Performance Gain**: Widget 2 is {speedup:.1f}x faster than Widget 1")
    st.write("Some optimization benefit from caching.")
else:
    st.info("⚡ **Consistent Performance**: Both widgets render at similar speeds")

st.info("💡 **Tip**: The first render will be slower due to data fetching. Subsequent renders benefit from caching!")

# Original functionality
st.header("Original Charts")
use_plotly = st.toggle("Use Plotly charts (heavier, but interactive)", value=False)

Chart = PlotlyBarChart if use_plotly else NativeBarChart

col1, col2 = st.columns(2)
with col1:
    Chart(endpoint="/country-allocation", title="By Country").render(backend_url)
with col2:
    Chart(endpoint="/sector-allocation", title="By Sector").render(backend_url)

st.caption(f"Backend: {backend_url}")
