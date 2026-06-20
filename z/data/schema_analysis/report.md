# Database Schema Analysis Report

**Database:** `raw_data_db`  
**Schema:** `seed_data_raw`  
**Analyzed:** 2026-01-08T17:23:23.642493  
**Analyzer Version:** 2.0  

## Executive Summary

- **Tables:** 8
- **Total Rows:** 383,096
- **High Cardinality Threshold:** 200

### Overall Assessment

- **Quality:** Good
- **Normalization:** mixed
- **NL2SQL Suitability:** Good

**Summary:** The schema models a retail/e‑commerce operational dataset with clear separation of orders, order items, products and inventory movements. It is generally well-structured for analytical workloads but lacks explicit primary/foreign key constraints and some referential rigor. With modest cleanup (declaring keys, adding indexes and a few reference tables) it will support reporting, OLAP and NL2SQL queries effectively.

## 📝 Schema Description

This appears to be a retail or e‑commerce / wholesale domain dataset capturing customers, stores, orders, order items, products, inventory movements, promotions and suppliers. Key entities: customers (customer master and segmentation), orders (transactional sales headers), order_items (sales line items/fact), products (catalog), inventory_transactions (stock movements), promotions (discount rules), stores (physical/virtual locations) and suppliers (vendor master). The model is largely star-like for analytics: orders and inventory_transactions act as fact-ish tables linked to dimensional entities such as customers, products, stores and suppliers. Typical business analyses enabled include sales by customer segment or geography, product/category performance, promotion effectiveness, inventory movement and stock reconciliation, and supplier performance. Top 5 business questions that can be answered: 1) What are sales (revenue, units) by product, category, store and customer segment over time? 2) Which promotions generated the highest lift in orders or revenue and what was their ROI? 3) Which products have the highest inventory turnover or are at risk of stockouts? 4) Who are the top customers by lifetime value and what segments show churn or growth? 5) How do suppliers perform on volume, country, and lead time metrics and which suppliers drive the most cost or quality issues?

### Table Relationships

**Central/Fact Tables:** `orders`, `order_items`, `inventory_transactions`  
**Lookup/Dimension Tables:** `customers`, `products`, `promotions`, `stores`, `suppliers`  

Analytical joins center on orders -> order_items (order_id), and order_items/inventory_transactions -> products (product_id). Orders link to customers (customer_id) and optionally promotions (promotion_id); stores reference customers (store owner/relationship) and can be joined to orders if order-store linkage exists in data. Products reference suppliers (supplier_id) for vendor analytics. inventory_transactions.reference_id/reference_type appears to link stock movements to orders, order items or stores (polymorphic reference) which supports audit and stock reconciliation but should be formalized. These paths enable time series sales and inventory analysis, customer segmentation and cohorting, promotion lift and supplier performance reporting. To improve clarity and analytic performance, add primary/foreign keys, indexes on join columns and normalize any repeated categorical reference columns (e.g., promotion applicable categories).

## 🚨 Data Quality Issues (NL2SQL Risks)

*No data quality issues detected.*

## 💡 Recommendations

*No recommendations available.*

## 📊 Table Details

### customers

**Rows:** 10,000  
**Columns:** 15  
**Primary Keys:** *None*  

**Purpose:** Master customer reference for the business: contains customer identifiers, contact and address details, classification (type/segment/status), registration date and credit limit. Serves as the primary source for customer-level reporting, segmentation and as the join point for transactional tables (orders, order_items, promotions, etc.).

**Business Questions:**

- How many active customers are in each customer_segment and customer_type?
- How many new customers registered in a given period (month/quarter/year)?
- What is the distribution of customers by city/state and which locations have the most customers?
- What is the total and average credit_limit by segment/type (requires casting credit_limit to numeric)?
- Which customers (by customer_id or company_name) are inactive or have no recent registrations and should be targeted for reactivation?

**Key Columns:**

- **`customer_id`** (nvarchar(32), NULL) - 10,000 distinct values ⚠️ HIGH CARDINALITY
  - *Unique customer identifier string (nvarchar). Appears to be unique for each row (10,000 distinct values).*
- **`customer_type`** (nvarchar(16), NULL) - 2 distinct values
  - *High-level type classification: B2C or B2B.*
- **`customer_segment`** (nvarchar(44), NULL) - 4 distinct values
  - *More granular customer segmentation (Direct Consumer, Modern Trade, Traditional Trade, Ecommerce).*
- **`company_name`** (nvarchar(38), NULL) - 25 distinct values ⚠️ 70.0% NULL
  - *Business/company name for B2B customers; ~70% NULL (likely null for individual consumers).*
