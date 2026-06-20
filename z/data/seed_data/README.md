# Synthetic Seed Data Documentation

## Overview

This directory contains realistic synthetic B2B and B2C sales data generated for testing, development, and demonstration purposes. The dataset includes 383,096 rows across 8 interconnected tables with proper foreign key relationships.

**Generated:** January 4, 2026
**Random Seed:** 42 (reproducible)
**Total Sales Value:** $7,012,392,446.88
**Total Orders:** 15,000
**Total Items Sold:** 30,092,262 units

## Dataset Summary

| Table | Rows | Size | Description |
|-------|------|------|-------------|
| `suppliers.csv` | 100 | 11 KB | Supplier companies providing products |
| `products.csv` | 994 | 119 KB | Product catalog across 7 categories |
| `customers.csv` | 10,000 | 1.4 MB | B2B (3,000) and B2C (7,000) customers |
| `stores.csv` | 2,500 | 287 KB | Physical store locations for B2B customers |
| `promotions.csv` | 50 | 5.3 KB | Active promotional campaigns |
| `orders.csv` | 15,000 | 2.1 MB | Order headers with calculated totals |
| `order_items.csv` | 176,729 | 12 MB | Line items for each order |
| `inventory_transactions.csv` | 177,723 | 17 MB | Stock movements (IN/OUT/ADJUSTMENT) |

## Business Context

### B2B Sales Segments

**Ecommerce (30%)** - 899 customers
- Online B2B marketplaces and platforms
- Higher order frequency, moderate order values
- Payment methods: Wire Transfer, Credit Card, Net 30

**Modern Trade (40%)** - 1,186 customers
- Supermarkets, hypermarkets, retail chains
- Large bulk orders, longer payment terms
- Payment methods: Wire Transfer, Credit Card, Net 30, Net 60

**Traditional Trade (30%)** - 915 customers
- Small retailers, local shops, distributors
- Smaller but frequent orders
- Payment methods: Wire Transfer, Cash on Delivery

### B2C Sales - 7,000 customers
- Direct consumer purchases
- Smaller order values, immediate payment
- Payment methods: Credit Card, Debit Card, Digital Wallet, COD

## Database Schema

### 1. suppliers.csv

Supplier companies providing products to the platform.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `supplier_id` | INT | Unique identifier | 1 |
| `supplier_name` | VARCHAR | Company name | TechSupply Inc |
| `contact_name` | VARCHAR | Contact person | John Smith |
| `contact_email` | VARCHAR | Email address | john@techsupply.com |
| `contact_phone` | VARCHAR | Phone number | +1-555-0123 |
| `country` | VARCHAR | Operating country | United States |
| `city` | VARCHAR | Operating city | New York |
| `rating` | FLOAT | Supplier rating (1-5) | 4.5 |
| `created_at` | DATE | Registration date | 2022-01-15 |

**Key Characteristics:**
- 100 unique suppliers
- Global distribution across 20+ countries
- Rating distribution: 3.0-5.0
- Created between 2020-2024

### 2. products.csv

Product catalog with 7 categories and pricing.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `product_id` | INT | Unique identifier | 1001 |
| `product_name` | VARCHAR | Product name | Wireless Mouse Pro |
| `category` | VARCHAR | Product category | Electronics |
| `supplier_id` | INT | Supplier reference (FK) | 42 |
| `unit_price` | DECIMAL | Price per unit | 29.99 |
| `cost_price` | DECIMAL | Cost from supplier | 18.00 |
| `sku` | VARCHAR | Stock keeping unit | SKU-1001 |
| `description` | TEXT | Product description | High-precision wireless mouse |
| `created_at` | DATE | Product added date | 2023-06-15 |

**Categories and Pricing:**
- **Electronics:** $50 - $2,000 (smartphones, laptops, accessories)
- **Clothing:** $15 - $200 (apparel, footwear, accessories)
- **Home & Living:** $10 - $500 (furniture, decor, appliances)
- **Beauty & Personal Care:** $5 - $150 (cosmetics, skincare, grooming)
- **Sports & Outdoors:** $20 - $300 (equipment, apparel, accessories)
- **Books & Media:** $5 - $50 (books, ebooks, audiobooks)
- **Grocery & Food:** $2 - $50 (packaged foods, beverages, snacks)

