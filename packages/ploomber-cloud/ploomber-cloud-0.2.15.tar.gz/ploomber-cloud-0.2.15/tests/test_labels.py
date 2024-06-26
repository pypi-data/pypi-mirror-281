import sys
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, call

from ploomber_cloud.cli import cli
from ploomber_cloud import api

CMD_NAME = "ploomber-cloud"


@pytest.mark.parametrize(
    "labels, msg",
    (
        (
            ["label-one", "label-two"],
            "Labels added to your project: 'label-one', and 'label-two'",
        ),
        ([], "No labels added to your project."),
    ),
    ids=["labels", "no-labels"],
)
def test_get_all_labels(monkeypatch, set_key, capsys, labels, msg):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "labels"])
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')

    mock_requests_get = Mock(name="requests.get")

    def requests_get(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(
                return_value={
                    "id": "someid",
                    "type": "docker",
                    "labels": labels,
                }
            ),
        )

    mock_requests_get.side_effect = requests_get

    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    assert msg in capsys.readouterr().out
    mock_requests_get.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid",
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )


@pytest.mark.parametrize(
    "labels, msg",
    (
        (
            ["label-one", "label-two"],
            "Labels added to your project: 'label-one', and 'label-two'",
        ),
        ([], "No labels added to your project."),
    ),
    ids=["labels", "no-labels"],
)
def test_get_all_labels_custom_config(monkeypatch, set_key, capsys, labels, msg):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "labels", "--config", "custom.json"])
    Path("custom.json").write_text('{"id": "someid", "type": "docker"}')

    mock_requests_get = Mock(name="requests.get")

    def requests_get(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(
                return_value={
                    "id": "someid",
                    "type": "docker",
                    "labels": labels,
                }
            ),
        )

    mock_requests_get.side_effect = requests_get

    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    assert msg in capsys.readouterr().out
    mock_requests_get.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid",
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )


@pytest.mark.parametrize(
    "cmd, config",
    (
        (
            [CMD_NAME, "labels", "--add", "some-label"],
            {"id": "someid", "type": "docker", "labels": ["some-label"]},
        ),
        (
            [CMD_NAME, "labels", "--add", "some-label", "-a", "another-label"],
            {
                "id": "someid",
                "type": "docker",
                "labels": ["some-label", "another-label"],
            },
        ),
    ),
    ids=["single-label", "multiple-label"],
)
def test_add_labels(monkeypatch, set_key, cmd, config):
    monkeypatch.setattr(sys, "argv", cmd)
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == config

    mock_requests_put.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid/labels",
                json=config["labels"],
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )


def test_update_labels(monkeypatch, set_key):
    monkeypatch.setattr(
        sys, "argv", [CMD_NAME, "labels", "--add", "label-three", "-a", "label-four"]
    )
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", ' '"type": "docker", ' '"labels": ["label-one", "label-two"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == {
            "id": "someid",
            "type": "docker",
            "labels": ["label-one", "label-two", "label-three", "label-four"],
        }
    mock_requests_put.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid/labels",
                json=["label-one", "label-two", "label-three", "label-four"],
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )


def test_labels_already_added(monkeypatch, set_key, capsys):
    monkeypatch.setattr(
        sys, "argv", [CMD_NAME, "labels", "--add", "label-one", "--add", "label-three"]
    )
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", ' '"type": "docker", ' '"labels": ["label-one", "label-two"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == {
            "id": "someid",
            "type": "docker",
            "labels": ["label-one", "label-two", "label-three"],
        }
    assert (
        """Successfully updated. New set of labels: 'label-one', \
'label-three', and 'label-two'.
"""
        in capsys.readouterr().out
    )
    mock_requests_put.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid/labels",
                json=["label-one", "label-two", "label-three"],
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )


def test_add_duplicate_labels(monkeypatch, set_key, capsys):
    monkeypatch.setattr(
        sys, "argv", [CMD_NAME, "labels", "--add", "label-two", "--add", "label-two"]
    )
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", "labels": ["label-one"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == {
            "id": "someid",
            "type": "docker",
            "labels": ["label-one", "label-two"],
        }
    assert (
        """Successfully updated. New set of labels: 'label-one', \
and 'label-two'.
"""
        in capsys.readouterr().out
    )
    mock_requests_put.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid/labels",
                json=["label-one", "label-two"],
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )


def test_labels_already_exist(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "labels", "--add", "label-one"])
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", ' '"type": "docker", ' '"labels": ["label-one", "label-two"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == {
            "id": "someid",
            "type": "docker",
            "labels": ["label-one", "label-two"],
        }
    assert (
        """Error: All labels already added. Please try adding a new label.
"""
        in capsys.readouterr().err
    )


@pytest.mark.parametrize(
    "cmd, config",
    (
        (
            [CMD_NAME, "labels", "--delete", "label-two"],
            {"id": "someid", "type": "docker", "labels": ["label-one", "label-three"]},
        ),
        (
            [CMD_NAME, "labels", "--delete", "label-one", "-d", "label-three"],
            {
                "id": "someid",
                "type": "docker",
                "labels": ["label-two"],
            },
        ),
    ),
    ids=["single-label", "multiple-labels"],
)
def test_delete_labels(monkeypatch, set_key, cmd, config):
    monkeypatch.setattr(sys, "argv", cmd)
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", '
        '"labels": ["label-one", "label-two", "label-three"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == config
    mock_requests_put.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid/labels",
                json=config["labels"],
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )


def test_delete_all_labels(monkeypatch, set_key, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            CMD_NAME,
            "labels",
            "--delete",
            "label-one",
            "-d",
            "label-three",
            "-d",
            "label-two",
        ],
    )
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", '
        '"labels": ["label-one", "label-two", "label-three"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == {"id": "someid", "type": "docker"}
    mock_requests_put.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid/labels",
                json=[],
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )
    assert "All labels of the project have been deleted." in capsys.readouterr().out


def test_delete_missing_label_warning(monkeypatch, set_key, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [CMD_NAME, "labels", "--delete", "label-one", "-d", "label-three"],
    )
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", ' '"labels": ["label-one", "label-two"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == {
            "id": "someid",
            "type": "docker",
            "labels": ["label-two"],
        }
    assert (
        "WARNING: Skipping deletion of non-existing labels: "
        "'label-three'" in capsys.readouterr().out
    )


def test_delete_label_error(monkeypatch, set_key, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [CMD_NAME, "labels", "--delete", "missing"],
    )
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", ' '"labels": ["label-one", "label-two"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == {
            "id": "someid",
            "type": "docker",
            "labels": ["label-one", "label-two"],
        }
    assert (
        "Failed to delete labels as they are not "
        "associated with the project" in capsys.readouterr().err
    )


@pytest.mark.parametrize(
    "cmd, config",
    (
        (
            [CMD_NAME, "labels", "--add", "label-three", "--delete", "label-one"],
            {"id": "someid", "type": "docker", "labels": ["label-two", "label-three"]},
        ),
        (
            [
                CMD_NAME,
                "labels",
                "--add",
                "label-three",
                "--delete",
                "label-one",
                "-a",
                "label-four",
            ],
            {
                "id": "someid",
                "type": "docker",
                "labels": ["label-two", "label-three", "label-four"],
            },
        ),
    ),
    ids=["one-each", "multiple-adds"],
)
def test_add_and_delete_labels(monkeypatch, set_key, cmd, config):
    monkeypatch.setattr(sys, "argv", cmd)
    Path("ploomber-cloud.json").touch()
    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", ' '"labels": ["label-one", "label-two"]}'
    )

    mock_requests_put = Mock(name="requests.put")

    def requests_put(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value={"id": "someid", "type": "docker"}))

    mock_requests_put.side_effect = requests_put

    monkeypatch.setattr(api.requests, "put", mock_requests_put)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    with open("ploomber-cloud.json") as f:
        assert json.loads(f.read()) == config
    mock_requests_put.assert_has_calls(
        [
            call(
                "https://cloud-prod.ploomber.io/projects/someid/labels",
                json=config["labels"],
                headers={"accept": "application/json", "api_key": "somekey"},
            )
        ]
    )
