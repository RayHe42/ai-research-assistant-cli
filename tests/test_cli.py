from research_assistant.cli import main


def test_main_importable():
    assert callable(main)