**Relationships:**
- `supplier_id` → `suppliers.supplier_id`

### 3. customers.csv

B2B and B2C customer base with segment classification.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `customer_id` | INT | Unique identifier | 5001 |
| `customer_type` | VARCHAR | B2B or B2C | B2B |
| `b2b_segment` | VARCHAR | B2B segment (nullable) | Ecommerce |
| `company_name` | VARCHAR | Company name (B2B only) | RetailCo Ltd |
| `first_name` | VARCHAR | Contact first name | Sarah |
| `last_name` | VARCHAR | Contact last name | Johnson |
| `email` | VARCHAR | Email address | sarah.j@retailco.com |
| `phone` | VARCHAR | Phone number | +1-555-0456 |
| `address` | TEXT | Street address | 123 Main St |
| `city` | VARCHAR | City | Los Angeles |
| `state` | VARCHAR | State/Province | CA |
| `country` | VARCHAR | Country | United States |
| `postal_code` | VARCHAR | Postal code | 90001 |
| `created_at` | DATE | Registration date | 2023-01-20 |

**Customer Distribution:**
- **B2B Total:** 3,000 (30%)
  - Ecommerce: 899 (30% of B2B)
  - Modern Trade: 1,186 (40% of B2B)
  - Traditional Trade: 915 (30% of B2B)
- **B2C Total:** 7,000 (70%)

**Relationships:**
- `customer_id` → `stores.customer_id` (B2B only)
- `customer_id` → `orders.customer_id`

### 4. stores.csv

Physical store locations for B2B customers.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `store_id` | INT | Unique identifier | 8001 |
| `customer_id` | INT | Customer reference (FK) | 5001 |
| `store_name` | VARCHAR | Store name | RetailCo Downtown |
| `store_code` | VARCHAR | Internal store code | RC-DT-001 |
| `address` | TEXT | Street address | 456 Commerce Ave |
| `city` | VARCHAR | City | Los Angeles |
| `state` | VARCHAR | State/Province | CA |
| `country` | VARCHAR | Country | United States |
| `postal_code` | VARCHAR | Postal code | 90015 |
| `store_size_sqft` | INT | Store size | 15000 |
| `opened_at` | DATE | Store opening date | 2022-03-10 |

**Key Characteristics:**
- 2,500 stores linked to 3,000 B2B customers
- Average stores per B2B customer: 0.83
- Store size range: 5,000 - 50,000 sq ft
- Opened between 2020-2025

**Relationships:**
- `customer_id` → `customers.customer_id` (B2B only)

### 5. promotions.csv

Active promotional campaigns with various discount types.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `promotion_id` | INT | Unique identifier | 101 |
| `promotion_name` | VARCHAR | Campaign name | Summer Sale 2024 |
| `promotion_code` | VARCHAR | Promo code | SUMMER2024 |
| `promotion_type` | VARCHAR | Discount type | Percentage |
| `discount_value` | DECIMAL | Discount amount | 15.00 |
| `min_order_amount` | DECIMAL | Minimum order value | 100.00 |
| `max_discount_amount` | DECIMAL | Maximum discount cap | 500.00 |
| `valid_from` | DATE | Start date | 2024-06-01 |
| `valid_until` | DATE | End date | 2024-08-31 |
| `applicable_to` | VARCHAR | Customer segment | All |
| `is_active` | BOOLEAN | Currently active | true |

**Promotion Types:**
- **Percentage:** X% off (5-25% range)
- **Fixed Amount:** $X off (e.g., $50 off)
- **BOGO:** Buy One Get One (50% off second item)
- **Bundle:** Bundle discount (10-30% off)
- **Cashback:** Cash back percentage (5-15%)

**Applicability:**
- All Customers
- B2B Only
- B2C Only
- Ecommerce Segment
- Modern Trade Segment
- Traditional Trade Segment

**Relationships:**
- `promotion_id` → `orders.promotion_id` (nullable)

### 6. orders.csv

