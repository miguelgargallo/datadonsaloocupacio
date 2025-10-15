---
marp: true
theme: default
class: 
  - lead
  - invert
paginate: true
backgroundColor: #0a0a0a
color: #ffffff
style: |
  @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700;900&display=swap');
  
  section {
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    background: radial-gradient(circle at 20% 80%, #FF6B35 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, #00D4FF 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, #7C3AED 0%, transparent 50%),
                linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    color: #ffffff;
    justify-content: center;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  
  section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      linear-gradient(45deg, transparent 30%, rgba(0,212,255,0.1) 50%, transparent 70%),
      linear-gradient(-45deg, transparent 30%, rgba(255,107,53,0.1) 50%, transparent 70%);
    pointer-events: none;
    animation: pulse 4s ease-in-out infinite alternate;
  }
  
  @keyframes pulse {
    0% { opacity: 0.3; }
    100% { opacity: 0.7; }
  }
  
  h1 {
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(45deg, #FF6B35, #00D4FF, #7C3AED, #10B981);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
    animation: gradientShift 3s ease infinite;
    text-shadow: 0 0 30px rgba(255,107,53,0.5);
  }
  
  @keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
  
  h2 {
    font-size: 3rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
    text-shadow: 0 0 20px rgba(0,212,255,0.6);
  }
  
  h3 {
    font-size: 1.8rem;
    font-weight: 600;
    background: linear-gradient(90deg, #00D4FF, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2rem;
    letter-spacing: 0.01em;
  }
  
  .hero {
    background: 
      radial-gradient(circle at 30% 70%, #FF6B35 0%, transparent 60%),
      radial-gradient(circle at 70% 30%, #00D4FF 0%, transparent 60%),
      linear-gradient(135deg, #0a0a0a 0%, #2D1B69 50%, #0a0a0a 100%);
    padding: 4rem 2rem;
    position: relative;
  }
  
  .hero::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, #00D4FF20, transparent);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: rotate 10s linear infinite;
  }
  
  @keyframes rotate {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to { transform: translate(-50%, -50%) rotate(360deg); }
  }
  
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    margin: 2rem 0;
    z-index: 2;
    position: relative;
  }
  
  .feature-card {
    background: linear-gradient(145deg, 
      rgba(255,107,53,0.15) 0%, 
      rgba(0,212,255,0.15) 50%, 
      rgba(124,58,237,0.15) 100%);
    border-radius: 20px;
    padding: 2rem;
    border: 2px solid;
    border-image: linear-gradient(45deg, #FF6B35, #00D4FF, #7C3AED) 1;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .feature-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 60px rgba(0,212,255,0.3);
  }
  
  .feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s;
  }
  
  .feature-card:hover::before {
    left: 100%;
  }
  
  .metric {
    font-size: 5rem;
    font-weight: 900;
    background: linear-gradient(45deg, #FF6B35, #00D4FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(255,107,53,0.5);
    animation: glow 2s ease-in-out infinite alternate;
  }
  
  @keyframes glow {
    from { filter: brightness(1) saturate(1); }
    to { filter: brightness(1.2) saturate(1.3); }
  }
  
  .company-logo {
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(45deg, #FF6B35, #00D4FF, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    animation: logoGlow 3s ease-in-out infinite;
  }
  
  @keyframes logoGlow {
    0%, 100% { filter: drop-shadow(0 0 10px rgba(255,107,53,0.7)); }
    50% { filter: drop-shadow(0 0 20px rgba(0,212,255,0.7)); }
  }
  
  .tagline {
    font-size: 1.2rem;
    color: #A0AEC0;
    font-weight: 400;
    background: linear-gradient(90deg, #00D4FF, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .cta-button {
    background: linear-gradient(45deg, #FF6B35, #00D4FF);
    color: white;
    padding: 1.2rem 3rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 1.2rem;
    border: none;
    margin-top: 2rem;
    display: inline-block;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(255,107,53,0.4);
    position: relative;
    overflow: hidden;
  }
  
  .cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(0,212,255,0.6);
  }
  
  .cta-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
  }
  
  .cta-button:hover::before {
    left: 100%;
  }
  
  .tech-stack {
    background: linear-gradient(135deg, #7C3AED, #2D1B69);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    border: 2px solid #00D4FF;
    position: relative;
  }
  
  .tech-stack::before {
    content: '';
    position: absolute;
    inset: -2px;
    background: linear-gradient(45deg, #FF6B35, #00D4FF, #7C3AED, #10B981);
    border-radius: 20px;
    z-index: -1;
    animation: borderGlow 2s linear infinite;
  }
  
  @keyframes borderGlow {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
  }
  
  .impact-section {
    background: linear-gradient(135deg, #FF6B35, #FF8E53);
    border-radius: 20px;
    padding: 3rem;
    color: white;
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
  }
  
  .impact-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: rotate 8s linear infinite;
  }
  
  .roadmap-item {
    background: rgba(0,212,255,0.1);
    border-left: 4px solid #00D4FF;
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 0 15px 15px 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
  }
  
  .roadmap-item:hover {
    background: rgba(0,212,255,0.2);
    transform: translateX(10px);
  }
  
  .final-cta {
    background: 
      radial-gradient(circle at 20% 20%, #FF6B35 0%, transparent 50%),
      radial-gradient(circle at 80% 80%, #7C3AED 0%, transparent 50%),
      linear-gradient(45deg, #0a0a0a, #2D1B69);
    border-radius: 25px;
    padding: 4rem;
    text-align: center;
    color: white;
    margin: 3rem 0;
    border: 3px solid;
    border-image: linear-gradient(45deg, #FF6B35, #00D4FF, #7C3AED) 1;
    position: relative;
    overflow: hidden;
  }
  
  .final-cta::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.05) 50%, transparent 70%);
    animation: sweep 3s ease-in-out infinite;
  }
  
  @keyframes sweep {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }

---

<!-- _class: hero -->

# Water Intelligence
### *Redefining Urban Consumption Analytics*

**Transforming Barcelona's Water Data into Strategic Insights**

<div class="company-logo">CONAN DATA</div>
<div class="tagline">Data Consultancy • Barcelona • 2024</div>

---

## The Challenge

<div class="feature-grid">
<div class="feature-card">

### 🔥 **Data Complexity**
Multiple districts, usage types, and consumption patterns create analytical chaos

</div>
<div class="feature-card">

### ⚡ **Real-time Demands**
Decision makers need instant access to consumption insights NOW

</div>
<div class="feature-card">

### 🎯 **Strategic Impact**
Water management directly affects urban sustainability and economic efficiency

</div>
<div class="feature-card">

### 💎 **Intelligence Gap**
Raw data needs transformation into clear, actionable strategic recommendations

</div>
</div>

---

## Our Revolution

### **Water Consumption Analytics Dashboard**

**Real-time intelligence platform engineered for Barcelona's water ecosystem**

<div class="tech-stack">

- **Interactive visualization** of consumption patterns
- **District-by-district** performance analysis  
- **Predictive insights** and trend identification
- **Executive-ready** reporting capabilities

</div>

---

## Power Features

<div class="feature-grid">
<div class="feature-card">

### 🚀 **Instant Analytics**
Real-time dashboard with interactive filtering and live visualization

</div>
<div class="feature-card">

### 🔮 **Predictive Intelligence**
Advanced time-series analysis reveals consumption trends and future patterns

</div>
<div class="feature-card">

### 🎨 **Executive Design**
Apple-inspired interface ensures professional presentation to stakeholders

</div>
<div class="feature-card">

### ⚡ **Tesla Performance**
Lightning-fast data processing and visualization rendering

</div>
</div>

---

## The Numbers

<div style="display: flex; justify-content: space-around; align-items: center; margin: 3rem 0;">

<div style="text-align: center;">
<div class="metric">365</div>
<div style="color: #00D4FF; font-weight: 600;">Days of Data</div>
</div>

<div style="text-align: center;">
<div class="metric">10+</div>
<div style="color: #FF6B35; font-weight: 600;">Districts Analyzed</div>
</div>

<div style="text-align: center;">
<div class="metric">3</div>
<div style="color: #7C3AED; font-weight: 600;">Usage Categories</div>
</div>

</div>

### Comprehensive coverage of Barcelona's water consumption ecosystem

---

## Live Dashboard Experience

<div class="impact-section">

### **Interactive Intelligence Platform**

- **Time-series Analysis**: Consumption patterns over time
- **District Comparison**: Performance across Barcelona neighborhoods  
- **Usage Breakdown**: Commercial, Domestic, and Industrial insights
- **Heat Maps**: Visual consumption intensity mapping

**Built with Streamlit + Plotly for maximum interactivity**

</div>

---

## Technology Powerhouse

<div class="feature-grid">
<div class="feature-card">

### 🖥️ **Frontend**
Streamlit with custom Apple-inspired CSS styling

</div>
<div class="feature-card">

### 📊 **Analytics Engine**
Pandas, NumPy for high-performance data processing

</div>
<div class="feature-card">

### 📈 **Visualization**
Plotly for interactive, publication-ready charts

</div>
<div class="feature-card">

### ⚙️ **Architecture**
Modular, scalable design for enterprise deployment

</div>
</div>

---

## Business Impact

<div class="impact-section">

### **Strategic Value Creation**

**For Water Utilities:**
- Optimize resource allocation across districts
- Identify peak usage patterns for capacity planning
- Monitor efficiency metrics in real-time

**For City Planners:**
- Support sustainable urban development initiatives
- Analyze consumption trends for infrastructure investment
- Generate data-driven policy recommendations

**For Executive Teams:**
- Access professional reports for board presentations
- Track KPIs with visual performance dashboards
- Make informed strategic decisions with confidence

</div>

---

## Why Conan Data?

<div class="feature-grid">
<div class="feature-card">

### 🎯 **Catalan Expertise**
Deep understanding of local market needs and regulatory requirements

</div>
<div class="feature-card">

### 🚀 **Startup Velocity**
Rapid development cycles and innovative solution approaches

</div>
<div class="feature-card">

### 🏆 **Enterprise Quality**
Professional-grade deliverables with startup flexibility

</div>
<div class="feature-card">

### 📈 **Growth Partnership**
Long-term consulting relationship focused on your success

</div>
</div>

---

## Implementation Roadmap

<div style="text-align: left; max-width: 900px; margin: 0 auto;">

<div class="roadmap-item">
<strong>Phase 1: Foundation</strong> (Week 1-2)<br>
Data integration, validation, and core dashboard development
</div>

<div class="roadmap-item">
<strong>Phase 2: Enhancement</strong> (Week 3-4)<br>
Advanced analytics, custom styling, and performance optimization
</div>

<div class="roadmap-item">
<strong>Phase 3: Excellence</strong> (Week 5-6)<br>
Predictive modeling, executive reporting, and training delivery
</div>

</div>

---

## Future Vision

<div class="tech-stack">

### **Next-Generation Roadmap**

- **AI Integration**: Machine learning for consumption prediction
- **Mobile Applications**: Native iOS and Android apps
- **API Development**: RESTful services for third-party integration
- **Real-time Streaming**: Live data connection capabilities

### **Scalability Ready**
Built to evolve with your organization's growing needs

</div>

---

## Transform Your Data

<div class="final-cta">

### **Ready to revolutionize your water consumption intelligence?**

**Schedule a consultation with Conan Data TODAY**

<div class="cta-button">🚀 Start Your Data Revolution</div>

### Contact Information
**Email**: hello@conandata.com  
**Location**: Barcelona, Catalunya  
**Expertise**: Data Strategy • Analytics • Visualization

</div>

---

<!-- _class: hero -->

# Gràcies!

### **Questions & Live Demo**

<div class="company-logo">CONAN DATA</div>
<div class="tagline">Transforming Data into Strategic Advantage</div>

**Barcelona • 2024**
