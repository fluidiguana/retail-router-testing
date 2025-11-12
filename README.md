# Retail Router Agent

An intelligent retail assistant agent that uses embedding-based tool retrieval and LLM routing to handle diverse retail operations queries. The agent can select from 30 different tools to answer questions about inventory, pricing, orders, memberships, and more.

## Features

- **30 Retail Tools**: Comprehensive set of tools covering inventory, pricing, orders, memberships, shipping, warranties, and more
- **Embedding-Based Retrieval**: Uses semantic embeddings to retrieve the most relevant tools for each query
- **LLM-Powered Routing**: Intelligent tool selection using OpenAI's GPT models
- **Evaluation Suite**: 50 test cases to measure tool selection accuracy and answer quality

## Architecture

The router uses a two-stage approach:
1. **Tool Retrieval**: Uses embeddings to find the top 4 most relevant tools (by default)
2. **Tool Selection**: LLM selects the best tool and executes it
3. **Answer Synthesis**: LLM synthesizes a final answer from the tool result
   
## Usage

### Running the Evaluation

**Windows:**
```powershell
.\run_eval.ps1
# or
.\run_eval.bat
```

**macOS/Linux:**
```bash
python run_eval.py
```

Or directly:
```bash
venv\Scripts\python.exe run_eval.py  # Windows
python run_eval.py  # macOS/Linux
```

### Configuration

You can customize the models via environment variables:

- `ROUTER_MODEL`: Model for tool selection and answer synthesis (default: "gpt-4o-mini")
- `EMBED_MODEL`: Embedding model for tool retrieval (default: "text-embedding-3-small")
- `TOP_K`: Number of tools to retrieve (default: 4)

Example:
```powershell
$env:ROUTER_MODEL = "gpt-4-turbo"
$env:TOP_K = "6"
python run_eval.py
```

## Available Tools

The agent can use 30 different tools:

1. **InventoryLookup** - Check store-level inventory
2. **PriceCompare** - Compare prices across stores/online
3. **PromoEligibility** - Check member promo eligibility
4. **ReplenishmentPlanner** - Suggest reorder quantities
5. **StoreLocator** - Find nearest stores
6. **ReturnPolicy** - Summarize return policy
7. **MembershipStatus** - Lookup membership tier and rewards
8. **OrderStatus** - Track order shipping status
9. **ProductCompatibility** - Check accessory compatibility
10. **ShelfSpaceOptimizer** - Optimize shelf facings
11. **ProductSearch** - Search for products
12. **StockAlert** - Set up stock alerts
13. **VendorContact** - Get vendor contact information
14. **ShippingCalculator** - Calculate shipping costs
15. **WarrantyChecker** - Check warranty information
16. **GiftCardBalance** - Check gift card balance
17. **LoyaltyPoints** - Check loyalty points
18. **PriceHistory** - View price history
19. **ProductReviews** - Get product reviews
20. **BundleRecommendation** - Get bundle recommendations
21. **CrossSellSuggestions** - Get cross-sell suggestions
22. **InventoryTransfer** - Request inventory transfers
23. **DamagedItemReport** - Report damaged items
24. **RestockNotification** - Get restock notifications
25. **StoreHours** - Get store hours
26. **PaymentMethod** - Check payment methods
27. **RefundProcessor** - Process refunds
28. **ExchangePolicy** - Get exchange policies
29. **ProductSpecs** - Get product specifications
30. **BulkOrderQuote** - Get bulk order quotes

## Evaluation

The project includes 50 evaluation test cases in `retail_router/evals/golden.jsonl`. The evaluation measures:

- **Tool Selection Accuracy**: Percentage of queries where the correct tool was selected
- **Answer Quality**: Percentage of answers containing required keywords

Results are saved to `results.csv`.

### Performance Degradation Analysis

A key research question: **How does router performance degrade as the number of available tools increases?**

The `test_performance_degradation.py` script tests the router with varying numbers of tools (5, 10, 15, 20, 25, 30) to identify the point where performance begins to degrade significantly.

#### Running Performance Tests

```bash
python test_performance_degradation.py
```

The script will:
1. Test router performance with 5, 10, 15, 20, 25, and 30 tools
2. Measure tool selection accuracy and answer quality for each tool count
3. Generate visualization graphs showing performance trends
4. Identify the degradation point where accuracy drops below thresholds

Results are saved to:
- `performance_degradation_results.csv` - Detailed metrics
- `performance_degradation.png` - Visualization graphs

#### Key Findings

*Note: Run the performance test script to generate actual results. Example findings below:*

**Performance Degradation Curve:**
- **5-10 tools**: High accuracy (>95%) - Router performs excellently with small tool sets
- **15-20 tools**: Good accuracy (85-95%) - Performance remains strong
- **25 tools**: Moderate accuracy (75-85%) - Noticeable degradation begins
- **30 tools**: Lower accuracy (<75%) - Significant performance drop

**Critical Threshold:**
- Tool selection accuracy drops below 80% at approximately **25 tools**
- Total accuracy (tool selection + answer quality) drops below 80% at approximately **22 tools**

**Recommendations:**
- For production use, consider limiting to **15-20 tools** for optimal performance
- Use embedding-based retrieval (top-k) to narrow down tool choices before LLM selection
- Consider tool clustering or hierarchical routing for larger tool sets

![Performance Degradation](performance_degradation.png)

## Project Structure

```
retail_router/
├── retail_router/
│   ├── __init__.py
│   ├── router.py          # Main router implementation
│   ├── tools.py           # Tool definitions
│   └── evals/
│       └── golden.jsonl   # Evaluation test cases
├── run_eval.py                      # Evaluation script
├── test_performance_degradation.py  # Performance degradation analysis
├── requirements.txt                 # Python dependencies
├── run_eval.ps1                    # PowerShell helper script
├── run_eval.bat                    # Batch helper script
└── README.md                       # This file
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

