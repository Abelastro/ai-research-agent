from ..models.schemas import ToolResult


def validate_tool_results(results: list[ToolResult]) -> dict:
    if not results:
        return {"valid": False, "errors": ["No results to validate"], "warnings": []}

    errors = []
    warnings = []

    for result in results:
        if not result.success:
            errors.append(f"Tool {result.tool.value} failed: {result.error}")
        elif not result.output:
            warnings.append(f"Tool {result.tool.value} returned empty output")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "total": len(results),
        "successful": sum(1 for r in results if r.success),
        "failed": len(errors),
    }


def calculate_confidence(results: list[ToolResult]) -> float:
    if not results:
        return 0.0

    successful = sum(1 for r in results if r.success)
    base_confidence = successful / len(results)

    has_output = sum(1 for r in results if r.success and r.output)
    if successful > 0:
        output_ratio = has_output / successful
        base_confidence *= output_ratio

    return round(base_confidence, 2)


def filter_relevant_results(query: str, results: list[ToolResult]) -> list[ToolResult]:
    if not results:
        return []

    query_words = set(query.lower().split())
    relevant = []

    for result in results:
        if not result.success:
            continue

        output_lower = result.output.lower()
        overlap = sum(1 for word in query_words if word in output_lower)

        if overlap > 0 or not query_words:
            relevant.append(result)

    return relevant if relevant else [r for r in results if r.success]
