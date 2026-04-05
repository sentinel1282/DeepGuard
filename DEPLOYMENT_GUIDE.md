# DeepGuard Deployment & Usage Guide

## 📦 Complete System Overview

DeepGuard is a **multi-agentic deepfake detection system** with embedded Responsible AI guardrails. The system consists of:

- **8 Specialized AI Agents** orchestrated via LangGraph
- **6 Core RAI Principles** enforced at every decision point
- **Real-time transparency** showing how agents collaborate
- **Web-based UI** for easy media upload and analysis

---

## 🚀 Quick Deployment

### Method 1: Automated Startup (Recommended)

```bash
cd /home/claude/deepguard
./start.sh
```

The script will:
1. Check Python version
2. Create necessary directories
3. Set up virtual environment
4. Install dependencies
5. Start the API server

### Method 2: Manual Setup

```bash
# 1. Navigate to project
cd /home/claude/deepguard

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create directories
mkdir -p uploads outputs static logs

# 5. Start server
python api.py
```

---

## 🌐 Accessing DeepGuard

Once the server is running, access:

| Interface | URL | Description |
|-----------|-----|-------------|
| **Web UI** | http://localhost:8000/static/index.html | Main user interface |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | System status |
| **RAI Principles** | http://localhost:8000/api/rai/principles | View RAI framework |

---

## 📱 Using the Web Interface

### Step 1: Upload Media

1. Open http://localhost:8000/static/index.html
2. Drag and drop a file or click to browse
3. Supported formats:
   - **Images**: JPG, PNG, BMP, WebP
   - **Videos**: MP4, AVI, MOV, MKV, WebM
   - **Audio**: MP3, WAV, OGG, M4A

### Step 2: Analyze

1. Click **"Analyze for Deepfakes"** button
2. Watch real-time agent activity in the timeline
3. Each agent shows:
   - Current status (Pending → Running → Complete)
   - Confidence score
   - Execution time
   - RAI flags (if any)

### Step 3: Review Results

The system provides:

- **Verdict Card**: Final classification (Authentic / Deepfake / Suspicious / Human Review Required)
- **Confidence Score**: Overall detection confidence (0-100%)
- **Metrics Dashboard**: Processing time, agent count, alerts
- **RAI Compliance**: Fairness flags, governance alerts
- **Explainability Insights**: Grad-CAM and SHAP visualizations

---

## 🔧 API Usage Examples

### Upload Media

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@suspicious_video.mp4"
```

Response:
```json
{
  "success": true,
  "media_id": "abc123...",
  "media_type": "video",
  "filename": "suspicious_video.mp4",
  "file_size": 5242880
}
```

### Analyze Media

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "media_id": "abc123...",
    "media_type": "video"
  }'
```

### Get Agent Status

```bash
curl http://localhost:8000/api/agents/status
```

### View RAI Principles

```bash
curl http://localhost:8000/api/rai/principles | jq
```

---

## 🧪 Running Tests

### Automated Test Suite

```bash
cd /home/claude/deepguard
python test_deepguard.py
```

This will:
1. Create sample images (authentic & deepfake)
2. Run detection on both
3. Display agent logs
4. Show bias metrics
5. Verify RAI compliance

### Expected Output

```
==========================================
DeepGuard Test - Single Media Detection
==========================================

📁 Creating sample test images...
   ✓ Sample images created

🤖 Initializing DeepGuard orchestrator...
   ✓ Orchestrator ready

TEST 1: Analyzing AUTHENTIC image
------------------------------------------------------------
📊 Results:
   Final Verdict: authentic
   Overall Confidence: 78.50%
   Human Review Required: False
   Processing Time: 425.32ms
   Agents Executed: 8

TEST 2: Analyzing DEEPFAKE image
------------------------------------------------------------
📊 Results:
   Final Verdict: deepfake
   Overall Confidence: 87.20%
   Human Review Required: True
   Processing Time: 438.15ms
   Manipulation Indicators: 3
```

---

## 📊 Understanding Results

### Verdict Classifications

| Verdict | Meaning | Action |
|---------|---------|--------|
| **Authentic** | Media appears genuine (confidence < 30%) | Safe to proceed |
| **Deepfake** | Strong indicators of manipulation (confidence > 70%) | Flag for review/block |
| **Suspicious** | Uncertain indicators (30-70% confidence) | Investigate further |
| **Human Review Required** | High-stakes or ambiguous case | Escalate to expert |

### Human Review Triggers

Human review is **automatically triggered** when:

- Deepfake confidence > 85% (high-impact potential)
- Confidence in ambiguous range (40-60%)
- Demographic bias detected (FPR > 10% for any group)
- Critical governance alert raised

### RAI Compliance Indicators

✅ **Green Badge**: All RAI checks passed  
⚠️ **Yellow Badge**: Minor fairness concern  
🛑 **Red Badge**: Critical governance violation

---

## 🎯 Agent Workflow

### Standard Image Analysis Flow