Order headers with calculated totals and applied discounts.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `order_id` | INT | Unique identifier | 100001 |
| `customer_id` | INT | Customer reference (FK) | 5001 |
| `order_date` | DATE | Order placement date | 2024-07-15 |
| `order_status` | VARCHAR | Current status | Completed |
| `payment_method` | VARCHAR | Payment method used | Wire Transfer |
| `payment_status` | VARCHAR | Payment status | Paid |
| `promotion_id` | INT | Applied promotion (FK, nullable) | 105 |
| `subtotal_amount` | DECIMAL | Sum of line items | 12500.00 |
| `discount_amount` | DECIMAL | Promotion discount | 1250.00 |
| `tax_amount` | DECIMAL | Sales tax (8%) | 900.00 |
| `shipping_amount` | DECIMAL | Shipping fee | 150.00 |
| `final_amount` | DECIMAL | Total payable | 12300.00 |
| `shipped_at` | DATE | Shipment date | 2024-07-17 |
| `delivered_at` | DATE | Delivery date | 2024-07-20 |

**Order Statuses:**
- Pending
- Processing
- Shipped
- Delivered
- Completed
- Cancelled

**Payment Methods (B2B):**
- Wire Transfer (most common)
- Credit Card
- Net 30
- Net 60

**Payment Methods (B2C):**
- Credit Card
- Debit Card
- Digital Wallet
- COD (Cash on Delivery)

**Payment Statuses:**
- Pending
- Paid
- Failed
- Refunded

**Key Metrics:**
- Total Orders: 15,000
- Orders with Promotions: 830 (5.5%)
- Average Order Value: $480,333.75
- Order Date Range: 2023-2025

**Relationships:**
- `customer_id` → `customers.customer_id`
- `promotion_id` → `promotions.promotion_id` (nullable)

### 7. order_items.csv

Line items for each order with quantities and pricing.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `order_item_id` | INT | Unique identifier | 200001 |
| `order_id` | INT | Order reference (FK) | 100001 |
| `product_id` | INT | Product reference (FK) | 1001 |
| `quantity` | INT | Units ordered | 100 |
| `unit_price` | DECIMAL | Price per unit at order time | 29.99 |
| `discount_percent` | DECIMAL | Item-level discount | 0.00 |
| `line_total` | DECIMAL | quantity × unit_price × (1 - discount) | 2999.00 |

**Key Characteristics:**
- Total Order Items: 176,729
- Average Items per Order: 11.78
- Quantity Range: 1-20 (B2C), 10-500 (B2B)
- Line totals calculated with item-level discounts

**Relationships:**
- `order_id` → `orders.order_id`
- `product_id` → `products.product_id`

### 8. inventory_transactions.csv

Stock movements tracking inventory changes.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `transaction_id` | INT | Unique identifier | 300001 |
| `product_id` | INT | Product reference (FK) | 1001 |
| `transaction_type` | VARCHAR | Type of movement | OUT |
| `quantity` | INT | Units moved (+/-) | -100 |
| `transaction_date` | DATE | Transaction date | 2024-07-15 |
| `reference_id` | INT | Order ID (if applicable) | 100001 |
| `reference_type` | VARCHAR | Reference type | order |
| `notes` | TEXT | Transaction notes | Order fulfillment |

**Transaction Types:**
- **IN:** Stock received from suppliers (initial stock)
- **OUT:** Stock sold to customers (order fulfillment)
- **ADJUSTMENT:** Manual inventory adjustments (corrections, damage, etc.)

**Key Characteristics:**
- Total Transactions: 177,723
- Initial Stock (IN): ~994 transactions (one per product)
- Order Fulfillment (OUT): ~176,729 transactions (matches order items)
- Adjustments: Minimal

**Relationships:**
- `product_id` → `products.product_id`
- `reference_id` → `orders.order_id` (when reference_type = 'order')

## Data Relationships

### Entity Relationship Diagram

```
suppliers (1) ──────< (N) products
                           |
                           v
                    order_items (N) ────> (1) orders ────> (1) customers
                           |                    |                  |
                           v                    v                  v
                    inventory_txns (N)   promotions (1)      stores (N)
```

### Key Relationships:

