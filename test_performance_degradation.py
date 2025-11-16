"""
Test how tool calling performance degrades as the number of available tools increases.
This script tests the router with varying numbers of tools and measures accuracy.
"""

import os
import json
import sys
from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

from retail_router.router import RetailRouter
from retail_router.tools import TOOLS


def load_golden(path: str) -> List[Dict[str, Any]]:
    """Load evaluation test cases."""
    items = []
    with open(path, "r") as f:
        for line in f:
            items.append(json.loads(line))
    return items


def create_router_with_subset_tools(
    num_tools: int, model: str, embed_model: str, top_k: int = 4
):
    """
    Create a router with a subset of tools.
    We'll use the first N tools to maintain consistency across runs.
    """
    # Use first N tools for consistency
    subset_tools = TOOLS[:num_tools]
    return RetailRouter(
        model=model, embed_model=embed_model, top_k=top_k, tools=subset_tools
    )


def evaluate_with_tool_count(
    num_tools: int,
    goldens: List[Dict[str, Any]],
    model: str,
    embed_model: str,
    top_k: int,
    num_runs: int = 1,
    tool_pbar: tqdm = None,
    overall_pbar: tqdm = None,
) -> Dict[str, float]:
    """
    Evaluate router performance with a specific number of tools.
    Returns average metrics across runs.
    """
    # Filter goldens to only include those that use tools in our subset
    available_tool_names = {t.name for t in TOOLS[:num_tools]}
    filtered_goldens = [
        g for g in goldens if g["expected_tool"] in available_tool_names
    ]

    if not filtered_goldens:
        return {
            "num_tools": num_tools,
            "tool_accuracy": 0.0,
            "num_testable": 0,
        }

    all_tool_matches = []

    for run in range(num_runs):
        try:
            router = create_router_with_subset_tools(
                num_tools, model, embed_model, top_k
            )
        except Exception as e:
            error_msg = str(e)
            # If router creation fails, it's likely a model issue
            raise Exception(
                f"Failed to create router with model '{model}': {error_msg}"
            )

        tool_matches = []

        for g in filtered_goldens:
            try:
                r = router.decide_and_execute(g["query"])

                picked_tool = r.get("tool_name")
                tool_match = int(picked_tool == g["expected_tool"])

                tool_matches.append(tool_match)
            except Exception as e:
                error_msg = str(e)
                # Check if it's a model-related error
                if (
                    "model" in error_msg.lower()
                    or "not found" in error_msg.lower()
                    or "invalid" in error_msg.lower()
                ):
                    raise  # Re-raise model errors to be caught by outer handler
                print(f"Error on query {g['qid']}: {e}")
                tool_matches.append(0)

            # Update both progress bars
            if tool_pbar:
                tool_pbar.update(1)
            if overall_pbar:
                overall_pbar.update(1)

        all_tool_matches.append(np.mean(tool_matches))

    return {
        "num_tools": num_tools,
        "tool_accuracy": np.mean(all_tool_matches),
        "num_testable": len(filtered_goldens),
    }


def save_partial_results(all_results: Dict[str, List[Dict[str, float]]]):
    """Save results incrementally and generate chart even with partial data."""
    for model, results in all_results.items():
        if results:  # Only save if we have data
            df = pd.DataFrame(results)
            safe_model_name = model.replace(".", "-").replace("_", "-")
            filename = f"performance_degradation_{safe_model_name}.csv"
            df.to_csv(filename, index=False)
            print(f"\nResults for {model} saved to {filename}")


