from dataclasses import dataclass
from typing import Callable, Dict, Any, List

@dataclass
class Tool:
    name: str
    description: str
    schema: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Dict[str, Any]]

def _resp(ok: bool, content: str, **extra) -> Dict[str, Any]:
    d = {"ok": ok, "content": content}
    d.update(extra)
    return d

def InventoryLookup(args):
    sku = args.get("sku") or args.get("query","").upper()
    store = args.get("store","0001")
    return _resp(True, f"Inventory for SKU {sku} at store {store}: 12 on-hand, 9 sellable, 2 backroom, 1 damaged.")

def PriceCompare(args):
    query = args.get("query", "")
    return _resp(True, f"Lowest price for '{query}': $19.99 at Store 112, $21.49 online. Price match eligible.")

def PromoEligibility(args):
    member = args.get("member_id","unknown")
    return _resp(True, f"Member {member}: eligible for 20% off weekend promo; excludes clearance and marketplace items.")

def ReplenishmentPlanner(args):
    sku = args.get("sku","UNK")
    return _resp(True, f"SKU {sku}: reorder recommended. Forecast 7d demand = 18, safety stock = 6, reorder qty = 20.")

def StoreLocator(args):
    near = args.get("near","")
    return _resp(True, f"Closest stores near {near}: Store 112 (0.9 mi), Store 203 (2.1 mi).")

def ReturnPolicy(args):
    item = args.get("item","item")
    return _resp(True, f"Return policy for {item}: 90 days with receipt; electronics 30 days; opened consumables not returnable.")

def MembershipStatus(args):
    member = args.get("member_id","unknown")
    return _resp(True, f"Member {member}: Plus tier, renewal due in 23 days; 3 rewards available ($12.40).")

def OrderStatus(args):
    order = args.get("order_id","N/A")
    return _resp(True, f"Order {order}: shipped, ETA in 2 days via UPS. Tracking 1Z999AA10123456784.")

def ProductCompatibility(args):
    base_item = args.get("base_item","")
    add_on = args.get("add_on","")
    return _resp(True, f"Compatibility: {add_on} fits {base_item}: YES (verified dimensions; adapter not required).")

def ShelfSpaceOptimizer(args):
    category = args.get("category","category")
    return _resp(True, f"Planogram suggestion for {category}: expand top seller facings from 3→5; move long-tail to lower shelf.")

def ProductSearch(args):
    query = args.get("query", "")
    return _resp(True, f"Found 12 products matching '{query}': Top 3 results - Item A ($29.99), Item B ($34.99), Item C ($19.99). All in stock.")

def StockAlert(args):
    sku = args.get("sku", "")
    threshold = args.get("threshold", "5")
    return _resp(True, f"Stock alert set for SKU {sku}: notify when inventory drops below {threshold} units. Current stock: 8 units.")

def VendorContact(args):
    vendor = args.get("vendor", "")
    return _resp(True, f"Vendor {vendor}: Contact - sales@vendor.com, Phone: 555-0123, Lead time: 5-7 business days.")

def ShippingCalculator(args):
    zip_code = args.get("zip_code", "")
    weight = args.get("weight", "1")
    return _resp(True, f"Shipping to {zip_code} for {weight}lbs: Standard (5-7 days) $8.99, Express (2-3 days) $15.99, Overnight $29.99.")

def WarrantyChecker(args):
    sku = args.get("sku", "")
    return _resp(True, f"Warranty for SKU {sku}: 1-year manufacturer warranty, 90-day return window. Extended warranty available: +$29.99 for 2 years.")

def GiftCardBalance(args):
    card_number = args.get("card_number", "")
    return _resp(True, f"Gift card {card_number}: Balance $47.50, expires 12/31/2025. Last used: 01/15/2024.")

def LoyaltyPoints(args):
    member_id = args.get("member_id", "")
    return _resp(True, f"Member {member_id}: 2,450 points available. 550 points = $5 reward. Next reward in 100 points.")

def PriceHistory(args):
    sku = args.get("sku", "")
    return _resp(True, f"Price history for SKU {sku}: Current $49.99, 30d avg $52.99, 90d low $44.99. Price dropped 5.7% this month.")

def ProductReviews(args):
    sku = args.get("sku", "")
    return _resp(True, f"Reviews for SKU {sku}: 4.3/5 stars (127 reviews). 78% recommend. Top feedback: 'Great quality, fast shipping'.")

