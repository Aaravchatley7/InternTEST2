import uuid
import time
import logging
import os

os.makedirs(
    "logs",
    exist_ok=True
)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

metrics_data = {
    "total_requests": 0,
    "total_errors": 0,
    "latencies": [],
    "confidences": []
}


def start_trace():

    return {
        "trace_id": str(uuid.uuid4()),
        "start_time": time.time()
    }


def end_trace(trace):

    latency = round(
        (time.time() - trace["start_time"]) * 1000,
        2
    )

    return latency


def log_event(
    event,
    trace_id,
    extra=None
):

    logging.info(
        {
            "event": event,
            "trace_id": trace_id,
            "details": extra
        }
    )


def update_metrics(
    latency,
    confidence
):

    metrics_data["total_requests"] += 1

    metrics_data["latencies"].append(
        latency
    )

    metrics_data["confidences"].append(
        confidence
    )


def record_error():

    metrics_data["total_errors"] += 1


def get_metrics():

    avg_latency = 0

    if metrics_data["latencies"]:
        avg_latency = round(
            sum(metrics_data["latencies"])
            /
            len(metrics_data["latencies"]),
            2
        )

    avg_confidence = 0

    if metrics_data["confidences"]:
        avg_confidence = round(
            sum(metrics_data["confidences"])
            /
            len(metrics_data["confidences"]),
            2
        )

    return {
        "total_requests":
            metrics_data["total_requests"],

        "total_errors":
            metrics_data["total_errors"],

        "average_latency_ms":
            avg_latency,

        "average_confidence":
            avg_confidence
    }