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
         "Check store-level inventory, on-hand vs sellable, backroom, damages. This tool provides comprehensive inventory visibility by querying real-time stock levels across multiple dimensions including on-hand quantities, sellable units available for customer purchase, items stored in backroom locations, and damaged goods that need to be removed from circulation. Essential for store operations, customer service inquiries, and inventory management decisions.",
         {"type":"object","properties":{"sku":{"type":"string"},"store":{"type":"string"}},"required":["sku"]},
         InventoryLookup),
    Tool("PriceCompare",
         "Compare prices across stores/online and flag price match eligibility. This tool searches and compares product pricing from multiple sources including physical store locations, online marketplace listings, and competitor websites. It identifies the lowest available price and determines whether the item qualifies for price matching policies, helping customers get the best deal and stores maintain competitive pricing strategies.",
         {"type":"object","properties":{"query":{"type":"string"}},"required":["query"]},
         PriceCompare),
    Tool("PromoEligibility",
         "Check member promo eligibility and exclusions. This tool verifies whether a specific member account qualifies for promotional offers, discounts, or special sales events. It reviews membership tier status, purchase history, and any restrictions or exclusions that might apply to certain product categories, clearance items, or marketplace products. Critical for ensuring accurate pricing and customer satisfaction during promotional periods.",
         {"type":"object","properties":{"member_id":{"type":"string"}},"required":["member_id"]},
         PromoEligibility),
    Tool("ReplenishmentPlanner",
         "Suggest reorder qty using simple forecast and safety stock heuristics. This tool analyzes historical sales data, current inventory levels, and seasonal trends to generate intelligent reorder recommendations. It calculates optimal order quantities by combining demand forecasting algorithms with safety stock calculations to prevent stockouts while minimizing excess inventory. Helps maintain optimal inventory levels and reduce carrying costs.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         ReplenishmentPlanner),
    Tool("StoreLocator",
         "Find nearest stores by location text or lat/lon. This tool searches for physical store locations based on various input formats including street addresses, zip codes, city names, or geographic coordinates. It returns a list of nearby stores sorted by distance, along with contact information, directions, and store-specific details. Essential for helping customers find convenient shopping locations and for routing inventory transfers between stores.",
         {"type":"object","properties":{"near":{"type":"string"}},"required":["near"]},
         StoreLocator),
    Tool("ReturnPolicy",
         "Summarize return policy nuances for a given item. This tool provides detailed information about return and refund policies specific to different product categories, including time limits, condition requirements, receipt necessities, and any special restrictions. It covers standard merchandise, electronics, consumables, and clearance items, each with potentially different return windows and conditions. Helps customers understand their options and assists staff with policy enforcement.",
         {"type":"object","properties":{"item":{"type":"string"}},"required":["item"]},
         ReturnPolicy),
    Tool("MembershipStatus",
         "Lookup club membership tier, renewal, and rewards. This tool retrieves comprehensive membership information including current tier level, membership expiration date, renewal requirements, available rewards balance, and redemption options. It provides details about tier benefits, points accumulation, and upcoming membership milestones. Essential for customer service inquiries about membership benefits and for processing membership-related transactions.",
         {"type":"object","properties":{"member_id":{"type":"string"}},"required":["member_id"]},
         MembershipStatus),
    Tool("OrderStatus",
         "Track ecommerce order shipping status and ETA. This tool provides real-time tracking information for online orders including current shipping status, carrier details, tracking numbers, estimated delivery dates, and delivery address confirmation. It monitors order progress from processing through shipment to final delivery, helping customers stay informed about their purchases and enabling customer service to resolve shipping-related inquiries efficiently.",
         {"type":"object","properties":{"order_id":{"type":"string"}},"required":["order_id"]},
         OrderStatus),
    Tool("ProductCompatibility",
         "Check accessory compatibility with base product. This tool verifies whether accessories, add-ons, or complementary products are compatible with a specified base product. It checks technical specifications, dimensions, connector types, and system requirements to ensure proper fit and functionality. Critical for preventing customer returns due to incompatibility issues and for providing accurate product recommendations during sales consultations.",
         {"type":"object","properties":{"base_item":{"type":"string"},"add_on":{"type":"string"}},"required":["base_item","add_on"]},
         ProductCompatibility),
    Tool("ShelfSpaceOptimizer",
         "Optimize shelf facings by sales rank and velocity heuristics. This tool analyzes product performance metrics including sales velocity, profit margins, and customer demand patterns to recommend optimal shelf space allocation. It suggests adjustments to product facings, shelf placement, and display arrangements to maximize sales per square foot while ensuring popular items remain well-stocked. Helps merchandising teams make data-driven decisions about product placement and inventory display.",
         {"type":"object","properties":{"category":{"type":"string"}},"required":["category"]},
         ShelfSpaceOptimizer),
    Tool("ProductSearch",
         "Search for products by name, description, or keywords. This tool performs comprehensive product searches across the entire catalog using natural language queries, product names, descriptions, or keyword combinations. It returns relevant results ranked by relevance, popularity, and availability, helping customers find exactly what they're looking for even with vague or incomplete search terms. Essential for both online and in-store product discovery experiences.",
         {"type":"object","properties":{"query":{"type":"string"}},"required":["query"]},
         ProductSearch),
    Tool("StockAlert",
         "Set up stock alerts to notify when inventory drops below threshold. This tool allows users to configure automated notifications that trigger when product inventory levels fall below specified thresholds. It monitors stock levels in real-time and sends alerts via preferred communication channels, enabling proactive inventory management and helping customers be notified when out-of-stock items become available again. Useful for both inventory managers and customers waiting for restocked items.",
         {"type":"object","properties":{"sku":{"type":"string"},"threshold":{"type":"string"}},"required":["sku"]},
         StockAlert),
    Tool("VendorContact",
         "Get vendor contact information and lead times. This tool retrieves comprehensive vendor details including primary contact information, phone numbers, email addresses, account manager assignments, and typical lead times for order fulfillment. It provides essential information for procurement teams, buyers, and inventory managers who need to communicate with suppliers, place orders, or resolve vendor-related issues. Helps streamline the purchasing and vendor management processes.",
         {"type":"object","properties":{"vendor":{"type":"string"}},"required":["vendor"]},
         VendorContact),
    Tool("ShippingCalculator",
         "Calculate shipping costs and delivery times for a destination. This tool computes shipping charges and estimated delivery dates based on package weight, dimensions, destination zip code, and selected shipping method. It provides multiple shipping options including standard, express, and overnight delivery with corresponding costs and timeframes. Essential for ecommerce checkout processes and for providing customers with accurate shipping estimates before completing their purchase.",
         {"type":"object","properties":{"zip_code":{"type":"string"},"weight":{"type":"string"}},"required":["zip_code"]},
         ShippingCalculator),
    Tool("WarrantyChecker",
         "Check warranty information and extended warranty options for a product. This tool retrieves detailed warranty coverage information including manufacturer warranty duration, coverage terms, and available extended warranty plans. It provides information about what's covered under warranty, claim procedures, and pricing for extended protection plans. Helps customers understand their product protection options and assists sales staff in offering appropriate warranty upgrades during the purchase process.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         WarrantyChecker),
    Tool("GiftCardBalance",
         "Check gift card balance and expiration date. This tool retrieves current balance information, expiration dates, usage history, and transaction details for gift cards. It verifies card validity, checks for any restrictions or limitations, and provides information about where and how the card can be used. Essential for customer service inquiries and for processing gift card transactions at point of sale, ensuring accurate balance verification and preventing fraud.",
         {"type":"object","properties":{"card_number":{"type":"string"}},"required":["card_number"]},
         GiftCardBalance),
    Tool("LoyaltyPoints",
         "Check member loyalty points balance and redemption options. This tool provides comprehensive loyalty program information including current points balance, points expiration dates, available redemption options, and point value calculations. It shows how many points are needed for various rewards, tracks points earning history, and identifies upcoming point expiration dates. Helps customers maximize their loyalty program benefits and assists staff in processing point redemptions accurately.",
         {"type":"object","properties":{"member_id":{"type":"string"}},"required":["member_id"]},
         LoyaltyPoints),
    Tool("PriceHistory",
         "View price history and trends for a product over time. This tool displays historical pricing data showing how product prices have changed over various time periods including 30-day, 90-day, and annual trends. It identifies price patterns, seasonal fluctuations, and current pricing relative to historical averages. Helps customers make informed purchasing decisions by understanding price trends, and assists pricing teams in analyzing competitive positioning and optimal pricing strategies.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         PriceHistory),
    Tool("ProductReviews",
         "Get product reviews, ratings, and customer feedback. This tool aggregates customer reviews, ratings, and detailed feedback for products, providing comprehensive insights into product quality, customer satisfaction, and common issues or praises. It includes overall star ratings, review counts, sentiment analysis, and detailed customer comments. Essential for helping customers make informed purchase decisions and for product teams to understand customer perceptions and identify areas for product improvement.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         ProductReviews),
    Tool("BundleRecommendation",
         "Get recommended product bundles with savings information. This tool analyzes product relationships, purchase patterns, and promotional opportunities to suggest product bundles that provide value to customers. It identifies complementary products that are frequently purchased together and calculates potential savings from bundle purchases versus individual item pricing. Helps increase average order value while providing customers with convenient, cost-effective product combinations and special bundle pricing.",
         {"type":"object","properties":{"base_sku":{"type":"string"}},"required":["base_sku"]},
         BundleRecommendation),
    Tool("CrossSellSuggestions",
         "Get cross-sell product suggestions based on purchase history. This tool uses collaborative filtering and purchase pattern analysis to recommend additional products that customers who bought similar items also purchased. It identifies complementary products, accessories, and related items that enhance the primary purchase. Helps increase sales through intelligent product recommendations while improving customer satisfaction by suggesting relevant items they might not have considered, based on what similar customers found useful.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         CrossSellSuggestions),
    Tool("InventoryTransfer",
         "Request inventory transfer between stores. This tool facilitates the movement of inventory from one store location to another, handling transfer requests, tracking shipment status, and managing transfer costs. It coordinates between source and destination stores, calculates transfer fees, and provides estimated arrival times. Essential for balancing inventory across locations, fulfilling customer requests for items available at other stores, and optimizing overall inventory distribution throughout the retail network.",
         {"type":"object","properties":{"from_store":{"type":"string"},"to_store":{"type":"string"},"sku":{"type":"string"},"qty":{"type":"string"}},"required":["from_store","to_store","sku"]},
         InventoryTransfer),
    Tool("DamagedItemReport",
         "Report damaged items and process credits or replacements. This tool handles the documentation and processing of damaged merchandise, including creating damage reports, issuing credits or refunds, and initiating replacement orders when applicable. It tracks damage types, quantities, and financial impact, ensuring proper inventory adjustments and customer satisfaction. Essential for maintaining accurate inventory records, processing insurance claims, and ensuring customers receive appropriate compensation or replacements for damaged goods.",
         {"type":"object","properties":{"sku":{"type":"string"},"store":{"type":"string"}},"required":["sku","store"]},
         DamagedItemReport),
    Tool("RestockNotification",
         "Get restock notifications and expected delivery dates. This tool provides information about upcoming inventory replenishments including expected delivery dates, quantities being restocked, and current reorder status. It tracks purchase orders, monitors supplier shipments, and alerts when restocked items become available for sale. Helps customers know when out-of-stock items will be available again and assists inventory managers in planning for incoming stock and coordinating with sales teams about product availability.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         RestockNotification),
    Tool("StoreHours",
         "Get store hours and holiday schedule information. This tool retrieves current operating hours, special holiday schedules, and any temporary hour modifications for store locations. It provides day-by-day schedules, identifies holiday closures or special hours, and includes information about seasonal schedule changes. Essential for helping customers plan their visits, for staff scheduling, and for ensuring accurate information is displayed on websites and store directories about when stores are open for business.",
         {"type":"object","properties":{"store":{"type":"string"}},"required":["store"]},
         StoreHours),
    Tool("PaymentMethod",
         "Check payment method and status for an order. This tool retrieves payment information associated with orders including payment method type, card details, transaction status, authorization results, and payment confirmation. It verifies payment processing, checks for payment issues or declines, and provides transaction history. Essential for order fulfillment verification, customer service inquiries about payment problems, and for processing refunds or payment adjustments when necessary.",
         {"type":"object","properties":{"order_id":{"type":"string"}},"required":["order_id"]},
         PaymentMethod),
    Tool("RefundProcessor",
         "Process refunds for orders and return items. This tool handles the complete refund workflow including calculating refund amounts, processing payments back to original payment methods, updating order status, and generating refund confirmations. It manages partial refunds, full refunds, and handles various payment method types with appropriate processing times. Essential for customer service operations, return processing, and ensuring customers receive timely refunds while maintaining accurate financial records and inventory adjustments.",
         {"type":"object","properties":{"order_id":{"type":"string"},"amount":{"type":"string"}},"required":["order_id","amount"]},
         RefundProcessor),
    Tool("ExchangePolicy",
         "Get exchange policy details for specific items. This tool provides comprehensive information about product exchange policies including time limits, condition requirements, exchange eligibility, and any restrictions or fees. It covers different exchange scenarios such as size exchanges, color changes, or model upgrades, each with potentially different terms. Helps customers understand their exchange options and assists staff in processing exchanges according to policy guidelines while ensuring customer satisfaction and proper inventory management.",
         {"type":"object","properties":{"item":{"type":"string"}},"required":["item"]},
         ExchangePolicy),
    Tool("ProductSpecs",
         "Get detailed product specifications and technical details. This tool retrieves comprehensive product information including dimensions, weight, materials, technical specifications, compatibility requirements, and feature lists. It provides detailed technical data that helps customers make informed purchasing decisions and ensures products meet their specific needs. Essential for customer service inquiries, sales consultations, and for verifying product compatibility with other items or systems before purchase.",
         {"type":"object","properties":{"sku":{"type":"string"}},"required":["sku"]},
         ProductSpecs),
    Tool("BulkOrderQuote",
         "Get pricing quotes for bulk orders with volume discounts. This tool calculates pricing for large quantity orders, applying volume discount tiers, special pricing agreements, and bulk purchase incentives. It provides detailed quotes including unit pricing, total costs, applicable discounts, and shipping considerations for bulk orders. Essential for business customers, institutional buyers, and for processing large orders that may qualify for special pricing or require custom fulfillment arrangements beyond standard retail transactions.",
         {"type":"object","properties":{"sku":{"type":"string"},"qty":{"type":"string"}},"required":["sku","qty"]},
         BulkOrderQuote),
]