1. **Suppliers → Products**: One supplier provides many products
2. **Products → Order Items**: One product appears in many order items
3. **Orders → Order Items**: One order contains many line items
4. **Customers → Orders**: One customer places many orders
5. **Customers → Stores**: One B2B customer operates many stores
6. **Promotions → Orders**: One promotion applies to many orders
7. **Products → Inventory Transactions**: One product has many stock movements
8. **Orders → Inventory Transactions**: One order triggers inventory OUT transactions

## Data Quality & Realism

### Realistic Distributions

- **Product Pricing:** Category-appropriate price ranges
- **Order Values:** B2B orders significantly larger than B2C
- **Promotions:** 5.5% promotion usage rate (realistic)
- **Customer Segments:** 30/40/30 split for B2B segments
- **Geographic Distribution:** Global customers with weighted countries
- **Temporal Data:** Orders span 2023-2025 with realistic dates

### Data Integrity

- **Foreign Keys:** All relationships properly maintained
- **Referential Integrity:** No orphaned records
- **Business Logic:** Tax, shipping, discounts calculated correctly
- **Inventory Tracking:** Stock movements match order fulfillment
- **Date Consistency:** shipped_at > order_date, delivered_at > shipped_at

## Usage Examples

### Load Data with Pandas

```python
import pandas as pd

# Load datasets
suppliers = pd.read_csv('data/seed_data/suppliers.csv')
products = pd.read_csv('data/seed_data/products.csv')
customers = pd.read_csv('data/seed_data/customers.csv')
stores = pd.read_csv('data/seed_data/stores.csv')
promotions = pd.read_csv('data/seed_data/promotions.csv')
orders = pd.read_csv('data/seed_data/orders.csv')
order_items = pd.read_csv('data/seed_data/order_items.csv')
inventory = pd.read_csv('data/seed_data/inventory_transactions.csv')
```

### Query Examples

```python
# Get total sales by customer type
sales_by_type = orders.merge(customers, on='customer_id') \
    .groupby('customer_type')['final_amount'].sum()

# Get top 10 products by revenue
top_products = order_items.merge(products, on='product_id') \
    .groupby('product_name')['line_total'].sum() \
    .nlargest(10)

# Calculate average order value by B2B segment
b2b_aov = orders.merge(
    customers[customers['customer_type'] == 'B2B'],
    on='customer_id'
).groupby('b2b_segment')['final_amount'].mean()

# Get promotion effectiveness
promo_stats = orders[orders['promotion_id'].notna()] \
    .groupby('promotion_id').agg({
        'order_id': 'count',
        'discount_amount': 'sum',
        'final_amount': 'sum'
    })

# Inventory turnover by category
inventory_turnover = inventory.merge(products, on='product_id') \
    .groupby('category')['quantity'].sum()
```

### SQL Import Example

```sql
-- PostgreSQL
COPY suppliers FROM '/path/to/suppliers.csv' DELIMITER ',' CSV HEADER;
COPY products FROM '/path/to/products.csv' DELIMITER ',' CSV HEADER;
COPY customers FROM '/path/to/customers.csv' DELIMITER ',' CSV HEADER;
COPY stores FROM '/path/to/stores.csv' DELIMITER ',' CSV HEADER;
COPY promotions FROM '/path/to/promotions.csv' DELIMITER ',' CSV HEADER;
COPY orders FROM '/path/to/orders.csv' DELIMITER ',' CSV HEADER;
COPY order_items FROM '/path/to/order_items.csv' DELIMITER ',' CSV HEADER;
COPY inventory_transactions FROM '/path/to/inventory_transactions.csv' DELIMITER ',' CSV HEADER;
```

## Regenerating Data

To regenerate the seed data with different characteristics:

```bash
# Activate virtual environment
cd /Users/aritra.biswas/Desktop/workspace/projects/z/scripts
source .venv/bin/activate

# Run generator script
python generate_synthetic_seed_data.py

# Or from project root
../scripts/.venv/bin/python scripts/generate_synthetic_seed_data.py
```

### Customization Options

Edit `scripts/generate_synthetic_seed_data.py` to modify:

```python
# Configuration constants (lines 19-31)
NUM_SUPPLIERS = 100          # Number of supplier companies
NUM_PRODUCTS = 1000          # Number of products
NUM_B2B_CUSTOMERS = 3000     # B2B customers
NUM_B2C_CUSTOMERS = 7000     # B2C customers
NUM_STORES = 2500            # Physical stores
NUM_PROMOTIONS = 50          # Promotional campaigns
NUM_ORDERS = 15000           # Total orders

RANDOM_SEED = 42             # For reproducibility
```

## Business Insights

### Sales Performance

- **Total Revenue:** $7.01 billion across 15,000 orders
- **Average Order Value:** $480,334 (heavily influenced by large B2B orders)
- **Items Sold:** 30.09 million units
- **Promotion Usage:** 5.5% of orders use promotions

### Customer Analysis

- **B2B vs B2C Split:** 30% B2B customers generate majority of revenue
- **B2B Segments:** Modern Trade (40%) > Traditional (30%) = Ecommerce (30%)
- **B2C Volume:** 70% of customers, smaller individual transactions

### Product Categories

- **Electronics:** Highest unit price ($50-$2,000)
- **Grocery:** Highest volume, lowest prices ($2-$50)
- **Clothing:** Mid-range pricing ($15-$200)

### Geographic Distribution

- Customers across 50+ countries
- Major markets: United States, United Kingdom, Canada, Germany, India

## Technical Notes

### Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
Faker>=18.0.0
```

### Performance

- Generation time: ~30 seconds
- Memory usage: ~500MB peak
- Output size: 32MB total (uncompressed CSV)

### Warnings

The script may show FutureWarning messages about dtype compatibility when updating order totals. These are harmless and will be resolved in future pandas versions.

## Support

For issues or questions about the seed data:

1. Check if data regeneration resolves the issue
2. Verify CSV files are not corrupted
3. Ensure pandas, numpy, and Faker are properly installed
4. Review script logs for generation errors

## Version History

- **v1.0.0** (January 4, 2026)
  - Initial seed data generation
  - 8 interconnected tables
  - 383,096 total rows
  - B2B/B2C sales simulation
  - Promotion system
  - Inventory tracking

---

**Last Updated:** January 4, 2026
**Generated By:** Synthetic Seed Data Generator v1.0

---

Perfect! I've successfully completed the synthetic seed data generation task. Here's what was delivered:

Summary

✅ Generated 383,096 rows of realistic sales data across 8 interconnected tables
✅ Created comprehensive documentation explaining schema, relationships, and usage

Generated Files

Location: data/seed_data/

| File                       | Rows    | Size   | Description                    |
|----------------------------|---------|--------|--------------------------------|
| suppliers.csv              | 100     | 11 KB  | Supplier companies             |
| products.csv               | 994     | 119 KB | Product catalog (7 categories) |
| customers.csv              | 10,000  | 1.4 MB | B2B (3,000) + B2C (7,000)      |
| stores.csv                 | 2,500   | 287 KB | Physical store locations       |
| promotions.csv             | 50      | 5.3 KB | Promotional campaigns          |
| orders.csv                 | 15,000  | 2.1 MB | Order headers with totals      |
| order_items.csv            | 176,729 | 12 MB  | Line items per order           |
| inventory_transactions.csv | 177,723 | 17 MB  | Stock movements                |
| README.md                  | -       | -      | Comprehensive documentation    |

Business Metrics

- Total Sales: $7.01 billion
- Average Order Value: $480,334
- Total Items Sold: 30.09 million units
- Orders with Promotions: 830 (5.5%)

B2B Segment Distribution

- Ecommerce: 899 customers (30%)
- Modern Trade: 1,186 customers (40%)
- Traditional Trade: 915 customers (30%)

Key Features

✅ Proper foreign key relationships across all tables
✅ Realistic pricing by product category (Electronics: $50-$2K, Grocery: $2-$50)
✅ Business logic for order calculations (discounts, tax, shipping)
✅ Inventory tracking tied to order fulfillment
✅ Geographic distribution across 50+ countries
✅ Date consistency (shipped_at > order_date > created_at)

Documentation Highlights

The README includes:
- Complete schema documentation for all 8 tables
- Entity relationship diagram
- Usage examples with pandas and SQL
- Instructions to regenerate data
- Business insights and analytics examples

All seed data is now ready for use in testing, development, or demonstrations!