def generate_chart(all_results: Dict[str, List[Dict[str, float]]]):
    """Generate chart from results dictionary."""
    if not all_results:
        print("No results to visualize!")
        return

    # Filter out empty results
    filtered_results = {k: v for k, v in all_results.items() if v}
    if not filtered_results:
        print("No valid results to visualize!")
        return

    plt.figure(figsize=(14, 6))

    # Main chart - tool selection accuracy
    plt.subplot(1, 2, 1)

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]  # Blue, Orange, Green
    markers = ["o", "s", "^"]

    for idx, (model, results) in enumerate(filtered_results.items()):
        df = pd.DataFrame(results)
        plt.plot(
            df["num_tools"],
            df["tool_accuracy"] * 100,  # Convert to percentage
            marker=markers[idx % len(markers)],
            linestyle="-",
            label=model,
            linewidth=2,
            markersize=8,
            color=colors[idx % len(colors)],
        )

    plt.xlabel("Number of Available Tools", fontsize=12)
    plt.ylabel("Tool Selection Accuracy (%)", fontsize=12)
    plt.title("Performance Degradation vs Tool Count", fontsize=14, fontweight="bold")
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    # Format y-axis as percentage
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: "{:.0f}%".format(y)))

    # Set appropriate y-axis limits based on data
    all_accuracies = []
    for results in filtered_results.values():
        df = pd.DataFrame(results)
        all_accuracies.extend(df["tool_accuracy"].values * 100)

    if all_accuracies:
        min_acc = min(all_accuracies)
        max_acc = max(all_accuracies)
        # Add padding: 5% below min, 5% above max, but ensure we show 0-100% range appropriately
        y_min = max(0, min_acc - 5)
        y_max = min(100, max_acc + 5)
        plt.ylim([y_min, y_max])

    # Test coverage chart
    plt.subplot(1, 2, 2)
    # Use first model's results for test coverage (same for all models)
    first_model_results = list(filtered_results.values())[0]
    if first_model_results:
        df_coverage = pd.DataFrame(first_model_results)
        plt.bar(
            df_coverage["num_tools"],
            df_coverage["num_testable"],
            alpha=0.7,
            color="steelblue",
        )
        plt.xlabel("Number of Available Tools", fontsize=12)
        plt.ylabel("Number of Testable Cases", fontsize=12)
        plt.title("Test Coverage by Tool Count", fontsize=14, fontweight="bold")
        plt.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig("performance_degradation.png", dpi=300, bbox_inches="tight")
    print("\nVisualization saved to performance_degradation.png")

    # Optionally display (comment out for headless environments)
    try:
        plt.show()
    except Exception:
        pass  # Skip if display not available


