import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set page config for professional appearance
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
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #FF8C00;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(90deg, #2E8B57, #228B22);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #2E8B57, #FF8C00);
        margin: 2rem 0;
        border-radius: 2px;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 1rem 0;
    }
    .highlight-text {
        color: #2E8B57;
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Sidebar Navigation
    st.sidebar.markdown("# 🌱 ReUpyog Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Choose Section:",
        ["🏠 Project Overview", "📊 Dataset Excellence", "🔬 Technical Innovation", 
         "🎯 Performance Results", "🌍 Applications & Impact"]
    )
    
    # Main content based on navigation
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
    st.markdown('<h2 class="sub-header">AI-Powered Smart Waste Classification</h2>', unsafe_allow_html=True)
    
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
    
    # Project description
    st.markdown("""
    <div class="feature-box">
    <h3>🚀 Revolutionary Multi-Object Detection</h3>
    <p class="highlight-text">ReUpyog transforms waste management through AI-powered classification that handles real-world clustered images, not just single objects.</p>
    
    <strong>Key Innovations:</strong>
    • SAM + YOLOv8 hybrid architecture for multi-object processing<br>
    • Advanced shadow detection and fragment merging<br>
    • Production-ready deployment with cross-platform compatibility<br>
    • Real-time confidence scoring with visual interface
    </div>
    """, unsafe_allow_html=True)
    
    # Upload section for overview images
    st.subheader("📸 Project Overview Images")
    st.info("💡 **Upload:** Project logo, system architecture overview, or project summary infographics")
    
    overview_images = st.file_uploader(
        "Upload overview images (PNG, JPG, JPEG)",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="overview_images"
    )
    
    if overview_images:
        cols = st.columns(len(overview_images))
        for i, img in enumerate(overview_images):
            with cols[i]:
                image = Image.open(img)
                st.image(image, caption=img.name, use_column_width=True)

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
        <li><strong>213,000 total images</strong> - Largest waste dataset</li>
        <li><strong>22 waste categories</strong> - Comprehensive classification</li>
        <li><strong>Professional splits:</strong> 70% train, 15% val, 15% test</li>
        <li><strong>~9,682 images per class</strong> - Statistical significance</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create comparison chart
        comparison_data = {
            'Dataset': ['TrashNet', 'E-waste Studies', 'Standard Research', 'ReUpyog'],
            'Images': [2527, 12000, 15000, 213000],
            'Classes': [6, 13, 10, 22]
        }
        
        df = pd.DataFrame(comparison_data)
        fig = px.bar(df, x='Dataset', y='Images', color='Classes',
                    title="Dataset Size Comparison",
                    color_continuous_scale='Viridis')
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Upload section for dataset visualizations
    st.subheader("📈 Dataset Visualization Images")
    st.info("💡 **Upload:** Dataset distribution charts, class samples, data split visualizations, or comparison graphs")
    
    dataset_images = st.file_uploader(
        "Upload dataset visualization images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="dataset_images"
    )
    
    if dataset_images:
        for img in dataset_images:
            image = Image.open(img)
            st.image(image, caption=f"📊 {img.name}", use_column_width=True)
            st.markdown("---")

def show_technical():
    """Technical Innovation Section"""
    st.markdown("# 🔬 Advanced Technical Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🤖 Core Technologies</h3>
        <ul>
        <li><strong>YOLOv8 Nano Classification:</strong> Base model for efficiency</li>
        <li><strong>SAM Integration:</strong> Segment Anything Model for object boundaries</li>
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
        <li><strong>Shadow Detection:</strong> HSV color space analysis</li>
        <li><strong>Fragment Merging:</strong> 80px distance-based clustering</li>
        <li><strong>Size Filtering:</strong> Minimum 0.5% area threshold</li>
        <li><strong>Confidence Scoring:</strong> 25% minimum reliability</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical specifications
    st.subheader("⚙️ Training Specifications")
    
    specs_col1, specs_col2, specs_col3 = st.columns(3)
    
    with specs_col1:
        st.metric("Epochs", "45", "Early stopping: 15")
        st.metric("Batch Size", "96", "GPU optimized")
    
    with specs_col2:
        st.metric("Image Size", "224×224", "Standard classification")
        st.metric("Learning Rate", "0.001", "Cosine scheduling")
    
    with specs_col3:
        st.metric("Model Formats", "2", "PyTorch + ONNX")
        st.metric("Deployment", "Cross-platform", "Production ready")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Upload section for technical diagrams
    st.subheader("🔧 Technical Architecture Images")
    st.info("💡 **Upload:** System architecture diagrams, pipeline flowcharts, model comparison charts, or technical specifications")
    
    tech_images = st.file_uploader(
        "Upload technical diagrams and architecture images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="tech_images"
    )
    
    if tech_images:
        for img in tech_images:
            image = Image.open(img)
            st.image(image, caption=f"🔧 {img.name}", use_column_width=True)
            st.markdown("---")

def show_results():
    """Performance Results Section"""
    st.markdown("# 🎯 Outstanding Performance Results")
    
    # Key performance metrics
    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    
    with perf_col1:
        st.metric("Overall Accuracy", "99.09%", "Exceptional")
    
    with perf_col2:
        st.metric("F1-Score", "99.08%", "Balanced performance")
    
    with perf_col3:
        st.metric("Classes with 100%", "Most", "Perfect classification")
    
    with perf_col4:
        st.metric("Training Stability", "Excellent", "No overfitting")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Performance highlights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🏆 Training Excellence</h3>
        <ul>
        <li><strong>Stable Convergence:</strong> Smooth loss reduction</li>
        <li><strong>No Overfitting:</strong> Validation follows training</li>
        <li><strong>Early Convergence:</strong> High accuracy by epoch 10</li>
        <li><strong>Consistent Performance:</strong> All 22 classes excel</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
        <h3>📈 Validation Results</h3>
        <ul>
        <li><strong>Perfect Predictions:</strong> 100% confidence achieved</li>
        <li><strong>High Reliability:</strong> 89-100% typical confidence</li>
        <li><strong>Minimal Confusion:</strong> Clear diagonal patterns</li>
        <li><strong>Production Ready:</strong> Consistent real-world performance</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Upload section for performance images
    st.subheader("📊 Performance Visualization Images")
    st.info("💡 **Upload:** Confusion matrices, training curves, accuracy plots, ROC curves, or performance comparison charts")
    
    results_images = st.file_uploader(
        "Upload performance results images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="results_images"
    )
    
    if results_images:
        # Display in a grid layout
        if len(results_images) == 1:
            st.image(Image.open(results_images[0]), caption=f"📊 {results_images[0].name}", use_column_width=True)
        elif len(results_images) == 2:
            col1, col2 = st.columns(2)
            with col1:
                st.image(Image.open(results_images[0]), caption=f"📊 {results_images[0].name}", use_column_width=True)
            with col2:
                st.image(Image.open(results_images[1]), caption=f"📊 {results_images[1].name}", use_column_width=True)
        else:
            for img in results_images:
                image = Image.open(img)
                st.image(image, caption=f"📊 {img.name}", use_column_width=True)
                st.markdown("---")

def show_applications():
    """Applications & Impact Section"""
    st.markdown("# 🌍 Real-World Applications & Impact")
    
    # Applications grid
    app_col1, app_col2 = st.columns(2)
    
    with app_col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🏭 Industrial Applications</h3>
        <ul>
        <li><strong>Smart Waste Management:</strong> Automated recycling facilities</li>
        <li><strong>IoT Integration:</strong> Intelligent waste bin systems</li>
        <li><strong>Municipal Services:</strong> Enhanced collection efficiency</li>
        <li><strong>Industrial Automation:</strong> Large-scale processing</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with app_col2:
        st.markdown("""
        <div class="feature-box">
        <h3>🌱 Environmental Impact</h3>
        <ul>
        <li><strong>Improved Recycling:</strong> Higher accuracy rates</li>
        <li><strong>Reduced Labor:</strong> Automated classification</li>
        <li><strong>Enhanced Purity:</strong> Better waste stream quality</li>
        <li><strong>Sustainable Processing:</strong> Eco-friendly solutions</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Future roadmap
    st.subheader("🚀 Future Development")
    
    future_col1, future_col2, future_col3 = st.columns(3)
    
    with future_col1:
        st.markdown("""
        **🔮 Next Phase**
        - Mobile app development
        - Edge device deployment
        - Real-time IoT integration
        """)
    
    with future_col2:
        st.markdown("""
        **📈 Scaling**
        - Additional waste categories
        - Multi-language support
        - Global deployment
        """)
    
    with future_col3:
        st.markdown("""
        **🤝 Partnerships**
        - Industry collaborations
        - Municipality integration
        - Research community
        """)
    
    # Upload section for application images
    st.subheader("🌍 Application & Impact Images")
    st.info("💡 **Upload:** Use case diagrams, deployment scenarios, impact visualizations, or application mockups")
    
    app_images = st.file_uploader(
        "Upload application and impact images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="app_images"
    )
    
    if app_images:
        for img in app_images:
            image = Image.open(img)
            st.image(image, caption=f"🌍 {img.name}", use_column_width=True)
            st.markdown("---")
    
    # Contact section
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("# 📞 Contact & Learn More")
    
    contact_col1, contact_col2 = st.columns(2)
    
    with contact_col1:
        st.markdown("""
        **🔗 Project Links:**
        - 📧 Email: your.email@domain.com
        - 💻 GitHub: [ReUpyog Repository](https://github.com/yourusername/ReUpyog)
        - 📱 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
        """)
    
    with contact_col2:
        st.markdown("""
        **📄 Documentation:**
        - 📊 Technical Paper: [Research Publication](#)
        - 📈 Dataset Details: [Data Documentation](#)
        - 🔧 Implementation Guide: [Developer Docs](#)
        """)

# Footer
def show_footer():
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🌱 <strong>ReUpyog</strong> - Transforming Waste Management Through AI | Built with ❤️ for a Sustainable Future</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()