def BundleRecommendation(args):
    base_sku = args.get("base_sku", "")
    return _resp(True, f"Bundle recommendations for {base_sku}: Bundle A (save $15), Bundle B (save $22), Bundle C (save $8). All items in stock.")

def CrossSellSuggestions(args):
    sku = args.get("sku", "")
    return _resp(True, f"Customers who bought {sku} also purchased: Item X (45%), Item Y (32%), Item Z (28%). All available.")

def InventoryTransfer(args):
    from_store = args.get("from_store", "")
    to_store = args.get("to_store", "")
    sku = args.get("sku", "")
    qty = args.get("qty", "1")
    return _resp(True, f"Transfer request: {qty} units of SKU {sku} from Store {from_store} to Store {to_store}. ETA: 2-3 days. Cost: $5.00.")

def DamagedItemReport(args):
    sku = args.get("sku", "")
    store = args.get("store", "")
    return _resp(True, f"Damage report logged for SKU {sku} at Store {store}. Credit issued: $24.99. Replacement order created.")

def RestockNotification(args):
    sku = args.get("sku", "")
    return _resp(True, f"Restock notification for SKU {sku}: Expected delivery 01/25/2024. Quantity: 50 units. Auto-reorder enabled.")

def StoreHours(args):
    store = args.get("store", "")
    return _resp(True, f"Store {store} hours: Mon-Fri 9am-9pm, Sat 9am-10pm, Sun 10am-8pm. Holiday hours may vary.")

def PaymentMethod(args):
    order_id = args.get("order_id", "")
    return _resp(True, f"Payment for order {order_id}: Visa ending 4532, charged $89.99. Payment status: Confirmed. Receipt sent.")

def RefundProcessor(args):
    order_id = args.get("order_id", "")
    amount = args.get("amount", "")
    return _resp(True, f"Refund processed for order {order_id}: ${amount} refunded to original payment method. Processing time: 3-5 business days.")

def ExchangePolicy(args):
    item = args.get("item", "")
    return _resp(True, f"Exchange policy for {item}: 30 days with receipt, same item different size/color. No restocking fee for exchanges.")

def ProductSpecs(args):
    sku = args.get("sku", "")
    return _resp(True, f"Specs for SKU {sku}: Dimensions 12x8x4in, Weight 2.5lbs, Material: Plastic, Color: Black, Warranty: 1 year.")

def BulkOrderQuote(args):
    sku = args.get("sku", "")
    qty = args.get("qty", "")
    return _resp(True, f"Bulk quote for {qty} units of SKU {sku}: Unit price $19.99, Total $999.50 (5% discount). Free shipping on orders $500+.")