- **`contact_person`** (nvarchar(38), NULL) - 10,000 distinct values ⚠️ HIGH CARDINALITY
  - *Name of the contact person at the customer/company. High cardinality (likely unique per customer).*
- **`email`** (nvarchar(68), NULL) - 10,000 distinct values ⚠️ HIGH CARDINALITY
  - *Customer email address; high cardinality and likely unique per customer.*
- **`phone`** (nvarchar(40), NULL) - 10,000 distinct values ⚠️ HIGH CARDINALITY
  - *Customer phone number; high cardinality, stored as text with formatting characters.*
- **`address`** (nvarchar(42), NULL) - 9,793 distinct values ⚠️ HIGH CARDINALITY
  - *Street address free-text field; high cardinality and many unique values.*
- **`city`** (nvarchar(36), NULL) - 18 distinct values
  - *City of the customer; low-to-moderate cardinality (18 distinct values).*
- **`state`** (nvarchar(14), NULL) - 11 distinct values
  - *Two-letter state code (observed lengths up to 2); 11 distinct states with distribution across the dataset.*
- *(... and 5 more columns)*

---

### inventory_transactions

**Rows:** 177,723  
**Columns:** 8  
**Primary Keys:** *None*  

**Purpose:** Records of inventory movements (inbound and outbound) per product. Each row represents one transaction affecting stock levels and references an origin (Order or Initial Stock). It is the primary event log for inventory flow in the schema.

**Business Questions:**

- Which products have the highest outbound (OUT) quantity over a given time range?
- What is the daily/weekly trend of inventory movements (IN vs OUT) for a product or product group?
- What was the cumulative stock change per product since initial stock entries?
- Which orders (reference_id) generated the largest inventory outflows?
- Which products have unexpected negative/positive quantity sign patterns relative to transaction_type?

**Key Columns:**

- **`transaction_id`** (nvarchar(32), NULL) - 177,723 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for each inventory transaction event.*
- **`product_id`** (nvarchar(28), NULL) - 994 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier of the product affected by the transaction.*
- **`transaction_type`** (nvarchar(16), NULL) - 2 distinct values
  - *Categorical indicator of movement direction, e.g., 'IN' or 'OUT'.*
- **`quantity`** (nvarchar(18), NULL) - 1,125 distinct values ⚠️ HIGH CARDINALITY
  - *The amount of stock moved in the transaction, stored as text (nvarchar). Values appear numeric and often negative (e.g., -1, -3).*
- **`transaction_date`** (nvarchar(48), NULL) - 15,649 distinct values ⚠️ HIGH CARDINALITY
  - *Timestamp of when the transaction occurred stored as nvarchar (text). Likely in 'YYYY-MM-DD HH:MM:SS' or similar format (max len 19).*
- **`reference_id`** (nvarchar(32), NULL) - 15,000 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier for the source or related entity of the transaction (e.g., order id). Some values may be null (~0.6%).*
- **`reference_type`** (nvarchar(36), NULL) - 2 distinct values
  - *Categorizes the reference_id (e.g., 'Order' or 'Initial Stock').*
- **`notes`** (nvarchar(70), NULL) - 15,001 distinct values ⚠️ HIGH CARDINALITY
  - *Free-text notes about the transaction (reason, context).*

---

### order_items

**Rows:** 176,729  
**Columns:** 8  
**Primary Keys:** *None*  

**Purpose:** Line-level order data: each row is a single item on an order. It records which product was sold, the quantity and per-item price, and monetary adjustments (discount, tax) and the computed total for that line. This table is the detailed transactional layer that supports roll-ups to orders, products, customers and store-level sales analyses.

**Business Questions:**

- What is total revenue, total discounts and tax collected over a time period (after joining to orders for dates)?
- Which products generate the most revenue and the highest quantity sold?
- What is the average number of items and average line total per order?
- How do discounts and taxes affect line totals and margins (e.g., average discount per line or percent discount)?
- Are there mismatches between reported total_amount and computed line total (quantity*unit_price - discount + tax)?

**Key Columns:**

- **`order_item_id`** (nvarchar(38), NULL) - 176,729 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for the line item (string). Distinct count equals row count, suggesting it functions as a row-level unique id.*
- **`order_id`** (nvarchar(32), NULL) - 15,000 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier for the order that this line belongs to (string). 15,000 distinct values across 176,729 rows — multiple items per order.*
- **`product_id`** (nvarchar(28), NULL) - 994 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier of the product sold for this line (string). ~994 distinct product values; top products show small percentage shares.*
- **`quantity`** (nvarchar(16), NULL) - 496 distinct values ⚠️ HIGH CARDINALITY
  - *Quantity of the product sold on this line (stored as nvarchar). Small integer values dominate; distinct ~496 (may include formatting noise or junk).*
