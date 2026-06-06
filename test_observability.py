import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from observability import (
    start_trace,
    end_trace,
    get_metrics,
    update_metrics
)


def test_trace_creation():

    trace = start_trace()

    assert "trace_id" in trace
    assert "start_time" in trace


def test_latency_calculation():

    trace = start_trace()

    latency = end_trace(trace)

    assert latency >= 0


def test_metrics_update():

    update_metrics(
        latency=100,
        confidence=0.9
    )

    metrics = get_metrics()

    assert (
        metrics["total_requests"]
        >= 1
    )