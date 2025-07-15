from unittest.mock import patch, MagicMock

import app.main


@patch("app.main.configure_logging")
@patch("app.main.GitLabAdapter")
@patch("app.main.MistralAdapter")
@patch("app.main.JSONCacheAdapter")
@patch("app.main.start_scheduler")
@patch("app.main.settings")
def test_main_calls_dependencies(
    mock_settings,
    mock_start_scheduler,
    mock_JSONCacheAdapter,
    mock_MistralAdapter,
    mock_GitLabAdapter,
    mock_configure_logging,
):
    # Arrange
    mock_settings.gitlab_token = "token"
    mock_settings.gitlab_url = "url"
    mock_settings.mistral_api_key = "api_key"
    mock_settings.mistral_model = "model"
    mock_settings.cache_file = "cache.json"
    mock_settings.polling_interval = 42

    # Act
    app.main.main()

    # Assert
    mock_configure_logging.assert_called_once()
    mock_GitLabAdapter.assert_called_once_with(token="token", base_url="url")
    mock_MistralAdapter.assert_called_once_with(api_key="api_key", model="model")
    mock_JSONCacheAdapter.assert_called_once_with(cache_file="cache.json")
    mock_start_scheduler.assert_called_once()
    args, kwargs = mock_start_scheduler.call_args
    assert callable(args[0])
    assert args[1] == 42


@patch("app.main.start_scheduler")
def test_main_runs_lambda(mock_start_scheduler):
    # Arrange
    fake_gitlab = MagicMock()
    fake_ai = MagicMock()
    fake_cache = MagicMock()
    with (
        patch("app.main.GitLabAdapter", return_value=fake_gitlab),
        patch("app.main.MistralAdapter", return_value=fake_ai),
        patch("app.main.JSONCacheAdapter", return_value=fake_cache),
        patch("app.main.configure_logging"),
        patch("app.main.settings") as mock_settings,
        patch("app.main.run_merge_request_review") as mock_review,
    ):

        mock_settings.gitlab_token = "token"
        mock_settings.gitlab_url = "url"
        mock_settings.mistral_api_key = "api_key"
        mock_settings.mistral_model = "model"
        mock_settings.cache_file = "cache.json"
        mock_settings.polling_interval = 42

        app.main.main()

        # Extract the lambda and call it
        lambda_func = mock_start_scheduler.call_args[0][0]
        lambda_func()
        mock_review.assert_called_once_with(fake_gitlab, fake_ai, fake_cache)
