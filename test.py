import os
import pytest

from haaska import HomeAssistant, Configuration


@pytest.fixture
def configuration():
    return Configuration(opts_dict={
        "url": "http://localhost:8123",
        "bearer_token": "",
        "debug": False,
        "ssl_verify": True,
        "ssl_client": "",
        "proxy_url": "http://localhost:1055"
    })


@pytest.fixture
def home_assistant(configuration):
    return HomeAssistant(configuration)


def test_ha_build_url(home_assistant):
    url = home_assistant.build_url("test")
    assert url == "http://localhost:8123/api/test"


def test_get_user_agent(home_assistant):
    os.environ["AWS_DEFAULT_REGION"] = "test"
    user_agent = home_assistant.get_user_agent()
    assert user_agent.startswith(
        "Home Assistant Alexa Smart Home Skill - test - python-requests/"
    )


def test_config_get(configuration):
    assert not configuration.get(["debug"])
    assert configuration.get(["test"]) is None
    assert configuration.get(["test"], default="default") == "default"


def test_proxy_present(home_assistant):
    assert home_assistant.session.proxies == {
        "http": "http://localhost:1055",
        "https": "http://localhost:1055"
    }