- **`unit_price`** (nvarchar(24), NULL) - 970 distinct values ⚠️ HIGH CARDINALITY
  - *Price per unit for the product on this line (stored as nvarchar). Many distinct values, decimals visible in top values.*
- **`discount_amount`** (nvarchar(28), NULL) - 105,131 distinct values ⚠️ HIGH CARDINALITY
  - *Discount applied to the line (string representing numeric currency). Very high distinct count indicating line-specific discounts.*
- **`tax_amount`** (nvarchar(26), NULL) - 111,530 distinct values ⚠️ HIGH CARDINALITY
  - *Tax applied to the line (string representing numeric currency). High distinctness, likely many small variations per line.*
- **`total_amount`** (nvarchar(28), NULL) - 156,037 distinct values ⚠️ HIGH CARDINALITY
  - *Reported line total (string). Should represent final line charge: quantity*unit_price minus discount plus tax (but must be validated). Distinct values nearly as many as rows, indicating mostly unique totals.*

---

### orders

**Rows:** 15,000  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** This table records individual customer orders (transaction header) including identifiers, monetary amounts, status, payment and shipping metadata. It functions as the central sales/orders source in the schema and is the primary join point to order_items, customers and promotions for revenue, fulfillment and customer analytics.

**Business Questions:**

- What is total revenue and order count by day/week/month?
- Which payment methods and order statuses contribute most to revenue?
- How often and how much are discounts used, and what is their impact on final_amount?
- What is the distribution of shipping charges and which orders pay shipping?
- What is on-time delivery performance (where delivery_date exists) and average delivery lag?

**Key Columns:**

- **`order_id`** (nvarchar(32), NULL) - 15,000 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for the order (transaction header). Stored as nvarchar; max observed length 11. No declared primary key.*
- **`customer_id`** (nvarchar(32), NULL) - 7,519 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier for the customer who placed the order. nvarchar; high cardinality (~7.5k distinct).*
- **`order_date`** (nvarchar(48), NULL) - 14,996 distinct values ⚠️ HIGH CARDINALITY
  - *Order placement date/time stored as nvarchar (observed max length 19). Many distinct values (~14996) indicating timestamp granularity.*
- **`order_status`** (nvarchar(28), NULL) - 5 distinct values
  - *Order lifecycle status (Categorical: Delivered, Shipped, Confirmed, Pending, Cancelled).*
- **`num_items`** (nvarchar(14), NULL) - 50 distinct values
  - *Number of items in the order stored as nvarchar (small integer-like values, distinct 50).*
- **`subtotal_amount`** (nvarchar(30), NULL) - 14,909 distinct values ⚠️ HIGH CARDINALITY
  - *Order subtotal before discounts, tax and shipping stored as nvarchar (monetary values). Very high cardinality.*
- **`discount_amount`** (nvarchar(22), NULL) - 130 distinct values
  - *Discount applied to the order stored as nvarchar. Mostly zero (97.1%); 2.7% nulls; 130 distinct values.*
- **`tax_amount`** (nvarchar(28), NULL) - 13,687 distinct values ⚠️ HIGH CARDINALITY
  - *Tax applied to the order stored as nvarchar; high cardinality and 2.7% nulls.*
- **`shipping_amount`** (nvarchar(22), NULL) - 4,235 distinct values ⚠️ HIGH CARDINALITY
  - *Shipping charge for the order stored as nvarchar; many zeroes (70.4%) indicating free shipping for most orders; otherwise many distinct values.*
- **`final_amount`** (nvarchar(30), NULL) - 14,507 distinct values ⚠️ HIGH CARDINALITY
  - *Final charged amount after discounts, tax and shipping stored as nvarchar; high cardinality and 2.7% nulls.*
- *(... and 4 more columns)*

---

### products

**Rows:** 994  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Catalog of products sold by the business. Contains identification (ids, sku, name), classification (category, subcategory, brand), pricing/costs, inventory snapshot, supplier link, physical attributes (weight) and creation date. Serves as the product master for sales, inventory, procurement and promotion analyses.

**Business Questions:**

