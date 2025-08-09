import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
from io import BytesIO

# Configure page settings
st.set_page_config(
    page_title="ReUpyog - AI Waste Classification",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for stunning UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2E8B57, #32CD32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #FF8C00;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2E8B57 0%, #32CD32 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(46, 139, 87, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(46, 139, 87, 0.4);
    }
    
    .section-divider {
        height: 4px;
        background: linear-gradient(90deg, #2E8B57 0%, #FF8C00 50%, #2E8B57 100%);
        margin: 4rem 0;
        border-radius: 2px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border-left: 6px solid #2E8B57;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
    }
    
    .highlight-text {
        color: #2E8B57;
        font-weight: 600;
        font-size: 1.2rem;
        line-height: 1.6;
    }
    
    .stats-showcase {
        background: linear-gradient(135deg, #FF8C00 0%, #FFB347 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(255, 140, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .stats-showcase:hover {
        transform: translateY(-3px);
    }
    
    .image-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .image-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f0f8f0 0%, #e8f5e8 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px dashed #2E8B57;
        margin: 2rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #FF8C00;
        background: linear-gradient(135deg, #fff8f0 0%, #ffeee8 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2E8B57 0%, #228B22 100%);
    }
    
    .nav-item {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 15px;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    .performance-badge {
        display: inline-block;
        background: linear-gradient(135deg, #32CD32, #228B22);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.5rem;
        box-shadow: 0 4px 16px rgba(50, 205, 50, 0.3);
    }
    
    .tech-stack-item {
        background: linear-gradient(135deg, #87CEEB, #4682B4);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem;
        text-align: center;
        font-weight: 500;
        box-shadow: 0 4px 16px rgba(135, 206, 235, 0.3);
    }
    
    .application-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(46, 139, 87, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .application-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.12);
        border-color: #FF8C00;
    }
    
    .footer-section {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-top: 4rem;
        box-shadow: 0 8px 32px rgba(46, 139, 87, 0.3);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2E8B57, #32CD32);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #32CD32, #2E8B57);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for uploaded images
def init_session_state():
    image_keys = [
        'logo', 'hero_banner', 'architecture_diagram', 'waste_icons',
        'overview_infographic', 'applications_illustration', 'team_avatar',
        'footer_banner', 'confusion_matrix', 'training_curves'
    ]
    for key in image_keys:
        if key not in st.session_state:
            st.session_state[key] = None

def create_comparison_chart():
    """Generate dataset comparison visualization"""
    data = {
        'Dataset': ['TrashNet', 'E-waste Studies', 'Typical Research', 'ReUpyog'],
        'Images': [2527, 12000, 15000, 213000],
        'Classes': [6, 13, 10, 22]
    }
    
    df = pd.DataFrame(data)
    fig = go.Figure()
    
    # Add bars for images
    fig.add_trace(go.Bar(
        name='Images (thousands)',
        x=df['Dataset'],
        y=df['Images'] / 1000,
        marker_color=['#FFB347', '#87CEEB', '#DDA0DD', '#2E8B57'],
        text=[f'{x/1000:.1f}K' for x in df['Images']],
        textposition='outside',
        yaxis='y'
    ))
    
    # Add bars for classes
    fig.add_trace(go.Bar(
        name='Classes',
        x=df['Dataset'],
        y=df['Classes'],
        marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FF8C00'],
        text=df['Classes'],
        textposition='outside',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title={
            'text': 'ReUpyog vs. Existing Datasets',
            'x': 0.5,
            'font': {'size': 24, 'color': '#2E8B57'}
        },
        xaxis_title='Datasets',
        yaxis=dict(title='Images (thousands)', side='left'),
        yaxis2=dict(title='Number of Classes', side='right', overlaying='y'),
        legend=dict(x=0.02, y=0.98),
        height=500,
        template='plotly_white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_performance_radar():
    """Generate performance metrics radar chart"""
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Stability']
    values = [99.09, 99.12, 99.05, 99.08, 98.5]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=metrics,
        fill='toself',
        name='ReUpyog Performance',
        line=dict(color='#2E8B57', width=3),
        fillcolor='rgba(46, 139, 87, 0.2)',
        marker=dict(size=8, color='#FF8C00')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[95, 100],
                tickfont=dict(size=12),
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color='#2E8B57')
            )
        ),
        title={
            'text': "ReUpyog Performance Metrics",
            'x': 0.5,
            'font': {'size': 20, 'color': '#2E8B57'}
        },
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def display_image_with_container(image, caption, key=None):
    """Display image with beautiful container styling"""
    if image is not None:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(image, caption=caption, use_column_width=True, key=key)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info(f"📸 {caption} will be displayed here once uploaded")

def main():
    init_session_state()
    
    # Sidebar Navigation with enhanced styling
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: white; font-size: 2rem; margin-bottom: 0.5rem;'>🌱 ReUpyog</h1>
        <p style='color: rgba(255,255,255,0.8); font-size: 1rem;'>Navigation</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Choose Section:",
        ["🏠 Project Overview", "📊 Dataset Excellence", "🔬 Technical Innovation", 
         "🎯 Performance Results", "🌍 Applications & Impact", "📁 Upload Images"],
        key="navigation"
    )
    
    # Add sidebar stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='color: white; padding: 1rem; text-align: center;'>
        <h3 style='color: #32CD32; margin-bottom: 1rem;'>Project Stats</h3>
        <p><strong>📊 Images:</strong> 213,000</p>
        <p><strong>🗂️ Classes:</strong> 22</p>
        <p><strong>🎯 Accuracy:</strong> 99.09%</p>
        <p><strong>💾 Size:</strong> 19 GB</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "🏠 Project Overview":
        show_overview()
    elif page == "📊 Dataset Excellence":
        show_dataset()
    elif page == "🔬 Technical Innovation":
        show_technical()
    elif page == "🎯 Performance Results":
        show_results()
    elif page == "🌍 Applications & Impact":
        show_applications()
    elif page == "📁 Upload Images":
        show_upload_center()

def show_overview():
    """Project Overview Section with Hero Design"""
    
    # Hero Section with Logo
    if st.session_state.logo:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            display_image_with_container(st.session_state.logo, "ReUpyog Logo", "overview_logo")
    
    st.markdown('<h1 class="main-header">ReUpyog</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Revolutionary AI-Powered Smart Waste Classification</h2>', unsafe_allow_html=True)
    
    # Hero Banner
    if st.session_state.hero_banner:
        display_image_with_container(st.session_state.hero_banner, "AI-Powered Waste Management Hero", "hero_display")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Hero Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("📊 Total Images", "213,000", "84x larger than TrashNet"),
        ("🗂️ Categories", "22 Classes", "+9 vs standard studies"),
        ("🎯 Accuracy", "99.09%", "Industry-leading performance"),
        ("💾 Dataset Size", "19 GB", "Enterprise-scale preparation")
    ]
    
    for i, (metric, col) in enumerate(zip(metrics_data, [col1, col2, col3, col4])):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin-bottom: 0.5rem; font-size: 1.8rem;">{metric[1]}</h3>
                <p style="font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem;">{metric[0]}</p>
                <p style="font-size: 0.9rem; opacity: 0.9;">{metric[2]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Project Description with Visual
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #2E8B57; font-size: 1.8rem; margin-bottom: 1rem;">🚀 Revolutionary Multi-Object Detection</h3>
            <p class="highlight-text">ReUpyog transforms waste management through AI-powered classification that handles real-world clustered images, not just single objects.</p>
            
            <h4 style="color: #FF8C00; margin-top: 1.5rem; margin-bottom: 1rem;">Key Innovations:</h4>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>SAM + YOLOv8 hybrid architecture</strong> for multi-object processing</li>
                <li><strong>Advanced shadow detection</strong> and fragment merging</li>
                <li><strong>Production-ready deployment</strong> with cross-platform compatibility</li>
                <li><strong>Real-time confidence scoring</strong> with visual interface</li>
                <li><strong>213,000 image training dataset</strong> - largest in research</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Display architecture diagram if uploaded
        if st.session_state.architecture_diagram:
            display_image_with_container(
                st.session_state.architecture_diagram, 
                "SAM + YOLOv8 Hybrid Architecture Pipeline", 
                "arch_overview"
            )
        else:
            st.info("🔧 System Architecture Diagram will be displayed here once uploaded")
    
    # Overview Infographic
    if st.session_state.overview_infographic:
        st.markdown("### 📈 Project Overview Dashboard")
        display_image_with_container(
            st.session_state.overview_infographic, 
            "ReUpyog Key Metrics & Statistics Overview", 
            "overview_infographic"
        )

def show_dataset():
    """Dataset Excellence Section"""
    st.markdown("# 📊 Industry-Leading Dataset Scale")
    
    # Dataset highlights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #2E8B57; font-size: 1.6rem; margin-bottom: 1rem;">🏆 Massive Scale Achievement</h3>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>213,000 total images</strong> - Largest waste dataset in research</li>
                <li><strong>22 waste categories</strong> - Most comprehensive classification</li>
                <li><strong>Professional data splits:</strong>
                    <ul style="margin-top: 0.5rem;">
                        <li>149,393 training images (70%)</li>
                        <li>32,015 validation images (15%)</li>
                        <li>32,016 test images (15%)</li>
                    </ul>
                </li>
                <li><strong>~9,682 images per class</strong> - Ensures statistical significance</li>
                <li><strong>19GB total size</strong> - Enterprise-scale preparation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Dataset split visualization
        st.markdown("### 📈 Data Distribution")
        split_col1, split_col2 = st.columns(2)
        
        with split_col1:
            st.markdown("""
            <div class="stats-showcase">
                <h4 style="margin-bottom: 0.5rem;">Training Set</h4>
                <h2 style="margin: 0;">149,393</h2>
                <p style="opacity: 0.9;">70% of total data</p>
            </div>
            """, unsafe_allow_html=True)
        
        with split_col2:
            st.markdown("""
            <div class="stats-showcase">
                <h4 style="margin-bottom: 0.5rem;">Val + Test</h4>
                <h2 style="margin: 0;">64,031</h2>
                <p style="opacity: 0.9;">30% for validation</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Dataset comparison chart
        comparison_fig = create_comparison_chart()
        st.plotly_chart(comparison_fig, use_container_width=True, key="dataset_comparison")
        
        # Competitive advantages
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #FF8C00; font-size: 1.6rem; margin-bottom: 1rem;">🥇 Competitive Advantages</h3>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>84x larger</strong> than standard TrashNet dataset</li>
                <li><strong>22 categories</strong> vs typical 6-13 in research</li>
                <li><strong>Real-world ready</strong> with clustered image processing</li>
                <li><strong>Production scale</strong> suitable for industry deployment</li>
                <li><strong>Professional validation</strong> with proper train/val/test splits</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Waste categories display
    if st.session_state.waste_icons:
        st.markdown("### 🗂️ Comprehensive Waste Categories")
        display_image_with_container(
            st.session_state.waste_icons, 
            "22 Waste Categories Covered by ReUpyog Dataset", 
            "waste_categories"
        )

def show_technical():
    """Technical Innovation Section"""
    st.markdown("# 🔬 Advanced Technical Architecture")
    
    # Main architecture display
    if st.session_state.architecture_diagram:
        display_image_with_container(
            st.session_state.architecture_diagram, 
            "Complete ReUpyog Processing Pipeline: Input → SAM → Shadow Detection → Fragment Merging → YOLOv8 → Confidence Scoring", 
            "tech_architecture"
        )
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Technical details in cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #2E8B57; font-size: 1.6rem; margin-bottom: 1rem;">🤖 Core Technologies</h3>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>YOLOv8 Nano Classification:</strong> Efficient base model for single-object training on 213K images</li>
                <li><strong>SAM Integration:</strong> Segment Anything Model for precise object boundary detection</li>
                <li><strong>Hybrid Pipeline:</strong> Segmentation → Classification workflow for multi-object scenes</li>
                <li><strong>Alternative Architecture:</strong> Robust deployment solution bypassing YAML issues</li>
                <li><strong>Cross-Platform Deployment:</strong> PyTorch (.pt) and ONNX formats available</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #FF8C00; font-size: 1.6rem; margin-bottom: 1rem;">⚡ Advanced Processing Features</h3>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>Shadow Detection:</strong> HSV color space analysis (brightness < 80, saturation < 50)</li>
                <li><strong>Fragment Merging:</strong> 80-pixel distance-based clustering algorithm</li>
                <li><strong>Size Filtering:</strong> Minimum 0.5% image area threshold for noise reduction</li>
                <li><strong>Confidence Scoring:</strong> 25% minimum reliability threshold with visual interface</li>
                <li><strong>Real-time Processing:</strong> Optimized for interactive multi-object classification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical specifications grid
    st.markdown("### ⚙️ Training & Deployment Specifications")
    
    spec_col1, spec_col2, spec_col3 = st.columns(3)
    
    specs_data = [
        [("Training Epochs", "45", "Early stopping: 15"), ("Batch Size", "96", "GPU optimized"), ("Image Size", "224×224", "Standard classification")],
        [("Learning Rate", "0.001", "Cosine scheduling"), ("Model Size", "Nano", "Lightweight deployment"), ("GPU Memory", "Optimized", "AMP enabled")],
        [("Output Formats", "2", "PyTorch + ONNX"), ("Deployment", "Cross-platform", "Production ready"), ("Inference Speed", "Real-time", "Interactive processing")]
    ]
    
    for i, (specs, col) in enumerate(zip(specs_data, [spec_col1, spec_col2, spec_col3])):
        with col:
            for spec in specs:
                st.markdown(f"""
                <div class="tech-stack-item">
                    <h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">{spec[1]}</h4>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">{spec[0]}</p>
                    <p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">{spec[2]}</p>
                </div>
                """, unsafe_allow_html=True)

def show_results():
    """Performance Results Section"""
    st.markdown("# 🎯 Outstanding Performance Results")
    
    # Performance metrics header
    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    
    performance_data = [
        ("Overall Accuracy", "99.09%", "Exceptional"),
        ("F1-Score", "99.08%", "Balanced performance"),
        ("Training Stability", "Excellent", "No overfitting"),
        ("Classes Perfect", "Most", "Minimal confusion")
    ]
    
    for i, (perf, col) in enumerate(zip(performance_data, [perf_col1, perf_col2, perf_col3, perf_col4])):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin-bottom: 0.5rem; font-size: 1.6rem;">{perf[1]}</h3>
                <p style="font-size: 1rem; font-weight: 500; margin-bottom: 0.5rem;">{perf[0]}</p>
                <p style="font-size: 0.9rem; opacity: 0.9;">{perf[2]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Performance radar chart
    st.markdown("### 📊 Comprehensive Performance Analysis")
    perf_fig = create_performance_radar()
    radar_col1, radar_col2, radar_col3 = st.columns([1, 2, 1])
    with radar_col2:
        st.plotly_chart(perf_fig, use_container_width=True, key="performance_radar")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Display actual model results
    st.markdown("### 📈 Actual Model Results")
    
    results_col1, results_col2 = st.columns(2)
    
    with results_col1:
        st.markdown("#### 🎯 Confusion Matrix Analysis")
        if st.session_state.confusion_matrix:
            display_image_with_container(
                st.session_state.confusion_matrix, 
                "22x22 Confusion Matrix - 99.09% Accuracy Across All Waste Classes", 
                "confusion_display"
            )
        else:
            st.info("📊 Confusion Matrix will be displayed here once uploaded")
    
    with results_col2:
        st.markdown("#### 📉 Training Progression")
        if st.session_state.training_curves:
            display_image_with_container(
                st.session_state.training_curves, 
                "Training Curves - Stable Convergence Over 45 Epochs", 
                "curves_display"
            )
        else:
            st.info("📈 Training curves will be displayed here once uploaded")
    
    # Performance highlights
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🏆 Performance Highlights")
    
    highlight_col1, highlight_col2 = st.columns(2)
    
    with highlight_col1:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color: #2E8B57; font-size: 1.4rem; margin-bottom: 1rem;">🎯 Training Excellence</h4>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>Stable Convergence:</strong> Smooth loss reduction without oscillation over 45 epochs</li>
                <li><strong>No Overfitting:</strong> Validation loss follows training loss closely throughout</li>
                <li><strong>Early Achievement:</strong> High accuracy reached by epoch 10-15</li>
                <li><strong>Consistent Performance:</strong> All 22 waste classes show excellent results</li>
                <li><strong>Robust Validation:</strong> 99%+ accuracy maintained across test set</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with highlight_col2:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color: #FF8C00; font-size: 1.4rem; margin-bottom: 1rem;">📊 Real-World Validation</h4>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>Perfect Predictions:</strong> Multiple 100% confidence classifications achieved</li>
                <li><strong>High Reliability:</strong> 89-100% confidence scores typical in testing</li>
                <li><strong>Minimal Confusion:</strong> Clear diagonal patterns in confusion matrix</li>
                <li><strong>Production Ready:</strong> Consistent performance on diverse waste images</li>
                <li><strong>Multi-Object Success:</strong> Excellent results on clustered image scenarios</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_applications():
    """Applications & Impact Section"""
    st.markdown("# 🌍 Real-World Applications & Environmental Impact")
    
    # Applications illustration
    if st.session_state.applications_illustration:
        display_image_with_container(
            st.session_state.applications_illustration, 
            "AI-Powered Waste Management Applications Across Industries", 
            "applications_visual"
        )
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Applications grid
    app_col1, app_col2 = st.columns(2)
    
    with app_col1:
        st.markdown("""
        <div class="application-card">
            <h3 style="color: #2E8B57; font-size: 1.6rem; margin-bottom: 1rem;">🏭 Industrial Applications</h3>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>Smart Waste Management:</strong> Automated recycling facilities with 99% accuracy classification</li>
                <li><strong>IoT Integration:</strong> Intelligent waste bin systems for real-time sorting and monitoring</li>
                <li><strong>Municipal Services:</strong> Enhanced collection and processing efficiency for city-wide deployment</li>
                <li><strong>Industrial Automation:</strong> Large-scale waste processing plants with multi-object detection</li>
                <li><strong>Environmental Monitoring:</strong> Real-time waste stream analysis and quality control</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with app_col2:
        st.markdown("""
        <div class="application-card">
            <h3 style="color: #FF8C00; font-size: 1.6rem; margin-bottom: 1rem;">🌱 Environmental Impact</h3>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>Improved Recycling Rates:</strong> Higher accuracy reduces contamination and increases yield</li>
                <li><strong>Reduced Manual Labor:</strong> Automated classification systems reduce human exposure</li>
                <li><strong>Enhanced Stream Purity:</strong> Better waste separation for higher recycling quality</li>
                <li><strong>Sustainable Processing:</strong> Eco-friendly waste management solutions at scale</li>
                <li><strong>Carbon Footprint Reduction:</strong> Optimized transportation and processing efficiency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Impact metrics
    st.markdown("### 📊 Projected Impact Metrics")
    
    impact_col1, impact_col2, impact_col3, impact_col4 = st.columns(4)
    
    impact_data = [
        ("Waste Sorting Accuracy", "99%+", "vs 70-80% manual"),
        ("Processing Speed", "Real-time", "vs hours manually"),
        ("Cost Reduction", "60-80%", "in sorting operations"),
        ("Environmental Benefit", "Significant", "improved recycling rates")
    ]
    
    for i, (impact, col) in enumerate(zip(impact_data, [impact_col1, impact_col2, impact_col3, impact_col4])):
        with col:
            st.markdown(f"""
            <div class="stats-showcase">
                <h4 style="margin-bottom: 0.5rem; font-size: 1rem;">{impact[0]}</h4>
                <h3 style="margin: 0.5rem 0; font-size: 1.4rem;">{impact[1]}</h3>
                <p style="opacity: 0.9; font-size: 0.9rem;">{impact[2]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Future roadmap (without the "coming soon" image since you don't have it)
    st.markdown("### 🚀 Future Development Roadmap")
    
    future_col1, future_col2, future_col3 = st.columns(3)
    
    with future_col1:
        st.markdown("""
        <div class="application-card">
            <h4 style="color: #2E8B57; margin-bottom: 1rem;">🔮 Phase 1: Immediate</h4>
            <ul style="line-height: 1.6;">
                <li>Mobile app development</li>
                <li>Edge device deployment</li>
                <li>Real-time IoT integration</li>
                <li>API development for third-party integration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with future_col2:
        st.markdown("""
        <div class="application-card">
            <h4 style="color: #FF8C00; margin-bottom: 1rem;">📈 Phase 2: Scaling</h4>
            <ul style="line-height: 1.6;">
                <li>Additional waste categories</li>
                <li>Multi-language support</li>
                <li>Global dataset expansion</li>
                <li>Cloud infrastructure scaling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with future_col3:
        st.markdown("""
        <div class="application-card">
            <h4 style="color: #32CD32; margin-bottom: 1rem;">🤝 Phase 3: Partnerships</h4>
            <ul style="line-height: 1.6;">
                <li>Industry collaborations</li>
                <li>Municipality partnerships</li>
                <li>Research community engagement</li>
                <li>Open-source contributions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Team avatar display
    if st.session_state.team_avatar:
        st.markdown("### 👥 Our Team")
        display_image_with_container(
            st.session_state.team_avatar, 
            "ReUpyog Development Team", 
            "team_display"
        )

def show_upload_center():
    """Centralized Upload Section"""
    st.markdown("# 📁 Image Upload Center")
    st.markdown("Upload all your project images here. Each image will be automatically displayed in the appropriate sections throughout the website.")
    
    upload_sections = [
        {
            'title': '🌱 Logo',
            'key': 'logo',
            'description': 'Upload your ReUpyog logo (square format recommended)',
            'help': 'This will appear in the header and project overview'
        },
        {
            'title': '🎨 Hero Banner',
            'key': 'hero_banner',
            'description': 'Upload your hero/landing page banner image',
            'help': 'This will be displayed prominently on the project overview page'
        },
        {
            'title': '🔧 Architecture Diagram',
            'key': 'architecture_diagram',
            'description': 'Upload your SAM + YOLOv8 pipeline diagram',
            'help': 'This will be shown in both overview and technical sections'
        },
        {
            'title': '🗂️ Waste Category Icons',
            'key': 'waste_icons',
            'description': 'Upload your 22 waste category icons image',
            'help': 'This will be displayed in the dataset section'
        },
        {
            'title': '📊 Overview Infographic',
            'key': 'overview_infographic',
            'description': 'Upload your project metrics infographic',
            'help': 'This will be shown in the project overview section'
        },
        {
            'title': '🌍 Applications Illustration',
            'key': 'applications_illustration',
            'description': 'Upload your use cases/applications illustration',
            'help': 'This will be displayed in the applications & impact section'
        },
        {
            'title': '👥 Team Avatar',
            'key': 'team_avatar',
            'description': 'Upload your team photo or avatar illustration',
            'help': 'This will be shown in the applications section'
        },
        {
            'title': '📞 Footer Banner',
            'key': 'footer_banner',
            'description': 'Upload your footer/contact banner',
            'help': 'This will be displayed at the bottom of pages'
        },
        {
            'title': '🎯 Confusion Matrix',
            'key': 'confusion_matrix',
            'description': 'Upload your 22x22 confusion matrix image',
            'help': 'This will be displayed in the performance results section'
        },
        {
            'title': '📈 Training Curves',
            'key': 'training_curves',
            'description': 'Upload your training loss/accuracy curves',
            'help': 'This will be displayed in the performance results section'
        }
    ]
    
    # Create upload sections in a grid
    for i in range(0, len(upload_sections), 2):
        col1, col2 = st.columns(2)
        
        # First column
        section1 = upload_sections[i]
        with col1:
            st.markdown(f"""
            <div class="upload-section">
                <h3 style="color: #2E8B57; margin-bottom: 0.5rem;">{section1['title']}</h3>
                <p style="color: #666; margin-bottom: 1rem;">{section1['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                f"Choose {section1['title']} image",
                type=['png', 'jpg', 'jpeg'],
                key=f"upload_{section1['key']}",
                help=section1['help']
            )
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.session_state[section1['key']] = image
                st.success(f"✅ {section1['title']} uploaded successfully!")
                st.image(image, caption=f"{section1['title']} Preview", width=200)
            elif st.session_state[section1['key']]:
                st.info(f"✅ {section1['title']} already uploaded")
                st.image(st.session_state[section1['key']], caption=f"{section1['title']} Current", width=200)
        
        # Second column (if exists)
        if i + 1 < len(upload_sections):
            section2 = upload_sections[i + 1]
            with col2:
                st.markdown(f"""
                <div class="upload-section">
                    <h3 style="color: #2E8B57; margin-bottom: 0.5rem;">{section2['title']}</h3>
                    <p style="color: #666; margin-bottom: 1rem;">{section2['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                uploaded_file = st.file_uploader(
                    f"Choose {section2['title']} image",
                    type=['png', 'jpg', 'jpeg'],
                    key=f"upload_{section2['key']}",
                    help=section2['help']
                )
                
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.session_state[section2['key']] = image
                    st.success(f"✅ {section2['title']} uploaded successfully!")
                    st.image(image, caption=f"{section2['title']} Preview", width=200)
                elif st.session_state[section2['key']]:
                    st.info(f"✅ {section2['title']} already uploaded")
                    st.image(st.session_state[section2['key']], caption=f"{section2['title']} Current", width=200)
        
        st.markdown("---")
    
    # Upload status summary
    st.markdown("### 📋 Upload Status")
    uploaded_count = sum(1 for key in ['logo', 'hero_banner', 'architecture_diagram', 'waste_icons', 
                                       'overview_infographic', 'applications_illustration', 'team_avatar', 
                                       'footer_banner', 'confusion_matrix', 'training_curves'] 
                        if st.session_state[key] is not None)
    
    st.progress(uploaded_count / 10)
    st.write(f"**{uploaded_count}/10 images uploaded** - {(uploaded_count/10)*100:.0f}% complete")
    
    if uploaded_count == 10:
        st.balloons()
        st.success("🎉 All images uploaded! Your presentation website is complete!")

def show_footer():
    """Enhanced Footer Section"""
    # Footer banner display
    if st.session_state.footer_banner:
        display_image_with_container(st.session_state.footer_banner, "Contact & Links Banner", "footer_banner_display")
    
    st.markdown("""
    <div class="footer-section">
        <h2 style="margin-bottom: 1rem; color: white;">🌱 ReUpyog</h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">Transforming Waste Management Through AI</p>
        
        <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 2rem;">
            <div style="text-align: center;">
                <h4 style="color: #32CD32; margin-bottom: 0.5rem;">📊 Dataset</h4>
                <p style="margin: 0; font-size: 1.1rem; font-weight: 500;">213,000 Images</p>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #32CD32; margin-bottom: 0.5rem;">🗂️ Categories</h4>
                <p style="margin: 0; font-size: 1.1rem; font-weight: 500;">22 Classes</p>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #32CD32; margin-bottom: 0.5rem;">🎯 Accuracy</h4>
                <p style="margin: 0; font-size: 1.1rem; font-weight: 500;">99.09%</p>
            </div>
            <div style="text-align: center;">
                <h4 style="color: #32CD32; margin-bottom: 0.5rem;">🚀 Status</h4>
                <p style="margin: 0; font-size: 1.1rem; font-weight: 500;">Production Ready</p>
            </div>
        </div>
        
        <p style="opacity: 0.8; margin-bottom: 1rem;">Built with ❤️ for a Sustainable Future | Powered by SAM + YOLOv8 Technology</p>
        <p style="opacity: 0.7; font-size: 0.9rem;"><em>"Revolutionizing waste management through cutting-edge AI technology"</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()
