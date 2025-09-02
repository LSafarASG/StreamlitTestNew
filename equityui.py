# equityui.py
from __future__ import annotations
import os
import pandas as pd
import requests
import streamlit as st
import time

DEFAULT_BACKEND = "http://localhost:8000"

# Pre-load Plotly to avoid initialization overhead
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_LOADED = True
except ImportError:
    PLOTLY_LOADED = False
    px = None
    go = None

@st.cache_data(ttl=600, show_spinner=False)
def _fetch(backend_url: str, path: str, params: dict | None = None) -> dict:
    backend_url = backend_url.rstrip("/")
    url = f"{backend_url}/{path.lstrip('/')}"
    r = requests.get(url, params=params or {}, timeout=10)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=60, show_spinner=False)  # Reduced TTL for testing
def _get_cached_data(endpoint: str, backend_url: str, sort: bool, y: str, cache_key: str) -> pd.DataFrame:
    """Cached method to fetch and process data for fast rendering."""
    return _load_df(endpoint, backend_url, sort, y)

def _load_df(endpoint: str, backend_url: str | None, sort: bool, y: str) -> pd.DataFrame:
    backend_url = backend_url or os.getenv("BACKEND_URL", DEFAULT_BACKEND)
    payload = _fetch(backend_url, endpoint, params=None)
    df = pd.DataFrame(payload.get("data", []))
    if not df.empty and sort and y in df:
        df = df.sort_values(y, ascending=False).reset_index(drop=True)
    return df

class PlotlyBarChart:
    """Interactive bar chart with Plotly (heavier initial load)."""
    def __init__(self, endpoint: str, title: str, x: str = "label", y: str = "weight", sort: bool = True):
        self.endpoint = endpoint
        self.title = title
        self.x = x
        self.y = y
        self.sort = sort

    def render(self, backend_url: str | None = None, cache_key: str = "", profile_performance: bool = False):
        # Performance profiling
        if profile_performance:
            st.write("🔍 **Performance Profiling Enabled**")
        
        # Step 1: Data fetching
        start_data = time.time()
        df = _get_cached_data(self.endpoint, backend_url, self.sort, self.y, cache_key)
        data_time = time.time() - start_data
        
        if profile_performance:
            st.write(f"📊 Data fetch: {data_time:.3f}s")
            
            # Show cache status
            if data_time < 0.1:
                st.success("✅ Data served from cache")
            else:
                st.warning("⚠️ Data fetched from backend (slow)")
        
        if df.empty:
            st.info("No data available.")
            return
        
        # Check if Plotly is available
        if not PLOTLY_LOADED:
            st.error("Plotly is not installed. Please install with: pip install plotly")
            return

        # Step 2: Chart creation
        start_chart = time.time()
        fig = px.bar(df, x=self.x, y=self.y, title=self.title)
        chart_time = time.time() - start_chart
        
        if profile_performance:
            st.write(f"📈 Chart creation: {chart_time:.3f}s")
        
        # Step 3: Layout optimization
        start_layout = time.time()
        # Format y-axis for percentage values
        try:
            if 0 <= float(df[self.y].max()) <= 1.0:
                fig.update_yaxes(tickformat=".1%")
        except Exception:
            pass
        
        # Optimize layout for faster rendering
        fig.update_layout(
            margin=dict(l=10, r=10, t=50, b=10), 
            height=420,
            # Disable hover info for faster rendering
            hovermode=False,
            # Use simpler rendering mode
            uirevision=True
        )
        
        # Optimize chart configuration
        fig.update_traces(
            hovertemplate=None,
            hoverinfo="skip"
        )
        layout_time = time.time() - start_layout
        
        if profile_performance:
            st.write(f"🎨 Layout optimization: {layout_time:.3f}s")
        
        # Step 4: Streamlit rendering (this is the big one!)
        start_render = time.time()
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': False,  # Hide toolbar for faster rendering
            'responsive': True
        })
        render_time = time.time() - start_render
        
        if profile_performance:
            st.write(f"🚀 Streamlit render: {render_time:.3f}s")
            st.write(f"⏱️ **Total time: {data_time + chart_time + layout_time + render_time:.3f}s**")
            
            # Identify bottleneck
            times = [("Data", data_time), ("Chart", chart_time), ("Layout", layout_time), ("Render", render_time)]
            bottleneck = max(times, key=lambda x: x[1])
            st.warning(f"🐌 **Bottleneck**: {bottleneck[0]} ({bottleneck[1]:.3f}s)")

    @staticmethod
    def clear_cache():
        """Clear the cache for testing purposes."""
        st.cache_data.clear()

class NativeBarChart:
    """Fast, lightweight bar chart using Streamlit's native st.bar_chart."""
    def __init__(self, endpoint: str, title: str, x: str = "label", y: str = "weight", sort: bool = True):
        self.endpoint = endpoint
        self.title = title
        self.x = x
        self.y = y
        self.sort = sort

    def render(self, backend_url: str | None = None):
        df = _load_df(self.endpoint, backend_url, self.sort, self.y)
        st.subheader(self.title)
        if df.empty:
            st.info("No data available.")
            return

        # st.bar_chart expects index on x; keep only needed cols
        if self.x not in df.columns or self.y not in df.columns:
            st.warning(f"Expected columns '{self.x}' and '{self.y}' not found.")
            return

        plot_df = df[[self.x, self.y]].set_index(self.x)

        # If values look like 0..1, optionally show a small caption so the axis
        # (which native chart can’t format) isn’t confusing.
        try:
            if 0 <= float(plot_df[self.y].max()) <= 1.0:
                st.caption("Values shown as fractions (0–1). Switch to Plotly for % axis formatting.")
        except Exception:
            pass

        st.bar_chart(plot_df, use_container_width=True)
