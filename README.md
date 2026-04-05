# DeepGuard: Multi-Agentic Deepfake Detection System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-Academic-orange)

**An Agentic AI Framework for Deepfake Detection and Responsible Media Authenticity**

DeepGuard is a research and development initiative to design, build, and evaluate a responsible Agentic AI system capable of detecting deepfake media — including synthetic images, manipulated videos, and AI-generated audio — in real time.

---

## 🎯 Project Overview

Beyond a purely technical artifact, DeepGuard serves as a case study in embedding ethics, accountability, and fairness directly into AI system design. It explores how agentic architectures can be harnessed not only to detect deception but also to audit their own decisions with full transparency and explainability.

**Team**: Group 7 - AAI-531 Responsible AI  
**Institution**: University of San Diego, Shiley-Marcos School of Engineering  
**Project Lead**: Prashant Khare  
**Team Members**: Prashant Khare, Gaurav Kulkarni, Jasmeet Kaur

---

## 🏗️ Architecture

### Multi-Agent System (8 Specialized Agents)

DeepGuard employs a **LangGraph-based multi-agent pipeline** with eight specialized agents:

1. **Orchestrator Agent** - Coordinates agent workflow, manages StateGraph routing
2. **Visual Forensics Agent** - Detects facial inconsistencies, GAN artifacts using CNN models
3. **Audio Analysis Agent** - Identifies voice-cloning artifacts via spectrogram analysis
4. **Provenance Verification Agent** - Cross-references metadata and digital watermarks
5. **Bias Auditor Agent** - Evaluates detection confidence across demographic groups
6. **Explainability Agent** - Generates Grad-CAM & SHAP visualizations
7. **Governance & Compliance Agent** - Ensures RAI policy alignment
8. **Report Generation Agent** - Synthesizes findings into stakeholder reports

### RAI Principles (6 Core Pillars)