- Which products have the highest gross margin (unit_price - cost_price) and what are their categories?
- How many products are currently low-stock (stock_quantity below a threshold) per supplier or category?
- What is the distribution of products by category/subcategory/brand?
- When were products added (created_date): how many new products per month/quarter?
- Which suppliers provide the most products and which product lines (by category) are concentrated with a single supplier?

**Key Columns:**

- **`product_id`** (nvarchar(28), NULL) - 994 distinct values ⚠️ HIGH CARDINALITY
  - *Primary product identifier from the source system (string). Appears to be unique per row (distinct ~= row count).*
- **`product_name`** (nvarchar(78), NULL) - 992 distinct values ⚠️ HIGH CARDINALITY
  - *Human-readable product title or description.*
- **`category`** (nvarchar(38), NULL) - 7 distinct values
  - *High-level product category (e.g., Clothing, Electronics, Books).*
- **`subcategory`** (nvarchar(38), NULL) - 32 distinct values
  - *More granular classification under category (e.g., Footwear, Accessories).*
- **`brand`** (nvarchar(40), NULL) - 35 distinct values
  - *Manufacturer or brand name associated with the product.*
- **`sku`** (nvarchar(38), NULL) - 994 distinct values ⚠️ HIGH CARDINALITY
  - *Stock keeping unit identifier (string). Typically unique per sellable item or variant.*
- **`unit_price`** (nvarchar(24), NULL) - 970 distinct values ⚠️ HIGH CARDINALITY
  - *Selling price per unit stored as nvarchar text (floating numeric values in string form).*
- **`cost_price`** (nvarchar(24), NULL) - 957 distinct values ⚠️ HIGH CARDINALITY
  - *Cost to acquire/manufacture the product stored as nvarchar text (floating numeric values as strings).*
- **`stock_quantity`** (nvarchar(18), NULL) - 629 distinct values ⚠️ HIGH CARDINALITY
  - *Current on-hand inventory quantity snapshot, stored as nvarchar (integers represented as text).*
- **`supplier_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Identifier of the supplier providing the product (string), can link to suppliers table.*
- *(... and 2 more columns)*

---

### promotions

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** Catalog of promotional offers (discounts, BOGO, bundles, cashback) used by the business to apply incentives to orders/products/customers. It defines promotion metadata and constraints (dates, eligibility, caps) that are used when analyzing promotion performance or when enforcing promotion rules.

**Business Questions:**

- How many promotions exist by promotion_type and applicable_category?
- Which promotions are currently active or will start within a given date range?
- What are the typical discount values and caps (percent vs amount) across promotions?
- Which promotions are restricted to B2B or B2C, and how many promos target each customer type?
- Which promotions have low usage limits (per-customer or total) that may constrain adoption?

**Key Columns:**

- **`promotion_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Unique identifier for a promotion (catalog key).*
- **`promotion_name`** (nvarchar(70), NULL) - 50 distinct values
  - *Human-readable name/label for the promotion.*
- **`promotion_type`** (nvarchar(48), NULL) - 5 distinct values
  - *Category of promotion logic (e.g., Bundle Deal, BOGO, Percentage Discount, Fixed Amount Off, Cashback).*
- **`discount_percentage`** (nvarchar(18), NULL) - 14 distinct values ⚠️ 68.0% NULL
  - *Percent-off value for percentage-type promotions (stored as text). Many rows null — only relevant for percentage discounts.*
- **`discount_amount`** (nvarchar(20), NULL) - 8 distinct values ⚠️ 84.0% NULL
  - *Fixed discount amount (monetary) applied by some promotions (stored as text). Mostly NULL except for fixed-amount promotions or cashback entries.*
- **`start_date`** (nvarchar(30), NULL) - 49 distinct values
  - *Promotion start date (stored as string YYYY-MM-DD).*
- **`end_date`** (nvarchar(30), NULL) - 49 distinct values
  - *Promotion end date (stored as string YYYY-MM-DD).*
- **`applicable_customer_type`** (nvarchar(16), NULL) - 3 distinct values
  - *Target customer segment for the promotion: B2B, B2C, or ALL.*
- **`applicable_category`** (nvarchar(38), NULL) - 7 distinct values
  - *Product category that the promotion applies to (e.g., Beauty, Home & Kitchen). NULL means category unspecified or applies broadly.*
- **`min_order_amount`** (nvarchar(16), NULL) - 5 distinct values
  - *Minimum order total required to qualify for the promotion (stored as text).*
- *(... and 4 more columns)*

---

### stores

