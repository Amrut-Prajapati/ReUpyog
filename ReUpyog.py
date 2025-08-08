import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

# Set page config
st.set_page_config(
    page_title="ReUpyog - AI Waste Classification",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.8rem;
        color: #FF8C00;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    .metric-container {
        background: linear-gradient(135deg, #2E8B57, #32CD32);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .section-divider {
        height: 4px;
        background: linear-gradient(90deg, #2E8B57, #FF8C00, #2E8B57);
        margin: 3rem 0;
        border-radius: 2px;
    }
    .feature-box {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 15px;
        border-left: 6px solid #2E8B57;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .highlight-text {
        color: #2E8B57;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .stats-box {
        background: linear-gradient(135deg, #FF8C00, #FFB347);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2E8B57, #228B22);
    }
</style>
""", unsafe_allow_html=True)

def create_logo():
    """Generate ReUpyog logo programmatically"""
    fig, ax = plt.subplots(figsize=(8, 3), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    
    # Create circular arrows for recycling symbol
    circle1 = plt.Circle((2, 1.5), 0.8, fill=False, color='#2E8B57', linewidth=4)
    circle2 = plt.Circle((2, 1.5), 0.6, fill=False, color='#FF8C00', linewidth=3)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    
    # Add arrows
    ax.annotate('', xy=(2.8, 2.2), xytext=(2.8, 1.8), 
                arrowprops=dict(arrowstyle='->', color='#2E8B57', lw=3))
    ax.annotate('', xy=(1.2, 0.8), xytext=(1.2, 1.2), 
                arrowprops=dict(arrowstyle='->', color='#2E8B57', lw=3))
    
    # Add text
    ax.text(4.5, 1.8, 'ReUpyog', fontsize=32, fontweight='bold', color='#2E8B57')
    ax.text(4.5, 1.2, 'AI-Powered Waste Classification', fontsize=16, color='#FF8C00')
    
    ax.axis('off')
    
    # Save to BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buf.seek(0)
    plt.close()
    
    return buf

def create_architecture_diagram():
    """Generate SAM + YOLOv8 pipeline diagram"""
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
    
    # Define boxes and their positions
    boxes = [
        {'name': 'Input Image\n(Clustered Waste)', 'pos': (1, 4), 'color': '#FFB347'},
        {'name': 'SAM Segmentation\n(Segment Anything)', 'pos': (4, 4), 'color': '#87CEEB'},
        {'name': 'Shadow Detection\n(HSV Analysis)', 'pos': (7, 5.5), 'color': '#DDA0DD'},
        {'name': 'Fragment Merging\n(Distance-based)', 'pos': (7, 2.5), 'color': '#DDA0DD'},
        {'name': 'YOLOv8 Classification\n(22 Categories)', 'pos': (10, 4), 'color': '#98FB98'},
        {'name': 'Confidence Scoring\n(Visual Interface)', 'pos': (13, 4), 'color': '#F0E68C'}
    ]
    
    # Draw boxes
    for box in boxes:
        rect = plt.Rectangle((box['pos'][0]-0.8, box['pos'][1]-0.6), 1.6, 1.2, 
                           facecolor=box['color'], edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(box['pos'][0], box['pos'][1], box['name'], ha='center', va='center', 
                fontsize=10, fontweight='bold', wrap=True)
    
    # Draw arrows
    arrows = [
        ((1.8, 4), (3.2, 4)),
        ((4.8, 4.3), (6.2, 5.2)),
        ((4.8, 3.7), (6.2, 2.8)),
        ((7.8, 5.5), (9.2, 4.3)),
        ((7.8, 2.5), (9.2, 3.7)),
        ((10.8, 4), (12.2, 4))
    ]
    
    for arrow in arrows:
        ax.annotate('', xy=arrow[1], xytext=arrow[0],
                   arrowprops=dict(arrowstyle='->', color='#2E8B57', lw=2))
    
    ax.set_xlim(0, 14)
    ax.set_ylim(1, 6)
    ax.set_title('ReUpyog: SAM + YOLOv8 Hybrid Architecture', 
                fontsize=18, fontweight='bold', color='#2E8B57', pad=20)
    ax.axis('off')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buf.seek(0)
    plt.close()
    
    return buf

def create_comparison_chart():
    """Generate dataset comparison visualization"""
    data = {
        'Dataset': ['TrashNet', 'E-waste Studies', 'Typical Research', 'ReUpyog'],
        'Images': [2527, 12000, 15000, 213000],
        'Classes': [6, 13, 10, 22],
        'Scale_Factor': [1, 4.7, 5.9, 84.3]
    }
    
    fig = go.Figure(data=[
        go.Bar(name='Images (thousands)', x=data['Dataset'], 
               y=[x/1000 for x in data['Images']], 
               marker_color=['#FFB347', '#87CEEB', '#DDA0DD', '#2E8B57']),
        go.Bar(name='Classes', x=data['Dataset'], y=data['Classes'],
               marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FF8C00'],
               yaxis='y2')
    ])
    
    fig.update_layout(
        title='ReUpyog vs. Existing Datasets',
        xaxis_title='Datasets',
        yaxis=dict(title='Images (thousands)', side='left'),
        yaxis2=dict(title='Number of Classes', side='right', overlaying='y'),
        legend=dict(x=0.02, y=0.98),
        height=500,
        template='plotly_white'
    )
    
    return fig

def create_performance_metrics():
    """Generate performance metrics visualization"""
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    values = [99.09, 99.12, 99.05, 99.08]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=metrics,
        fill='toself',
        line_color='#2E8B57',
        fillcolor='rgba(46, 139, 87, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[95, 100])
        ),
        title="ReUpyog Performance Metrics",
        height=400
    )
    
    return fig

def create_waste_categories():
    """Generate 22 waste categories visualization"""
    categories = [
        'Paper', 'Cardboard', 'Plastic', 'Metal', 'Glass', 'Organic',
        'Electronics', 'Battery', 'Clothes', 'Shoes', 'Medical',
        'Hazardous', 'Wood', 'Rubber', 'Ceramic', 'Textile',
        'LDPA', 'PET', 'Vegetation', 'Mixed', 'Construction', 'Chemical'
    ]
    
    # Create a grid visualization
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
    
    # Create a grid of colored rectangles
    colors = plt.cm.Set3(np.linspace(0, 1, 22))
    
    for i, (cat, color) in enumerate(zip(categories, colors)):
        row, col = divmod(i, 6)
        rect = plt.Rectangle((col, 3-row), 0.9, 0.9, facecolor=color, 
                           edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        ax.text(col+0.45, 3-row+0.45, cat, ha='center', va='center', 
                fontsize=9, fontweight='bold')
    
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.set_title('22 Waste Categories in ReUpyog Dataset', 
                fontsize=16, fontweight='bold', color='#2E8B57')
    ax.axis('off')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buf.seek(0)
    plt.close()
    
    return buf

def main():
    # Create logo and display
    logo_buf = create_logo()
    logo_img = Image.open(logo_buf)
    
    # Display logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo_img, use_column_width=True)
    
    # Sidebar Navigation
    st.sidebar.markdown("# 🌱 Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Choose Section:",
        ["🏠 Project Overview", "📊 Dataset Excellence", "🔬 Technical Innovation", 
         "🎯 Performance Results", "🌍 Applications & Impact"]
    )
    
    # Main content
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

def show_overview():
    """Project Overview Section"""
    st.markdown('<h1 class="main-header">🌱 ReUpyog</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Revolutionary AI-Powered Waste Classification</h2>', unsafe_allow_html=True)
    
    # Hero metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Images",
            value="213,000",
            delta="84x larger than TrashNet"
        )
    
    with col2:
        st.metric(
            label="🗂️ Categories",
            value="22 Classes",
            delta="+9 vs standard studies"
        )
    
    with col3:
        st.metric(
            label="🎯 Accuracy",
            value="99.09%",
            delta="Industry-leading"
        )
    
    with col4:
        st.metric(
            label="💾 Dataset Size",
            value="19 GB",
            delta="Enterprise-scale"
        )
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Project description with generated architecture
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🚀 Revolutionary Multi-Object Detection</h3>
        <p class="highlight-text">ReUpyog transforms waste management through AI-powered classification that handles real-world clustered images, not just single objects.</p>
        
        <strong>Key Innovations:</strong><br>
        • SAM + YOLOv8 hybrid architecture for multi-object processing<br>
        • Advanced shadow detection and fragment merging<br>
        • Production-ready deployment with cross-platform compatibility<br>
        • Real-time confidence scoring with visual interface<br>
        • 213,000 image training dataset - largest in research
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Display generated architecture diagram
        arch_buf = create_architecture_diagram()
        arch_img = Image.open(arch_buf)
        st.image(arch_img, caption="SAM + YOLOv8 Hybrid Architecture", use_column_width=True)
    
    # Display waste categories
    st.subheader("🗂️ Comprehensive Waste Classification")
    waste_buf = create_waste_categories()
    waste_img = Image.open(waste_buf)
    st.image(waste_img, caption="22 Waste Categories Covered by ReUpyog", use_column_width=True)

def show_dataset():
    """Dataset Excellence Section"""
    st.markdown("# 📊 Industry-Leading Dataset Scale")
    
    # Dataset statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🏆 Massive Scale Achievement</h3>
        <ul>
        <li><strong>213,000 total images</strong> - Largest waste dataset in research</li>
        <li><strong>22 waste categories</strong> - Most comprehensive classification</li>
        <li><strong>Professional splits:</strong> 149,393 train / 32,015 val / 32,016 test</li>
        <li><strong>~9,682 images per class</strong> - Ensures statistical significance</li>
        <li><strong>19GB total size</strong> - Enterprise-scale preparation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Add key stats
        st.subheader("📈 Dataset Statistics")
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.metric("Training Images", "149,393", "70% split")
            st.metric("Validation Images", "32,015", "15% split")
        
        with stats_col2:
            st.metric("Test Images", "32,016", "15% split")
            st.metric("Average per Class", "~9,682", "Strong representation")
    
    with col2:
        # Display comparison chart
        comparison_fig = create_comparison_chart()
        st.plotly_chart(comparison_fig, use_container_width=True)
        
        # Competitive advantage
        st.markdown("""
        <div class="feature-box">
        <h3>🥇 Competitive Advantages</h3>
        <ul>
        <li><strong>84x larger</strong> than standard TrashNet dataset</li>
        <li><strong>22 categories</strong> vs typical 6-13 in research</li>
        <li><strong>Real-world ready</strong> with clustered image processing</li>
        <li><strong>Production scale</strong> suitable for industry deployment</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def show_technical():
    """Technical Innovation Section"""
    st.markdown("# 🔬 Advanced Technical Architecture")
    
    # Display main architecture
    arch_buf = create_architecture_diagram()
    arch_img = Image.open(arch_buf)
    st.image(arch_img, caption="Complete ReUpyog Processing Pipeline", use_column_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🤖 Core Technologies</h3>
        <ul>
        <li><strong>YOLOv8 Nano Classification:</strong> Efficient base model for single-object training</li>
        <li><strong>SAM Integration:</strong> Segment Anything Model for precise object boundaries</li>
        <li><strong>Hybrid Pipeline:</strong> Segmentation → Classification workflow</li>
        <li><strong>Alternative Architecture:</strong> Robust deployment solution</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
        <h3>⚡ Advanced Processing Features</h3>
        <ul>
        <li><strong>Shadow Detection:</strong> HSV color space analysis (brightness < 80)</li>
        <li><strong>Fragment Merging:</strong> 80px distance-based clustering algorithm</li>
        <li><strong>Size Filtering:</strong> Minimum 0.5% area threshold</li>
        <li><strong>Confidence Scoring:</strong> 25% minimum reliability threshold</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical specifications
    st.subheader("⚙️ Training & Deployment Specifications")
    
    specs_col1, specs_col2, specs_col3 = st.columns(3)
    
    with specs_col1:
        st.metric("Training Epochs", "45", "Early stopping: 15")
        st.metric("Batch Size", "96", "GPU optimized")
        st.metric("Image Size", "224×224", "Standard classification")
    
    with specs_col2:
        st.metric("Learning Rate", "0.001", "Cosine scheduling")
        st.metric("Model Size", "Nano", "Lightweight deployment")
        st.metric("GPU Memory", "Optimized", "AMP enabled")
    
    with specs_col3:
        st.metric("Output Formats", "2", "PyTorch + ONNX")
        st.metric("Deployment", "Cross-platform", "Production ready")
        st.metric("Inference Speed", "Real-time", "Interactive processing")

def show_results():
    """Performance Results Section - This is where you upload your images"""
    st.markdown("# 🎯 Outstanding Performance Results")
    
    # Key performance metrics
    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    
    with perf_col1:
        st.metric("Overall Accuracy", "99.09%", "Exceptional")
    
    with perf_col2:
        st.metric("F1-Score", "99.08%", "Balanced performance")
    
    with perf_col3:
        st.metric("Training Stability", "Excellent", "No overfitting")
    
    with perf_col4:
        st.metric("Classes Perfect", "Most", "Minimal confusion")
    
    # Performance radar chart
    perf_fig = create_performance_metrics()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(perf_fig, use_container_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 🚨 THIS IS WHERE YOU UPLOAD YOUR CONFUSION MATRIX AND TRAINING CURVES
    st.subheader("📊 Upload Your Model Results")
    st.info("💡 **Upload your confusion matrix and training curves here**")
    
    # Confusion Matrix Upload
    st.markdown("### 📈 Confusion Matrix")
    confusion_matrix = st.file_uploader(
        "Upload your 22x22 confusion matrix image (PNG, JPG)",
        type=['png', 'jpg', 'jpeg'],
        key="confusion_matrix",
        help="Upload the confusion matrix showing 99% accuracy across 22 waste classes"
    )
    
    if confusion_matrix:
        conf_img = Image.open(confusion_matrix)
        st.image(conf_img, caption="🎯 Confusion Matrix - 99.09% Accuracy Across 22 Classes", use_column_width=True)
        st.success("✅ Confusion Matrix uploaded successfully!")
    else:
        st.warning("⬆️ Please upload your confusion matrix image")
    
    # Training Curves Upload
    st.markdown("### 📉 Training Curves")
    training_curves = st.file_uploader(
        "Upload your training curves image (PNG, JPG)",
        type=['png', 'jpg', 'jpeg'], 
        key="training_curves",
        help="Upload the loss/accuracy curves showing training progression over 45 epochs"
    )
    
    if training_curves:
        curves_img = Image.open(training_curves)
        st.image(curves_img, caption="📈 Training Curves - Stable Convergence Over 45 Epochs", use_column_width=True)
        st.success("✅ Training curves uploaded successfully!")
    else:
        st.warning("⬆️ Please upload your training curves image")
    
    # Performance highlights
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🏆 Training Excellence</h3>
        <ul>
        <li><strong>Stable Convergence:</strong> Smooth loss reduction without oscillation</li>
        <li><strong>No Overfitting:</strong> Validation loss follows training closely</li>
        <li><strong>Early Convergence:</strong> High accuracy achieved by epoch 10-15</li>
        <li><strong>Consistent Performance:</strong> All 22 classes show excellent results</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
        <h3>📈 Validation Results</h3>
        <ul>
        <li><strong>Perfect Predictions:</strong> Multiple 100% confidence classifications</li>
        <li><strong>High Reliability:</strong> 89-100% confidence scores typical</li>
        <li><strong>Minimal Confusion:</strong> Clear diagonal patterns in matrix</li>
        <li><strong>Production Ready:</strong> Consistent real-world performance</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def show_applications():
    """Applications & Impact Section"""
    st.markdown("# 🌍 Real-World Applications & Environmental Impact")
    
    # Applications grid
    app_col1, app_col2 = st.columns(2)
    
    with app_col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🏭 Industrial Applications</h3>
        <ul>
        <li><strong>Smart Waste Management:</strong> Automated recycling facilities with 99% accuracy</li>
        <li><strong>IoT Integration:</strong> Intelligent waste bin systems for real-time sorting</li>
        <li><strong>Municipal Services:</strong> Enhanced collection and processing efficiency</li>
        <li><strong>Industrial Automation:</strong> Large-scale waste processing plants</li>
        <li><strong>Environmental Monitoring:</strong> Real-time waste stream analysis</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with app_col2:
        st.markdown("""
        <div class="feature-box">
        <h3>🌱 Environmental Impact</h3>
        <ul>
        <li><strong>Improved Recycling Rates:</strong> Higher accuracy reduces contamination</li>
        <li><strong>Reduced Manual Labor:</strong> Automated classification systems</li>
        <li><strong>Enhanced Purity:</strong> Better waste stream quality for recycling</li>
        <li><strong>Sustainable Processing:</strong> Eco-friendly waste management solutions</li>
        <li><strong>Carbon Footprint:</strong> Reduced transportation and processing costs</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Future roadmap
    st.subheader("🚀 Future Development Roadmap")
    
    future_col1, future_col2, future_col3 = st.columns(3)
    
    with future_col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🔮 Phase 1: Immediate</h3>
        <ul>
        <li>Mobile app development</li>
        <li>Edge device deployment</li>
        <li>Real-time IoT integration</li>
        <li>API development for third-party integration</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with future_col2:
        st.markdown("""
        <div class="feature-box">
        <h3>📈 Phase 2: Scaling</h3>
        <ul>
        <li>Additional waste categories</li>
        <li>Multi-language support</li>
        <li>Global dataset expansion</li>
        <li>Cloud infrastructure scaling</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with future_col3:
        st.markdown("""
        <div class="feature-box">
        <h3>🤝 Phase 3: Partnerships</h3>
        <ul>
        <li>Industry collaborations</li>
        <li>Municipality partnerships</li>
        <li>Research community engagement</li>
        <li>Open-source contributions</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Impact metrics
    st.subheader("📊 Projected Impact Metrics")
    
    impact_col1, impact_col2, impact_col3, impact_col4 = st.columns(4)
    
    with impact_col1:
        st.metric("Waste Sorting Accuracy", "99%+", "vs 70-80% manual")
    
    with impact_col2:
        st.metric("Processing Speed", "Real-time", "vs hours manually")
    
    with impact_col3:
        st.metric("Cost Reduction", "60-80%", "in sorting operations")
    
    with impact_col4:
        st.metric("Environmental Benefit", "Significant", "improved recycling rates")
    
    # Contact and conclusion
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("# 📞 Project Contact & Information")
    
    contact_col1, contact_col2 = st.columns(2)
    
    with contact_col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🔗 Project Links & Resources</h3>
        <ul>
        <li><strong>📧 Email:</strong> your.email@domain.com</li>
        <li><strong>💻 GitHub:</strong> ReUpyog Repository</li>
        <li><strong>📱 LinkedIn:</strong> Professional Profile</li>
        <li><strong>📄 Documentation:</strong> Technical Papers & Guides</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with contact_col2:
        st.markdown("""
        <div class="feature-box">
        <h3>🎯 Key Achievements Summary</h3>
        <ul>
        <li><strong>✅ Largest Dataset:</strong> 213,000 images in waste classification</li>
        <li><strong>✅ Highest Accuracy:</strong> 99.09% across 22 categories</li>
        <li><strong>✅ Real-world Ready:</strong> Multi-object clustered processing</li>
        <li><strong>✅ Production Scale:</strong> Enterprise deployment capability</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
def show_footer():
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🌱 <strong>ReUpyog</strong> - Transforming Waste Management Through AI</p>
    <p>Built with ❤️ for a Sustainable Future | Powered by SAM + YOLOv8 Technology</p>
    <p><em>"213,000 Images • 22 Categories • 99% Accuracy • Production Ready"</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()