TOOLS: List[Tool] = [
    Tool("InventoryLookup",
         "Check store-level inventory, on-hand vs sellable, backroom, damages.",
         {"type":"object","properties":{"sku":{"type":"string"},"store":{"type":"string"}},"required":["sku"]},
         InventoryLookup),
    Tool("PriceCompare",
         "Compare prices across stores/online and flag price match eligibility.",
         {"type":"object","properties":{"query":{"type":"string"}},"required":["query"]},
         PriceCompare),
    Tool("PromoEligibility",
         "Check member promo eligibility and exclusions.",
         {"type":"object","properties":{"member_id":{"type":"string"}},"required":["member_id"]},
         PromoEligibility),
    Tool("ReplenishmentPlanner",
         "Suggest reorder qty using simple forecast and safety stock heuristics.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         ReplenishmentPlanner),
    Tool("StoreLocator",
         "Find nearest stores by location text or lat/lon.",
         {"type":"object","properties":{"near":{"type":"string"}},"required":["near"]},
         StoreLocator),
    Tool("ReturnPolicy",
         "Summarize return policy nuances for a given item.",
         {"type":"object","properties":{"item":{"type":"string"}},"required":["item"]},
         ReturnPolicy),
    Tool("MembershipStatus",
         "Lookup club membership tier, renewal, and rewards.",
         {"type":"object","properties":{"member_id":{"type":"string"}},"required":["member_id"]},
         MembershipStatus),
    Tool("OrderStatus",
         "Track ecommerce order shipping status and ETA.",
         {"type":"object","properties":{"order_id":{"type":"string"}},"required":["order_id"]},
         OrderStatus),
    Tool("ProductCompatibility",
         "Check accessory compatibility with base product.",
         {"type":"object","properties":{"base_item":{"type":"string"},"add_on":{"type":"string"}},"required":["base_item","add_on"]},
         ProductCompatibility),
    Tool("ShelfSpaceOptimizer",
         "Optimize shelf facings by sales rank and velocity heuristics.",
         {"type":"object","properties":{"category":{"type":"string"}},"required":["category"]},
         ShelfSpaceOptimizer),
    Tool("ProductSearch",
         "Search for products by name, description, or keywords.",
         {"type":"object","properties":{"query":{"type":"string"}},"required":["query"]},
         ProductSearch),
    Tool("StockAlert",
         "Set up stock alerts to notify when inventory drops below threshold.",
         {"type":"object","properties":{"sku":{"type":"string"},"threshold":{"type":"string"}},"required":["sku"]},
         StockAlert),
    Tool("VendorContact",
         "Get vendor contact information and lead times.",
         {"type":"object","properties":{"vendor":{"type":"string"}},"required":["vendor"]},
         VendorContact),
    Tool("ShippingCalculator",
         "Calculate shipping costs and delivery times for a destination.",
         {"type":"object","properties":{"zip_code":{"type":"string"},"weight":{"type":"string"}},"required":["zip_code"]},
         ShippingCalculator),
    Tool("WarrantyChecker",
         "Check warranty information and extended warranty options for a product.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         WarrantyChecker),
    Tool("GiftCardBalance",
         "Check gift card balance and expiration date.",
         {"type":"object","properties":{"card_number":{"type":"string"}},"required":["card_number"]},
         GiftCardBalance),
    Tool("LoyaltyPoints",
         "Check member loyalty points balance and redemption options.",
         {"type":"object","properties":{"member_id":{"type":"string"}},"required":["member_id"]},
         LoyaltyPoints),
    Tool("PriceHistory",
         "View price history and trends for a product over time.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         PriceHistory),
    Tool("ProductReviews",
         "Get product reviews, ratings, and customer feedback.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         ProductReviews),
    Tool("BundleRecommendation",
         "Get recommended product bundles with savings information.",
         {"type":"object","properties":{"base_sku":{"type":"string"}},"required":["base_sku"]},
         BundleRecommendation),
    Tool("CrossSellSuggestions",
         "Get cross-sell product suggestions based on purchase history.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         CrossSellSuggestions),
    Tool("InventoryTransfer",
         "Request inventory transfer between stores.",
         {"type":"object","properties":{"from_store":{"type":"string"},"to_store":{"type":"string"},"sku":{"type":"string"},"qty":{"type":"string"}},"required":["from_store","to_store","sku"]},
         InventoryTransfer),
    Tool("DamagedItemReport",
         "Report damaged items and process credits or replacements.",
         {"type":"object","properties":{"sku":{"type":"string"},"store":{"type":"string"}},"required":["sku","store"]},
         DamagedItemReport),
    Tool("RestockNotification",
         "Get restock notifications and expected delivery dates.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         RestockNotification),
    Tool("StoreHours",
         "Get store hours and holiday schedule information.",
         {"type":"object","properties":{"store":{"type":"string"}},"required":["store"]},
         StoreHours),
    Tool("PaymentMethod",
         "Check payment method and status for an order.",
         {"type":"object","properties":{"order_id":{"type":"string"}},"required":["order_id"]},
         PaymentMethod),
    Tool("RefundProcessor",
         "Process refunds for orders and return items.",
         {"type":"object","properties":{"order_id":{"type":"string"},"amount":{"type":"string"}},"required":["order_id","amount"]},
         RefundProcessor),
    Tool("ExchangePolicy",
         "Get exchange policy details for specific items.",
         {"type":"object","properties":{"item":{"type":"string"}},"required":["item"]},
         ExchangePolicy),
    Tool("ProductSpecs",
         "Get detailed product specifications and technical details.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         ProductSpecs),
    Tool("BulkOrderQuote",
         "Get pricing quotes for bulk orders with volume discounts.",
         {"type":"object","properties":{"sku":{"type":"string"},"qty":{"type":"string"}},"required":["sku","qty"]},
         BulkOrderQuote),
]
