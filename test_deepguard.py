"""
DeepGuard Test Suite
Demonstrates system functionality with sample deepfake detection
"""

import sys
import os
import uuid
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core import get_orchestrator, MediaType
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def create_sample_image(filename: str, deepfake: bool = False) -> str:
    """Create a sample test image"""
    
    # Create a simple test image
    img = Image.new('RGB', (512, 512), color=(73, 109, 137))
    
    # Add some visual elements
    draw = ImageDraw.Draw(img)
    
    if deepfake:
        # Simulate deepfake with obvious artifacts
        draw.rectangle([100, 100, 400, 400], fill=(255, 100, 100))
        draw.text((150, 250), "DEEPFAKE SAMPLE", fill=(255, 255, 255))
    else:
        # Authentic-looking image
        draw.ellipse([100, 100, 400, 400], fill=(200, 200, 200))
        draw.text((150, 250), "AUTHENTIC SAMPLE", fill=(0, 0, 0))
    
    # Save
    filepath = f"/home/claude/deepguard/uploads/{filename}"
    img.save(filepath)
    
    return filepath


def test_single_detection():
    """Test single media detection"""
    print("=" * 60)
    print("DeepGuard Test - Single Media Detection")
    print("=" * 60)
    print()
    
    # Create sample images
    print("📁 Creating sample test images...")
    authentic_path = create_sample_image("test_authentic.jpg", deepfake=False)
    deepfake_path = create_sample_image("test_deepfake.jpg", deepfake=True)
    print("   ✓ Sample images created")
    print()
    
    # Initialize orchestrator
    print("🤖 Initializing DeepGuard orchestrator...")
    orchestrator = get_orchestrator()
    print("   ✓ Orchestrator ready")
    print()
    
    # Test 1: Authentic image
    print("-" * 60)
    print("TEST 1: Analyzing AUTHENTIC image")
    print("-" * 60)
    
    result1 = orchestrator.analyze_media(
        media_id="test_authentic",
        media_type="image",
        media_path=authentic_path,
        session_id=str(uuid.uuid4())
    )
    
    print(f"\n📊 Results:")
    print(f"   Final Verdict: {result1['final_verdict']}")
    print(f"   Overall Confidence: {result1['overall_confidence']:.2%}")
    print(f"   Human Review Required: {result1['human_review_required']}")
    print(f"   Processing Time: {result1['total_processing_time_ms']:.2f}ms")
    print(f"   Agents Executed: {len(result1['completed_agents'])}")
    print()
    
    # Test 2: Deepfake image
    print("-" * 60)
    print("TEST 2: Analyzing DEEPFAKE image")
    print("-" * 60)
    
    result2 = orchestrator.analyze_media(
        media_id="test_deepfake",
        media_type="image",
        media_path=deepfake_path,
        session_id=str(uuid.uuid4())
    )
    
    print(f"\n📊 Results:")
    print(f"   Final Verdict: {result2['final_verdict']}")
    print(f"   Overall Confidence: {result2['overall_confidence']:.2%}")
    print(f"   Human Review Required: {result2['human_review_required']}")
    print(f"   Processing Time: {result2['total_processing_time_ms']:.2f}ms")
    print(f"   Manipulation Indicators: {len(result2['manipulation_indicators'])}")
    print()
    
    # Display agent logs
    print("-" * 60)
    print("AGENT ACTIVITY LOG (Test 2)")
    print("-" * 60)
    
    for log in result2['agent_logs']:
        print(f"\n🤖 {log['agent_name']}")
        print(f"   Action: {log['action']}")
        print(f"   Confidence: {log['confidence']:.2%}")
        print(f"   Execution Time: {log['execution_time_ms']:.2f}ms")
        if log.get('rai_flags'):
            print(f"   ⚠️  RAI Flags: {', '.join(log['rai_flags'])}")
    
    print()
    print("=" * 60)
    print("✅ Tests completed successfully!")
    print("=" * 60)


def test_rai_compliance():
    """Test RAI compliance features"""
    print()
    print("=" * 60)
    print("DeepGuard Test - RAI Compliance Features")
    print("=" * 60)
    print()
    
    orchestrator = get_orchestrator()
    
    # Check agent configurations
    print("📋 Agent RAI Configurations:")
    print("-" * 60)
    
    for agent_type, config in orchestrator.agent_configs.items():
        print(f"\n{config['name']}")
        print(f"   Enabled: {config['enabled']}")
        print(f"   Confidence Threshold: {config['confidence_threshold']:.2f}")
        print(f"   RAI Principles: {', '.join(config['rai_principles']) if config['rai_principles'] else 'N/A'}")
        print(f"   GPU Required: {config['requires_gpu']}")
    
    print()
    print("=" * 60)
    print("✅ RAI compliance check completed!")
    print("=" * 60)


def test_bias_metrics():
    """Test bias detection and fairness metrics"""
    print()
    print("=" * 60)
    print("DeepGuard Test - Bias & Fairness Metrics")
    print("=" * 60)
    print()
    
    # Create test image
    test_path = create_sample_image("test_bias.jpg", deepfake=False)
    
    orchestrator = get_orchestrator()
    
    result = orchestrator.analyze_media(
        media_id="test_bias",
        media_type="image",
        media_path=test_path,
        session_id=str(uuid.uuid4())
    )
    
    print("📊 Demographic Bias Analysis:")
    print("-" * 60)
    
    for metric in result.get('bias_metrics', []):
        print(f"\nDemographic Group: {metric['demographic_group']}")
        print(f"   False Positive Rate: {metric['false_positive_rate']:.2%}")
        print(f"   False Negative Rate: {metric['false_negative_rate']:.2%}")
        print(f"   Accuracy: {metric['accuracy']:.2%}")
    
    if result.get('fairness_flags'):
        print("\n⚠️  Fairness Alerts:")
        for flag in result['fairness_flags']:
            print(f"   - {flag}")
    else:
        print("\n✅ No fairness violations detected")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    try:
        # Run tests
        test_single_detection()
        test_rai_compliance()
        test_bias_metrics()
        
        print()
        print("🎉 All tests completed successfully!")
        print()
        print("Next steps:")
        print("1. Start the web server: python api.py")
        print("2. Open the web UI: http://localhost:8000/static/index.html")
        print("3. Upload real media files for detection")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