```
1. Orchestrator Agent
   ↓ (Routes to appropriate agents)
2. Visual Forensics Agent
   ↓ (Analyzes visual artifacts)
3. Provenance Verification Agent
   ↓ (Checks metadata)
4. Bias Auditor Agent
   ↓ (Evaluates fairness)
5. Explainability Agent
   ↓ (Generates XAI outputs)
6. Governance & Compliance Agent
   ↓ (RAI validation)
7. Report Generation Agent
   ↓ (Synthesizes findings)
```

### Multi-Modal Video Analysis

For videos, both **Visual Forensics** and **Audio Analysis** agents run in parallel before converging at Provenance Verification.

---

## 🔒 Security & Privacy

### Data Handling

- **Temporary Storage**: Uploaded files stored in `/uploads` (cleared periodically)
- **No Cloud**: All processing happens locally
- **GDPR Aligned**: Minimal data retention, anonymization enabled
- **Audit Logs**: Immutable logs for accountability

### File Validation

- Max file size: 100 MB (configurable in `config.ini`)
- File type verification
- Malware scanning (if enabled)

---

## ⚙️ Configuration

Edit `config.ini` to customize:

```ini
[agents]
visual_forensics_confidence_threshold = 0.7
bias_auditor_demographic_groups = lighter_skin,darker_skin,male,female

[human_review]
high_confidence_deepfake_threshold = 0.85
ambiguous_range_low = 0.40
ambiguous_range_high = 0.60

[rai_principles]
fairness_max_fpr_disparity = 0.10
transparency_xai_required = true
```

---

## 🐛 Troubleshooting

### Issue: Server won't start

**Solution**: Check if port 8000 is available
```bash
lsof -i :8000
kill -9 <PID>  # If occupied
```

### Issue: Upload fails

**Solutions**:
- Check file size (< 100 MB default)
- Verify file format is supported
- Check disk space in `/uploads`

### Issue: Low detection accuracy

**Solutions**:
- Ensure GPU is available (for visual forensics)
- Verify model files are downloaded
- Check confidence thresholds in config

### Issue: Agent timeout

**Solution**: Increase timeout in `config.ini`
```ini
[agents]
visual_forensics_timeout = 180  # Increase from 120
```

---

## 📈 Performance Optimization

### For Faster Processing

1. **Enable GPU**: Set `visual_forensics_gpu = true`
2. **Reduce Resolution**: Preprocess images to 512x512
3. **Parallel Agents**: Configure multi-threading
4. **Cache Models**: Pre-load detection models

### For Better Accuracy

1. **Fine-tune Models**: Train on domain-specific data
2. **Ensemble Methods**: Combine multiple detectors
3. **Adversarial Testing**: Test with known deepfakes
4. **Regular Updates**: Retrain on latest forgery techniques

---

## 🔬 Advanced Usage

### Programmatic API

```python
from core import get_orchestrator

# Initialize
orchestrator = get_orchestrator()

# Analyze
result = orchestrator.analyze_media(
    media_id="custom_001",
    media_type="image",
    media_path="/path/to/image.jpg",
    session_id="session_123"
)

# Access specific agent logs
for log in result['agent_logs']:
    if log['agent_name'] == 'Bias Auditor Agent':
        print(f"Bias metrics: {log['findings']}")

# Check fairness
if result['fairness_flags']:
    print("Fairness concerns detected!")
```

### Custom Agent Configuration

```python
from core.agents import create_agent, AgentConfig

custom_config = AgentConfig(
    name="Custom Forensics Agent",
    enabled=True,
    confidence_threshold=0.8,
    timeout_seconds=150,
    rai_principles=["fairness", "robustness"],
    requires_gpu=True
)

agent = create_agent("visual_forensics", custom_config)
```

---

## 📚 Additional Resources

- **Project Proposal**: `/mnt/user-data/uploads/AAI-531_Group_7_-_DeepGuard_Project_Proposal.pdf`
- **Ethics Presentation**: `/mnt/user-data/uploads/DeepGuard_Ethics_Presentation.pptx`
- **API Documentation**: http://localhost:8000/docs (when server running)
- **Research Papers**: See `README.md` references section

---

## 🤝 Support & Feedback

For issues, questions, or contributions:

1. Check the troubleshooting section above
2. Review the comprehensive `README.md`
3. Examine agent logs in `/logs` directory
4. Contact the project team (Group 7 - AAI-531)

---

## ✅ Deployment Checklist

Before production deployment:

- [ ] Test with diverse media samples
- [ ] Verify all 8 agents functioning correctly
- [ ] Configure appropriate confidence thresholds
- [ ] Set up human review workflows
- [ ] Enable audit logging
- [ ] Configure privacy settings (GDPR compliance)
- [ ] Set up monitoring and alerting
- [ ] Document escalation procedures
- [ ] Train review team on RAI principles
- [ ] Establish responsible disclosure protocol

---

**DeepGuard** - Multi-Agentic Deepfake Detection with Responsible AI Guardrails

*"Trustworthy AI is not a feature — it is the architecture itself."*
