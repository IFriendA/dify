"""Tests for Langfuse trace entity models and workflow_trace behaviour."""

from datetime import UTC, datetime

from core.ops.langfuse_trace.entities.langfuse_trace_entity import LangfuseTrace
from core.ops.utils import filter_none_values


class TestLangfuseTraceTimestamp:
    """Tests for the timestamp field on LangfuseTrace."""

    def test_timestamp_defaults_to_none(self):
        """When timestamp is not provided it should default to None."""
        trace = LangfuseTrace(id="t1")
        assert trace.timestamp is None

    def test_timestamp_set_explicitly(self):
        """When a datetime is provided it should be stored as-is."""
        now = datetime.now(tz=UTC)
        trace = LangfuseTrace(id="t1", timestamp=now)
        assert trace.timestamp == now

    def test_timestamp_excluded_by_filter_none_values_when_none(self):
        """filter_none_values should omit timestamp when it is None."""
        trace = LangfuseTrace(id="t1")
        filtered = filter_none_values(trace.model_dump())
        assert "timestamp" not in filtered

    def test_timestamp_included_by_filter_none_values_when_set(self):
        """filter_none_values should include (and ISO-format) timestamp when set."""
        now = datetime.now(tz=UTC)
        trace = LangfuseTrace(id="t1", timestamp=now)
        filtered = filter_none_values(trace.model_dump())
        assert "timestamp" in filtered
        assert filtered["timestamp"] == now.isoformat()


class TestLangfuseTraceAppName:
    """Tests for app-name substitution in trace name and tags."""

    def test_name_defaults_when_app_name_is_none(self):
        """Without an app name, name should be whatever was passed (or None)."""
        trace = LangfuseTrace(id="t1", name="workflow")
        assert trace.name == "workflow"

    def test_tags_is_list(self):
        """Tags should accept a list and round-trip correctly."""
        trace = LangfuseTrace(id="t1", tags=["workflow", "my-app"])
        assert trace.tags == ["workflow", "my-app"]
