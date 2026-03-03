"""Test that LangFuseDataTrace.trace() skips GenerateNameTraceInfo."""

from unittest.mock import MagicMock, patch

from core.ops.entities.trace_entity import GenerateNameTraceInfo
from core.ops.langfuse_trace.langfuse_trace import LangFuseDataTrace


class TestSkipGenerateNameTrace:
    """Verify that generate_name_trace is not dispatched by trace()."""

    @patch.object(LangFuseDataTrace, "__init__", lambda self, *a, **kw: None)
    def test_generate_name_trace_not_called(self):
        """trace() should return early for GenerateNameTraceInfo without calling generate_name_trace."""
        instance = LangFuseDataTrace.__new__(LangFuseDataTrace)
        instance.generate_name_trace = MagicMock()

        trace_info = MagicMock(spec=GenerateNameTraceInfo)
        instance.trace(trace_info)

        instance.generate_name_trace.assert_not_called()
