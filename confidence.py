def confidence_level(score):

    if score >= 0.85:
        return "High"

    if score >= 0.65:
        return "Medium"

    return "Low"


def calculate_confidence_v2(scores, answer):

    similarities = [
        float(1 / (1 + float(score)))
        for score in scores
    ]

    avg_similarity = sum(similarities) / len(similarities)

    source_coverage = min(len(scores) / 4, 1)

    answer_length_score = min(
        len(answer) / 200,
        1
    )

    source_count_score = min(
        len(scores) / 4,
        1
    )

    confidence = (
        avg_similarity * 0.4 +
        source_coverage * 0.3 +
        answer_length_score * 0.15 +
        source_count_score * 0.15
    )

    reasons = []

    if avg_similarity > 0.8:
        reasons.append(
            "High retrieval similarity"
        )

    if source_count_score > 0.5:
        reasons.append(
            "Multiple supporting sources"
        )

    if answer_length_score > 0.5:
        reasons.append(
            "Complete answer generated"
        )

    return {
        "score": float(round(confidence, 2)),
        "level": confidence_level(confidence),
        "avg_similarity": float(
            round(avg_similarity, 2)
        ),
        "reasons": reasons
    }