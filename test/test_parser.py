from src.ingestion.parser import parse_transcript


def test_parse_transcript(tmp_path):

    sample_text = """
[00:00:01] John: Build authentication API
[00:00:05] Sarah: Use JWT tokens
"""

    file_path = tmp_path / "sample.txt"

    file_path.write_text(sample_text)

    utterances = parse_transcript(str(file_path))

    assert len(utterances) == 2

    assert utterances[0].speaker == "John"

    assert utterances[1].text == "Use JWT tokens"