- ⚖️ **Fairness** - Demographic bias testing across age, gender, ethnicity, skin tone
- 📊 **Accountability** - Immutable audit logs, agent-level traceability
- 🔍 **Transparency** - Grad-CAM & SHAP explanations for interpretability
- 🔒 **Privacy** - Minimal biometric retention, GDPR compliance
- 💪 **Robustness** - Adversarial testing, confidence gating
- 🤝 **Non-Maleficence** - Mandatory human-in-the-loop for high-stakes decisions

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js (optional, for extended features)
- 8GB+ RAM recommended
- GPU recommended for visual forensics (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/deepguard.git
cd deepguard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads static outputs
```

### Running DeepGuard

#### 1. Start the Backend API

```bash
# From the deepguard directory
python api.py
```

The API will be available at `http://localhost:8000`

#### 2. Open the Web UI

Navigate to: `http://localhost:8000/static/index.html`

Or serve the static files separately:

```bash
# Using Python's built-in server
cd static
python -m http.server 8080
```

Then open `http://localhost:8080/index.html`

---

## 📊 Usage Examples

### Via Web UI

1. **Upload Media**: Drag and drop an image/video/audio file
2. **Analyze**: Click "Analyze for Deepfakes"
3. **Review Results**: See real-time agent activity and detection verdict
4. **Check Explanations**: Review Grad-CAM and SHAP insights

### Via Python API

```python
from core import get_orchestrator

# Initialize orchestrator
orchestrator = get_orchestrator()

# Analyze media
result = orchestrator.analyze_media(
    media_id="test_001",
    media_type="image",
    media_path="path/to/image.jpg",
    session_id="session_123"
)

# Access results
print(f"Verdict: {result['final_verdict']}")
print(f"Confidence: {result['overall_confidence']:.2%}")
print(f"Human Review Required: {result['human_review_required']}")
```

### Via REST API

```bash
# Upload file
curl -X POST http://localhost:8000/api/upload \
  -F "file=@deepfake_sample.jpg"

# Analyze
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"media_id":"<media_id>","media_type":"image"}'

# Get RAI principles
curl http://localhost:8000/api/rai/principles

# Check agent status
curl http://localhost:8000/api/agents/status
```

---

## 🔬 Technical Stack

### Core Framework
- **LangGraph** - Multi-agent orchestration
- **LangChain** - Agent communication
- **FastAPI** - REST API backend
- **Pydantic** - Data validation

### Deep Learning & Computer Vision
- **PyTorch** - Deep learning framework
- **torchvision** - Computer vision utilities
- **OpenCV** - Image/video processing
- **FaceNet-PyTorch** - Face detection
- **timm** - Vision model zoo (EfficientNet-B4)

### Explainability
- **Grad-CAM** - Visual explanations
- **SHAP** - Feature importance
- **Captum** - Model interpretability

### Audio Processing
- **librosa** - Audio analysis
- **soundfile** - Audio I/O

---

## 📁 Project Structure

```
deepguard/
├── core/
│   ├── __init__.py          # Package initialization
│   ├── state.py             # State management & type definitions
│   ├── agents.py            # 8 specialized agent implementations
│   └── orchestrator.py      # LangGraph workflow orchestration
├── static/
│   └── index.html           # Web UI (Outstanding HTML interface)
├── uploads/                 # Uploaded media storage
├── outputs/                 # Generated reports & visualizations
├── api.py                   # FastAPI backend server
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🧪 Datasets Used

For production deployment, DeepGuard is designed to work with:

1. **FaceForensics++** - Facial manipulation detection
2. **DFDC (DeepFake Detection Challenge)** - Large-scale deepfake dataset
3. **DGM4** - Demographic-balanced deepfake dataset
4. **Custom datasets** - Domain-specific media

**Note**: Due to licensing and institutional access requirements, dataset downloads are not included in this repository. Please request access directly from the dataset providers.

---

## 🎯 Key Features

### ✅ Real-Time Agent Transparency
- Live visualization of agent activity
- Timeline view showing each agent's progress
- Confidence scores and execution times

### ✅ Comprehensive RAI Compliance
- Demographic bias auditing
- Fairness metrics across age, gender, ethnicity
- Privacy-preserving analysis

### ✅ Explainable AI (XAI)
- Grad-CAM heatmaps showing detection focus areas
- SHAP feature importance rankings
- Natural language explanations for non-experts

### ✅ Human-in-the-Loop
- Automatic escalation for ambiguous cases
- High-stakes detection review workflows
- Governance alert system

### ✅ Multi-Modal Detection
- Image deepfake detection
- Video manipulation detection
- Audio voice-cloning detection

---

## 📈 Responsible AI Evaluation

DeepGuard is evaluated across **12 RAI governance dimensions**:

1. Fairness & Non-Discrimination
2. Transparency & Explainability
3. Accountability
4. Privacy & Data Minimization
5. Robustness & Security
6. Safety
7. Human Oversight
8. Societal Impact
9. Data Governance
10. Dual-Use Risk Management
11. Environmental Sustainability
12. Legal & Regulatory Compliance

---

## ⚠️ Ethical Considerations

### Dual-Use Tension
The same technical knowledge enabling detection also accelerates generation. DeepGuard follows **responsible disclosure protocols** and explores dynamic adaptation strategies.

### Surveillance Concerns
Deploying deepfake detectors at scale raises privacy concerns. DeepGuard analyzes the tension between protective use and invasive overreach, drawing on EU AI Act classifications.

### Accountability Gaps
Multi-agent architectures introduce novel accountability challenges. DeepGuard specifically examines how agentic design choices can either amplify or mitigate these gaps.

---

## 🔮 Future Enhancements

- [ ] Integration with blockchain for immutable provenance tracking
- [ ] Real-time video stream analysis
- [ ] Multi-language support for global deployment
- [ ] Advanced adversarial training against evolving deepfakes
- [ ] Federated learning for privacy-preserving model updates
- [ ] Integration with content moderation platforms
- [ ] Mobile application for on-the-go detection

---

## 📚 References

1. Rossler et al. (2019). FaceForensics++: Learning to Detect Manipulated Facial Images. ICCV 2019.
2. Dolhansky et al. (2020). The DeepFake Detection Challenge (DFDC) Dataset.
3. European Commission (2024). Regulation (EU) 2024/1689 — EU Artificial Intelligence Act.
4. Selvaraju et al. (2017). Grad-CAM: Visual Explanations from Deep Networks.
5. Lundberg & Lee (2017). A Unified Approach to Interpreting Model Predictions (SHAP).
6. Chase, H. (2023). LangGraph: Multi-Agent Orchestration Framework.

---

## 🤝 Contributing

This is an academic research project for AAI-531 (Responsible AI) at the University of San Diego. 

For collaboration inquiries, please contact the team lead.

---

## 📄 License

Academic use only. See project documentation for details.

---

## 🙏 Acknowledgments

- **University of San Diego** - Shiley-Marcos School of Engineering
- **AAI-531 Course** - Ethics in AI
- **Accenture RAI Center of Excellence** - Professional insights and expertise

---

## 📞 Contact

**Project Lead**: Prashant Khare  
**Team**: Group 7 - AAI-531  
**Institution**: University of San Diego

---

**DeepGuard** - *Restoring Trust in Authentic Media through Responsible AI*

🛡️ Protecting truth. Preserving trust. Promoting fairness.
