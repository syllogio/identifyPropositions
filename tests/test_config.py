from identifyPropositions import config


def test_config_get_existing():
    assert config.get("model_name") == "en_core_web_sm"


def test_config_get_missing():
    assert config.get("i_do_not_exist") is None
