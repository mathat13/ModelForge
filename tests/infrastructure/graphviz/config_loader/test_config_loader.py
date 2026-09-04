import pytest

from blueprint_forge import (
    GraphvizConfigLoader,
    ConfigFileNotFound,
    GraphvizConfig,
)

def test_GraphvizConfigLoader_accepts_existing_files(tmp_path):
    header_path = tmp_path / "header.dot"
    header_text = "header test data."
    header_path.write_text(header_text)

    footer_path = tmp_path / "footer.dot"
    footer_text = "footer test data."
    footer_path.write_text(footer_text)

    # Execution
    config = GraphvizConfigLoader.load(header_path=header_path,
                              footer_path=footer_path
                              )
    
    assert isinstance (config, GraphvizConfig)
    assert footer_text in config.footer
    assert header_text in config.header

def test_GraphvizConfigLoader_rejects_missing_header(tmp_path):
    header_path = tmp_path / "header.dot"

    footer_path = tmp_path / "footer.dot"

    footer_path.write_text(
        """
        footer test data.
        """
    )

    # Execution
    with pytest.raises(ConfigFileNotFound) as exc_info:
        GraphvizConfigLoader.load(header_path=header_path,
                                  footer_path=footer_path
                                  )
        
    assert header_path.as_posix() in str(exc_info.value)
    assert exc_info.value.path == header_path

def test_GraphvizConfigLoader_rejects_missing_footer(tmp_path):
    header_path = tmp_path / "header.dot"

    header_path.write_text(
            """
            header test data.
            """
        )
    
    footer_path = tmp_path / "footer.dot"

    # Execution
    with pytest.raises(ConfigFileNotFound) as exc_info:
        config = GraphvizConfigLoader.load(header_path=header_path,
                                footer_path=footer_path
                                )
        
    assert footer_path.as_posix() in str(exc_info.value)
    assert exc_info.value.path == footer_path