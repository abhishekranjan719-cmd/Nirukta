import sys
from pathlib import Path


# Add engine directory to path
engine_path = Path(__file__).parent.parent.parent / "engine"
sys.path.insert(0, str(engine_path))

from app.services.processor import MessageProcessor


def test_processor_basic():
    """Test basic message processing"""
    processor = MessageProcessor()
    response, metadata = processor.process("Hello")

    assert response == "Echo: Hello"
    assert "processed_at" in metadata
    assert "original_message_length" in metadata
    assert metadata["original_message_length"] == 5


def test_processor_transform():
    """Test message transformation"""
    processor = MessageProcessor()
    result = processor.transform("hello world")

    assert result == "HELLO WORLD"


def test_processor_analyze():
    """Test message analysis"""
    processor = MessageProcessor()
    analysis = processor.analyze("Hello world?")

    assert analysis["length"] == 12
    assert analysis["word_count"] == 2
    assert analysis["has_question"] is True


def test_processor_analyze_no_question():
    """Test analysis without question mark"""
    processor = MessageProcessor()
    analysis = processor.analyze("Hello world")

    assert analysis["has_question"] is False


def test_processor_with_context():
    """Test processing with context"""
    processor = MessageProcessor()
    response, metadata = processor.process("Test", context={"user": "test_user"})

    assert response == "Echo: Test"
    assert metadata["processing_type"] == "echo"