def print_analysis(all_results: Dict[str, List[Dict[str, float]]]):
    """Print performance analysis for each model."""
    print("\n" + "=" * 60)
    print("PERFORMANCE ANALYSIS")
    print("=" * 60)

    for model, results in all_results.items():
        if not results:
            continue
        df = pd.DataFrame(results)
        if len(df) > 1:
            tool_acc = df["tool_accuracy"].values * 100  # Convert to percentage

            threshold = 80  # 80% threshold
            tool_below_threshold = df[df["tool_accuracy"] * 100 < threshold]

            print(f"\n{model}:")
            if len(tool_below_threshold) > 0:
                first_failure = tool_below_threshold.iloc[0]
                print(
                    f"  Tool selection accuracy drops below {threshold}% at {first_failure['num_tools']} tools"
                )
            else:
                print(
                    f"  Tool selection accuracy remains above {threshold}% for all tested tool counts"
                )

            # Calculate degradation rate
            if len(df) >= 2:
                initial_acc = tool_acc[0]
                final_acc = tool_acc[-1]
                degradation = (initial_acc - final_acc) / initial_acc * 100
                print(
                    f"  Accuracy degrades by {degradation:.1f}% from {df.iloc[0]['num_tools']} to {df.iloc[-1]['num_tools']} tools"
                )


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in your environment.")

    embed_model = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    top_k = int(os.getenv("TOP_K", "4"))
    num_runs = int(os.getenv("NUM_RUNS", "1"))

    # Test with multiple models
    # Note: If a model name is invalid, it will be skipped with an error message
    # Common valid models: gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-4
    models = ["gpt-4.1-mini", "gpt-4o-mini", "gpt-4.1"]

    # Allow override via environment variable
    models_env = os.getenv("TEST_MODELS")
    if models_env:
        models = [m.strip() for m in models_env.split(",")]

    print(f"Testing performance degradation with models: {models}")
    print(f"Embedding model: {embed_model}, Top-K: {top_k}")
    print(f"Number of runs per tool count: {num_runs}\n")

    goldens = load_golden("retail_router/evals/golden.jsonl")
    print(f"Loaded {len(goldens)} test cases\n")

    # Test with different numbers of tools
    tool_counts = [5, 10, 15, 20, 25, 30]

    all_results = {}

    # Calculate total iterations for progress tracking
    # We need to count actual testable cases per tool count
    total_iterations = 0
    for num_tools in tool_counts:
        if num_tools <= len(TOOLS):
            available_tool_names = {t.name for t in TOOLS[:num_tools]}
            filtered_goldens = [
                g for g in goldens if g["expected_tool"] in available_tool_names
            ]
            total_iterations += len(models) * num_runs * len(filtered_goldens)

    # Outer progress bar for overall progress
    overall_pbar = tqdm(
        total=total_iterations, desc="Overall progress", position=0, leave=True
    )

    try:
        for model_idx, model in enumerate(models):
            print(f"\n{'=' * 60}")
            print(f"Testing model: {model} ({model_idx + 1}/{len(models)})")
            print(f"{'=' * 60}\n")

            results = []
            model_failed = False

            try:
                for num_tools in tool_counts:
                    if num_tools > len(TOOLS):
                        print(
                            f"Skipping {num_tools} tools (only {len(TOOLS)} available)"
                        )
                        continue

                    # Filter goldens for this tool count
                    available_tool_names = {t.name for t in TOOLS[:num_tools]}
                    filtered_goldens = [
                        g for g in goldens if g["expected_tool"] in available_tool_names
                    ]

                    # Create progress bar for this tool count
                    tool_pbar = tqdm(
                        total=num_runs * len(filtered_goldens),
                        desc=f"  {num_tools} tools",
                        position=1,
                        leave=False,
                    )

                    try:
                        metrics = evaluate_with_tool_count(
                            num_tools,
                            goldens,
                            model,
                            embed_model,
                            top_k,
                            num_runs,
                            tool_pbar=tool_pbar,
                            overall_pbar=overall_pbar,
                        )
                    except Exception as e:
                        tool_pbar.close()
                        error_msg = str(e)
                        if (
                            "model" in error_msg.lower()
                            or "not found" in error_msg.lower()
                            or "invalid" in error_msg.lower()
                        ):
                            print(
                                f"\n  ERROR: Model '{model}' appears to be invalid or unavailable."
                            )
                            print(f"  Error details: {error_msg}")
                            print("  Skipping remaining tests for this model.")
                            model_failed = True
                            break
                        else:
                            print(f"\n  ERROR on {num_tools} tools: {error_msg}")
                            print("  Continuing with next tool count...")
                            # Add a failed entry
                            metrics = {
                                "num_tools": num_tools,
                                "tool_accuracy": 0.0,
                                "num_testable": len(filtered_goldens),
                            }

                    tool_pbar.close()

                    results.append(metrics)
                    print(
                        f"  Tool Accuracy: {metrics['tool_accuracy']:.3f} ({metrics['tool_accuracy'] * 100:.1f}%)"
                    )
                    print(f"  Testable cases: {metrics['num_testable']}")

                    # Save incrementally after each tool count
                    all_results[model] = results
                    save_partial_results(all_results)

                    if model_failed:
                        break

            except KeyboardInterrupt:
                raise  # Re-raise to be caught by outer handler
            except Exception as e:
                error_msg = str(e)
                if (
                    "model" in error_msg.lower()
                    or "not found" in error_msg.lower()
                    or "invalid" in error_msg.lower()
                ):
                    print(
                        f"\n  ERROR: Model '{model}' appears to be invalid or unavailable."
                    )
                    print(f"  Error details: {error_msg}")
                    print("  Skipping this model and continuing with others.")
                    all_results[model] = []  # Mark as failed
                    continue
                else:
                    raise  # Re-raise other errors

        overall_pbar.close()

        # Final save and visualization
        print("\n" + "=" * 60)
        print("Testing complete! Generating final results...")
        print("=" * 60)
        save_partial_results(all_results)
        generate_chart(all_results)
        print_analysis(all_results)

    except KeyboardInterrupt:
        overall_pbar.close()
        print("\n\n" + "=" * 60)
        print("INTERRUPTED! Saving partial results...")
        print("=" * 60)
        save_partial_results(all_results)
        generate_chart(all_results)
        print_analysis(all_results)
        print(
            "\nPartial results saved. You can resume testing later or analyze the current data."
        )
        sys.exit(0)
    except Exception as e:
        overall_pbar.close()
        print(f"\n\nError occurred: {e}")
        print("Saving partial results...")
        save_partial_results(all_results)
        generate_chart(all_results)
        raise


if __name__ == "__main__":
    main()