**Rows:** 2,500  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** This table stores master-level information about retail stores (locations) for the business: identifiers, ownership customer, descriptive attributes (name, type), address and geography, opening date, physical size and employee counts. It acts as the canonical store dimension for analyses that require store characteristics and as the join point between transactional tables (orders, inventory, order_items) and store-level attributes.

**Business Questions:**

- How many stores do we have by store_type, city and state?
- Which stores opened in the last 12 months (or a given date range)?
- What is the distribution of store sizes (sqft) and employee_count across store types?
- Which customers own the largest number of stores (by customer_id)?
- List stores in a given city or postal code area for operations planning

**Key Columns:**

- **`store_id`** (nvarchar(28), NULL) - 2,500 distinct values ⚠️ HIGH CARDINALITY
  - *Unique store identifier (string). Appears to uniquely identify rows; high cardinality with 2500 distinct values across 2500 rows.*
- **`customer_id`** (nvarchar(32), NULL) - 1,502 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier for the customer/account associated with the store (string). Not unique at row level; 1502 distinct values.*
- **`store_name`** (nvarchar(70), NULL) - 450 distinct values ⚠️ HIGH CARDINALITY
  - *Human-readable store name (string). Useful for display, fuzzy matching and grouping similar brand names.*
- **`store_type`** (nvarchar(44), NULL) - 3 distinct values
  - *Categorical store channel/type (Modern Trade, Traditional Trade, Ecommerce). Low cardinality (3 values).*
- **`address`** (nvarchar(38), NULL) - 2,424 distinct values ⚠️ HIGH CARDINALITY
  - *Street address for the store (string). High cardinality and largely unique.*
- **`city`** (nvarchar(36), NULL) - 18 distinct values
  - *City where the store is located (string). Medium-low cardinality (18 distinct).*
- **`state`** (nvarchar(14), NULL) - 11 distinct values
  - *Two-letter state code (string). 11 distinct values in dataset; common grouping dimension.*
- **`country`** (nvarchar(16), NULL) - 1 distinct values
  - *Country code or name (string). In this dataset contains only 'USA'.*
- **`postal_code`** (nvarchar(20), NULL) - 2,464 distinct values ⚠️ HIGH CARDINALITY
  - *Postal / ZIP code for the store (string). High cardinality (2464 distinct).*
- **`opening_date`** (nvarchar(30), NULL) - 766 distinct values ⚠️ HIGH CARDINALITY
  - *Store opening date, currently stored as nvarchar (appears ISO yyyy-mm-dd). 766 distinct values and many recent dates in sample.*
- *(... and 2 more columns)*

---

### suppliers

**Rows:** 100  
**Columns:** 8  
**Primary Keys:** *None*  

**Purpose:** Master list of external suppliers providing goods or components to the business; holds supplier identity and contact/metadata used for supplier-level analysis, filtering and joining with transactional tables (products, orders, inventory, promotions) to measure supply-side activity and performance.

**Business Questions:**

- How many suppliers do we have and how are they distributed by country?
- Which suppliers have the highest/lowest ratings?
- Which suppliers were established before a given year (e.g., 1990)?
- Which suppliers are missing contact information (email or phone)?
- What is the average rating per country or per cohort of established_year?

**Key Columns:**

- **`supplier_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Unique identifier for the supplier (nvarchar). Appears unique across rows but stored as text and can be NULL.*
- **`supplier_name`** (nvarchar(68), NULL) - 56 distinct values
  - *Human-readable supplier company name (nvarchar). Not strictly unique; some repeated or similar names exist.*
- **`contact_person`** (nvarchar(46), NULL) - 100 distinct values
  - *Primary contact person at the supplier (nvarchar), typically a name or role.*
- **`email`** (nvarchar(88), NULL) - 100 distinct values
  - *Supplier contact email address (nvarchar), used for electronic communications.*
- **`phone`** (nvarchar(40), NULL) - 100 distinct values
  - *Supplier contact phone number (nvarchar), may include country codes and punctuation.*
- **`country`** (nvarchar(32), NULL) - 10 distinct values
  - *Country of the supplier (nvarchar); low cardinality with top entries like China, France, Italy, Japan, South Korea.*
- **`rating`** (nvarchar(16), NULL) - 21 distinct values
  - *Supplier quality/performance rating stored as nvarchar; values look numeric (decimals) but are text (e.g., '3.10000000000000', '4.0').*
- **`established_year`** (nvarchar(18), NULL) - 35 distinct values
  - *Year the supplier was established stored as nvarchar; values appear as 4-digit years (e.g., '1986').*

---


---

*Report generated on 2026-01-08 17:28:58*
