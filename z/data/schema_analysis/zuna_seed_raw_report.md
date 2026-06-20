# Database Schema Analysis Report

**Database:** `raw_data_db`  
**Schema:** `zuna_seed_raw`  
**Analyzed:** 2026-01-08T23:58:17.374143  
**Analyzer Version:** 2.0  

## Executive Summary

- **Tables:** 86
- **Total Rows:** 86,140
- **High Cardinality Threshold:** 200

### Overall Assessment

- **Quality:** Needs_Improvement
- **Normalization:** mixed
- **NL2SQL Suitability:** Fair

**Summary:** The schema covers a broad omni‑channel retail domain (B2B, ecom, POS, inventory and logistics) and contains many clearly named, domain‑relevant tables. However, it lacks declared primary/foreign keys, has several 'Unnamed' columns and inconsistent column naming/units and uses JSON columns in many places — all of which reduce data integrity and make relational querying and automation harder. With modest cleanup (keys, consistent types, removed/renamed unnamed columns) it would be well suited for analytics and NL2SQL access.

## 📝 Schema Description

This is an omni‑channel retail and logistics schema spanning B2B commerce, e‑commerce, point‑of‑sale, inventory and shipment operations. Key entities include customers, orders (and order_items/lines), products (and variants), inventory/product_inventory, shipments/dispatches/tracking events, payments/invoices/credit_notes, returns/quality_inspections, and aggregated sales snapshots (daily/monthly/yearly). The data model mixes transactional tables (orders, order_items, payments, shipments) with operational event streams and precomputed aggregated summary tables for fast analytical queries. Typical business analyses supported include channel‑level sales and trends, SKU performance, inventory health and reorder needs, fulfillment and delivery performance, return and quality root‑cause analyses, and financial reconciliation between invoices/payments/refunds. Top 5 business questions this schema can answer: (1) What are sales (gross/net) by channel, centre or time period and which SKUs drive revenue? (2) Which SKUs or centres are at risk of stockouts or need reorder based on inventory and sales velocity? (3) What are on‑time delivery and fulfillment metrics and where are delays occurring (dispatch -> tracking -> delivery events)? (4) What are return and refund rates by SKU, customer segment and reason code and how do they impact net sales? (5) Are invoices and payments reconciled (aging/unpaid invoices, credit notes, refunds) and what is outstanding AR?

### Table Relationships

**Central/Fact Tables:** `orders / ecom_orders / b2b_orders / pos_transactions`, `order_items / b2b_order_lines / pos_transaction_lines`, `products / b2b_products / pos_products / product_variants`, `product_inventory / inventory_items / product_pricing`, `shipments / b2b_dispatches / shipment_tracking_events / delivery_status`, `payments / b2b_payments / ecom_payments / ecom_refunds / b2b_credit_notes`, `customers / ecom_customers / b2b_customers / ecom_customer_addresses`  
**Lookup/Dimension Tables:** `product_variants, pos_stores, pos_terminals, b2b_sales_agents, b2b_vendor_partners, ecom_vendors, delivery_slots, ecom_coupons, product_pricing, price_list`  

The logical model is typical star‑like for retail analytics: transactional facts (orders, order_items, pos_transactions, product_sales aggregates) join to dimensions (products, customers, stores/centres, vendors). Order_id is the primary analytical key that links orders -> order_items -> shipments -> returns -> invoices -> payments and related events. Product SKU ties sales aggregates (product_wise_sales, pos_product_wise_sales, ecom_product_wise_sales) to product metadata and inventory tables for SKU‑level analysis. Event and stream tables (b2b_events_stream, ecom_activity_log, shipment_tracking_events) allow time‑series and operational metrics; precomputed daily/monthly/yearly summary tables enable fast reporting. Current gaps (no declared PKs/FKs, inconsistent column naming, JSON fields for structured data) mean relationships are inferred rather than enforced—analytics are possible but require upfront lineage mapping and some ETL/curation to ensure reliable joins.

## 🚨 Data Quality Issues (NL2SQL Risks)

### ❌ Wrong Table Selection Risks (94 issues)

1. **Similar Tables:** `b2b_product_sales` ↔️ `product_sales`
   - *Issue:* Similar table names 'b2b_product_sales' and 'product_sales' may confuse NL2SQL

2. **Similar Tables:** `b2b_products` ↔️ `products`
   - *Issue:* Similar table names 'b2b_products' and 'products' may confuse NL2SQL

3. **Similar Tables:** `b2b_returns` ↔️ `returns`
   - *Issue:* Similar table names 'b2b_returns' and 'returns' may confuse NL2SQL

4. **Similar Tables:** `ecom_ticket` ↔️ `ecom_ticket_messages`
   - *Issue:* Similar table names 'ecom_ticket' and 'ecom_ticket_messages' may confuse NL2SQL

5. **Similar Tables:** `pos_products` ↔️ `pos_products_sales`
   - *Issue:* Similar table names 'pos_products' and 'pos_products_sales' may confuse NL2SQL

6. **Similar Tables:** `pos_products` ↔️ `products`
   - *Issue:* Similar table names 'pos_products' and 'products' may confuse NL2SQL

7. **Similar Tables:** `pos_products_sales` ↔️ `products`
   - *Issue:* Similar table names 'pos_products_sales' and 'products' may confuse NL2SQL

8. **Similar Tables:** `pos_returns` ↔️ `returns`
   - *Issue:* Similar table names 'pos_returns' and 'returns' may confuse NL2SQL

9. **Table:** `b2b_contracts`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_contracts

10. **Table:** `b2b_credit_notes`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_credit_notes

11. **Table:** `b2b_customer_addresses`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_customer_addresses

12. **Table:** `b2b_customers`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_customers

13. **Table:** `b2b_dispatches`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_dispatches

14. **Table:** `b2b_events_stream`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_events_stream

15. **Table:** `b2b_invoices`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_invoices

16. **Table:** `b2b_kpi_daily_snapshots`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_kpi_daily_snapshots

17. **Table:** `b2b_order_allocations`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_order_allocations

18. **Table:** `b2b_order_events`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_order_events

19. **Table:** `b2b_order_lines`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_order_lines

20. **Table:** `b2b_orders`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_orders

21. **Table:** `b2b_payments`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_payments

22. **Table:** `b2b_picking_batches`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_picking_batches

23. **Table:** `b2b_portal_api_clients`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_portal_api_clients

24. **Table:** `b2b_price_list`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_price_list

25. **Table:** `b2b_product_sales`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_product_sales

26. **Table:** `b2b_product_wise_sales`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_product_wise_sales

27. **Table:** `b2b_products`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_products

28. **Table:** `b2b_quality_inspections`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_quality_inspections

29. **Table:** `b2b_returns`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_returns

30. **Table:** `b2b_sales_agents`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_sales_agents

31. **Table:** `b2b_sales_daily`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_sales_daily

32. **Table:** `b2b_sales_monthly`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_sales_monthly

33. **Table:** `b2b_sales_yearly`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_sales_yearly

34. **Table:** `b2b_shipment_tracking_events`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_shipment_tracking_events

35. **Table:** `b2b_vendor_partners`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_vendor_partners

36. **Table:** `delivery_slots`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to delivery_slots

37. **Table:** `delivery_status`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to delivery_status

38. **Table:** `ecom_ab_test`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_ab_test

39. **Table:** `ecom_acquisition_agents`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_acquisition_agents

40. **Table:** `ecom_activity_log`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_activity_log

41. **Table:** `ecom_browsing_history`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_browsing_history

42. **Table:** `ecom_cart_items`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_cart_items

43. **Table:** `ecom_carts`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_carts

44. **Table:** `ecom_coupon_usage`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_coupon_usage

45. **Table:** `ecom_coupons`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_coupons

46. **Table:** `ecom_customer_addresses`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_customer_addresses

47. **Table:** `ecom_customer_segmentation`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_customer_segmentation

48. **Table:** `ecom_customers`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_customers

49. **Table:** `ecom_frequently_bought`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_frequently_bought

50. **Table:** `ecom_notifications`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_notifications

51. **Table:** `ecom_orders`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_orders

52. **Table:** `ecom_payment_status_log`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_payment_status_log

53. **Table:** `ecom_payments`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_payments

54. **Table:** `ecom_product_events`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_product_events

55. **Table:** `ecom_product_wise_sales`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_product_wise_sales

56. **Table:** `ecom_ratings_summary`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_ratings_summary

57. **Table:** `ecom_refunds`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_refunds

58. **Table:** `ecom_return_items`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_return_items

59. **Table:** `ecom_reviews`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_reviews

60. **Table:** `ecom_sales_daily`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_sales_daily

61. **Table:** `ecom_sales_monthly`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_sales_monthly

62. **Table:** `ecom_sales_yearly`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_sales_yearly

63. **Table:** `ecom_search_keywords`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_search_keywords

64. **Table:** `ecom_ticket`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_ticket

65. **Table:** `ecom_ticket_messages`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_ticket_messages

66. **Table:** `ecom_vendors`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_vendors

67. **Table:** `ecom_wishlist`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_wishlist

68. **Table:** `inventory_items`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to inventory_items

69. **Table:** `order_items`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to order_items

70. **Table:** `pos_daily_sales_summary`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_daily_sales_summary

71. **Table:** `pos_inventory_adjustments`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_inventory_adjustments

72. **Table:** `pos_loyalty_redemptions`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_loyalty_redemptions

73. **Table:** `pos_product_wise_sales`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_product_wise_sales

74. **Table:** `pos_products`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_products

75. **Table:** `pos_products_sales`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_products_sales

76. **Table:** `pos_returns`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_returns

77. **Table:** `pos_sales_daily`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_sales_daily

78. **Table:** `pos_sales_monthly`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_sales_monthly

79. **Table:** `pos_sales_yearly`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_sales_yearly

80. **Table:** `pos_shift_closures`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_shift_closures

81. **Table:** `pos_stores`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_stores

82. **Table:** `pos_sync_log`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_sync_log

83. **Table:** `pos_terminals`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_terminals

84. **Table:** `pos_transaction_lines`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_transaction_lines

85. **Table:** `pos_transactions`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_transactions

86. **Table:** `pos_users`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_users

87. **Table:** `pos_vendors`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_vendors

88. **Table:** `product_inventory`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to product_inventory

89. **Table:** `product_pricing`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to product_pricing

90. **Table:** `product_sales`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to product_sales

91. **Table:** `product_variants`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to product_variants

92. **Table:** `products`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to products

93. **Table:** `returns`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to returns

94. **Table:** `shipments`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to shipments

### ❌ Wrong Column Selection Risks (134 issues)

1. **Column:** `customer_id`
   - *Found in tables:* `b2b_contracts`, `b2b_customer_addresses`, `b2b_customers`, `b2b_invoices`, `b2b_orders`, `b2b_payments`, `b2b_portal_api_clients`, `b2b_price_list`, `b2b_returns`, `ecom_browsing_history`, `ecom_carts`, `ecom_coupon_usage`, `ecom_customer_addresses`, `ecom_customer_segmentation`, `ecom_customers`, `ecom_notifications`, `ecom_orders`, `ecom_reviews`, `ecom_ticket`, `ecom_wishlist`, `pos_loyalty_redemptions`
   - *Issue:* Column 'customer_id' exists in 21 tables: b2b_contracts, b2b_customer_addresses, b2b_customers, b2b_invoices, b2b_orders, b2b_payments, b2b_portal_api_clients, b2b_price_list, b2b_returns, ecom_browsing_history, ecom_carts, ecom_coupon_usage, ecom_customer_addresses, ecom_customer_segmentation, ecom_customers, ecom_notifications, ecom_orders, ecom_reviews, ecom_ticket, ecom_wishlist, pos_loyalty_redemptions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

2. **Column:** `status`
   - *Found in tables:* `b2b_contracts`, `b2b_credit_notes`, `b2b_invoices`, `b2b_order_allocations`, `b2b_payments`, `b2b_picking_batches`, `b2b_sales_agents`, `delivery_status`, `ecom_ab_test`, `ecom_acquisition_agents`, `ecom_customers`, `ecom_payments`, `ecom_refunds`, `ecom_ticket`, `ecom_vendors`, `pos_terminals`, `pos_transactions`, `returns`
   - *Issue:* Column 'status' exists in 18 tables: b2b_contracts, b2b_credit_notes, b2b_invoices, b2b_order_allocations, b2b_payments, b2b_picking_batches, b2b_sales_agents, delivery_status, ecom_ab_test, ecom_acquisition_agents, ecom_customers, ecom_payments, ecom_refunds, ecom_ticket, ecom_vendors, pos_terminals, pos_transactions, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

3. **Column:** `created_at`
   - *Found in tables:* `b2b_contracts`, `b2b_customers`, `b2b_dispatches`, `b2b_events_stream`, `b2b_invoices`, `b2b_kpi_daily_snapshots`, `b2b_order_events`, `b2b_order_lines`, `b2b_orders`, `b2b_picking_batches`, `b2b_portal_api_clients`, `b2b_price_list`, `b2b_quality_inspections`, `b2b_sales_agents`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `b2b_shipment_tracking_events`, `b2b_vendor_partners`, `delivery_slots`, `ecom_ab_test`, `ecom_acquisition_agents`, `ecom_browsing_history`, `ecom_carts`, `ecom_coupon_usage`, `ecom_coupons`, `ecom_customer_addresses`, `ecom_customer_segmentation`, `ecom_customers`, `ecom_notifications`, `ecom_orders`, `ecom_payment_status_log`, `ecom_payments`, `ecom_product_events`, `ecom_reviews`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `ecom_search_keywords`, `ecom_ticket`, `ecom_ticket_messages`, `ecom_vendors`, `inventory_items`, `order_items`, `pos_daily_sales_summary`, `pos_inventory_adjustments`, `pos_returns`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`, `pos_sync_log`, `pos_terminals`, `pos_transaction_lines`, `pos_transactions`, `pos_users`, `pos_vendors`, `product_pricing`, `product_variants`, `products`, `returns`, `shipments`
   - *Issue:* Column 'created_at' exists in 61 tables: b2b_contracts, b2b_customers, b2b_dispatches, b2b_events_stream, b2b_invoices, b2b_kpi_daily_snapshots, b2b_order_events, b2b_order_lines, b2b_orders, b2b_picking_batches, b2b_portal_api_clients, b2b_price_list, b2b_quality_inspections, b2b_sales_agents, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, b2b_shipment_tracking_events, b2b_vendor_partners, delivery_slots, ecom_ab_test, ecom_acquisition_agents, ecom_browsing_history, ecom_carts, ecom_coupon_usage, ecom_coupons, ecom_customer_addresses, ecom_customer_segmentation, ecom_customers, ecom_notifications, ecom_orders, ecom_payment_status_log, ecom_payments, ecom_product_events, ecom_reviews, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, ecom_search_keywords, ecom_ticket, ecom_ticket_messages, ecom_vendors, inventory_items, order_items, pos_daily_sales_summary, pos_inventory_adjustments, pos_returns, pos_sales_daily, pos_sales_monthly, pos_sales_yearly, pos_sync_log, pos_terminals, pos_transaction_lines, pos_transactions, pos_users, pos_vendors, product_pricing, product_variants, products, returns, shipments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

4. **Column:** `credit_note_id`
   - *Found in tables:* `b2b_credit_notes`, `b2b_returns`, `returns`
   - *Issue:* Column 'credit_note_id' exists in 3 tables: b2b_credit_notes, b2b_returns, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

5. **Column:** `invoice_id`
   - *Found in tables:* `b2b_credit_notes`, `b2b_invoices`, `b2b_payments`
   - *Issue:* Column 'invoice_id' exists in 3 tables: b2b_credit_notes, b2b_invoices, b2b_payments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

6. **Column:** `amount`
   - *Found in tables:* `b2b_credit_notes`, `b2b_payments`, `ecom_payments`
   - *Issue:* Column 'amount' exists in 3 tables: b2b_credit_notes, b2b_payments, ecom_payments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

7. **Column:** `reason`
   - *Found in tables:* `b2b_credit_notes`, `b2b_order_allocations`, `ecom_refunds`, `pos_inventory_adjustments`, `pos_returns`
   - *Issue:* Column 'reason' exists in 5 tables: b2b_credit_notes, b2b_order_allocations, ecom_refunds, pos_inventory_adjustments, pos_returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

8. **Column:** `approved_by`
   - *Found in tables:* `b2b_credit_notes`, `returns`
   - *Issue:* Column 'approved_by' exists in 2 tables: b2b_credit_notes, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

9. **Column:** `notes`
   - *Found in tables:* `b2b_credit_notes`, `b2b_kpi_daily_snapshots`, `b2b_payments`, `b2b_price_list`, `b2b_returns`, `delivery_status`, `ecom_activity_log`, `ecom_cart_items`, `ecom_payment_status_log`, `ecom_payments`, `ecom_refunds`, `ecom_return_items`, `ecom_wishlist`, `pos_daily_sales_summary`, `pos_loyalty_redemptions`
   - *Issue:* Column 'notes' exists in 15 tables: b2b_credit_notes, b2b_kpi_daily_snapshots, b2b_payments, b2b_price_list, b2b_returns, delivery_status, ecom_activity_log, ecom_cart_items, ecom_payment_status_log, ecom_payments, ecom_refunds, ecom_return_items, ecom_wishlist, pos_daily_sales_summary, pos_loyalty_redemptions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

10. **Column:** `address_id`
   - *Found in tables:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Issue:* Column 'address_id' exists in 2 tables: b2b_customer_addresses, ecom_customer_addresses
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

11. **Column:** `addr_line1`
   - *Found in tables:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Issue:* Column 'addr_line1' exists in 2 tables: b2b_customer_addresses, ecom_customer_addresses
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

12. **Column:** `addr_line2`
   - *Found in tables:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Issue:* Column 'addr_line2' exists in 2 tables: b2b_customer_addresses, ecom_customer_addresses
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

13. **Column:** `city`
   - *Found in tables:* `b2b_customer_addresses`, `b2b_vendor_partners`, `ecom_customer_addresses`, `ecom_vendors`, `pos_stores`, `pos_vendors`
   - *Issue:* Column 'city' exists in 6 tables: b2b_customer_addresses, b2b_vendor_partners, ecom_customer_addresses, ecom_vendors, pos_stores, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

14. **Column:** `state`
   - *Found in tables:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Issue:* Column 'state' exists in 2 tables: b2b_customer_addresses, ecom_customer_addresses
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

15. **Column:** `pincode`
   - *Found in tables:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Issue:* Column 'pincode' exists in 2 tables: b2b_customer_addresses, ecom_customer_addresses
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

16. **Column:** `country`
   - *Found in tables:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Issue:* Column 'country' exists in 2 tables: b2b_customer_addresses, ecom_customer_addresses
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

17. **Column:** `latitude`
   - *Found in tables:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Issue:* Column 'latitude' exists in 2 tables: b2b_customer_addresses, ecom_customer_addresses
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

18. **Column:** `longitude`
   - *Found in tables:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Issue:* Column 'longitude' exists in 2 tables: b2b_customer_addresses, ecom_customer_addresses
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

19. **Column:** `name`
   - *Found in tables:* `b2b_customers`, `b2b_products`, `b2b_sales_agents`, `ecom_acquisition_agents`, `inventory_items`, `pos_products`, `pos_users`
   - *Issue:* Column 'name' exists in 7 tables: b2b_customers, b2b_products, b2b_sales_agents, ecom_acquisition_agents, inventory_items, pos_products, pos_users
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

20. **Column:** `email`
   - *Found in tables:* `b2b_customers`, `b2b_sales_agents`, `b2b_vendor_partners`, `ecom_acquisition_agents`, `ecom_customers`, `ecom_vendors`, `pos_users`, `pos_vendors`
   - *Issue:* Column 'email' exists in 8 tables: b2b_customers, b2b_sales_agents, b2b_vendor_partners, ecom_acquisition_agents, ecom_customers, ecom_vendors, pos_users, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

21. **Column:** `delivery_address_id`
   - *Found in tables:* `b2b_customers`, `ecom_orders`
   - *Issue:* Column 'delivery_address_id' exists in 2 tables: b2b_customers, ecom_orders
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

22. **Column:** `dispatch_id`
   - *Found in tables:* `b2b_dispatches`, `b2b_shipment_tracking_events`
   - *Issue:* Column 'dispatch_id' exists in 2 tables: b2b_dispatches, b2b_shipment_tracking_events
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

23. **Column:** `order_id`
   - *Found in tables:* `b2b_dispatches`, `b2b_invoices`, `b2b_order_allocations`, `b2b_order_events`, `b2b_order_lines`, `b2b_orders`, `b2b_returns`, `delivery_status`, `ecom_coupon_usage`, `ecom_orders`, `ecom_payments`, `ecom_refunds`, `ecom_ticket`, `order_items`, `returns`, `shipments`
   - *Issue:* Column 'order_id' exists in 16 tables: b2b_dispatches, b2b_invoices, b2b_order_allocations, b2b_order_events, b2b_order_lines, b2b_orders, b2b_returns, delivery_status, ecom_coupon_usage, ecom_orders, ecom_payments, ecom_refunds, ecom_ticket, order_items, returns, shipments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

24. **Column:** `tracking_no`
   - *Found in tables:* `b2b_dispatches`, `shipments`
   - *Issue:* Column 'tracking_no' exists in 2 tables: b2b_dispatches, shipments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

25. **Column:** `remarks`
   - *Found in tables:* `b2b_dispatches`, `b2b_order_lines`, `b2b_quality_inspections`
   - *Issue:* Column 'remarks' exists in 3 tables: b2b_dispatches, b2b_order_lines, b2b_quality_inspections
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

26. **Column:** `created_by`
   - *Found in tables:* `b2b_dispatches`, `b2b_payments`, `b2b_picking_batches`, `b2b_price_list`, `pos_loyalty_redemptions`, `product_pricing`
   - *Issue:* Column 'created_by' exists in 6 tables: b2b_dispatches, b2b_payments, b2b_picking_batches, b2b_price_list, pos_loyalty_redemptions, product_pricing
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

27. **Column:** `event_ts`
   - *Found in tables:* `b2b_events_stream`, `b2b_order_events`, `b2b_shipment_tracking_events`, `delivery_status`, `ecom_browsing_history`, `ecom_product_events`
   - *Issue:* Column 'event_ts' exists in 6 tables: b2b_events_stream, b2b_order_events, b2b_shipment_tracking_events, delivery_status, ecom_browsing_history, ecom_product_events
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

28. **Column:** `event_type`
   - *Found in tables:* `b2b_events_stream`, `b2b_order_events`, `b2b_shipment_tracking_events`, `delivery_status`, `ecom_browsing_history`, `ecom_product_events`
   - *Issue:* Column 'event_type' exists in 6 tables: b2b_events_stream, b2b_order_events, b2b_shipment_tracking_events, delivery_status, ecom_browsing_history, ecom_product_events
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

29. **Column:** `source_system`
   - *Found in tables:* `b2b_events_stream`, `b2b_order_events`
   - *Issue:* Column 'source_system' exists in 2 tables: b2b_events_stream, b2b_order_events
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

30. **Column:** `processed_flag`
   - *Found in tables:* `b2b_events_stream`, `b2b_order_events`, `ecom_payment_status_log`
   - *Issue:* Column 'processed_flag' exists in 3 tables: b2b_events_stream, b2b_order_events, ecom_payment_status_log
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

31. **Column:** `processed_at`
   - *Found in tables:* `b2b_events_stream`, `ecom_refunds`
   - *Issue:* Column 'processed_at' exists in 2 tables: b2b_events_stream, ecom_refunds
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

32. **Column:** `retry_count`
   - *Found in tables:* `b2b_events_stream`, `ecom_payment_status_log`, `pos_sync_log`
   - *Issue:* Column 'retry_count' exists in 3 tables: b2b_events_stream, ecom_payment_status_log, pos_sync_log
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

33. **Column:** `total_tax`
   - *Found in tables:* `b2b_invoices`, `pos_daily_sales_summary`
   - *Issue:* Column 'total_tax' exists in 2 tables: b2b_invoices, pos_daily_sales_summary
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

34. **Column:** `centre_id`
   - *Found in tables:* `b2b_kpi_daily_snapshots`, `b2b_picking_batches`, `delivery_slots`, `product_inventory`
   - *Issue:* Column 'centre_id' exists in 4 tables: b2b_kpi_daily_snapshots, b2b_picking_batches, delivery_slots, product_inventory
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

35. **Column:** `date`
   - *Found in tables:* `b2b_kpi_daily_snapshots`, `b2b_product_wise_sales`, `b2b_sales_daily`, `delivery_slots`, `ecom_product_wise_sales`, `ecom_sales_daily`, `pos_daily_sales_summary`, `pos_product_wise_sales`, `pos_sales_daily`
   - *Issue:* Column 'date' exists in 9 tables: b2b_kpi_daily_snapshots, b2b_product_wise_sales, b2b_sales_daily, delivery_slots, ecom_product_wise_sales, ecom_sales_daily, pos_daily_sales_summary, pos_product_wise_sales, pos_sales_daily
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

36. **Column:** `total_orders`
   - *Found in tables:* `b2b_kpi_daily_snapshots`, `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`
   - *Issue:* Column 'total_orders' exists in 9 tables: b2b_kpi_daily_snapshots, b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

37. **Column:** `total_kg`
   - *Found in tables:* `b2b_kpi_daily_snapshots`, `b2b_picking_batches`
   - *Issue:* Column 'total_kg' exists in 2 tables: b2b_kpi_daily_snapshots, b2b_picking_batches
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

38. **Column:** `gross_sales`
   - *Found in tables:* `b2b_kpi_daily_snapshots`, `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `pos_product_wise_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'gross_sales' exists in 13 tables: b2b_kpi_daily_snapshots, b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, pos_product_wise_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

39. **Column:** `allocation_id`
   - *Found in tables:* `b2b_order_allocations`, `b2b_order_lines`
   - *Issue:* Column 'allocation_id' exists in 2 tables: b2b_order_allocations, b2b_order_lines
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

40. **Column:** `order_line_id`
   - *Found in tables:* `b2b_order_allocations`, `b2b_order_lines`, `b2b_quality_inspections`
   - *Issue:* Column 'order_line_id' exists in 3 tables: b2b_order_allocations, b2b_order_lines, b2b_quality_inspections
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

41. **Column:** `inventory_id`
   - *Found in tables:* `b2b_order_allocations`, `product_inventory`
   - *Issue:* Column 'inventory_id' exists in 2 tables: b2b_order_allocations, product_inventory
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

42. **Column:** `expiry_ts`
   - *Found in tables:* `b2b_order_allocations`, `product_inventory`
   - *Issue:* Column 'expiry_ts' exists in 2 tables: b2b_order_allocations, product_inventory
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

43. **Column:** `event_id`
   - *Found in tables:* `b2b_order_events`, `ecom_product_events`
   - *Issue:* Column 'event_id' exists in 2 tables: b2b_order_events, ecom_product_events
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

44. **Column:** `ip_address`
   - *Found in tables:* `b2b_order_events`, `ecom_activity_log`
   - *Issue:* Column 'ip_address' exists in 2 tables: b2b_order_events, ecom_activity_log
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

45. **Column:** `sku`
   - *Found in tables:* `b2b_order_lines`, `b2b_price_list`, `b2b_product_sales`, `b2b_products`, `ecom_browsing_history`, `ecom_cart_items`, `ecom_frequently_bought`, `ecom_product_events`, `ecom_ratings_summary`, `ecom_return_items`, `ecom_reviews`, `ecom_wishlist`, `inventory_items`, `order_items`, `pos_products`, `pos_products_sales`, `pos_returns`, `pos_transaction_lines`, `product_inventory`, `product_pricing`, `product_sales`, `product_variants`, `products`
   - *Issue:* Column 'sku' exists in 23 tables: b2b_order_lines, b2b_price_list, b2b_product_sales, b2b_products, ecom_browsing_history, ecom_cart_items, ecom_frequently_bought, ecom_product_events, ecom_ratings_summary, ecom_return_items, ecom_reviews, ecom_wishlist, inventory_items, order_items, pos_products, pos_products_sales, pos_returns, pos_transaction_lines, product_inventory, product_pricing, product_sales, product_variants, products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

46. **Column:** `qty_units`
   - *Found in tables:* `b2b_order_lines`, `order_items`, `product_inventory`
   - *Issue:* Column 'qty_units' exists in 3 tables: b2b_order_lines, order_items, product_inventory
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

47. **Column:** `qty_kg`
   - *Found in tables:* `b2b_order_lines`, `b2b_returns`, `order_items`, `product_inventory`
   - *Issue:* Column 'qty_kg' exists in 4 tables: b2b_order_lines, b2b_returns, order_items, product_inventory
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

48. **Column:** `unit_price`
   - *Found in tables:* `b2b_order_lines`, `order_items`, `pos_transaction_lines`
   - *Issue:* Column 'unit_price' exists in 3 tables: b2b_order_lines, order_items, pos_transaction_lines
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

49. **Column:** `line_total`
   - *Found in tables:* `b2b_order_lines`, `order_items`, `pos_transaction_lines`
   - *Issue:* Column 'line_total' exists in 3 tables: b2b_order_lines, order_items, pos_transaction_lines
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

50. **Column:** `batch_id`
   - *Found in tables:* `b2b_order_lines`, `inventory_items`, `order_items`, `pos_transaction_lines`
   - *Issue:* Column 'batch_id' exists in 4 tables: b2b_order_lines, inventory_items, order_items, pos_transaction_lines
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

51. **Column:** `order_ts`
   - *Found in tables:* `b2b_orders`, `ecom_orders`
   - *Issue:* Column 'order_ts' exists in 2 tables: b2b_orders, ecom_orders
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

52. **Column:** `order_channel`
   - *Found in tables:* `b2b_orders`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`
   - *Issue:* Column 'order_channel' exists in 4 tables: b2b_orders, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

53. **Column:** `order_status`
   - *Found in tables:* `b2b_orders`, `ecom_orders`
   - *Issue:* Column 'order_status' exists in 2 tables: b2b_orders, ecom_orders
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

54. **Column:** `currency`
   - *Found in tables:* `b2b_orders`, `b2b_price_list`, `ecom_carts`, `product_pricing`
   - *Issue:* Column 'currency' exists in 4 tables: b2b_orders, b2b_price_list, ecom_carts, product_pricing
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

55. **Column:** `tax_amount`
   - *Found in tables:* `b2b_orders`, `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_orders`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `order_items`, `pos_product_wise_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'tax_amount' exists in 15 tables: b2b_orders, b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_orders, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, order_items, pos_product_wise_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

56. **Column:** `discount_amount`
   - *Found in tables:* `b2b_orders`, `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_orders`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `order_items`, `pos_loyalty_redemptions`, `pos_product_wise_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'discount_amount' exists in 16 tables: b2b_orders, b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_orders, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, order_items, pos_loyalty_redemptions, pos_product_wise_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

57. **Column:** `net_amount`
   - *Found in tables:* `b2b_orders`, `ecom_orders`
   - *Issue:* Column 'net_amount' exists in 2 tables: b2b_orders, ecom_orders
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

58. **Column:** `pickup_centre_id`
   - *Found in tables:* `b2b_orders`, `shipments`
   - *Issue:* Column 'pickup_centre_id' exists in 2 tables: b2b_orders, shipments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

59. **Column:** `payment_id`
   - *Found in tables:* `b2b_payments`, `ecom_payment_status_log`, `ecom_payments`, `ecom_refunds`
   - *Issue:* Column 'payment_id' exists in 4 tables: b2b_payments, ecom_payment_status_log, ecom_payments, ecom_refunds
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

60. **Column:** `payment_ts`
   - *Found in tables:* `b2b_payments`, `ecom_payments`
   - *Issue:* Column 'payment_ts' exists in 2 tables: b2b_payments, ecom_payments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

61. **Column:** `payment_mode`
   - *Found in tables:* `b2b_payments`, `ecom_payments`, `pos_transactions`
   - *Issue:* Column 'payment_mode' exists in 3 tables: b2b_payments, ecom_payments, pos_transactions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

62. **Column:** `active_flag`
   - *Found in tables:* `b2b_portal_api_clients`, `b2b_products`, `ecom_coupons`, `pos_products`, `pos_users`, `product_variants`
   - *Issue:* Column 'active_flag' exists in 6 tables: b2b_portal_api_clients, b2b_products, ecom_coupons, pos_products, pos_users, product_variants
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

63. **Column:** `start_ts`
   - *Found in tables:* `b2b_price_list`, `ecom_ab_test`, `product_pricing`
   - *Issue:* Column 'start_ts' exists in 3 tables: b2b_price_list, ecom_ab_test, product_pricing
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

64. **Column:** `end_ts`
   - *Found in tables:* `b2b_price_list`, `ecom_ab_test`, `product_pricing`
   - *Issue:* Column 'end_ts' exists in 3 tables: b2b_price_list, ecom_ab_test, product_pricing
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

65. **Column:** `price_per_unit`
   - *Found in tables:* `b2b_price_list`, `product_pricing`
   - *Issue:* Column 'price_per_unit' exists in 2 tables: b2b_price_list, product_pricing
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

66. **Column:** `min_order_qty`
   - *Found in tables:* `b2b_price_list`, `product_pricing`
   - *Issue:* Column 'min_order_qty' exists in 2 tables: b2b_price_list, product_pricing
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

67. **Column:** `gross sales`
   - *Found in tables:* `b2b_product_sales`, `pos_products_sales`, `product_sales`
   - *Issue:* Column 'gross sales' exists in 3 tables: b2b_product_sales, pos_products_sales, product_sales
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

68. **Column:** `discount amount`
   - *Found in tables:* `b2b_product_sales`, `pos_products_sales`
   - *Issue:* Column 'discount amount' exists in 2 tables: b2b_product_sales, pos_products_sales
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

69. **Column:** `tax amount`
   - *Found in tables:* `b2b_product_sales`, `pos_products_sales`
   - *Issue:* Column 'tax amount' exists in 2 tables: b2b_product_sales, pos_products_sales
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

70. **Column:** `net sales`
   - *Found in tables:* `b2b_product_sales`, `pos_products_sales`, `product_sales`
   - *Issue:* Column 'net sales' exists in 3 tables: b2b_product_sales, pos_products_sales, product_sales
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

71. **Column:** `product_id`
   - *Found in tables:* `b2b_product_wise_sales`, `ecom_product_wise_sales`, `pos_product_wise_sales`
   - *Issue:* Column 'product_id' exists in 3 tables: b2b_product_wise_sales, ecom_product_wise_sales, pos_product_wise_sales
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

72. **Column:** `total_qty_kg`
   - *Found in tables:* `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `pos_product_wise_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'total_qty_kg' exists in 12 tables: b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, pos_product_wise_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

73. **Column:** `net_sales`
   - *Found in tables:* `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `pos_product_wise_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'net_sales' exists in 12 tables: b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, pos_product_wise_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

74. **Column:** `plucode`
   - *Found in tables:* `b2b_products`, `pos_products`
   - *Issue:* Column 'plucode' exists in 2 tables: b2b_products, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

75. **Column:** `uom`
   - *Found in tables:* `b2b_products`, `pos_products`, `product_variants`, `products`
   - *Issue:* Column 'uom' exists in 4 tables: b2b_products, pos_products, product_variants, products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

76. **Column:** `pos_price`
   - *Found in tables:* `b2b_products`, `pos_products`
   - *Issue:* Column 'pos_price' exists in 2 tables: b2b_products, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

77. **Column:** `tax_rate`
   - *Found in tables:* `b2b_products`, `pos_products`
   - *Issue:* Column 'tax_rate' exists in 2 tables: b2b_products, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

78. **Column:** `stock_qty`
   - *Found in tables:* `b2b_products`, `pos_products`
   - *Issue:* Column 'stock_qty' exists in 2 tables: b2b_products, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

79. **Column:** `reorder_point`
   - *Found in tables:* `b2b_products`, `pos_products`, `product_inventory`
   - *Issue:* Column 'reorder_point' exists in 3 tables: b2b_products, pos_products, product_inventory
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

80. **Column:** `updated_at`
   - *Found in tables:* `b2b_products`, `ecom_cart_items`, `ecom_coupons`, `ecom_orders`, `ecom_payment_status_log`, `ecom_ratings_summary`, `ecom_ticket`, `inventory_items`, `pos_products`
   - *Issue:* Column 'updated_at' exists in 9 tables: b2b_products, ecom_cart_items, ecom_coupons, ecom_orders, ecom_payment_status_log, ecom_ratings_summary, ecom_ticket, inventory_items, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

81. **Column:** `photo_url`
   - *Found in tables:* `b2b_quality_inspections`, `delivery_status`
   - *Issue:* Column 'photo_url' exists in 2 tables: b2b_quality_inspections, delivery_status
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

82. **Column:** `return_id`
   - *Found in tables:* `b2b_returns`, `ecom_return_items`, `returns`
   - *Issue:* Column 'return_id' exists in 3 tables: b2b_returns, ecom_return_items, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

83. **Column:** `received_at`
   - *Found in tables:* `b2b_returns`, `inventory_items`
   - *Issue:* Column 'received_at' exists in 2 tables: b2b_returns, inventory_items
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

84. **Column:** `reason_code`
   - *Found in tables:* `b2b_returns`, `returns`
   - *Issue:* Column 'reason_code' exists in 2 tables: b2b_returns, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

85. **Column:** `refund_amount`
   - *Found in tables:* `b2b_returns`, `ecom_refunds`, `pos_returns`, `returns`
   - *Issue:* Column 'refund_amount' exists in 4 tables: b2b_returns, ecom_refunds, pos_returns, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

86. **Column:** `disposition`
   - *Found in tables:* `b2b_returns`, `ecom_return_items`
   - *Issue:* Column 'disposition' exists in 2 tables: b2b_returns, ecom_return_items
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

87. **Column:** `agent_id`
   - *Found in tables:* `b2b_sales_agents`, `ecom_acquisition_agents`
   - *Issue:* Column 'agent_id' exists in 2 tables: b2b_sales_agents, ecom_acquisition_agents
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

88. **Column:** `phone`
   - *Found in tables:* `b2b_sales_agents`, `b2b_vendor_partners`, `ecom_acquisition_agents`, `ecom_customers`, `ecom_vendors`, `pos_users`, `pos_vendors`
   - *Issue:* Column 'phone' exists in 7 tables: b2b_sales_agents, b2b_vendor_partners, ecom_acquisition_agents, ecom_customers, ecom_vendors, pos_users, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

89. **Column:** `region`
   - *Found in tables:* `b2b_sales_agents`, `pos_stores`
   - *Issue:* Column 'region' exists in 2 tables: b2b_sales_agents, pos_stores
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

90. **Column:** `join_date`
   - *Found in tables:* `b2b_sales_agents`, `ecom_acquisition_agents`
   - *Issue:* Column 'join_date' exists in 2 tables: b2b_sales_agents, ecom_acquisition_agents
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

91. **Column:** `customer_type`
   - *Found in tables:* `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`
   - *Issue:* Column 'customer_type' exists in 3 tables: b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

92. **Column:** `unnamed: 9`
   - *Found in tables:* `b2b_sales_daily`, `pos_sales_daily`
   - *Issue:* Column 'unnamed: 9' exists in 2 tables: b2b_sales_daily, pos_sales_daily
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

93. **Column:** `unnamed: 10`
   - *Found in tables:* `b2b_sales_daily`, `pos_sales_daily`
   - *Issue:* Column 'unnamed: 10' exists in 2 tables: b2b_sales_daily, pos_sales_daily
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

94. **Column:** `unnamed: 11`
   - *Found in tables:* `b2b_sales_daily`, `ecom_sales_daily`, `pos_sales_daily`
   - *Issue:* Column 'unnamed: 11' exists in 3 tables: b2b_sales_daily, ecom_sales_daily, pos_sales_daily
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

95. **Column:** `unnamed: 12`
   - *Found in tables:* `b2b_sales_daily`, `ecom_sales_daily`, `pos_products`, `pos_sales_daily`
   - *Issue:* Column 'unnamed: 12' exists in 4 tables: b2b_sales_daily, ecom_sales_daily, pos_products, pos_sales_daily
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

96. **Column:** `year`
   - *Found in tables:* `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_sales_monthly`, `ecom_sales_yearly`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'year' exists in 6 tables: b2b_sales_monthly, b2b_sales_yearly, ecom_sales_monthly, ecom_sales_yearly, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

97. **Column:** `month`
   - *Found in tables:* `b2b_sales_monthly`, `ecom_sales_monthly`, `pos_sales_monthly`
   - *Issue:* Column 'month' exists in 3 tables: b2b_sales_monthly, ecom_sales_monthly, pos_sales_monthly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

98. **Column:** `gps_lat`
   - *Found in tables:* `b2b_shipment_tracking_events`, `delivery_status`
   - *Issue:* Column 'gps_lat' exists in 2 tables: b2b_shipment_tracking_events, delivery_status
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

99. **Column:** `gps_long`
   - *Found in tables:* `b2b_shipment_tracking_events`, `delivery_status`
   - *Issue:* Column 'gps_long' exists in 2 tables: b2b_shipment_tracking_events, delivery_status
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

100. **Column:** `vendor_id`
   - *Found in tables:* `b2b_vendor_partners`, `ecom_vendors`, `pos_vendors`
   - *Issue:* Column 'vendor_id' exists in 3 tables: b2b_vendor_partners, ecom_vendors, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

101. **Column:** `vendor_name`
   - *Found in tables:* `b2b_vendor_partners`, `ecom_vendors`, `pos_vendors`
   - *Issue:* Column 'vendor_name' exists in 3 tables: b2b_vendor_partners, ecom_vendors, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

102. **Column:** `gst_no`
   - *Found in tables:* `b2b_vendor_partners`, `ecom_vendors`, `pos_vendors`
   - *Issue:* Column 'gst_no' exists in 3 tables: b2b_vendor_partners, ecom_vendors, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

103. **Column:** `shipment_id`
   - *Found in tables:* `delivery_status`, `shipments`
   - *Issue:* Column 'shipment_id' exists in 2 tables: delivery_status, shipments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

104. **Column:** `device_type`
   - *Found in tables:* `ecom_browsing_history`, `ecom_carts`
   - *Issue:* Column 'device_type' exists in 2 tables: ecom_browsing_history, ecom_carts
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

105. **Column:** `cart_id`
   - *Found in tables:* `ecom_cart_items`, `ecom_carts`
   - *Issue:* Column 'cart_id' exists in 2 tables: ecom_cart_items, ecom_carts
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

106. **Column:** `qty`
   - *Found in tables:* `ecom_cart_items`, `ecom_return_items`, `pos_returns`, `pos_transaction_lines`
   - *Issue:* Column 'qty' exists in 4 tables: ecom_cart_items, ecom_return_items, pos_returns, pos_transaction_lines
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

107. **Column:** `added_at`
   - *Found in tables:* `ecom_cart_items`, `ecom_wishlist`
   - *Issue:* Column 'added_at' exists in 2 tables: ecom_cart_items, ecom_wishlist
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

108. **Column:** `variant_id`
   - *Found in tables:* `ecom_cart_items`, `order_items`, `product_variants`
   - *Issue:* Column 'variant_id' exists in 3 tables: ecom_cart_items, order_items, product_variants
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

109. **Column:** `total_amount`
   - *Found in tables:* `ecom_carts`, `ecom_orders`
   - *Issue:* Column 'total_amount' exists in 2 tables: ecom_carts, ecom_orders
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

110. **Column:** `coupon_code`
   - *Found in tables:* `ecom_carts`, `ecom_coupons`, `ecom_orders`
   - *Issue:* Column 'coupon_code' exists in 3 tables: ecom_carts, ecom_coupons, ecom_orders
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

111. **Column:** `coupon_id`
   - *Found in tables:* `ecom_coupon_usage`, `ecom_coupons`
   - *Issue:* Column 'coupon_id' exists in 2 tables: ecom_coupon_usage, ecom_coupons
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

112. **Column:** `description`
   - *Found in tables:* `ecom_coupons`, `ecom_ticket`
   - *Issue:* Column 'description' exists in 2 tables: ecom_coupons, ecom_ticket
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

113. **Column:** `last_login`
   - *Found in tables:* `ecom_customers`, `pos_users`
   - *Issue:* Column 'last_login' exists in 2 tables: ecom_customers, pos_users
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

114. **Column:** `title`
   - *Found in tables:* `ecom_notifications`, `ecom_reviews`
   - *Issue:* Column 'title' exists in 2 tables: ecom_notifications, ecom_reviews
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

115. **Column:** `shipping_charge`
   - *Found in tables:* `ecom_orders`, `shipments`
   - *Issue:* Column 'shipping_charge' exists in 2 tables: ecom_orders, shipments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

116. **Column:** `gateway_ref_no`
   - *Found in tables:* `ecom_payments`, `ecom_refunds`
   - *Issue:* Column 'gateway_ref_no' exists in 2 tables: ecom_payments, ecom_refunds
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

117. **Column:** `processed_by`
   - *Found in tables:* `ecom_payments`, `ecom_refunds`, `pos_returns`
   - *Issue:* Column 'processed_by' exists in 3 tables: ecom_payments, ecom_refunds, pos_returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

118. **Column:** `total_customers`
   - *Found in tables:* `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`
   - *Issue:* Column 'total_customers' exists in 4 tables: ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

119. **Column:** `delivery_fee`
   - *Found in tables:* `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`
   - *Issue:* Column 'delivery_fee' exists in 4 tables: ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

120. **Column:** `order_item_id`
   - *Found in tables:* `ecom_return_items`, `order_items`
   - *Issue:* Column 'order_item_id' exists in 2 tables: ecom_return_items, order_items
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

121. **Column:** `unnamed: 13`
   - *Found in tables:* `ecom_sales_daily`, `pos_products`
   - *Issue:* Column 'unnamed: 13' exists in 2 tables: ecom_sales_daily, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

122. **Column:** `unnamed: 14`
   - *Found in tables:* `ecom_sales_daily`, `pos_products`
   - *Issue:* Column 'unnamed: 14' exists in 2 tables: ecom_sales_daily, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

123. **Column:** `ticket_id`
   - *Found in tables:* `ecom_ticket`, `ecom_ticket_messages`
   - *Issue:* Column 'ticket_id' exists in 2 tables: ecom_ticket, ecom_ticket_messages
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

124. **Column:** `expiry_date`
   - *Found in tables:* `inventory_items`, `pos_transaction_lines`
   - *Issue:* Column 'expiry_date' exists in 2 tables: inventory_items, pos_transaction_lines
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

125. **Column:** `product_name`
   - *Found in tables:* `order_items`, `products`
   - *Issue:* Column 'product_name' exists in 2 tables: order_items, products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

126. **Column:** `store_id`
   - *Found in tables:* `pos_daily_sales_summary`, `pos_inventory_adjustments`, `pos_loyalty_redemptions`, `pos_products`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`, `pos_stores`, `pos_terminals`, `pos_users`
   - *Issue:* Column 'store_id' exists in 10 tables: pos_daily_sales_summary, pos_inventory_adjustments, pos_loyalty_redemptions, pos_products, pos_sales_daily, pos_sales_monthly, pos_sales_yearly, pos_stores, pos_terminals, pos_users
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

127. **Column:** `total_sales`
   - *Found in tables:* `pos_daily_sales_summary`, `pos_shift_closures`
   - *Issue:* Column 'total_sales' exists in 2 tables: pos_daily_sales_summary, pos_shift_closures
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

128. **Column:** `pos_sku`
   - *Found in tables:* `pos_inventory_adjustments`, `pos_products`
   - *Issue:* Column 'pos_sku' exists in 2 tables: pos_inventory_adjustments, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

129. **Column:** `pos_txn_id`
   - *Found in tables:* `pos_loyalty_redemptions`, `pos_returns`, `pos_transaction_lines`, `pos_transactions`
   - *Issue:* Column 'pos_txn_id' exists in 4 tables: pos_loyalty_redemptions, pos_returns, pos_transaction_lines, pos_transactions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

130. **Column:** `total_bills`
   - *Found in tables:* `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'total_bills' exists in 3 tables: pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

131. **Column:** `shift_id`
   - *Found in tables:* `pos_shift_closures`, `pos_transactions`
   - *Issue:* Column 'shift_id' exists in 2 tables: pos_shift_closures, pos_transactions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

132. **Column:** `terminal_id`
   - *Found in tables:* `pos_shift_closures`, `pos_sync_log`, `pos_terminals`, `pos_transactions`
   - *Issue:* Column 'terminal_id' exists in 4 tables: pos_shift_closures, pos_sync_log, pos_terminals, pos_transactions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

133. **Column:** `pos_user_id`
   - *Found in tables:* `pos_transactions`, `pos_users`
   - *Issue:* Column 'pos_user_id' exists in 2 tables: pos_transactions, pos_users
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

134. **Column:** `storage_temp_c`
   - *Found in tables:* `product_inventory`, `products`
   - *Issue:* Column 'storage_temp_c' exists in 2 tables: product_inventory, products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

### ❌ Wrong Filter Condition Risks (214 issues)

1. **Column:** `b2b_contracts.start_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE start_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(start_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_contracts.start_date to DATE or DATETIME type

2. **Column:** `b2b_contracts.end_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE end_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(end_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_contracts.end_date to DATE or DATETIME type

3. **Column:** `b2b_credit_notes.amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE amount > 100`
   - ✅ *Correct:* `WHERE CAST(amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_credit_notes.amount to appropriate numeric type

4. **Column:** `b2b_credit_notes.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

5. **Column:** `b2b_dispatches.freight_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE freight_amount > 100`
   - ✅ *Correct:* `WHERE CAST(freight_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_dispatches.freight_amount to appropriate numeric type

6. **Column:** `b2b_invoices.invoice_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE invoice_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(invoice_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_invoices.invoice_date to DATE or DATETIME type

7. **Column:** `b2b_invoices.due_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE due_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(due_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_invoices.due_date to DATE or DATETIME type

8. **Column:** `b2b_invoices.total_tax`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE total_tax > 100`
   - ✅ *Correct:* `WHERE CAST(total_tax AS DECIMAL) > 100`
   - *Fix:* Convert b2b_invoices.total_tax to appropriate numeric type

9. **Column:** `b2b_invoices.invoice_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(44)`
   - ❌ *Wrong:* `WHERE invoice_amount > 100`
   - ✅ *Correct:* `WHERE CAST(invoice_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_invoices.invoice_amount to appropriate numeric type

10. **Column:** `b2b_kpi_daily_snapshots.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_kpi_daily_snapshots.date to DATE or DATETIME type

11. **Column:** `b2b_kpi_daily_snapshots.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert b2b_kpi_daily_snapshots.total_orders to appropriate numeric type

12. **Column:** `b2b_kpi_daily_snapshots.total_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE total_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_kpi_daily_snapshots.total_kg to appropriate numeric type

13. **Column:** `b2b_kpi_daily_snapshots.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

14. **Column:** `b2b_order_allocations.allocated_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE allocated_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(allocated_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_order_allocations.allocated_qty_kg to appropriate numeric type

15. **Column:** `b2b_order_allocations.allocated_qty_units`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE allocated_qty_units > 100`
   - ✅ *Correct:* `WHERE CAST(allocated_qty_units AS DECIMAL) > 100`
   - *Fix:* Convert b2b_order_allocations.allocated_qty_units to appropriate numeric type

16. **Column:** `b2b_order_lines.qty_units`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE qty_units > 100`
   - ✅ *Correct:* `WHERE CAST(qty_units AS DECIMAL) > 100`
   - *Fix:* Convert b2b_order_lines.qty_units to appropriate numeric type

17. **Column:** `b2b_order_lines.qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_order_lines.qty_kg to appropriate numeric type

18. **Column:** `b2b_order_lines.unit_price`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE unit_price > 100`
   - ✅ *Correct:* `WHERE CAST(unit_price AS DECIMAL) > 100`
   - *Fix:* Convert b2b_order_lines.unit_price to appropriate numeric type

19. **Column:** `b2b_order_lines.line_total`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE line_total > 100`
   - ✅ *Correct:* `WHERE CAST(line_total AS DECIMAL) > 100`
   - *Fix:* Convert b2b_order_lines.line_total to appropriate numeric type

20. **Column:** `b2b_orders.gross_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE gross_amount > 100`
   - ✅ *Correct:* `WHERE CAST(gross_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_orders.gross_amount to appropriate numeric type

21. **Column:** `b2b_orders.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(12)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_orders.tax_amount to appropriate numeric type

22. **Column:** `b2b_orders.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_orders.discount_amount to appropriate numeric type

23. **Column:** `b2b_orders.net_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE net_amount > 100`
   - ✅ *Correct:* `WHERE CAST(net_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_orders.net_amount to appropriate numeric type

24. **Column:** `b2b_payments.amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE amount > 100`
   - ✅ *Correct:* `WHERE CAST(amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_payments.amount to appropriate numeric type

25. **Column:** `b2b_payments.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

26. **Column:** `b2b_picking_batches.total_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE total_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_picking_batches.total_kg to appropriate numeric type

27. **Column:** `b2b_price_list.price_list_id`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE price_list_id > 100`
   - ✅ *Correct:* `WHERE CAST(price_list_id AS DECIMAL) > 100`
   - *Fix:* Convert b2b_price_list.price_list_id to appropriate numeric type

28. **Column:** `b2b_price_list.price_per_unit`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE price_per_unit > 100`
   - ✅ *Correct:* `WHERE CAST(price_per_unit AS DECIMAL) > 100`
   - *Fix:* Convert b2b_price_list.price_per_unit to appropriate numeric type

29. **Column:** `b2b_price_list.min_order_qty`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE min_order_qty > 100`
   - ✅ *Correct:* `WHERE CAST(min_order_qty AS DECIMAL) > 100`
   - *Fix:* Convert b2b_price_list.min_order_qty to appropriate numeric type

30. **Column:** `b2b_price_list.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

31. **Column:** `b2b_product_sales.Discount Amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE Discount Amount > 100`
   - ✅ *Correct:* `WHERE CAST(Discount Amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_product_sales.Discount Amount to appropriate numeric type

32. **Column:** `b2b_product_sales.Tax Amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE Tax Amount > 100`
   - ✅ *Correct:* `WHERE CAST(Tax Amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_product_sales.Tax Amount to appropriate numeric type

33. **Column:** `b2b_product_wise_sales.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_product_wise_sales.date to DATE or DATETIME type

34. **Column:** `b2b_product_wise_sales.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(52)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert b2b_product_wise_sales.total_orders to appropriate numeric type

35. **Column:** `b2b_product_wise_sales.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_product_wise_sales.total_qty_kg to appropriate numeric type

36. **Column:** `b2b_product_wise_sales.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_product_wise_sales.discount_amount to appropriate numeric type

37. **Column:** `b2b_product_wise_sales.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_product_wise_sales.tax_amount to appropriate numeric type

38. **Column:** `b2b_products.pos_price`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE pos_price > 100`
   - ✅ *Correct:* `WHERE CAST(pos_price AS DECIMAL) > 100`
   - *Fix:* Convert b2b_products.pos_price to appropriate numeric type

39. **Column:** `b2b_products.stock_qty`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE stock_qty > 100`
   - ✅ *Correct:* `WHERE CAST(stock_qty AS DECIMAL) > 100`
   - *Fix:* Convert b2b_products.stock_qty to appropriate numeric type

40. **Column:** `b2b_products.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_products.updated_at to DATE or DATETIME type

41. **Column:** `b2b_quality_inspections.rejection_reason`
   - *Issue:* High NULL percentage (68.0%)
   - *Fix:* Handle NULLs explicitly: WHERE rejection_reason IS NOT NULL

42. **Column:** `b2b_quality_inspections.photo_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE photo_url IS NOT NULL

43. **Column:** `b2b_quality_inspections.remarks`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE remarks IS NOT NULL

44. **Column:** `b2b_returns.qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_returns.qty_kg to appropriate numeric type

45. **Column:** `b2b_returns.refund_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE refund_amount > 100`
   - ✅ *Correct:* `WHERE CAST(refund_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_returns.refund_amount to appropriate numeric type

46. **Column:** `b2b_sales_agents.join_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE join_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(join_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_sales_agents.join_date to DATE or DATETIME type

47. **Column:** `b2b_sales_daily.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert b2b_sales_daily.date to DATE or DATETIME type

48. **Column:** `b2b_sales_daily.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_daily.total_orders to appropriate numeric type

49. **Column:** `b2b_sales_daily.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_daily.total_qty_kg to appropriate numeric type

50. **Column:** `b2b_sales_daily.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_daily.discount_amount to appropriate numeric type

51. **Column:** `b2b_sales_daily.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_daily.tax_amount to appropriate numeric type

52. **Column:** `b2b_sales_daily.Unnamed: 9`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 9 IS NOT NULL

53. **Column:** `b2b_sales_daily.Unnamed: 10`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 10 IS NOT NULL

54. **Column:** `b2b_sales_daily.Unnamed: 11`
   - *Issue:* High NULL percentage (99.9%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 11 IS NOT NULL

55. **Column:** `b2b_sales_daily.Unnamed: 12`
   - *Issue:* High NULL percentage (99.9%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 12 IS NOT NULL

56. **Column:** `b2b_sales_monthly.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_monthly.total_orders to appropriate numeric type

57. **Column:** `b2b_sales_monthly.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_monthly.total_qty_kg to appropriate numeric type

58. **Column:** `b2b_sales_monthly.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_monthly.discount_amount to appropriate numeric type

59. **Column:** `b2b_sales_monthly.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_monthly.tax_amount to appropriate numeric type

60. **Column:** `b2b_sales_yearly.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_yearly.total_orders to appropriate numeric type

61. **Column:** `b2b_sales_yearly.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_yearly.total_qty_kg to appropriate numeric type

62. **Column:** `b2b_sales_yearly.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_yearly.discount_amount to appropriate numeric type

63. **Column:** `b2b_sales_yearly.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert b2b_sales_yearly.tax_amount to appropriate numeric type

64. **Column:** `b2b_shipment_tracking_events.scan_photo_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE scan_photo_url IS NOT NULL

65. **Column:** `b2b_shipment_tracking_events.status_note`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE status_note IS NOT NULL

66. **Column:** `delivery_slots.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert delivery_slots.date to DATE or DATETIME type

67. **Column:** `delivery_status.updated_by`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(52)`
   - ❌ *Wrong:* `WHERE updated_by > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_by AS DATE) > '2024-01-01'`
   - *Fix:* Convert delivery_status.updated_by to DATE or DATETIME type

68. **Column:** `delivery_status.photo_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE photo_url IS NOT NULL

69. **Column:** `delivery_status.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

70. **Column:** `ecom_acquisition_agents.join_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE join_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(join_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_acquisition_agents.join_date to DATE or DATETIME type

71. **Column:** `ecom_activity_log.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

72. **Column:** `ecom_cart_items.qty`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE qty > 100`
   - ✅ *Correct:* `WHERE CAST(qty AS DECIMAL) > 100`
   - *Fix:* Convert ecom_cart_items.qty to appropriate numeric type

73. **Column:** `ecom_cart_items.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_cart_items.updated_at to DATE or DATETIME type

74. **Column:** `ecom_cart_items.price_at_add`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE price_at_add > 100`
   - ✅ *Correct:* `WHERE CAST(price_at_add AS DECIMAL) > 100`
   - *Fix:* Convert ecom_cart_items.price_at_add to appropriate numeric type

75. **Column:** `ecom_cart_items.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

76. **Column:** `ecom_carts.last_updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE last_updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(last_updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_carts.last_updated_at to DATE or DATETIME type

77. **Column:** `ecom_carts.total_items`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(12)`
   - ❌ *Wrong:* `WHERE total_items > 100`
   - ✅ *Correct:* `WHERE CAST(total_items AS DECIMAL) > 100`
   - *Fix:* Convert ecom_carts.total_items to appropriate numeric type

78. **Column:** `ecom_carts.total_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE total_amount > 100`
   - ✅ *Correct:* `WHERE CAST(total_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_carts.total_amount to appropriate numeric type

79. **Column:** `ecom_carts.abandoned_at`
   - *Issue:* High NULL percentage (59.0%)
   - *Fix:* Handle NULLs explicitly: WHERE abandoned_at IS NOT NULL

80. **Column:** `ecom_coupons.max_discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE max_discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(max_discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_coupons.max_discount_amount to appropriate numeric type

81. **Column:** `ecom_coupons.min_order_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE min_order_amount > 100`
   - ✅ *Correct:* `WHERE CAST(min_order_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_coupons.min_order_amount to appropriate numeric type

82. **Column:** `ecom_coupons.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_coupons.updated_at to DATE or DATETIME type

83. **Column:** `ecom_customer_segmentation.last_purchase_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE last_purchase_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(last_purchase_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_customer_segmentation.last_purchase_date to DATE or DATETIME type

84. **Column:** `ecom_frequently_bought.last_updated`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE last_updated > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(last_updated AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_frequently_bought.last_updated to DATE or DATETIME type

85. **Column:** `ecom_orders.total_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE total_amount > 100`
   - ✅ *Correct:* `WHERE CAST(total_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_orders.total_amount to appropriate numeric type

86. **Column:** `ecom_orders.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_orders.tax_amount to appropriate numeric type

87. **Column:** `ecom_orders.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_orders.discount_amount to appropriate numeric type

88. **Column:** `ecom_orders.net_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE net_amount > 100`
   - ✅ *Correct:* `WHERE CAST(net_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_orders.net_amount to appropriate numeric type

89. **Column:** `ecom_orders.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_orders.updated_at to DATE or DATETIME type

90. **Column:** `ecom_orders.Unnamed: 19`
   - *Issue:* High NULL percentage (54.6%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 19 IS NOT NULL

91. **Column:** `ecom_payment_status_log.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_payment_status_log.updated_at to DATE or DATETIME type

92. **Column:** `ecom_payment_status_log.response_body`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE response_body IS NOT NULL

93. **Column:** `ecom_payment_status_log.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

94. **Column:** `ecom_payments.amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE amount > 100`
   - ✅ *Correct:* `WHERE CAST(amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_payments.amount to appropriate numeric type

95. **Column:** `ecom_payments.settlement_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE settlement_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(settlement_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_payments.settlement_date to DATE or DATETIME type

96. **Column:** `ecom_payments.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

97. **Column:** `ecom_product_events.old_value`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE old_value IS NOT NULL

98. **Column:** `ecom_product_events.new_value`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE new_value IS NOT NULL

99. **Column:** `ecom_product_wise_sales.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_product_wise_sales.date to DATE or DATETIME type

100. **Column:** `ecom_product_wise_sales.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert ecom_product_wise_sales.total_orders to appropriate numeric type

101. **Column:** `ecom_product_wise_sales.total_customers`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE total_customers > 100`
   - ✅ *Correct:* `WHERE CAST(total_customers AS DECIMAL) > 100`
   - *Fix:* Convert ecom_product_wise_sales.total_customers to appropriate numeric type

102. **Column:** `ecom_product_wise_sales.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert ecom_product_wise_sales.total_qty_kg to appropriate numeric type

103. **Column:** `ecom_product_wise_sales.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_product_wise_sales.discount_amount to appropriate numeric type

104. **Column:** `ecom_product_wise_sales.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_product_wise_sales.tax_amount to appropriate numeric type

105. **Column:** `ecom_ratings_summary.total_reviews`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE total_reviews > 100`
   - ✅ *Correct:* `WHERE CAST(total_reviews AS DECIMAL) > 100`
   - *Fix:* Convert ecom_ratings_summary.total_reviews to appropriate numeric type

106. **Column:** `ecom_ratings_summary.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_ratings_summary.updated_at to DATE or DATETIME type

107. **Column:** `ecom_refunds.refund_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE refund_amount > 100`
   - ✅ *Correct:* `WHERE CAST(refund_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_refunds.refund_amount to appropriate numeric type

108. **Column:** `ecom_refunds.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

109. **Column:** `ecom_return_items.qty`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE qty > 100`
   - ✅ *Correct:* `WHERE CAST(qty AS DECIMAL) > 100`
   - *Fix:* Convert ecom_return_items.qty to appropriate numeric type

110. **Column:** `ecom_return_items.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

111. **Column:** `ecom_reviews.responded_by`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE responded_by IS NOT NULL

112. **Column:** `ecom_reviews.response_text`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE response_text IS NOT NULL

113. **Column:** `ecom_sales_daily.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_sales_daily.date to DATE or DATETIME type

114. **Column:** `ecom_sales_daily.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_daily.total_orders to appropriate numeric type

115. **Column:** `ecom_sales_daily.total_customers`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE total_customers > 100`
   - ✅ *Correct:* `WHERE CAST(total_customers AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_daily.total_customers to appropriate numeric type

116. **Column:** `ecom_sales_daily.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_daily.total_qty_kg to appropriate numeric type

117. **Column:** `ecom_sales_daily.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_daily.discount_amount to appropriate numeric type

118. **Column:** `ecom_sales_daily.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_daily.tax_amount to appropriate numeric type

119. **Column:** `ecom_sales_daily.Unnamed: 11`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 11 IS NOT NULL

120. **Column:** `ecom_sales_daily.Unnamed: 12`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 12 IS NOT NULL

121. **Column:** `ecom_sales_daily.Unnamed: 13`
   - *Issue:* High NULL percentage (99.8%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 13 IS NOT NULL

122. **Column:** `ecom_sales_daily.Unnamed: 14`
   - *Issue:* High NULL percentage (99.8%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 14 IS NOT NULL

123. **Column:** `ecom_sales_monthly.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_monthly.total_orders to appropriate numeric type

124. **Column:** `ecom_sales_monthly.total_customers`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE total_customers > 100`
   - ✅ *Correct:* `WHERE CAST(total_customers AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_monthly.total_customers to appropriate numeric type

125. **Column:** `ecom_sales_monthly.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_monthly.total_qty_kg to appropriate numeric type

126. **Column:** `ecom_sales_monthly.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_monthly.discount_amount to appropriate numeric type

127. **Column:** `ecom_sales_monthly.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_monthly.tax_amount to appropriate numeric type

128. **Column:** `ecom_sales_yearly.total_orders`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE total_orders > 100`
   - ✅ *Correct:* `WHERE CAST(total_orders AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_yearly.total_orders to appropriate numeric type

129. **Column:** `ecom_sales_yearly.total_customers`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE total_customers > 100`
   - ✅ *Correct:* `WHERE CAST(total_customers AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_yearly.total_customers to appropriate numeric type

130. **Column:** `ecom_sales_yearly.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_yearly.total_qty_kg to appropriate numeric type

131. **Column:** `ecom_sales_yearly.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_yearly.discount_amount to appropriate numeric type

132. **Column:** `ecom_sales_yearly.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert ecom_sales_yearly.tax_amount to appropriate numeric type

133. **Column:** `ecom_ticket.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_ticket.updated_at to DATE or DATETIME type

134. **Column:** `ecom_ticket_messages.attachment_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE attachment_url IS NOT NULL

135. **Column:** `ecom_wishlist.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

136. **Column:** `inventory_items.total_stock_units`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE total_stock_units > 100`
   - ✅ *Correct:* `WHERE CAST(total_stock_units AS DECIMAL) > 100`
   - *Fix:* Convert inventory_items.total_stock_units to appropriate numeric type

137. **Column:** `inventory_items.expiry_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE expiry_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(expiry_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert inventory_items.expiry_date to DATE or DATETIME type

138. **Column:** `inventory_items.cost_per_unit`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE cost_per_unit > 100`
   - ✅ *Correct:* `WHERE CAST(cost_per_unit AS DECIMAL) > 100`
   - *Fix:* Convert inventory_items.cost_per_unit to appropriate numeric type

139. **Column:** `inventory_items.mfg_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE mfg_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(mfg_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert inventory_items.mfg_date to DATE or DATETIME type

140. **Column:** `inventory_items.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert inventory_items.updated_at to DATE or DATETIME type

141. **Column:** `order_items.qty_units`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE qty_units > 100`
   - ✅ *Correct:* `WHERE CAST(qty_units AS DECIMAL) > 100`
   - *Fix:* Convert order_items.qty_units to appropriate numeric type

142. **Column:** `order_items.qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert order_items.qty_kg to appropriate numeric type

143. **Column:** `order_items.unit_price`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE unit_price > 100`
   - ✅ *Correct:* `WHERE CAST(unit_price AS DECIMAL) > 100`
   - *Fix:* Convert order_items.unit_price to appropriate numeric type

144. **Column:** `order_items.line_total`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE line_total > 100`
   - ✅ *Correct:* `WHERE CAST(line_total AS DECIMAL) > 100`
   - *Fix:* Convert order_items.line_total to appropriate numeric type

145. **Column:** `order_items.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert order_items.tax_amount to appropriate numeric type

146. **Column:** `order_items.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(12)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert order_items.discount_amount to appropriate numeric type

147. **Column:** `pos_daily_sales_summary.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert pos_daily_sales_summary.date to DATE or DATETIME type

148. **Column:** `pos_daily_sales_summary.total_txns`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE total_txns > 100`
   - ✅ *Correct:* `WHERE CAST(total_txns AS DECIMAL) > 100`
   - *Fix:* Convert pos_daily_sales_summary.total_txns to appropriate numeric type

149. **Column:** `pos_daily_sales_summary.total_sales`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE total_sales > 100`
   - ✅ *Correct:* `WHERE CAST(total_sales AS DECIMAL) > 100`
   - *Fix:* Convert pos_daily_sales_summary.total_sales to appropriate numeric type

150. **Column:** `pos_daily_sales_summary.total_tax`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE total_tax > 100`
   - ✅ *Correct:* `WHERE CAST(total_tax AS DECIMAL) > 100`
   - *Fix:* Convert pos_daily_sales_summary.total_tax to appropriate numeric type

151. **Column:** `pos_daily_sales_summary.total_refunds`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE total_refunds > 100`
   - ✅ *Correct:* `WHERE CAST(total_refunds AS DECIMAL) > 100`
   - *Fix:* Convert pos_daily_sales_summary.total_refunds to appropriate numeric type

152. **Column:** `pos_inventory_adjustments.qty_change`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE qty_change > 100`
   - ✅ *Correct:* `WHERE CAST(qty_change AS DECIMAL) > 100`
   - *Fix:* Convert pos_inventory_adjustments.qty_change to appropriate numeric type

153. **Column:** `pos_loyalty_redemptions.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_loyalty_redemptions.discount_amount to appropriate numeric type

154. **Column:** `pos_product_wise_sales.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert pos_product_wise_sales.date to DATE or DATETIME type

155. **Column:** `pos_product_wise_sales.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert pos_product_wise_sales.total_qty_kg to appropriate numeric type

156. **Column:** `pos_product_wise_sales.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_product_wise_sales.discount_amount to appropriate numeric type

157. **Column:** `pos_product_wise_sales.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(46)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_product_wise_sales.tax_amount to appropriate numeric type

158. **Column:** `pos_products.pos_price`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE pos_price > 100`
   - ✅ *Correct:* `WHERE CAST(pos_price AS DECIMAL) > 100`
   - *Fix:* Convert pos_products.pos_price to appropriate numeric type

159. **Column:** `pos_products.stock_qty`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE stock_qty > 100`
   - ✅ *Correct:* `WHERE CAST(stock_qty AS DECIMAL) > 100`
   - *Fix:* Convert pos_products.stock_qty to appropriate numeric type

160. **Column:** `pos_products.updated_at`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE updated_at > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_at AS DATE) > '2024-01-01'`
   - *Fix:* Convert pos_products.updated_at to DATE or DATETIME type

161. **Column:** `pos_products.Unnamed: 12`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 12 IS NOT NULL

162. **Column:** `pos_products.Unnamed: 13`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 13 IS NOT NULL

163. **Column:** `pos_products.Unnamed: 14`
   - *Issue:* High NULL percentage (92.3%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 14 IS NOT NULL

164. **Column:** `pos_products_sales.Discount Amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE Discount Amount > 100`
   - ✅ *Correct:* `WHERE CAST(Discount Amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_products_sales.Discount Amount to appropriate numeric type

165. **Column:** `pos_products_sales.Tax Amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE Tax Amount > 100`
   - ✅ *Correct:* `WHERE CAST(Tax Amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_products_sales.Tax Amount to appropriate numeric type

166. **Column:** `pos_returns.qty`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(12)`
   - ❌ *Wrong:* `WHERE qty > 100`
   - ✅ *Correct:* `WHERE CAST(qty AS DECIMAL) > 100`
   - *Fix:* Convert pos_returns.qty to appropriate numeric type

167. **Column:** `pos_returns.refund_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE refund_amount > 100`
   - ✅ *Correct:* `WHERE CAST(refund_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_returns.refund_amount to appropriate numeric type

168. **Column:** `pos_sales_daily.date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(30)`
   - ❌ *Wrong:* `WHERE date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(date AS DATE) > '2024-01-01'`
   - *Fix:* Convert pos_sales_daily.date to DATE or DATETIME type

169. **Column:** `pos_sales_daily.total_bills`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE total_bills > 100`
   - ✅ *Correct:* `WHERE CAST(total_bills AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_daily.total_bills to appropriate numeric type

170. **Column:** `pos_sales_daily.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_daily.total_qty_kg to appropriate numeric type

171. **Column:** `pos_sales_daily.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_daily.discount_amount to appropriate numeric type

172. **Column:** `pos_sales_daily.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_daily.tax_amount to appropriate numeric type

173. **Column:** `pos_sales_daily.Unnamed: 9`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 9 IS NOT NULL

174. **Column:** `pos_sales_daily.Unnamed: 10`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 10 IS NOT NULL

175. **Column:** `pos_sales_daily.Unnamed: 11`
   - *Issue:* High NULL percentage (99.8%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 11 IS NOT NULL

176. **Column:** `pos_sales_daily.Unnamed: 12`
   - *Issue:* High NULL percentage (99.8%)
   - *Fix:* Handle NULLs explicitly: WHERE Unnamed: 12 IS NOT NULL

177. **Column:** `pos_sales_monthly.total_bills`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE total_bills > 100`
   - ✅ *Correct:* `WHERE CAST(total_bills AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_monthly.total_bills to appropriate numeric type

178. **Column:** `pos_sales_monthly.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_monthly.total_qty_kg to appropriate numeric type

179. **Column:** `pos_sales_monthly.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_monthly.discount_amount to appropriate numeric type

180. **Column:** `pos_sales_monthly.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_monthly.tax_amount to appropriate numeric type

181. **Column:** `pos_sales_yearly.total_bills`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE total_bills > 100`
   - ✅ *Correct:* `WHERE CAST(total_bills AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_yearly.total_bills to appropriate numeric type

182. **Column:** `pos_sales_yearly.total_qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE total_qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(total_qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_yearly.total_qty_kg to appropriate numeric type

183. **Column:** `pos_sales_yearly.discount_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE discount_amount > 100`
   - ✅ *Correct:* `WHERE CAST(discount_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_yearly.discount_amount to appropriate numeric type

184. **Column:** `pos_sales_yearly.tax_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(28)`
   - ❌ *Wrong:* `WHERE tax_amount > 100`
   - ✅ *Correct:* `WHERE CAST(tax_amount AS DECIMAL) > 100`
   - *Fix:* Convert pos_sales_yearly.tax_amount to appropriate numeric type

185. **Column:** `pos_shift_closures.total_sales`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(26)`
   - ❌ *Wrong:* `WHERE total_sales > 100`
   - ✅ *Correct:* `WHERE CAST(total_sales AS DECIMAL) > 100`
   - *Fix:* Convert pos_shift_closures.total_sales to appropriate numeric type

186. **Column:** `pos_shift_closures.discrepancies_note`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE discrepancies_note IS NOT NULL

187. **Column:** `pos_stores.first_active_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE first_active_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(first_active_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert pos_stores.first_active_date to DATE or DATETIME type

188. **Column:** `pos_sync_log.error_message`
   - *Issue:* High NULL percentage (58.0%)
   - *Fix:* Handle NULLs explicitly: WHERE error_message IS NOT NULL

189. **Column:** `pos_transaction_lines.qty`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE qty > 100`
   - ✅ *Correct:* `WHERE CAST(qty AS DECIMAL) > 100`
   - *Fix:* Convert pos_transaction_lines.qty to appropriate numeric type

190. **Column:** `pos_transaction_lines.unit_price`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE unit_price > 100`
   - ✅ *Correct:* `WHERE CAST(unit_price AS DECIMAL) > 100`
   - *Fix:* Convert pos_transaction_lines.unit_price to appropriate numeric type

191. **Column:** `pos_transaction_lines.line_total`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE line_total > 100`
   - ✅ *Correct:* `WHERE CAST(line_total AS DECIMAL) > 100`
   - *Fix:* Convert pos_transaction_lines.line_total to appropriate numeric type

192. **Column:** `pos_transaction_lines.variant_info`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE variant_info IS NOT NULL

193. **Column:** `pos_transaction_lines.expiry_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(16)`
   - ❌ *Wrong:* `WHERE expiry_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(expiry_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert pos_transaction_lines.expiry_date to DATE or DATETIME type

194. **Column:** `pos_transaction_lines.expiry_date`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE expiry_date IS NOT NULL

195. **Column:** `pos_transactions.txn_total`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE txn_total > 100`
   - ✅ *Correct:* `WHERE CAST(txn_total AS DECIMAL) > 100`
   - *Fix:* Convert pos_transactions.txn_total to appropriate numeric type

196. **Column:** `pos_transactions.tax_total`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(44)`
   - ❌ *Wrong:* `WHERE tax_total > 100`
   - ✅ *Correct:* `WHERE CAST(tax_total AS DECIMAL) > 100`
   - *Fix:* Convert pos_transactions.tax_total to appropriate numeric type

197. **Column:** `pos_transactions.discount_total`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(12)`
   - ❌ *Wrong:* `WHERE discount_total > 100`
   - ✅ *Correct:* `WHERE CAST(discount_total AS DECIMAL) > 100`
   - *Fix:* Convert pos_transactions.discount_total to appropriate numeric type

198. **Column:** `pos_transactions.cashier_note`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE cashier_note IS NOT NULL

199. **Column:** `product_inventory.qty_units`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE qty_units > 100`
   - ✅ *Correct:* `WHERE CAST(qty_units AS DECIMAL) > 100`
   - *Fix:* Convert product_inventory.qty_units to appropriate numeric type

200. **Column:** `product_inventory.qty_kg`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(18)`
   - ❌ *Wrong:* `WHERE qty_kg > 100`
   - ✅ *Correct:* `WHERE CAST(qty_kg AS DECIMAL) > 100`
   - *Fix:* Convert product_inventory.qty_kg to appropriate numeric type

201. **Column:** `product_pricing.price_id`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(34)`
   - ❌ *Wrong:* `WHERE price_id > 100`
   - ✅ *Correct:* `WHERE CAST(price_id AS DECIMAL) > 100`
   - *Fix:* Convert product_pricing.price_id to appropriate numeric type

202. **Column:** `product_pricing.price_per_unit`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(22)`
   - ❌ *Wrong:* `WHERE price_per_unit > 100`
   - ✅ *Correct:* `WHERE CAST(price_per_unit AS DECIMAL) > 100`
   - *Fix:* Convert product_pricing.price_per_unit to appropriate numeric type

203. **Column:** `product_pricing.min_order_qty`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(14)`
   - ❌ *Wrong:* `WHERE min_order_qty > 100`
   - ✅ *Correct:* `WHERE CAST(min_order_qty AS DECIMAL) > 100`
   - *Fix:* Convert product_pricing.min_order_qty to appropriate numeric type

204. **Column:** `product_variants.price_retail`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE price_retail > 100`
   - ✅ *Correct:* `WHERE CAST(price_retail AS DECIMAL) > 100`
   - *Fix:* Convert product_variants.price_retail to appropriate numeric type

205. **Column:** `product_variants.price_wholesale`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(20)`
   - ❌ *Wrong:* `WHERE price_wholesale > 100`
   - ✅ *Correct:* `WHERE CAST(price_wholesale AS DECIMAL) > 100`
   - *Fix:* Convert product_variants.price_wholesale to appropriate numeric type

206. **Column:** `products.hs_code`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE hs_code IS NOT NULL

207. **Column:** `products.default_image_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE default_image_url IS NOT NULL

208. **Column:** `returns.approved_by`
   - *Issue:* High NULL percentage (52.5%)
   - *Fix:* Handle NULLs explicitly: WHERE approved_by IS NOT NULL

209. **Column:** `returns.refund_amount`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(24)`
   - ❌ *Wrong:* `WHERE refund_amount > 100`
   - ✅ *Correct:* `WHERE CAST(refund_amount AS DECIMAL) > 100`
   - *Fix:* Convert returns.refund_amount to appropriate numeric type

210. **Column:** `returns.resolution_notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE resolution_notes IS NOT NULL

211. **Column:** `shipments.shipment_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE shipment_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(shipment_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert shipments.shipment_date to DATE or DATETIME type

212. **Column:** `shipments.expected_delivery_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE expected_delivery_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(expected_delivery_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert shipments.expected_delivery_date to DATE or DATETIME type

213. **Column:** `shipments.actual_delivery_date`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE actual_delivery_date > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(actual_delivery_date AS DATE) > '2024-01-01'`
   - *Fix:* Convert shipments.actual_delivery_date to DATE or DATETIME type

214. **Column:** `shipments.last_update`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(48)`
   - ❌ *Wrong:* `WHERE last_update > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(last_update AS DATE) > '2024-01-01'`
   - *Fix:* Convert shipments.last_update to DATE or DATETIME type

### ❌ Wrong Join Condition Risks (136 issues)

1. **Column:** `b2b_contracts.contract_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_contracts`
   - *Fix:* Add FK constraint or clarify relationship in documentation

2. **Column:** `b2b_contracts.customer_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_customer_addresses`, `b2b_customers`, `ecom_customer_addresses`, `ecom_customer_segmentation`, `ecom_customers`
   - *Fix:* Add FK constraint or clarify relationship in documentation

3. **Column:** `b2b_credit_notes.credit_note_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_credit_notes`
   - *Fix:* Add FK constraint or clarify relationship in documentation

4. **Column:** `b2b_credit_notes.invoice_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_invoices`
   - *Fix:* Add FK constraint or clarify relationship in documentation

5. **Column:** `b2b_customer_addresses.address_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_customer_addresses`, `ecom_customer_addresses`
   - *Fix:* Add FK constraint or clarify relationship in documentation

6. **Column:** `b2b_customer_addresses.customer_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_customer_addresses`, `b2b_customers`, `ecom_customer_addresses`, `ecom_customer_segmentation`, `ecom_customers`
   - *Fix:* Add FK constraint or clarify relationship in documentation

7. **Column:** `b2b_customers.customer_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_customer_addresses`, `b2b_customers`, `ecom_customer_addresses`, `ecom_customer_segmentation`, `ecom_customers`
   - *Fix:* Add FK constraint or clarify relationship in documentation

8. **Column:** `b2b_dispatches.dispatch_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_dispatches`
   - *Fix:* Add FK constraint or clarify relationship in documentation

9. **Column:** `b2b_dispatches.order_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_order_allocations`, `b2b_order_events`, `b2b_order_lines`, `b2b_orders`, `ecom_orders`, `order_items`
   - *Fix:* Add FK constraint or clarify relationship in documentation

10. **Column:** `b2b_invoices.invoice_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_invoices`
   - *Fix:* Add FK constraint or clarify relationship in documentation

### ❌ Wrong Aggregation Risks (86 issues)

1. **Column:** `b2b_contracts.discount_schema_json`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_schema_json directly, avoid SUM(discount_schema_json)

2. **Column:** `b2b_customer_addresses.country`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use country directly, avoid SUM(country)

3. **Column:** `b2b_customers.account_type`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use account_type directly, avoid SUM(account_type)

4. **Column:** `b2b_events_stream.retry_count`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use retry_count directly, avoid SUM(retry_count)

5. **Column:** `b2b_invoices.total_tax`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_tax directly, avoid SUM(total_tax)

6. **Column:** `b2b_kpi_daily_snapshots.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

7. **Column:** `b2b_kpi_daily_snapshots.total_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_kg directly, avoid SUM(total_kg)

8. **Column:** `b2b_kpi_daily_snapshots.avg_delivery_time_min`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use avg_delivery_time_min directly, avoid SUM(avg_delivery_time_min)

9. **Column:** `b2b_order_lines.line_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use line_total directly, avoid SUM(line_total)

10. **Column:** `b2b_orders.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

11. **Column:** `b2b_picking_batches.total_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_kg directly, avoid SUM(total_kg)

12. **Column:** `b2b_product_sales.Discount Amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use Discount Amount directly, avoid SUM(Discount Amount)

13. **Column:** `b2b_product_wise_sales.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

14. **Column:** `b2b_product_wise_sales.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

15. **Column:** `b2b_product_wise_sales.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

16. **Column:** `b2b_sales_daily.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

17. **Column:** `b2b_sales_daily.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

18. **Column:** `b2b_sales_daily.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

19. **Column:** `b2b_sales_monthly.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

20. **Column:** `b2b_sales_monthly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

21. **Column:** `b2b_sales_monthly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

22. **Column:** `b2b_sales_yearly.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

23. **Column:** `b2b_sales_yearly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

24. **Column:** `b2b_sales_yearly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

25. **Column:** `ecom_carts.total_items`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_items directly, avoid SUM(total_items)

26. **Column:** `ecom_carts.total_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_amount directly, avoid SUM(total_amount)

27. **Column:** `ecom_coupon_usage.discount_given`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_given directly, avoid SUM(discount_given)

28. **Column:** `ecom_coupons.discount_type`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_type directly, avoid SUM(discount_type)

29. **Column:** `ecom_coupons.discount_value`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_value directly, avoid SUM(discount_value)

30. **Column:** `ecom_coupons.max_discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use max_discount_amount directly, avoid SUM(max_discount_amount)

31. **Column:** `ecom_customer_addresses.country`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use country directly, avoid SUM(country)

32. **Column:** `ecom_customer_segmentation.avg_order_value`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use avg_order_value directly, avoid SUM(avg_order_value)

33. **Column:** `ecom_orders.total_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_amount directly, avoid SUM(total_amount)

34. **Column:** `ecom_orders.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

35. **Column:** `ecom_payment_status_log.retry_count`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use retry_count directly, avoid SUM(retry_count)

36. **Column:** `ecom_product_wise_sales.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

37. **Column:** `ecom_product_wise_sales.total_customers`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_customers directly, avoid SUM(total_customers)

38. **Column:** `ecom_product_wise_sales.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

39. **Column:** `ecom_product_wise_sales.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

40. **Column:** `ecom_ratings_summary.rating_summary_id`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use rating_summary_id directly, avoid SUM(rating_summary_id)

41. **Column:** `ecom_ratings_summary.avg_rating`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use avg_rating directly, avoid SUM(avg_rating)

42. **Column:** `ecom_ratings_summary.total_reviews`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_reviews directly, avoid SUM(total_reviews)

43. **Column:** `ecom_reviews.helpful_count`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use helpful_count directly, avoid SUM(helpful_count)

44. **Column:** `ecom_sales_daily.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

45. **Column:** `ecom_sales_daily.total_customers`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_customers directly, avoid SUM(total_customers)

46. **Column:** `ecom_sales_daily.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

47. **Column:** `ecom_sales_daily.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

48. **Column:** `ecom_sales_monthly.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

49. **Column:** `ecom_sales_monthly.total_customers`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_customers directly, avoid SUM(total_customers)

50. **Column:** `ecom_sales_monthly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

51. **Column:** `ecom_sales_monthly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

52. **Column:** `ecom_sales_yearly.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

53. **Column:** `ecom_sales_yearly.total_customers`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_customers directly, avoid SUM(total_customers)

54. **Column:** `ecom_sales_yearly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

55. **Column:** `ecom_sales_yearly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

56. **Column:** `inventory_items.total_stock_units`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_stock_units directly, avoid SUM(total_stock_units)

57. **Column:** `order_items.line_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use line_total directly, avoid SUM(line_total)

58. **Column:** `order_items.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

59. **Column:** `pos_daily_sales_summary.summary_id`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use summary_id directly, avoid SUM(summary_id)

60. **Column:** `pos_daily_sales_summary.total_txns`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_txns directly, avoid SUM(total_txns)

61. **Column:** `pos_daily_sales_summary.total_sales`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_sales directly, avoid SUM(total_sales)

62. **Column:** `pos_daily_sales_summary.total_tax`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_tax directly, avoid SUM(total_tax)

63. **Column:** `pos_daily_sales_summary.total_refunds`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_refunds directly, avoid SUM(total_refunds)

64. **Column:** `pos_daily_sales_summary.avg_txn_value`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use avg_txn_value directly, avoid SUM(avg_txn_value)

65. **Column:** `pos_loyalty_redemptions.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

66. **Column:** `pos_product_wise_sales.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

67. **Column:** `pos_product_wise_sales.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

68. **Column:** `pos_products_sales.Discount Amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use Discount Amount directly, avoid SUM(Discount Amount)

69. **Column:** `pos_sales_daily.total_bills`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_bills directly, avoid SUM(total_bills)

70. **Column:** `pos_sales_daily.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

71. **Column:** `pos_sales_daily.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

72. **Column:** `pos_sales_monthly.total_bills`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_bills directly, avoid SUM(total_bills)

73. **Column:** `pos_sales_monthly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

74. **Column:** `pos_sales_monthly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

75. **Column:** `pos_sales_yearly.total_bills`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_bills directly, avoid SUM(total_bills)

76. **Column:** `pos_sales_yearly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

77. **Column:** `pos_sales_yearly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

78. **Column:** `pos_shift_closures.total_sales`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_sales directly, avoid SUM(total_sales)

79. **Column:** `pos_shift_closures.counted_cash`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use counted_cash directly, avoid SUM(counted_cash)

80. **Column:** `pos_sync_log.retry_count`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use retry_count directly, avoid SUM(retry_count)

81. **Column:** `pos_transaction_lines.line_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use line_total directly, avoid SUM(line_total)

82. **Column:** `pos_transaction_lines.discount_amt`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amt directly, avoid SUM(discount_amt)

83. **Column:** `pos_transactions.txn_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use txn_total directly, avoid SUM(txn_total)

84. **Column:** `pos_transactions.tax_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use tax_total directly, avoid SUM(tax_total)

85. **Column:** `pos_transactions.discount_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_total directly, avoid SUM(discount_total)

86. **Column:** `product_sales.Discount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use Discount directly, avoid SUM(Discount)

## 💡 Recommendations

*No recommendations available.*

## 📊 Table Details

### b2b_contracts

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Repository of B2B contractual agreements between the business and customers. It captures contract metadata (period, covered SKUs, pricing model, minimum volumes, discount/delivery/penalty terms), lifecycle status and creation timestamp. Used as the canonical source of contract-level rules that must be applied when measuring compliance, pricing, invoicing and deliveries.

**Business Questions:**

- How many active contracts exist and how many are expiring in the next 30/90 days?
- Which customers have contracts with minimum monthly volumes above X and are they meeting those volumes?
- Which SKUs are covered by contracts and which product SKUs are not under any contract?
- What is the distribution of pricing models (Dynamic, Fixed, Tiered) and which model generates the most revenue when joined to invoices?
- Which contracts are pending activation (PENDING) vs active (ACTIVE) vs expired (EXPIRED) and how has contract creation trended over time?

**Key Columns:**

- **`contract_id`** (nvarchar(24), NULL) - 50 distinct values
  - *Unique identifier for the contract (string).*
- **`customer_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier of the customer the contract applies to.*
- **`start_date`** (nvarchar(48), NULL) - 50 distinct values
  - *Contract effective start timestamp (stored as nvarchar).*
- **`end_date`** (nvarchar(48), NULL) - 50 distinct values
  - *Contract end timestamp (stored as nvarchar).*
- **`sku_list_json`** (nvarchar(70), NULL) - 47 distinct values
  - *Serialized list of SKUs covered by the contract. In the current data it looks like array text with single quotes (e.g., ['SKU1','SKU2']).*
- **`pricing_model`** (nvarchar(24), NULL) - 3 distinct values
  - *Categorical field indicating the contract's pricing strategy (e.g., Dynamic, Fixed, Tiered).*
- **`min_monthly_volume`** (nvarchar(18), NULL) - 48 distinct values
  - *Minimum monthly purchase volume required by the contract (stored as nvarchar but represents a numeric quantity).*
- **`discount_schema_json`** (nvarchar(54), NULL) - 1 distinct values
  - *Structured discount rules for the contract (JSON). Current sample shows a consistent JSON object {"vol_discount":"5%"}.*
- **`delivery_windows_json`** (nvarchar(60), NULL) - 1 distinct values
  - *Structured delivery window information for the contract (JSON). Current value example: {"mon-fri":"08:00-12:00"}.*
- **`penalty_terms`** (nvarchar(68), NULL) - 1 distinct values
  - *Human-readable penalty clause text describing contract penalties (string). Example: 'Late delivery penalty applies'.*
- *(... and 2 more columns)*

---

### b2b_credit_notes

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Records credit and debit notes issued against B2B invoices. The table captures metadata about each note (id, type, amount, reason), who issued and approved it, timestamps, linkage to the originating invoice and any related return, and processing status. It supports financial adjustments, returns reconciliation, and audit/tracking of credit activity.

**Business Questions:**

- What is the total value of credit notes vs. debit notes over a period?
- Which reasons (Damage, Price Adjustment, Return) account for the most credit value and volume?
- Who are the top issuers and approvers of credit notes by count and amount?
- What is the average time to approval for credit notes and how many remain unapproved or void?
- How many credit notes are associated with returns and what is their total amount?

**Key Columns:**

- **`credit_note_id`** (nvarchar(24), NULL) - 50 distinct values
  - *Unique identifier for the credit or debit note (e.g., CN17001).*
- **`invoice_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier of the invoice against which this credit/debit note was issued (e.g., INV13001).*
- **`note_type`** (nvarchar(22), NULL) - 2 distinct values
  - *Indicates whether the record is a CREDIT or a DEBIT note.*
- **`amount`** (nvarchar(24), NULL) - 50 distinct values
  - *Monetary value of the credit/debit note stored as a string (examples: '104.13', '1120.3699999999999').*
- **`reason`** (nvarchar(42), NULL) - 3 distinct values
  - *Categorical reason for issuing the note (Damage, Price Adjustment, Return).*
- **`issued_by`** (nvarchar(46), NULL) - 50 distinct values
  - *Name of the person who created/issued the credit note.*
- **`issued_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the credit note was issued, stored as an nvarchar string (format appears 'YYYY-MM-DD HH:MM:SS').*
- **`approved_by`** (nvarchar(46), NULL) - 50 distinct values
  - *Name of the person who approved the credit note.*
- **`approved_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the credit note was approved, stored as an nvarchar string (format appears 'YYYY-MM-DD HH:MM:SS').*
- **`related_return_id`** (nvarchar(26), NULL) - 30 distinct values
  - *Reference to a return record associated with this credit note (e.g., RET15025).*
- *(... and 2 more columns)*

---

### b2b_customer_addresses

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Stores customer shipping/billing addresses for B2B customers. It is a lookup/reference table that maps customers to one or more physical addresses and provides textual and geo coordinates for routing, delivery and location-based analysis.

**Business Questions:**

- How many addresses does each customer have and which customers have multiple addresses?
- What is the distribution of customer addresses across cities / pincodes?
- Which addresses are within a given radius of a warehouse or delivery hub (after converting lat/long)?
- Are there customers with missing or malformed address lines or coordinates that need cleansing?
- Which addresses frequently receive orders when joined with orders/dispatches (requires join)?

**Key Columns:**

- **`address_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Unique identifier for the address record (alphanumeric).*
- **`customer_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier of the customer owning or associated with the address (alphanumeric).*
- **`addr_line1`** (nvarchar(44), NULL) - 48 distinct values
  - *Primary street address line (e.g., building number, street).*
- **`addr_line2`** (nvarchar(48), NULL) - 4 distinct values
  - *Secondary address line (landmark or additional directions). Nullable and low-cardinality with many repeated values like landmarks.*
- **`city`** (nvarchar(32), NULL) - 10 distinct values
  - *City of the address.*
- **`state`** (nvarchar(24), NULL) - 1 distinct values
  - *State/province of the address. In this dataset, it is constant (Gujarat).*
- **`pincode`** (nvarchar(22), NULL) - 50 distinct values
  - *Postal code (pincode) for the address, stored as text.*
- **`country`** (nvarchar(20), NULL) - 1 distinct values
  - *Country of the address. In this dataset, constant (India).*
- **`latitude`** (nvarchar(28), NULL) - 50 distinct values
  - *Latitude coordinate for the address, stored as text (nvarchar) with high precision.*
- **`longitude`** (nvarchar(28), NULL) - 50 distinct values
  - *Longitude coordinate for the address, stored as text (nvarchar) with high precision.*

---

### b2b_customers

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** Master customer registry for the B2B domain. Stores customer identifiers, contact details, commercial attributes (account type, credit terms/limit, GST), address pointers and linkage to sales reps. Serves as the primary lookup for customer-level joins to orders, invoices, contracts, addresses and sales reporting.

**Business Questions:**

- How many customers do we have by account_type and customer_segment?
- What is the total and average credit_limit by account_type or assigned_sales_rep_id?
- Which sales reps are assigned the most customers and how are those customers distributed across tiers?
- How many new customers were created per month/quarter (cohort analysis)?
- Which customers share the same billing and delivery address or have missing contact information?

**Key Columns:**

- **`customer_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Surrogate business identifier for each customer (string). Appears unique across rows in this snapshot (50 distinct values).*
- **`name`** (nvarchar(70), NULL) - 39 distinct values
  - *Customer display name or business name.*
- **`account_type`** (nvarchar(38), NULL) - 4 distinct values
  - *Categorical business classification (Retailer, Wholesale, Hotel/Catering, Exporter).*
- **`gst_number`** (nvarchar(40), NULL) - 50 distinct values
  - *Tax identifier (GST) for the customer. Unique per customer in this dataset.*
- **`primary_contact_name`** (nvarchar(46), NULL) - 50 distinct values
  - *Name of the main contact person at the customer.*
- **`primary_contact_phone`** (nvarchar(38), NULL) - 50 distinct values
  - *Primary contact phone number (string, includes country code).*
- **`email`** (nvarchar(82), NULL) - 50 distinct values
  - *Primary contact email address.*
- **`billing_address_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Pointer to the billing address (string id). Logical FK to b2b_customer_addresses table.*
- **`delivery_address_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Pointer to the delivery/shipping address (string id). Logical FK to b2b_customer_addresses.*
- **`customer_segment`** (nvarchar(22), NULL) - 3 distinct values
  - *Tier classification (Tier-1, Tier-2, Tier-3) used for prioritization and segmentation.*
- *(... and 4 more columns)*

---

### b2b_dispatches

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** Records dispatch events for B2B orders: one row per dispatch containing identifiers (dispatch, order, vehicle, driver), timing (scheduled and actual), logistics metadata (seal, carrier, tracking), cost (freight), status and audit info. It serves as the operational dispatching / shipping ledger in the B2B schema.

**Business Questions:**

- What is the on-time rate for dispatched B2B orders (scheduled vs actual) over a time window?
- Which carriers, drivers, or vehicles contribute most to freight cost and which have the highest delay rates?
- What is the distribution of dispatch_status (SCHEDULED, IN_TRANSIT, DELIVERED) over the last month?
- Which orders are missing tracking_no or have unusually high freight_amounts?
- Who (created_by) is creating the most dispatch records and are there data-entry anomalies by creator?

**Key Columns:**

- **`dispatch_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Unique identifier for a dispatch event (external business ID, e.g., DISP11001).*
- **`order_id`** (nvarchar(30), NULL) - 50 distinct values
  - *Business order identifier associated with the dispatch (e.g., B2BORD4001).*
- **`vehicle_id`** (nvarchar(20), NULL) - 50 distinct values
  - *Identifier of the vehicle used for the dispatch (e.g., VH106).*
- **`driver_id`** (nvarchar(20), NULL) - 50 distinct values
  - *Identifier for the driver assigned to the dispatch (e.g., DR104).*
- **`carrier_partner_id`** (nvarchar(44), NULL) - 2 distinct values
  - *Identifier for the carrier or logistics partner (e.g., LOCAL_TRUCKERS, PRIVATE_LOGISTICS).*
- **`scheduled_dispatch_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Scheduled dispatch timestamp stored as NVARCHAR in 'YYYY-MM-DD HH:MM:SS' format.*
- **`actual_dispatch_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Actual dispatch timestamp (when the dispatch occurred) stored as NVARCHAR 'YYYY-MM-DD HH:MM:SS'.*
- **`seal_no`** (nvarchar(22), NULL) - 50 distinct values
  - *Seal number affixed to the shipment (security/consignment seal).*
- **`dispatch_status`** (nvarchar(30), NULL) - 3 distinct values
  - *Dispatch lifecycle status (categorical): SCHEDULED, IN_TRANSIT, DELIVERED.*
- **`freight_amount`** (nvarchar(24), NULL) - 50 distinct values
  - *Freight charge amount for the dispatch stored as NVARCHAR representing decimals (e.g., '1097.49').*
- *(... and 4 more columns)*

---

### b2b_events_stream

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Event stream table capturing domain events (inventory, order, shipment) ingested from upstream systems (B2B portal, ERP). Acts as an audit / integration staging table for downstream processing, reconciliation, and operational monitoring.

**Business Questions:**

- How many events of each event_type (ORDER_CREATED, SHIPMENT_CREATED, INVENTORY_UPDATED) occurred in a given date range?
- What proportion of events from each source_system have been processed vs unprocessed?
- Which aggregate_ids (orders/shipments/inventory items) generate the most retries or repeated events?
- How long does it take (median/95th percentile) from event_ts to processed_at for processed events?
- Are there particular partitions (partition_key) or source systems that show higher failure/retry rates?

**Key Columns:**

- **`event_uuid`** (nvarchar(30), NULL) - 50 distinct values
  - *Unique identifier for each event message (string).*
- **`event_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the event occurred in source system, stored as text in 'YYYY-MM-DD HH:MM:SS' pattern.*
- **`aggregate_type`** (nvarchar(28), NULL) - 3 distinct values
  - *High-level domain type the event relates to (inventory, order, shipment).*
- **`aggregate_id`** (nvarchar(30), NULL) - 31 distinct values
  - *Identifier of the domain entity the event concerns (e.g., order id, shipment id, inventory id).*
- **`event_type`** (nvarchar(44), NULL) - 3 distinct values
  - *Specific event action name (INVENTORY_UPDATED, SHIPMENT_CREATED, ORDER_CREATED).*
- **`payload_json`** (nvarchar(14), NULL) - 1 distinct values
  - *Payload body of the event as JSON text; currently contains '{}' for all rows.*
- **`source_system`** (nvarchar(30), NULL) - 2 distinct values
  - *Origin system of the event (B2B_PORTAL, ERP).*
- **`processed_flag`** (nvarchar(12), NULL) - 2 distinct values
  - *Indicator whether the event has been processed by downstream consumers ('1'/'0' stored as text).*
- **`processed_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the event was processed, stored as text in 'YYYY-MM-DD HH:MM:SS' format.*
- **`retry_count`** (nvarchar(12), NULL) - 4 distinct values
  - *Number of times processing has been retried for this event, stored as text but representing small integers.*
- *(... and 2 more columns)*

---

### b2b_invoices

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** Holds invoice-level records for B2B transactions: identifies invoices, links them to orders and customers, and stores amounts, tax components, status, and timestamps. Serves as the primary source for invoice/fiscal reporting, accounts receivable analysis, and integrations with payments/credit notes.

**Business Questions:**

- What is total invoice_amount (revenue) over a date range (daily/weekly/monthly)?
- How many and what value of invoices are currently OVERDUE vs PAID vs ISSUED?
- Which customers have the highest invoiced amounts in a period?
- What is total tax (cgst/sgst/total_tax) collected in a month or quarter?
- What is the average time from invoice_date to due_date and how many invoices are past due?

**Key Columns:**

- **`invoice_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Unique identifier for each invoice (nvarchar). Appears to uniquely identify rows (50 distinct values).*
- **`order_id`** (nvarchar(30), NULL) - 50 distinct values
  - *Identifier for the related order that generated the invoice (nvarchar).*
- **`invoice_number`** (nvarchar(30), NULL) - 50 distinct values
  - *Human/business-facing invoice number (nvarchar) often used in reports and communications.*
- **`invoice_date`** (nvarchar(48), NULL) - 50 distinct values
  - *Date/time invoice was issued, stored as nvarchar in YYYY-MM-DD HH:MM:SS format.*
- **`due_date`** (nvarchar(48), NULL) - 50 distinct values
  - *Date by which invoice payment is due, stored as nvarchar.*
- **`customer_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier for the customer being invoiced (nvarchar).*
- **`taxable_value`** (nvarchar(26), NULL) - 50 distinct values
  - *Invoice taxable base amount (stored as nvarchar representing decimal values).*
- **`igst`** (nvarchar(12), NULL) - 1 distinct values
  - *Integrated GST amount (nvarchar). In this snapshot it is constant '0', indicating no IGST applied.*
- **`cgst`** (nvarchar(24), NULL) - 50 distinct values
  - *Central GST component charged on the invoice (nvarchar decimal).*
- **`sgst`** (nvarchar(24), NULL) - 50 distinct values
  - *State GST component charged on invoice (nvarchar decimal).*
- *(... and 4 more columns)*

---

### b2b_kpi_daily_snapshots

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Daily snapshot of B2B KPI metrics captured per fulfilment centre. Stores per-centre, per-day aggregates such as orders, weight moved, revenues, returns and delivery performance for operational and reporting use.

**Business Questions:**

- Which centre had the highest gross sales on a given date or date range?
- How have total orders and gross sales trended by centre over the past N days?
- What is the average on-time delivery percentage and average delivery time per centre for a period?
- Which days had unusually high returns_kg or wastage_kg for a centre?
- What is the correlation between total_kg moved and gross_sales at a centre level over time?

**Key Columns:**

- **`snapshot_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Identifier for the snapshot record (string). Appears to uniquely identify each row in current sample.*
- **`centre_id`** (nvarchar(32), NULL) - 4 distinct values
  - *Fulfilment centre identifier (string), low cardinality (~4 centres).*
- **`date`** (nvarchar(30), NULL) - 41 distinct values
  - *Snapshot date stored as string in ISO-like format (yyyy-mm-dd) for most rows.*
- **`total_orders`** (nvarchar(14), NULL) - 31 distinct values
  - *Total number of orders captured in the snapshot (stored as string, small integer-like values).*
- **`total_kg`** (nvarchar(24), NULL) - 50 distinct values
  - *Total weight (kilograms) moved/processed in the snapshot (string representing decimal values).*
- **`gross_sales`** (nvarchar(28), NULL) - 50 distinct values
  - *Gross sales value for the snapshot (string representing monetary decimal).*
- **`returns_kg`** (nvarchar(22), NULL) - 50 distinct values
  - *Weight of returns (kilograms) recorded on that day (string decimal).*
- **`wastage_kg`** (nvarchar(20), NULL) - 50 distinct values
  - *Weight lost to wastage in kilograms (string decimal).*
- **`avg_delivery_time_min`** (nvarchar(16), NULL) - 46 distinct values
  - *Average delivery time in minutes (string, small integer-like).*
- **`on_time_pct`** (nvarchar(20), NULL) - 50 distinct values
  - *On-time delivery percentage (string representing decimal percent, e.g., '70.34').*
- *(... and 2 more columns)*

---

### b2b_order_allocations

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Records inventory allocations for B2B orders — who/when/how much inventory was reserved for an order (and order line), when that allocation expires or is released, and why.

**Business Questions:**

- How many active vs released allocations exist and what quantity (kg and units) is tied to each status?
- Which inventory items have the most allocated quantity (kg or units) and may be constrained?
- Which order lines have multiple allocations or repeated allocations over time?
- Who are the top allocators (allocated_by) by count or total allocated quantity?
- How many allocations will expire within a given date range (and how much quantity will be freed)?

**Key Columns:**

- **`allocation_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Unique identifier for the allocation event/record.*
- **`order_id`** (nvarchar(30), NULL) - 50 distinct values
  - *Identifier of the B2B order associated with the allocation.*
- **`order_line_id`** (nvarchar(28), NULL) - 34 distinct values
  - *Identifier for the order line (specific line item) the allocation maps to.*
- **`inventory_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier for the inventory item (location/SKU instance) reserved for the allocation.*
- **`allocated_qty_kg`** (nvarchar(22), NULL) - 50 distinct values
  - *Allocated quantity expressed in kilograms, stored as a string (decimal).*
- **`allocated_qty_units`** (nvarchar(16), NULL) - 43 distinct values
  - *Allocated quantity expressed in units (integer-like), stored as a string.*
- **`allocated_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the allocation was created, stored as an nvarchar in ISO-like format.*
- **`allocated_by`** (nvarchar(52), NULL) - 50 distinct values
  - *Name/identifier of the person or system that made the allocation.*
- **`expiry_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the allocation expires (reservation window ends), stored as string.*
- **`status`** (nvarchar(26), NULL) - 2 distinct values
  - *Current state of the allocation (e.g., ACTIVE or RELEASED).*
- *(... and 2 more columns)*

---

### b2b_order_events

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Event log of lifecycle changes for B2B orders. Each row records a discrete event (status change, allocation, pick, dispatch, etc.) tied to an order and actor, providing an append-only audit/history feed used for operational tracking, SLA calculations and downstream joins to orders/customers/dispatches for richer analytics.

**Business Questions:**

- How many events of each type (CREATED, ALLOCATED, PICKED, DISPATCHED, CONFIRMED) occurred in a given date range?
- What is the distribution of event sources (ERP, MOBILE_APP, PORTAL) and which source contributes most to unprocessed events?
- Which orders have the most events or repeated status changes (potential anomalies)?
- How long does it take on average from CREATED to DISPATCHED per order (requires timeline reconstruction using event_ts)?
- Which users/agents (event_by) perform the most dispatch or confirmation actions?

**Key Columns:**

- **`event_id`** (nvarchar(24), NULL) - 50 distinct values
  - *Unique identifier assigned to each event record in the event stream.*
- **`order_id`** (nvarchar(30), NULL) - 50 distinct values
  - *Identifier of the B2B order that this event pertains to.*
- **`event_type`** (nvarchar(30), NULL) - 6 distinct values
  - *Categorical label for the event action (e.g., CREATED, ALLOCATED, PICKED, DISPATCHED, CONFIRMED).*
- **`event_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the event occurred (stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format).*
- **`event_by`** (nvarchar(48), NULL) - 50 distinct values
  - *The user or system actor who triggered the event (human name or system identifier).*
- **`prev_status`** (nvarchar(30), NULL) - 3 distinct values
  - *Order status before the event was applied.*
- **`new_status`** (nvarchar(30), NULL) - 3 distinct values
  - *Order status after the event was applied.*
- **`details_json`** (nvarchar(14), NULL) - 1 distinct values
  - *JSON blob with additional event details; in this snapshot it is empty ('{}').*
- **`source_system`** (nvarchar(30), NULL) - 3 distinct values
  - *Originating system for the event (ERP, MOBILE_APP, PORTAL).*
- **`ip_address`** (nvarchar(40), NULL) - 50 distinct values
  - *IP address of the actor/system when the event was generated (string).*
- *(... and 2 more columns)*

---

### b2b_order_lines

**Rows:** 101  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** Represents individual line items for B2B orders: product sku, quantities, pricing, allocation and fulfillment metadata. It is a transactional detail table used for revenue, fulfillment and inventory allocation analyses within the B2B ordering system.

**Business Questions:**

- What is total revenue (sum of line_total) and average unit_price per SKU?
- Which SKUs generate the highest revenue and quantity sold?
- How are order lines distributed across warehouses (warehouse_allocated_id) and allocation_ids?
- What are typical promised_by dates/times vs created_at for order lines (lead time) after casting to datetime?
- Which remarks (packaging types) are most common and how do they correlate with quantities or revenue?

**Key Columns:**

- **`order_line_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Unique identifier for the order line (text). Appears to be the natural primary key but not declared as PK.*
- **`order_id`** (nvarchar(30), NULL) - 50 distinct values
  - *Identifier for parent order (order header).*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product stock keeping unit code for the line item.*
- **`item_description`** (nvarchar(58), NULL) - 10 distinct values
  - *Human readable description of the SKU at time of order (may include name/pack size).*
- **`qty_units`** (nvarchar(16), NULL) - 84 distinct values
  - *Quantity expressed in units (stored as nvarchar). Likely integer count of units/crates/etc.*
- **`qty_kg`** (nvarchar(20), NULL) - 85 distinct values
  - *Quantity expressed in kilograms (stored as nvarchar, decimal-like).*
- **`unit_price`** (nvarchar(22), NULL) - 99 distinct values
  - *Unit selling price for the line (stored as nvarchar, decimal-like).*
- **`line_total`** (nvarchar(26), NULL) - 101 distinct values
  - *Total amount for the order line (stored as nvarchar) — should equal unit_price * quantity (after correct numeric types and potential discounts).*
- **`allocation_id`** (nvarchar(28), NULL) - 44 distinct values
  - *Identifier for the allocation record that reserved inventory for this line (text).*
- **`promised_by`** (nvarchar(48), NULL) - 101 distinct values
  - *Promised fulfillment/delivery datetime for the line (stored as nvarchar).*
- *(... and 4 more columns)*

---

### b2b_orders

**Rows:** 71  
**Columns:** 15  
**Primary Keys:** *None*  

**Purpose:** Stores B2B order header-level records — metadata about each order such as identifiers, timestamps, amounts, channel, status, pickup centre and fulfillment priority. Serves as the central order header table for analytical queries and joins to line-level, payment, invoice, dispatch and customer tables.

**Business Questions:**

- What is total gross/net revenue and average order value over a date range?
- How do order volumes and revenues break down by order_channel, order_status or pickup_centre_id?
- What percentage of orders are CANCELLED vs PLACED/CONFIRMED and how much revenue is lost?
- Which customers place the highest value or most frequent B2B orders?
- How does fulfillment_priority (URGENT/HIGH/NORMAL) relate to dispatch/delivery performance and revenue?

**Key Columns:**

- **`order_id`** (nvarchar(30), NULL) - 71 distinct values
  - *Internal unique identifier for the order (string).*
- **`external_order_code`** (nvarchar(28), NULL) - 71 distinct values
  - *Order identifier from an external system or partner (string).*
- **`customer_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier for the customer placing the order (string).*
- **`order_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the order was placed (stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format).*
- **`requested_delivery_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Customer-requested delivery timestamp (text, same datetime format).*
- **`order_channel`** (nvarchar(28), NULL) - 4 distinct values
  - *Channel through which the order was placed (categorical: WhatsApp, Email, Phone, Sales Rep).*
- **`order_status`** (nvarchar(30), NULL) - 5 distinct values
  - *Current lifecycle status of the order (PLACED, CANCELLED, CONFIRMED, DISPATCHED, DELIVERED).*
- **`currency`** (nvarchar(16), NULL) - 1 distinct values
  - *Currency for the amounts (string) — in this dataset constant 'INR'.*
- **`gross_amount`** (nvarchar(26), NULL) - 50 distinct values
  - *Gross order amount before discounts and tax, stored as nvarchar with decimal values.*
- **`tax_amount`** (nvarchar(12), NULL) - 1 distinct values
  - *Tax component of the order amount (stored as nvarchar). Currently all values 0 in sample.*
- *(... and 5 more columns)*

---

### b2b_payments

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Records individual B2B payment events for invoices/customers. It captures payment identifiers, timestamps, amounts, payment methods, bank references, status and reconciliation metadata. The table supports financial reconciliation, payment reporting, and linking payments back to invoices/customers.

**Business Questions:**

- What is the total amount received in a period and how does it trend over time?
- Which payment modes (UPI, NEFT, RTGS, CHEQUE) contribute most to receipts?
- What proportion of payments are SUCCESS vs PENDING vs FAILED and how many remain unreconciled?
- What are the top customers by payment volume or number of payments?
- How long does reconciliation take on average (time between payment_ts and reconciled_at)?

**Key Columns:**

- **`payment_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Unique identifier for the payment event (string).*
- **`invoice_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier of the invoice associated with the payment (string).*
- **`customer_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier for the customer who made the payment (string).*
- **`payment_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp of when the payment occurred, stored as a string in 'YYYY-MM-DD HH:MM:SS' format.*
- **`amount`** (nvarchar(26), NULL) - 50 distinct values
  - *Monetary amount of the payment stored as a string (contains decimal numeric values).*
- **`payment_mode`** (nvarchar(22), NULL) - 4 distinct values
  - *How payment was made (CHEQUE, RTGS, UPI, NEFT) stored as text with low cardinality.*
- **`bank_ref_no`** (nvarchar(24), NULL) - 50 distinct values
  - *Bank reference number associated with the payment (string), useful for bank reconciliation.*
- **`status`** (nvarchar(24), NULL) - 3 distinct values
  - *Payment processing outcome (SUCCESS, PENDING, FAILED) stored as text.*
- **`reconciled_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *Indicator whether payment has been reconciled ('1' or '0' stored as text).*
- **`reconciled_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the payment was reconciled, stored as string in the same format as payment_ts.*
- *(... and 2 more columns)*

---

### b2b_picking_batches

**Rows:** 50  
**Columns:** 13  
**Primary Keys:** *None*  

**Purpose:** Represents picking batch metadata for B2B order fulfilment — each row is a picking batch created at a fulfilment centre, listing picker, timings, status, workload (lines and kg), route and priority. Used for operational reporting, productivity, SLA and throughput analysis.

**Business Questions:**

- How many picking batches were completed, in progress or created in a given date range and per centre?
- What is the average picking duration (finished_at - started_at) by picker, centre or route?
- How often do actual_lines deviate from expected_lines (over/under performance) and which pickers/centres have the largest variances?
- What is the distribution of total_kg per batch and how does transport_priority (HIGH vs NORMAL) correlate with completion rate and duration?
- Which routes produce the most/least batches and what is their average throughput and completion percentage?

**Key Columns:**

- **`picking_batch_id`** (nvarchar(24), NULL) - 50 distinct values
  - *Unique identifier for the picking batch (string).*
- **`centre_id`** (nvarchar(32), NULL) - 4 distinct values
  - *Identifier of the fulfilment centre where the batch was created (string).*
- **`picker_id`** (nvarchar(22), NULL) - 50 distinct values
  - *Identifier of the picker (employee) who performed the batch (string).*
- **`created_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the picking batch was created (string in 'YYYY-MM-DD HH:MM:SS' format).*
- **`started_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when picking for this batch actually started (string).*
- **`finished_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when picking for this batch finished (string).*
- **`status`** (nvarchar(32), NULL) - 3 distinct values
  - *Lifecycle state of a picking batch (CREATED, IN_PROGRESS, COMPLETED).*
- **`expected_lines`** (nvarchar(14), NULL) - 10 distinct values
  - *Number of lines expected to be picked in the batch (stored as string but numeric semantically).*
- **`actual_lines`** (nvarchar(14), NULL) - 10 distinct values
  - *Number of lines actually picked in the batch (stored as string but numeric semantically).*
- **`total_kg`** (nvarchar(24), NULL) - 50 distinct values
  - *Total weight of the batch in kilograms (stored as string, decimal values present).*
- *(... and 3 more columns)*

---

### b2b_portal_api_clients

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Stores API client credentials and usage metadata for B2B portal integrations (which customer the client belongs to, hashed keys/secrets, allowed IPs, scopes, rate limits, creation and last-used timestamps, and active status). It supports access control, auditing, and quota enforcement for API consumers.

**Business Questions:**

- How many active API clients exist and how many are inactive?
- Which customers have the most API clients?
- What is the distribution of rate limits (100/200/500) across clients?
- Which API clients have not been used recently (stale last_used) or never used?
- When were API clients created over time (trend of created_at)?

**Key Columns:**

- **`api_client_id`** (nvarchar(24), NULL) - 50 distinct values
  - *Unique identifier for the API client (human-friendly code like 'API6001').*
- **`customer_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier of the customer that owns the API client (e.g., 'CUST1001').*
- **`api_key_hash`** (nvarchar(138), NULL) - 50 distinct values
  - *Hashed API key value (opaque; used for verification but not reversible).*
- **`secret_hash`** (nvarchar(90), NULL) - 50 distinct values
  - *Hashed secret associated with the API client (opaque credential material).*
- **`allowed_ips_json`** (nvarchar(14), NULL) - 1 distinct values
  - *JSON array of allowed IP addresses for the client (currently all rows contain []).*
- **`rate_limit`** (nvarchar(16), NULL) - 3 distinct values
  - *Rate limit quota for the client (stored as nvarchar but represents numeric limits like 100/200/500 requests).*
- **`scopes_json`** (nvarchar(54), NULL) - 1 distinct values
  - *JSON array describing authorized scopes for the client (in this dataset always ["orders","inventory"]).*
- **`created_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp (stored as nvarchar) when the client was created (ISO-like format).*
- **`last_used`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp (stored as nvarchar) of the last observed use of the API client.*
- **`active_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *Flag indicating if the client is active ('1') or inactive/disabled ('0') stored as nvarchar.*

---

### b2b_price_list

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Price list table capturing per-SKU pricing rules targeted at customers or customer groups over time. It defines unit price, valid date range, minimum order quantity and metadata for each price_list entry. Used to determine applicable price for an order, produce price audits and drive customer-specific pricing logic.

**Business Questions:**

- What is the active price for SKU X for customer Y on a given date?
- How do prices vary between RETAIL and WHOLESALE for a given SKU over a time period?
- Which customers have custom price lists (customer_id populated) versus group-based prices?
- Which price list entries overlap in time for the same SKU and customer (possible conflicts)?
- What is the distribution (min/avg/max) of price_per_unit for a SKU across all price lists?

**Key Columns:**

- **`price_list_id`** (nvarchar(22), NULL) - 50 distinct values
  - *Identifier for the price list entry (string). Appears to be unique per row in this snapshot and likely the canonical id for a price rule.*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Stock Keeping Unit — product identifier the price applies to.*
- **`customer_id`** (nvarchar(26), NULL) - 34 distinct values
  - *Identifier of the specific customer the price is targeted at. Null likely indicates the absence of customer-specific price (could be group-level).*
- **`customer_group`** (nvarchar(28), NULL) - 2 distinct values
  - *The customer group the price applies to (e.g., RETAIL, WHOLESALE).*
- **`start_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Start timestamp of the price validity window stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*
- **`end_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *End timestamp of the price validity window stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*
- **`price_per_unit`** (nvarchar(22), NULL) - 50 distinct values
  - *Unit price for the SKU under this price_list entry. Stored as nvarchar but represents a numeric monetary value.*
- **`currency`** (nvarchar(16), NULL) - 1 distinct values
  - *Currency code for the price (ISO code), stored as nvarchar.*
- **`min_order_qty`** (nvarchar(14), NULL) - 40 distinct values
  - *Minimum order quantity required for the price to apply. Stored as nvarchar but represents integer quantity.*
- **`created_by`** (nvarchar(20), NULL) - 1 distinct values
  - *User that created the price_list entry. In this snapshot always 'admin'.*
- *(... and 2 more columns)*

---

### b2b_product_sales

**Rows:** 10  
**Columns:** 5  
**Primary Keys:** *None*  

**Purpose:** Product-level aggregated sales metrics for B2B SKUs. Each row summarizes sales metrics (gross, discounts, tax, net) at the SKU level. It appears to be a denormalized reporting table intended to show revenue-related KPIs per SKU.

**Business Questions:**

- Which SKUs generate the highest gross sales and net sales?
- What is the discount rate and tax rate applied to each SKU (discount or tax as percent of gross)?
- Which SKUs have the largest absolute discount amounts or tax amounts?
- What is the ranking of SKUs by net sales and how much of total sales does each SKU contribute?
- Are there anomalies where net sales + discount + tax ≠ gross sales (data integrity checks)?

**Key Columns:**

- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product SKU identifier (string). Represents the stock-keeping unit for the product that the sales metrics apply to.*
- **`Gross Sales`** (nvarchar(30), NULL) - 10 distinct values
  - *Total gross sales amount for the SKU before discounts and tax. Stored as nvarchar containing decimal numeric text.*
- **`Discount Amount`** (nvarchar(28), NULL) - 10 distinct values
  - *Total discount amount applied to the SKU (string representation of decimal). Represents absolute discount currency value.*
- **`Tax Amount`** (nvarchar(28), NULL) - 10 distinct values
  - *Total tax amount charged on the SKU (stored as nvarchar decimal text).*
- **`Net Sales`** (nvarchar(30), NULL) - 10 distinct values
  - *Net sales amount for the SKU after discounts and including tax where appropriate. Stored as nvarchar decimal text.*

---

### b2b_product_wise_sales

**Rows:** 29,240  
**Columns:** 8  
**Primary Keys:** *None*  

**Purpose:** Daily product-level sales snapshot for the B2B channel. Each row captures metrics (orders, quantity, gross/discount/tax/net amounts) for a specific product on a specific date. Used for sales reporting, trend analysis, and feeding higher-level aggregates.

**Business Questions:**

- What is the daily net sales trend for a specific product over a date range?
- Which product generated the highest gross sales (or net sales) in a given month?
- How has the total quantity sold (kg) changed week-over-week for a product?
- What is the average order size (kg) and average order value for each product over the last 30 days?
- How much discount (absolute and percent of gross) was applied per product in a selected period?

**Key Columns:**

- **`date`** (nvarchar(30), NULL) - 731 distinct values ⚠️ HIGH CARDINALITY
  - *The reporting date for the metrics in the row (stored as nvarchar, observed format YYYY-MM-DD; max length 10).*
- **`product_id`** (nvarchar(22), NULL) - 10 distinct values
  - *SKU or product identifier (nvarchar up to length 6 observed) representing the product associated with the metrics.*
- **`total_orders`** (nvarchar(52), NULL) - 29,240 distinct values ⚠️ HIGH CARDINALITY
  - *Number of orders for the product on the given date (stored as nvarchar). Could be integer or decimal formatted as text.*
- **`total_qty_kg`** (nvarchar(46), NULL) - 29,240 distinct values ⚠️ HIGH CARDINALITY
  - *Total quantity sold in kilograms for the product on the date (stored as nvarchar).*
- **`gross_sales`** (nvarchar(46), NULL) - 29,240 distinct values ⚠️ HIGH CARDINALITY
  - *Gross monetary sales for the product before discounts and taxes on that date (stored as nvarchar).*
- **`discount_amount`** (nvarchar(46), NULL) - 29,240 distinct values ⚠️ HIGH CARDINALITY
  - *Total discount applied to the product's sales on that date (stored as nvarchar).*
- **`tax_amount`** (nvarchar(46), NULL) - 29,240 distinct values ⚠️ HIGH CARDINALITY
  - *Tax collected on the product's sales for the date (stored as nvarchar).*
- **`net_sales`** (nvarchar(46), NULL) - 29,240 distinct values ⚠️ HIGH CARDINALITY
  - *Net sales amount for the product on the date after discounts and taxes (stored as nvarchar).*

---

### b2b_products

**Rows:** 10  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Catalog of B2B product master and inventory snapshot. Stores product identifiers (SKU, PLU), descriptive name, unit-of-measure, POS price, tax rate, current stock quantity, reorder trigger, activity flag and last update timestamp. Serves as the canonical product view for inventory, pricing and basic product-level joins.

**Business Questions:**

- Which products are below their reorder_point and need replenishment?
- What is the current inventory value by product (stock_qty * pos_price) and total inventory value?
- Which products are active and have not been updated in the last X days (stale product data)?
- Which UOMs or product categories (by name patterns) contribute most to stock volume or value?
- Are any product prices or tax rates inconsistent with expected values (e.g., tax_rate <> 5%)?

**Key Columns:**

- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Stock Keeping Unit — internal product identifier (nvarchar).*
- **`plucode`** (nvarchar(18), NULL) - 10 distinct values
  - *PLU (Price Look-Up) code — alternate product identifier often used at POS (nvarchar).*
- **`name`** (nvarchar(54), NULL) - 10 distinct values
  - *Human-readable product name (nvarchar).*
- **`uom`** (nvarchar(18), NULL) - 3 distinct values
  - *Unit of measure for the product (e.g., kg, 250g, 500g) stored as nvarchar.*
- **`pos_price`** (nvarchar(16), NULL) - 10 distinct values
  - *POS price as stored text (nvarchar) — numeric semantic representing selling price.*
- **`tax_rate`** (nvarchar(18), NULL) - 1 distinct values
  - *Applicable tax rate for the product, stored as nvarchar but represents a numeric percent/decimal.*
- **`stock_qty`** (nvarchar(16), NULL) - 10 distinct values
  - *Current stock quantity on hand, stored as nvarchar but semantically integer/decimal.*
- **`reorder_point`** (nvarchar(14), NULL) - 9 distinct values
  - *Threshold quantity at which product should be reordered (nvarchar representing numeric).*
- **`active_flag`** (nvarchar(18), NULL) - 1 distinct values
  - *Activity indicator stored as nvarchar (sample value '1' for active).*
- **`updated_at`** (nvarchar(48), NULL) - 10 distinct values
  - *Last update timestamp stored as nvarchar (ISO-like datetime strings).*

---

### b2b_quality_inspections

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** Records individual quality inspections performed on B2B batch/order line items. Each row captures who inspected, when, measured attributes (temperature, visual score, microbial test), outcome (accept/reject), reason and corrective action. It is used for QA analytics, traceability and linking inspection outcomes back to orders/fulfilment.

**Business Questions:**

- What is the pass (acceptance) rate and rejection count over time (daily/weekly/monthly)?
- Which inspectors have higher rejection rates or lower average visual_score/temperature anomalies?
- What are the most common corrective actions and how often are they applied?
- Is there a correlation between microbial_test results and acceptance_flag or corrective_action?
- Which batch_item_id or order_line_id have repeated inspections or higher failure rates?

**Key Columns:**

- **`inspection_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Unique identifier assigned to each inspection record (string). Appears nearly unique across rows.*
- **`batch_item_id`** (nvarchar(28), NULL) - 30 distinct values
  - *Identifier for the batch item or inventory batch being inspected (string).*
- **`order_line_id`** (nvarchar(28), NULL) - 32 distinct values
  - *Identifier of the order line associated with the inspected item (string).*
- **`inspector_id`** (nvarchar(30), NULL) - 49 distinct values
  - *Identifier of the inspector who performed the inspection (string).*
- **`inspection_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the inspection took place, stored as nvarchar but representing a datetime (e.g., '2025-11-04 12:31:26').*
- **`temp_c`** (nvarchar(18), NULL) - 48 distinct values
  - *Measured temperature in Celsius at inspection time, stored as string (values like '8.6199999999').*
- **`visual_score`** (nvarchar(16), NULL) - 30 distinct values
  - *Numeric visual inspection score stored as string (integers like '89', '99').*
- **`acceptance_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *Binary-like flag indicating acceptance (values '1' or '0' stored as string).*
- **`rejection_reason`** (nvarchar(26), NULL) - 1 distinct values ⚠️ 68.0% NULL
  - *Text reason for rejection. In current data largely null; non-null values only show 'Spoilage'.*
- **`photo_url`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Link to inspection photo/evidence (string). Currently entirely NULL in the sample.*
- *(... and 4 more columns)*

---

### b2b_returns

**Rows:** 50  
**Columns:** 13  
**Primary Keys:** *None*  

**Purpose:** Records return transactions for B2B orders: each row represents a return event (requested and received), its status, reason, quantity (kg), refund amount and disposition. It is used to track returns lifecycle, financial impact (refunds/credit notes) and operational handling (inspection, disposition).

**Business Questions:**

- What is the total refund amount and total weight (kg) returned over a given period?
- Which return reasons and dispositions account for the majority of returned weight and refunds?
- What is the average time from return request to receipt (turnaround) and how does it vary by disposition or reason?
- Which customers or orders have the highest number/weight/value of returns (when joined to orders/customers)?
- Which inspectors record the most returns or highest returned weight and are any inspectors associated with higher rejection rates?

**Key Columns:**

- **`return_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Unique identifier for the return event.*
- **`order_id`** (nvarchar(30), NULL) - 50 distinct values
  - *Identifier of the order associated with the return.*
- **`customer_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier for the customer who initiated the return.*
- **`requested_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the return was requested (stored as nvarchar).*
- **`received_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the returned goods were received (stored as nvarchar).*
- **`return_status`** (nvarchar(28), NULL) - 4 distinct values
  - *Lifecycle status of the return (REQUESTED, APPROVED, REJECTED, COMPLETED).*
- **`reason_code`** (nvarchar(40), NULL) - 4 distinct values
  - *Categorized reason for return (EXCESS_QUANTITY, QUALITY, DAMAGED, WRONG_ITEM).*
- **`qty_kg`** (nvarchar(22), NULL) - 50 distinct values
  - *Returned quantity in kilograms, stored as nvarchar containing numeric values.*
- **`refund_amount`** (nvarchar(24), NULL) - 50 distinct values
  - *Monetary refund issued for the return, stored as nvarchar containing numeric values (floats).*
- **`credit_note_id`** (nvarchar(24), NULL) - 33 distinct values
  - *Identifier of the credit note issued for the refund (nullable; references credit notes).*
- *(... and 3 more columns)*

---

### b2b_sales_agents

**Rows:** 60  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Directory of B2B sales agents: contact details, region/specialization, commission configuration and lifecycle metadata. Used to identify agents, segment by geography or specialization, compute commissions when joined with sales/contract tables, and support operational workflows (contacting, activating/deactivating agents).

**Business Questions:**

- How many active vs inactive sales agents are there, overall and by region?
- What is the distribution (avg/median/min/max) of commission rates across regions and specializations?
- Which agents joined within a specified date range (e.g., last 12 months) and how are they distributed by region/specialization?
- Who are the contact points (name/phone/email) for agents in a given region or specialization?
- Which agents should be considered for reactivation or outreach based on status and join_date (e.g., inactive > 6 months)?

**Key Columns:**

- **`agent_id`** (nvarchar(28), NULL) - 60 distinct values
  - *Unique identifier for the sales agent (string).*
- **`name`** (nvarchar(50), NULL) - 60 distinct values
  - *Agent's full name.*
- **`phone`** (nvarchar(38), NULL) - 60 distinct values
  - *Agent phone number (stored as string, includes country code/formatting).*
- **`email`** (nvarchar(80), NULL) - 60 distinct values
  - *Agent email address.*
- **`region`** (nvarchar(32), NULL) - 8 distinct values
  - *Geographic region or city the agent operates in (low cardinality).*
- **`specialization`** (nvarchar(34), NULL) - 4 distinct values
  - *Agent business specialization (e.g., Caterer, HORECA, Retail Chain, Wholesale).*
- **`commission_rate_pct`** (nvarchar(18), NULL) - 57 distinct values
  - *Agent commission rate stored as text. Values appear as floating numbers (e.g., '3.23', '0.5899999999999999') representing percentage-like rates.*
- **`join_date`** (nvarchar(30), NULL) - 59 distinct values
  - *Date agent joined the program, stored as string in YYYY-MM-DD format for most rows.*
- **`status`** (nvarchar(26), NULL) - 2 distinct values
  - *Agent lifecycle state (INACTIVE/ACTIVE).*
- **`created_at`** (nvarchar(48), NULL) - 60 distinct values
  - *Record creation timestamp as string (appears to be YYYY-MM-DD HH:MM:SS format).*

---

### b2b_sales_daily

**Rows:** 2,924  
**Columns:** 13  
**Primary Keys:** *None*  

**Purpose:** Daily B2B sales summary by date and customer_type. It appears to be an ingestion/summary table containing aggregated counts and monetary metrics (orders, quantity, gross/discount/tax/net) for B2B channels.

**Business Questions:**

- How do daily net_sales and gross_sales trend over time (trend / seasonality)?
- Which customer_type contributes the most to gross_sales, net_sales and total_orders over a given period?
- What is the average order value (net_sales / total_orders) and how has it changed over time?
- How much discount is being given relative to gross_sales (discount_amount / gross_sales) by customer_type or day?
- Are there days with anomalous tax_amount or negative net_sales that require investigation?

**Key Columns:**

- **`date`** (nvarchar(30), NULL) - 731 distinct values ⚠️ HIGH CARDINALITY
  - *Business date for the aggregated metrics (string in 'YYYY-MM-DD' format).*
- **`customer_type`** (nvarchar(34), NULL) - 4 distinct values
  - *Type/category of customer (categorical: Retail Chain, HORECA, Caterer, Wholesaler).*
- **`total_orders`** (nvarchar(14), NULL) - 26 distinct values
  - *Count of orders on that date for the customer_type (stored as string/int-like).*
- **`total_qty_kg`** (nvarchar(24), NULL) - 2,877 distinct values ⚠️ HIGH CARDINALITY
  - *Total quantity sold in kilograms for the date and customer_type (stored as string representing a numeric float).*
- **`gross_sales`** (nvarchar(26), NULL) - 2,922 distinct values ⚠️ HIGH CARDINALITY
  - *Gross sales amount (pre-discount and pre-tax) stored as string representing a numeric value.*
- **`discount_amount`** (nvarchar(24), NULL) - 2,902 distinct values ⚠️ HIGH CARDINALITY
  - *Total discounts applied for the aggregated date/customer_type (string numeric).*
- **`tax_amount`** (nvarchar(24), NULL) - 2,890 distinct values ⚠️ HIGH CARDINALITY
  - *Total tax collected for the day/customer_type (string numeric).*
- **`net_sales`** (nvarchar(46), NULL) - 2,923 distinct values ⚠️ HIGH CARDINALITY
  - *Net sales after discounts and taxes (string numeric).*
- **`created_at`** (nvarchar(48), NULL) - 1 distinct values
  - *Ingestion or row creation timestamp (string), appears constant across rows—likely the import time.*
- **`Unnamed: 9`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Empty artifact column (all nulls). Likely from source CSV/ETL header artifact.*
- *(... and 3 more columns)*

---

### b2b_sales_monthly

**Rows:** 48  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Monthly aggregated B2B sales metrics broken down by customer type. It provides pre-aggregated monthly KPIs (orders, quantity, gross/discount/tax/net sales) for B2B channels and is intended for reporting/dashboards and as a source for comparing against other channels or rollups.

**Business Questions:**

- How did net sales and gross sales trend month-over-month in 2024 for each customer_type?
- Which customer_type contributed the most to total orders, total quantity (kg) and net sales in a given month or over the year?
- What is the average order value and average kg per order by customer_type each month?
- What were the effective discount and tax rates by customer_type and month (discount_amount/gross_sales, tax_amount/gross_sales)?
- How does B2B monthly performance compare to other channels when joined by year and month (e.g., ecom_sales_monthly, pos_sales_monthly)?

**Key Columns:**

- **`year`** (nvarchar(18), NULL) - 1 distinct values
  - *Calendar year for the aggregated row (stored as nvarchar). Currently contains only '2024'.*
- **`month`** (nvarchar(14), NULL) - 12 distinct values
  - *Month number (1-12) for the aggregated row, stored as nvarchar.*
- **`customer_type`** (nvarchar(34), NULL) - 4 distinct values
  - *Categorical bucket indicating customer segment (e.g., Caterer, HORECA, Retail Chain, Wholesaler).*
- **`total_orders`** (nvarchar(16), NULL) - 40 distinct values
  - *Count of orders in the month for the customer_type, stored as nvarchar (integer-like).*
- **`total_qty_kg`** (nvarchar(26), NULL) - 48 distinct values
  - *Total quantity sold in kilograms for the month and customer_type, stored as nvarchar (decimal-like).*
- **`gross_sales`** (nvarchar(28), NULL) - 48 distinct values
  - *Sum of gross sales (pre-discount) for the month and customer_type, stored as nvarchar (decimal-like).*
- **`discount_amount`** (nvarchar(26), NULL) - 48 distinct values
  - *Total discounts applied in the month for the customer_type, stored as nvarchar (decimal-like).*
- **`tax_amount`** (nvarchar(26), NULL) - 48 distinct values
  - *Total tax collected for the month and customer_type, stored as nvarchar (decimal-like).*
- **`net_sales`** (nvarchar(28), NULL) - 48 distinct values
  - *Net sales after discounts and tax adjustments for the month and customer_type, stored as nvarchar (decimal-like).*
- **`created_at`** (nvarchar(48), NULL) - 1 distinct values
  - *Load or snapshot timestamp for the row (string). In this dataset it is constant (one ingestion timestamp).*

---

### b2b_sales_yearly

**Rows:** 4  
**Columns:** 9  
**Primary Keys:** *None*  

**Purpose:** Yearly aggregated B2B sales metrics broken down by customer type. This table contains pre-aggregated yearly KPIs (orders, quantities, sales, discounts, tax, net) for B2B customer segments and appears to be an ETL landing/raw layer snapshot of yearly metrics.

**Business Questions:**

- How do total orders and net sales compare across customer types for 2024?
- Which customer type contributed the most gross sales and what share of total sales do they represent?
- What is the average order value (gross_sales / total_orders) by customer type for the year?
- How do discounts and tax as percentages of gross_sales vary between customer segments?
- What is kg sold per order (total_qty_kg / total_orders) by customer type?

**Key Columns:**

- **`year`** (nvarchar(18), NULL) - 1 distinct values
  - *Calendar year for which the aggregated metrics are reported (stored as nvarchar). In this dataset all rows are '2024'.*
- **`customer_type`** (nvarchar(34), NULL) - 4 distinct values
  - *Categorical label describing the B2B customer segment (e.g., Caterer, HORECA, Retail Chain, Wholesaler).*
- **`total_orders`** (nvarchar(18), NULL) - 4 distinct values
  - *Total number of orders in the year for the customer_type (stored as nvarchar representing integer values).*
- **`total_qty_kg`** (nvarchar(28), NULL) - 4 distinct values
  - *Total quantity sold in kilograms for the year and customer_type (stored as nvarchar with decimal precision).*
- **`gross_sales`** (nvarchar(30), NULL) - 4 distinct values
  - *Total gross sales (pre-discount and pre-tax) for the year and customer_type (stored as nvarchar with decimals).*
- **`discount_amount`** (nvarchar(28), NULL) - 4 distinct values
  - *Total discount value applied across orders for the year and customer_type (stored as nvarchar with decimals).*
- **`tax_amount`** (nvarchar(28), NULL) - 4 distinct values
  - *Total tax collected/charged for the year and customer_type (stored as nvarchar with decimals).*
- **`net_sales`** (nvarchar(30), NULL) - 4 distinct values
  - *Total net sales (likely gross_sales - discount_amount + tax_amount or another reconciliation) for the year and customer_type (stored as nvarchar with decimals).*
- **`created_at`** (nvarchar(48), NULL) - 1 distinct values
  - *Ingestion or snapshot timestamp when the row was created in the raw table (stored as nvarchar). In this dataset it is identical across rows (2025-12-02 10:46:16).*

---

### b2b_shipment_tracking_events

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Events captured for B2B shipment tracking. Each row represents a single tracking event (scan/load/delivery/etc.) for a dispatch, recording timestamp, event type, location, device and operator metadata. This table is used for operational monitoring, delivery SLAs, route/driver analytics and audit trails.

**Business Questions:**

- What is the sequence of tracking events for a specific dispatch (dispatch_id) and how long between key events (e.g., PICKED -> OUT_FOR_DELIVERY -> DELIVERED)?
- Which devices or scanners produce the most events or have anomalous patterns (gaps/duplicates)?
- What percentage of dispatches reach each final event_type (DELIVERED vs returned) and location distribution of events?
- Are there geographic deviations for expected routes (using gps_lat/gps_long) or clusters where deliveries frequently fail/delay?
- What is the time lag between event occurrence (event_ts) and event ingestion/creation (created_at) to monitor telemetry delays?

**Key Columns:**

- **`tracking_event_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Unique identifier for each tracking event (string).*
- **`dispatch_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Identifier for the dispatch/consignment this event belongs to (string).*
- **`event_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the event actually occurred, stored as string (appears 'YYYY-MM-DD hh:mm:ss').*
- **`event_type`** (nvarchar(42), NULL) - 5 distinct values
  - *Categorical event label (e.g., PICKED, LOADED, IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED).*
- **`gps_lat`** (nvarchar(28), NULL) - 50 distinct values
  - *Latitude coordinate of the event as a string representing decimal degrees.*
- **`gps_long`** (nvarchar(28), NULL) - 50 distinct values
  - *Longitude coordinate of the event as a string representing decimal degrees.*
- **`scanned_by`** (nvarchar(46), NULL) - 50 distinct values
  - *Name of the person/operator who scanned or recorded the event.*
- **`scan_photo_url`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *URL to a scan/photo associated with the event (currently all null in sample).*
- **`location_name`** (nvarchar(32), NULL) - 10 distinct values
  - *Human-readable location/city name for the event (e.g., Nadiad, Gandhinagar).*
- **`status_note`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Optional short note about the event status (currently all null in sample).*
- *(... and 2 more columns)*

---

### b2b_vendor_partners

**Rows:** 45  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Repository of partner vendor master data for B2B operations — contains identifying, contact, service and commercial terms for vendors that provide services (logistics, quality inspection, cold storage, bulk packaging, transport) used across B2B workflows.

**Business Questions:**

- How many active vendors do we have by service type (e.g., Transport, Cold Storage, Quality Inspection)?
- Which cities host the most vendors and what is the geographic distribution of vendor services?
- What proportion of vendors are on NET 7 vs NET 15 vs NET 30 credit terms?
- Who are the primary contacts and contact details for a given vendor_id or vendor_name?
- Are there potential duplicate vendors (matching gst_no or phone/email) that need deduplication?

**Key Columns:**

- **`vendor_id`** (nvarchar(26), NULL) - 45 distinct values
  - *Logical identifier for the vendor partner (e.g., B2BV2001). Stored as nvarchar; appears unique across rows though not declared primary key.*
- **`vendor_name`** (nvarchar(78), NULL) - 45 distinct values
  - *Human readable vendor/company name.*
- **`service_type`** (nvarchar(46), NULL) - 5 distinct values
  - *Categorical descriptor of vendor service (e.g., Quality Inspection, Transport). Low-cardinality field.*
- **`contact_name`** (nvarchar(48), NULL) - 45 distinct values
  - *Primary contact person at the vendor.*
- **`phone`** (nvarchar(38), NULL) - 45 distinct values
  - *Vendor contact phone number (string including country code).*
- **`email`** (nvarchar(94), NULL) - 45 distinct values
  - *Vendor contact email address.*
- **`credit_terms`** (nvarchar(22), NULL) - 3 distinct values
  - *Payment terms offered to vendor (NET 7, NET 15, NET 30). Low cardinality (3 values).*
- **`gst_no`** (nvarchar(40), NULL) - 45 distinct values
  - *Tax identification number for the vendor (GST number). High-cardinality and suitable for legal/entity-level identity.*
- **`city`** (nvarchar(32), NULL) - 9 distinct values
  - *City where the vendor is located.*
- **`created_at`** (nvarchar(48), NULL) - 1 distinct values
  - *Ingestion or creation timestamp stored as nvarchar; currently appears to hold a single repeated value across rows (2025-12-02 11:03:52), indicating batch load metadata rather than per-row creation time.*

---

### delivery_slots

**Rows:** 80  
**Columns:** 8  
**Primary Keys:** *None*  

**Purpose:** Represents delivery time slots offered by fulfilment centres (centre_id) for specific dates and times, with capacity and remaining availability. Used to track and query which slots exist, their capacities, and how many order slots remain.

**Business Questions:**

- Which delivery slots have available capacity greater than zero for a given date and centre?
- What is the total delivery capacity and total available slots per centre per date?
- Which time windows (start_time - end_time) are most utilized (lowest available_orders / highest booked) across the date range?
- When were the slots created (created_at) and which slots were added most recently for a centre?
- List the next N earliest available slots across all centres (by date then start_time) with available_orders > 0

**Key Columns:**

- **`slot_id`** (nvarchar(28), NULL) - 80 distinct values
  - *Unique identifier for the delivery slot (string). Appears to be distinct per row (80 distinct).*
- **`date`** (nvarchar(30), NULL) - 15 distinct values
  - *Date of the delivery slot stored as nvarchar (format appears to be 'YYYY-MM-DD').*
- **`start_time`** (nvarchar(20), NULL) - 5 distinct values
  - *Start time of the slot stored as nvarchar (format 'HH:MM'). Low cardinality (5 distinct).*
- **`end_time`** (nvarchar(20), NULL) - 5 distinct values
  - *End time of the slot stored as nvarchar (format 'HH:MM'). Paired with start_time to describe the time window.*
- **`capacity_orders`** (nvarchar(16), NULL) - 56 distinct values
  - *Declared capacity (maximum orders) for the slot stored as nvarchar numeric string.*
- **`available_orders`** (nvarchar(16), NULL) - 59 distinct values
  - *Remaining number of orders that can still be booked for the slot, stored as nvarchar numeric string.*
- **`centre_id`** (nvarchar(64), NULL) - 3 distinct values
  - *Human-readable identifier/name of the fulfilment centre (e.g., 'Rajkot Packaging Unit'), stored as nvarchar. Only 3 distinct values in the sample.*
- **`created_at`** (nvarchar(48), NULL) - 80 distinct values
  - *Timestamp when the slot row was created/inserted, stored as nvarchar (format 'YYYY-MM-DD HH:MM:SS'). Distinct per row.*

---

### delivery_status

**Rows:** 232  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Event-level delivery tracking table that records status updates for deliveries/shipments tied to orders. Serves as the event stream for delivery lifecycle (loaded, in transit, out for delivery, failed attempt, delivered) and stores who updated the event and where (location + GPS).

**Business Questions:**

- What percentage of delivery events are DELIVERED vs FAILED vs IN_TRANSIT over a time window?
- How long (median/avg) does it take from LOADED to DELIVERED per location or per shipment?
- Which couriers/operators (updated_by) have the highest failed attempt or failure rates?
- Which locations (or geographic clusters using gps_lat/gps_long) have the most failed deliveries?
- What is the distribution of event types over the course of a day / hour to identify peak delivery activity?

**Key Columns:**

- **`delivery_id`** (nvarchar(24), NULL) - 101 distinct values
  - *Identifier for the delivery instance. Multiple event rows per delivery_id represent the lifecycle of that delivery.*
- **`shipment_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Identifier for the shipment that this delivery event is part of. May group multiple deliveries or relate to carrier tracking.*
- **`order_id`** (nvarchar(28), NULL) - 100 distinct values
  - *Identifier for the order associated with this delivery event. Connects events back to the originating order.*
- **`event_ts`** (nvarchar(48), NULL) - 232 distinct values ⚠️ HIGH CARDINALITY
  - *Timestamp of the delivery event as a string (nvarchar). Records when the event occurred.*
- **`event_type`** (nvarchar(42), NULL) - 6 distinct values
  - *Categorical label for the kind of event recorded (e.g., LOADED, IN_TRANSIT, OUT_FOR_DELIVERY, FAILED_ATTEMPT, DELIVERED).*
- **`location`** (nvarchar(28), NULL) - 4 distinct values
  - *Named location (city/region) where the event took place (e.g., Surat, Vadodara).*
- **`status`** (nvarchar(30), NULL) - 3 distinct values
  - *Current high-level delivery status label for the event (e.g., FAILED, IN_TRANSIT, DELIVERED).*
- **`updated_by`** (nvarchar(52), NULL) - 231 distinct values ⚠️ HIGH CARDINALITY
  - *Name of the user/operator or system that recorded the event.*
- **`gps_lat`** (nvarchar(28), NULL) - 232 distinct values ⚠️ HIGH CARDINALITY
  - *Latitude coordinate of where the event was recorded, stored as nvarchar.*
- **`gps_long`** (nvarchar(28), NULL) - 232 distinct values ⚠️ HIGH CARDINALITY
  - *Longitude coordinate of where the event was recorded, stored as nvarchar.*
- *(... and 2 more columns)*

---

### ecom_ab_test

**Rows:** 80  
**Columns:** 11  
**Primary Keys:** *None*  

**Purpose:** Stores metadata and summary metrics for e‑commerce A/B tests (experiments) run on the platform. Each row describes one experiment instance including identifiers, variants, timestamps, status, winner, and summary conversion rates. This table is used for experiment tracking, basic summarization, and downstream analysis of experiment outcomes.

**Business Questions:**

- Which experiments are currently RUNNING, and what are their start and expected end dates?
- For completed experiments, which variant (A or B) won and how many experiments did each variant win?
- What is the distribution and average of conversion_rate_a and conversion_rate_b across experiments?
- Which experiments produced a statistically meaningful improvement in conversion (e.g., B > A) and how large was the uplift?
- What is the typical experiment duration and are cancelled experiments correlated with short durations or low sample conversion?

**Key Columns:**

- **`test_id`** (nvarchar(28), NULL) - 80 distinct values
  - *Unique identifier of the A/B test (experiment). Appears distinct for each row (80 distinct).*
- **`test_name`** (nvarchar(58), NULL) - 3 distinct values
  - *Human-readable name of the experiment (e.g., 'Pricing Banner Test'). Low cardinality (3 unique names here).*
- **`variant_a`** (nvarchar(24), NULL) - 1 distinct values
  - *Label for variant A in the test (string). In this dataset it is uniformly 'Control'.*
- **`variant_b`** (nvarchar(28), NULL) - 1 distinct values
  - *Label for variant B in the test (string). In this dataset it is uniformly 'Treatment'.*
- **`start_ts`** (nvarchar(48), NULL) - 80 distinct values
  - *Experiment start timestamp stored as nvarchar (ISO-like 'YYYY-MM-DD hh:mm:ss'). Distinct per experiment.*
- **`end_ts`** (nvarchar(48), NULL) - 80 distinct values
  - *Experiment end timestamp stored as nvarchar (ISO-like). Distinct per experiment.*
- **`status`** (nvarchar(28), NULL) - 3 distinct values
  - *Current lifecycle state of the experiment: RUNNING, CANCELLED, or COMPLETED.*
- **`winner_variant`** (nvarchar(18), NULL) - 3 distinct values
  - *Which variant won at the experiment conclusion: 'A', 'B', or 'NONE' (no winner determined).*
- **`conversion_rate_a`** (nvarchar(18), NULL) - 76 distinct values
  - *Observed conversion rate metric for variant A, stored as nvarchar. Values represent percentage or proportion (e.g., '3.25', '7.34'), but stored as text with decimal artifacts.*
- **`conversion_rate_b`** (nvarchar(18), NULL) - 75 distinct values
  - *Observed conversion rate metric for variant B, stored as nvarchar. Similar format considerations as conversion_rate_a.*
- *(... and 1 more columns)*

---

### ecom_acquisition_agents

**Rows:** 55  
**Columns:** 9  
**Primary Keys:** *None*  

**Purpose:** Holds e-commerce customer-acquisition agent directory and metadata used to track who performed customer acquisition, their contact information, acquisition channel, area, join date and record creation timestamp. Used for reporting on acquisition workforce, channel mix and simple agent-level lookups.

**Business Questions:**

- How many acquisition agents are active vs inactive?
- How many agents joined in each month/quarter/year?
- Which acquisition channels supplied the most agents and how are they distributed across areas?
- List contact details (phone, email) for all ACTIVE agents or agents in a given area.
- Which agents were created/added in a given period (by created_at) for auditing/recent-hire reporting?

**Key Columns:**

- **`agent_id`** (nvarchar(30), NULL) - 55 distinct values
  - *Unique identifier for the acquisition agent (e.g., 'ECOMAG3001').*
- **`name`** (nvarchar(54), NULL) - 55 distinct values
  - *Full name of the acquisition agent.*
- **`phone`** (nvarchar(38), NULL) - 55 distinct values
  - *Agent phone number including country code and formatting (stored as text).*
- **`email`** (nvarchar(84), NULL) - 55 distinct values
  - *Agent email address (text).*
- **`acq_channel`** (nvarchar(44), NULL) - 5 distinct values
  - *Acquisition channel through which the agent was onboarded (e.g., 'Social Media', 'Influencer').*
- **`area`** (nvarchar(32), NULL) - 9 distinct values
  - *Geographic area or city for the agent (e.g., 'Surat', 'Rajkot').*
- **`join_date`** (nvarchar(30), NULL) - 55 distinct values
  - *Agent join date stored as a string in YYYY-MM-DD format.*
- **`status`** (nvarchar(26), NULL) - 2 distinct values
  - *Operational status of the agent (ACTIVE or INACTIVE).*
- **`created_at`** (nvarchar(48), NULL) - 55 distinct values
  - *Timestamp when the agent record was created in the system, stored as a string 'YYYY-MM-DD HH:MM:SS'.*

---

### ecom_activity_log

**Rows:** 200  
**Columns:** 8  
**Primary Keys:** *None*  

**Purpose:** Activity / audit log for e-commerce entities (customers, orders, payments, products). Captures who performed what action, on which entity, when, from which IP, and optional notes. Serves auditing, troubleshooting, security monitoring, and change-tracking purposes in the schema.

**Business Questions:**

- How many CREATE / UPDATE / DELETE / STATUS_CHANGE actions happened each day over the last 30 days?
- Which users (performed_by) initiated the most DELETE actions in the last month and from which IPs?
- What was the last recorded action for a given entity (by entity_id) and when did it happen?
- Are there spikes in actions (especially DELETE or STATUS_CHANGE) for a specific entity_type or IP address indicating unusual activity?
- How many actions were recorded per entity_type (ORDER, CUSTOMER, PAYMENT, PRODUCT) and what is the distribution of action types within each entity_type?

**Key Columns:**

- **`audit_id`** (nvarchar(28), NULL) - 200 distinct values
  - *Unique identifier for the audit log entry. Presently distinct for all rows sampled.*
- **`entity_type`** (nvarchar(26), NULL) - 4 distinct values
  - *Type/category of the entity that the action applies to (examples: PAYMENT, CUSTOMER, ORDER, PRODUCT).*
- **`entity_id`** (nvarchar(26), NULL) - 126 distinct values
  - *Identifier of the specific entity instance that was acted upon. Values contain prefixed IDs (e.g., CUST..., EORD...).*
- **`action`** (nvarchar(36), NULL) - 4 distinct values
  - *Type of action performed on the entity (CREATE, UPDATE, DELETE, STATUS_CHANGE).*
- **`action_ts`** (nvarchar(48), NULL) - 200 distinct values
  - *Timestamp for when the action occurred, stored as an nvarchar string in 'YYYY-MM-DD HH:MM:SS' format in the sample.*
- **`performed_by`** (nvarchar(36), NULL) - 3 distinct values
  - *Identifier of who performed the action (examples observed: system, support_agent, admin).*
- **`ip_address`** (nvarchar(40), NULL) - 200 distinct values
  - *Source IP address of the actor when the action was performed (IPv4 format observed).*
- **`notes`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Optional short notes about the action. In the sample this column is fully null.*

---

### ecom_browsing_history

**Rows:** 300  
**Columns:** 9  
**Primary Keys:** *None*  

**Purpose:** Captures raw user browsing events on the e-commerce site (searches, category clicks, product views) and serves as the behavioural event source for analytics, personalization and funnel analyses.

**Business Questions:**

- Which search queries generate the most product views or category clicks?
- How many unique customers viewed a specific SKU in a given date range and on which device types?
- Which referrer sources drive the highest volume of search events and product views?
- What is the hourly/daily distribution of browsing events (event_ts) to detect peak times?
- Which customers performed searches but did not convert (requires join to orders) in the same session/window?

**Key Columns:**

- **`browse_id`** (nvarchar(26), NULL) - 300 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for the browsing event/row (string). Appears to be an event-level id.*
- **`customer_id`** (nvarchar(26), NULL) - 95 distinct values
  - *Identifier for the customer who generated the event (string).*
- **`sku`** (nvarchar(22), NULL) - 7 distinct values
  - *Product SKU related to the event (string). For VIEW_PRODUCT and possibly other events.*
- **`event_ts`** (nvarchar(48), NULL) - 300 distinct values ⚠️ HIGH CARDINALITY
  - *Event timestamp stored as nvarchar (string) representing when the event occurred.*
- **`event_type`** (nvarchar(38), NULL) - 3 distinct values
  - *Type of browsing event (enumeration): e.g., CATEGORY_CLICK, SEARCH, VIEW_PRODUCT.*
- **`search_query`** (nvarchar(42), NULL) - 5 distinct values
  - *The user's search text for SEARCH events; often NULL for non-search events.*
- **`device_type`** (nvarchar(24), NULL) - 3 distinct values
  - *Device platform used (ios, android, web).*
- **`referrer_source`** (nvarchar(26), NULL) - 4 distinct values
  - *Traffic source/referrer (FB Ads, WhatsApp, Google, Direct).*
- **`created_at`** (nvarchar(48), NULL) - 300 distinct values ⚠️ HIGH CARDINALITY
  - *Timestamp when the record was created or ingested into the raw table (string). May differ from event_ts.*

---

### ecom_cart_items

**Rows:** 150  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Holds individual e‑commerce cart line items captured from the raw data feed. Each row represents a product variant added to a shopping cart, with quantity, price at the time of add, timestamps and a reservation flag. It is a raw, denormalized source used for cart-level and item-level analyses, behavioral analysis and joining to product, variant and cart metadata.

**Business Questions:**

- Which SKUs and variants are most frequently added to carts (by count and quantity)?
- What is the distribution of items per cart and average basket size (item count / quantity)?
- How much nominal revenue (price_at_add * qty) is added to carts over time and by SKU/variant?
- What percentage of cart items are reserved (reserved_flag) and how does reservation correlate with conversion?
- What are peak times / hourly patterns for adding items to carts (based on added_at)?

**Key Columns:**

- **`cart_item_id`** (nvarchar(22), NULL) - 150 distinct values
  - *Surrogate identifier for the cart line item (unique id per item row).*
- **`cart_id`** (nvarchar(26), NULL) - 81 distinct values
  - *Identifier for the shopping cart that contains this item (links the item to a multi‑item cart).*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Stock Keeping Unit code identifying the product model at a SKU level (product-level identifier).*
- **`qty`** (nvarchar(14), NULL) - 10 distinct values
  - *Quantity of the SKU added to the cart for this cart_item. Stored as nvarchar but represents an integer.*
- **`added_at`** (nvarchar(48), NULL) - 150 distinct values
  - *Timestamp (string) when the item was added to the cart.*
- **`updated_at`** (nvarchar(48), NULL) - 150 distinct values
  - *Timestamp (string) of the last update to this cart item (quantity change, reservation change, etc.).*
- **`reserved_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *Binary flag stored as text indicating whether the item is reserved (values '1' or '0').*
- **`price_at_add`** (nvarchar(16), NULL) - 10 distinct values
  - *The price recorded for the item at the time it was added to the cart (stored as nvarchar; integer-like values observed).*
- **`variant_id`** (nvarchar(24), NULL) - 21 distinct values
  - *Identifier for the specific product variant (size/color/pack) added to the cart.*
- **`notes`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Free text notes for the cart item (user or system notes). Currently fully NULL in this dataset.*

---

### ecom_carts

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Captures shopping cart snapshots for e-commerce sessions: who created the cart (customer_id, session_id), timing (created_at, last_updated_at), contents summary (total_items, total_amount), promotion usage (coupon_code), platform (device_type), and abandonment state (abandoned_flag, abandoned_at). It is used as a staging/analytics source for cart behaviour, abandonment and pre-checkout metrics.

**Business Questions:**

- What is the overall cart abandonment rate and how has it trended over time?
- What is the average cart value (total_amount) and distribution by device_type or coupon_code?
- How effective are coupons (NEWUSER vs FRESH10) in changing average cart value or abandonment rate?
- Which customers or sessions generate the highest cart values and how many items do they contain?
- What is the time between cart creation and abandonment (or last update) and how does that vary by device?

**Key Columns:**

- **`cart_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Unique identifier for a cart snapshot. Appears unique per row (distinct 100).*
- **`customer_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Identifier of the customer who owns or created the cart; distinct per row in sample.*
- **`session_id`** (nvarchar(30), NULL) - 100 distinct values
  - *Identifier for browser/app session associated with the cart; useful to tie cart activity to session-level behaviours.*
- **`created_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp (as text) when the cart was created. Pattern appears to be 'YYYY-MM-DD hh:mm:ss'.*
- **`last_updated_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Text timestamp for the latest update to the cart (item added/removed or other changes).*
- **`total_items`** (nvarchar(12), NULL) - 8 distinct values
  - *Text field indicating the total count of items in the cart; low cardinality (8 distinct values) and small max length.*
- **`total_amount`** (nvarchar(24), NULL) - 100 distinct values
  - *Monetary total for the cart stored as text with decimals (many distinct values).*
- **`coupon_code`** (nvarchar(24), NULL) - 2 distinct values
  - *Applied coupon identifier (e.g., NEWUSER, FRESH10). Low cardinality (2 values) with ~37% nulls (no coupon).*
- **`currency`** (nvarchar(16), NULL) - 1 distinct values
  - *Currency code for the cart amounts (INR for all rows in this sample).*
- **`device_type`** (nvarchar(24), NULL) - 3 distinct values
  - *Platform where cart was created: web, ios, android. Small number of categories.*
- *(... and 2 more columns)*

---

### ecom_coupon_usage

**Rows:** 140  
**Columns:** 7  
**Primary Keys:** *None*  

**Purpose:** Records instances of coupon usage in the e-commerce system — one row per use of a coupon tied to a customer and an order. It is used to measure coupon redemptions, discounts applied, and temporal patterns of coupon usage for marketing and finance analyses.

**Business Questions:**

- Which coupons were redeemed most often in a given date range?
- What is the total discount given per coupon and overall in a period?
- How many unique customers used coupons vs total coupon uses (repeat usage)?
- What is the time distribution (hour/day/month) of coupon redemptions?
- Which customers or orders received the largest total discounts?

**Key Columns:**

- **`coupon_usage_id`** (nvarchar(28), NULL) - 120 distinct values
  - *Unique identifier for this coupon usage event (string).*
- **`coupon_id`** (nvarchar(28), NULL) - 54 distinct values
  - *Identifier of the coupon that was applied (links to coupon metadata/campaign).*
- **`customer_id`** (nvarchar(26), NULL) - 78 distinct values
  - *Identifier of the customer who used the coupon (links to customer profile).*
- **`order_id`** (nvarchar(28), NULL) - 84 distinct values
  - *Identifier of the order associated with the coupon usage (links to order and revenue data).*
- **`applied_ts`** (nvarchar(48), NULL) - 140 distinct values
  - *Timestamp when the coupon was applied (stored as text, samples show 'YYYY-MM-DD HH:MM:SS').*
- **`discount_given`** (nvarchar(22), NULL) - 135 distinct values
  - *Monetary value of discount applied for this usage (stored as text representing numeric values).*
- **`created_at`** (nvarchar(48), NULL) - 140 distinct values
  - *Timestamp when the coupon usage record was created in the system (stored as text, sample format 'YYYY-MM-DD HH:MM:SS').*

---

### ecom_coupons

**Rows:** 65  
**Columns:** 13  
**Primary Keys:** *None*  

**Purpose:** Holds master/definition records for promotional coupons used in the e-commerce system. It describes coupon identifiers, codes, discount rules, validity windows, eligibility criteria and administrative metadata. Used to determine which coupons exist and their properties for validation, application and reporting.

**Business Questions:**

- Which coupons are currently valid (now between valid_from and valid_to) and active?
- How many coupons of each discount_type (PERCENT vs FLAT) exist and what are their typical discount_value and max_discount_amount?
- What coupons require a minimum order amount above a given threshold (e.g., > 200)?
- Which coupons will expire in the next X days?
- Which coupons have low usage limits (e.g., usage_limit = 1) and might need replenishment or monitoring?

**Key Columns:**

- **`coupon_id`** (nvarchar(28), NULL) - 65 distinct values
  - *Unique identifier for the coupon record (string).*
- **`coupon_code`** (nvarchar(30), NULL) - 65 distinct values
  - *Human-facing coupon code customers enter at checkout (string).*
- **`description`** (nvarchar(48), NULL) - 2 distinct values
  - *Short human-readable classification of the coupon (e.g., 'Percentage Discount' or 'Flat Discount').*
- **`discount_type`** (nvarchar(24), NULL) - 2 distinct values
  - *Indicates calculation method for discount (e.g., 'PERCENT' or 'FLAT').*
- **`discount_value`** (nvarchar(14), NULL) - 6 distinct values
  - *Numeric value representing discount magnitude (percentage or flat amount) stored as text.*
- **`max_discount_amount`** (nvarchar(16), NULL) - 7 distinct values
  - *Maximum cap on discount amount (numeric stored as text) applied to percent discounts or absolute cap for promotions.*
- **`valid_from`** (nvarchar(48), NULL) - 63 distinct values
  - *Start of coupon validity window stored as a text timestamp.*
- **`valid_to`** (nvarchar(48), NULL) - 63 distinct values
  - *End of coupon validity window stored as a text timestamp.*
- **`min_order_amount`** (nvarchar(16), NULL) - 6 distinct values
  - *Minimum order total required for coupon to be applicable, stored as text numeric.*
- **`usage_limit`** (nvarchar(14), NULL) - 4 distinct values
  - *Maximum allowed uses for the coupon (per-coupon or global depending on business rules) stored as text numeric.*
- *(... and 3 more columns)*

---

### ecom_customer_addresses

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Stores customer postal and geolocation address records for the e-commerce domain. Used to map customers to delivery locations, support order routing, delivery analytics and customer contact/address history.

**Business Questions:**

- How many addresses does each customer have and what proportion are 'Home' vs 'Work'?
- Which cities and pincodes have the highest number of customer addresses?
- What is the geographic (lat/lon) coverage of our customer base within India and are there clusters with high address density?
- Which recent addresses (by created_at) were added in the last N days and which customers added them?
- Are there customers that have addresses in multiple cities or pincodes (potential fraud or multi-location customers)?

**Key Columns:**

- **`address_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Unique identifier for the address record (string ID like 'ADDR2001').*
- **`customer_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Identifier of the customer who owns the address (string ID like 'CUST1001').*
- **`label`** (nvarchar(18), NULL) - 2 distinct values
  - *Short categorization of the address (e.g., 'Home', 'Work').*
- **`addr_line1`** (nvarchar(44), NULL) - 98 distinct values
  - *Primary street address line containing house/number/street.*
- **`addr_line2`** (nvarchar(48), NULL) - 3 distinct values
  - *Secondary address line often containing landmarks or descriptors (e.g., 'Near Bus Stop').*
- **`city`** (nvarchar(32), NULL) - 10 distinct values
  - *City name where the address is located (e.g., 'Surat', 'Vadodara').*
- **`state`** (nvarchar(24), NULL) - 1 distinct values
  - *State/province of the address (all rows show 'Gujarat').*
- **`pincode`** (nvarchar(22), NULL) - 99 distinct values
  - *Postal code for the address (string form; numeric-like content).*
- **`country`** (nvarchar(20), NULL) - 1 distinct values
  - *Country of the address (all rows show 'India').*
- **`latitude`** (nvarchar(28), NULL) - 100 distinct values
  - *Latitude coordinate of the address stored as nvarchar (e.g., '22.007482').*
- *(... and 2 more columns)*

---

### ecom_customer_segmentation

**Rows:** 100  
**Columns:** 7  
**Primary Keys:** *None*  

**Purpose:** Stores per-customer segmentation metrics derived from RFM analysis and related loyalty/order behavior. Intended to support marketing segmentation, targeted campaigns, retention analysis and customer-value reporting within the e‑commerce analytics schema.

**Business Questions:**

- How many customers fall into each RFM segment and what proportion of the customer base does each segment represent?
- What is the average (and median) avg_order_value and purchase_frequency by rfm_segment?
- Which customers are 'Champions' and have a loyalty_score above a given threshold for VIP targeting?
- Who are the customers with recent purchases (last_purchase_date within X days) but low loyalty_score (possible conversion opportunities)?
- When were the segmentation records created (created_at) and how many new segment records were generated in a given time window?

**Key Columns:**

- **`customer_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Unique identifier for the customer in the segmentation dataset. Stored as nvarchar(26).*
- **`rfm_segment`** (nvarchar(32), NULL) - 4 distinct values
  - *Categorical RFM segmentation label (e.g., Hibernating, Regulars, At Risk, Champions). nvarchar(32).*
- **`loyalty_score`** (nvarchar(16), NULL) - 59 distinct values
  - *A numeric-like loyalty score stored as nvarchar(16) representing customer loyalty (integer-like values stored as text).*
- **`avg_order_value`** (nvarchar(24), NULL) - 100 distinct values
  - *Average order value per customer stored as nvarchar(24) (decimal-like values in string form).*
- **`purchase_frequency`** (nvarchar(18), NULL) - 84 distinct values
  - *Frequency of purchases for the customer (numeric-like) stored as nvarchar(18).*
- **`last_purchase_date`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp of the customer's last purchase stored as text (nvarchar(48)) in 'YYYY-MM-DD HH:MM:SS' format.*
- **`created_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the segmentation record was created in the system, stored as nvarchar(48).*

---

### ecom_customers

**Rows:** 100  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** Stores customer master/profile data for the e-commerce domain. It is the canonical customer dimension used to describe who the customers are, their contact details, demographic attributes, account status, consent and acquisition channel. It supports customer-centric reporting, segmentation, and joining to transactional tables (orders, payments, carts, addresses, etc.).

**Business Questions:**

- How many customers signed up each month and how has sign-up trend changed over time?
- What is the distribution of customers by preferred_language, gender, and source_channel?
- What percentage of customers have marketing_opt_in = 1, and how does opt-in vary by acquisition channel?
- How many customers are currently ACTIVE vs INACTIVE and how recently did they login?
- What are cohorts of customers by signup month and their last_login recency (to measure retention)?

**Key Columns:**

- **`customer_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Internal customer identifier used by the platform; appears unique per row (nvarchar).*
- **`external_customer_code`** (nvarchar(24), NULL) - 100 distinct values
  - *External/legacy identifier for the customer used by upstream/downstream systems.*
- **`first_name`** (nvarchar(28), NULL) - 81 distinct values
  - *Customer first/given name (nvarchar).*
- **`last_name`** (nvarchar(36), NULL) - 90 distinct values
  - *Customer last/family name (nvarchar).*
- **`email`** (nvarchar(70), NULL) - 100 distinct values
  - *Customer email address; appears unique in sample and is a common identifier for communications.*
- **`phone`** (nvarchar(38), NULL) - 100 distinct values
  - *Customer phone number, stored as a string with country code included in samples.*
- **`dob`** (nvarchar(30), NULL) - 100 distinct values
  - *Date of birth stored as nvarchar in 'YYYY-MM-DD' format in sample.*
- **`gender`** (nvarchar(22), NULL) - 3 distinct values
  - *Self-declared gender with low cardinality values (Other, Male, Female).*
- **`created_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Account creation timestamp stored as nvarchar; samples suggest format 'YYYY-MM-DD hh:mm:ss'.*
- **`last_login`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp of the customer's last login, stored as nvarchar (format similar to created_at).*
- *(... and 4 more columns)*

---

### ecom_frequently_bought

**Rows:** 100  
**Columns:** 5  
**Primary Keys:** *None*  

**Purpose:** Stores pairwise product co-purchase (frequently bought together) signals for e-commerce. Each row represents an association between a base SKU (sku) and another SKU frequently bought with it (freq_with_sku), with a numeric co-purchase strength and a last-updated timestamp. This table is used for product affinity, recommendation, and cross-sell analyses.

**Business Questions:**

- For a given SKU, which other SKUs are most frequently bought together (top N by co_purchase_rate)?
- Which SKU pairs have a co_purchase_rate above a chosen threshold (e.g., 5) for inclusion in cross-sell campaigns?
- When were the affinity signals last updated, and which signals changed recently?
- Which products (by sku) are the most common 'freq_with_sku' targets across all base SKUs (best candidates for site-level cross-sell slots)?
- Are there any SKU pairs where co_purchase_rate has increased or decreased over time (requires historical snapshots/join to previous tables if available)?

**Key Columns:**

- **`map_id`** (nvarchar(28), NULL) - 100 distinct values
  - *Internal mapping identifier for each affinity row. Likely a surrogate or source-system id for the map/record.*
- **`sku`** (nvarchar(22), NULL) - 6 distinct values
  - *The base product SKU for which co-purchase relationships are recorded (the item a customer viewed or purchased that has associated frequently-bought items).*
- **`freq_with_sku`** (nvarchar(22), NULL) - 6 distinct values
  - *The SKU that is frequently bought together with the base sku — the paired product in the affinity relationship.*
- **`co_purchase_rate`** (nvarchar(20), NULL) - 96 distinct values
  - *Numeric score representing the strength or rate of co-purchase between sku and freq_with_sku. Stored as text (nvarchar) but values are floating-point-like (e.g., '11.24', '6.61').*
- **`last_updated`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp string indicating when this affinity record was last updated. Stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*

---

### ecom_notifications

**Rows:** 150  
**Columns:** 9  
**Primary Keys:** *None*  

**Purpose:** Stores records of notifications (email, SMS, push) sent to customers related to orders and marketing; serves as the event/log table for outbound customer communications in the e-commerce schema.

**Business Questions:**

- What is the volume of notifications sent by channel (PUSH/EMAIL/SMS) over time?
- What are delivery outcomes (DELIVERED / FAILED / SENT) by notification type or by customer cohort?
- Which customers received the most notifications in a given period?
- How many notifications are tied to orders and what delivery outcomes do those tied notifications have?
- What are the peak hours/days when notifications are sent and which channels perform better at those times?

**Key Columns:**

- **`notification_id`** (nvarchar(30), NULL) - 150 distinct values
  - *Unique identifier for each notification event (string). Currently appears unique per row (150 distinct).*
- **`customer_id`** (nvarchar(26), NULL) - 78 distinct values
  - *Identifier of the customer who was targeted/received the notification (string, medium cardinality ~78 distinct).*
- **`notification_type`** (nvarchar(20), NULL) - 3 distinct values
  - *Channel/type of notification sent (PUSH/EMAIL/SMS). Low cardinality (3 distinct values).*
- **`title`** (nvarchar(52), NULL) - 3 distinct values
  - *Short title of the notification (e.g., 'Order Update', 'Delivery Confirmation', 'New Offer'). Low cardinality and closely tied to message text.*
- **`message`** (nvarchar(74), NULL) - 3 distinct values
  - *Full message body or template short text sent to the customer. Low cardinality here (3 distinct messages).*
- **`sent_ts`** (nvarchar(48), NULL) - 150 distinct values
  - *Timestamp when the notification was sent, stored as nvarchar but formatted like 'YYYY-MM-DD HH:MM:SS' (high cardinality).*
- **`delivery_status`** (nvarchar(28), NULL) - 3 distinct values
  - *Result of send attempt: FAILED, DELIVERED, SENT (low cardinality 3 values).*
- **`linked_order_id`** (nvarchar(26), NULL) - 75 distinct values
  - *Identifier of an order related to the notification (string, medium cardinality ~75 distinct). May be null if notification is promotional.*
- **`created_at`** (nvarchar(48), NULL) - 150 distinct values
  - *Timestamp when the notification record was created in the system, stored as nvarchar in ISO-like format. May differ from sent_ts (e.g., queued vs actually sent).*

---

### ecom_orders

**Rows:** 601  
**Columns:** 20  
**Primary Keys:** *None*  

**Purpose:** Orders table recording e-commerce order-level events and monetary amounts. It captures order identifiers, customer linkage, timestamps, channel and campaign attribution, fulfillment and delivery metadata, and financials (total, tax, discount, shipping, net). It acts as a primary fact table for sales/fulfilment/marketing analysis in the schema.

**Business Questions:**

- What is total/net revenue and number of orders over time (day/week/month) and by channel?
- Which campaigns or coupon codes generate the most revenue, orders, and highest average order value?
- What are cancellation and refund rates by channel, fulfillment centre, or delivery slot?
- How does order distribution and fulfillment load vary by delivery_slot_id and fulfillment_centre_id?
- Which customers are repeat vs new and what is their average order value and frequency?

**Key Columns:**

- **`order_id`** (nvarchar(28), NULL) - 601 distinct values ⚠️ HIGH CARDINALITY
  - *Internal unique order identifier (string). High-cardinality: 601 distinct values across 601 rows.*
- **`order_number`** (nvarchar(34), NULL) - 601 distinct values ⚠️ HIGH CARDINALITY
  - *Human-facing order reference (string). High-cardinality and often shown in reports/UX.*
- **`customer_id`** (nvarchar(26), NULL) - 98 distinct values
  - *Identifier linking the order to a customer (string). Distinct: 98 across 601 rows.*
- **`order_ts`** (nvarchar(48), NULL) - 463 distinct values ⚠️ HIGH CARDINALITY
  - *Order timestamp as string in 'YYYY-MM-DD HH:MM:SS' format. Distinct: 463.*
- **`channel`** (nvarchar(30), NULL) - 2 distinct values
  - *Sales channel where order originated (categorical: 'Web' or 'Mobile App').*
- **`order_status`** (nvarchar(28), NULL) - 6 distinct values
  - *Current lifecycle status of order (PLACED/CONFIRMED/PACKED/SHIPPED/CANCELLED/etc.).*
- **`payment_status`** (nvarchar(26), NULL) - 3 distinct values
  - *Payment lifecycle state (PENDING, REFUNDED, PAID).*
- **`delivery_slot_id`** (nvarchar(22), NULL) - 50 distinct values
  - *Identifier for the scheduled delivery slot (moderate cardinality: 50 distinct).*
- **`delivery_address_id`** (nvarchar(26), NULL) - 500 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier of delivery address for the order (high-cardinality: ~500 distinct).*
- **`total_amount`** (nvarchar(24), NULL) - 500 distinct values ⚠️ HIGH CARDINALITY
  - *Order gross total as string representing a numeric (float) value.*
- *(... and 10 more columns)*

---

### ecom_payment_status_log

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Event log of payment status transitions and processing attempts for e-commerce payments. Each row records a single logged transition or processing attempt for a payment (identified by payment_id), along with metadata about source, response, retry attempts, and timestamps. This table is used for operational monitoring, retry logic analysis, and debugging payment processing flows.

**Business Questions:**

- What proportion of payment status transitions result in FAILED vs PAID vs PENDING?
- How many retries are performed per payment and how many payments exceed a retry threshold (e.g., >2)?
- Are failures more common for a particular source (Manual vs PG Webhook) or response_code (200/402/500)?
- Which payments had status changed most recently (latest updated_at) and are still unprocessed (processed_flag = 0)?
- What is the time lag between created_at and updated_at for status changes and does it differ by source or response_code?

**Key Columns:**

- **`log_id`** (nvarchar(28), NULL) - 100 distinct values
  - *Unique identifier for the log row (string). Distinct count=100 suggests uniqueness for each record in this snapshot.*
- **`payment_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Identifier for the payment this log row relates to (string). Distinct=100 — many unique payments in sample.*
- **`status_before`** (nvarchar(28), NULL) - 3 distinct values
  - *Payment status before the logged transition (enum-like string). Distinct values: PENDING (36%), PAID (33%), INITIATED (31%).*
- **`status_after`** (nvarchar(24), NULL) - 3 distinct values
  - *Payment status after the logged transition (enum-like string). Distinct values: FAILED (50%), PENDING (30%), PAID (20%).*
- **`updated_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp string when the status change was recorded (format appears to be 'YYYY-MM-DD HH:MM:SS'); distinct=100.*
- **`source`** (nvarchar(30), NULL) - 2 distinct values
  - *Origin of the status update (string). Two values observed: 'Manual' (57%) and 'PG Webhook' (43%).*
- **`response_code`** (nvarchar(16), NULL) - 3 distinct values
  - *Response code returned by the payment gateway or processing system (string). Observed values: 500 (38%), 200 (33%), 402 (29%).*
- **`response_body`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Payload/body returned by the gateway for the response. In this snapshot it is 100% NULL — placeholder for detailed response if available.*
- **`retry_count`** (nvarchar(12), NULL) - 4 distinct values
  - *Number of retry attempts for processing the event stored as nvarchar. Distinct values small (0,1,2,3) with distribution: 1 (34%), 3 (27%), 0 (20%), 2 (19%).*
- **`processed_flag`** (nvarchar(12), NULL) - 2 distinct values
  - *Binary flag indicating whether the log event has been processed/handled (stored as nvarchar '0'/'1'). Distinct values: 1 (53%), 0 (47%).*
- *(... and 2 more columns)*

---

### ecom_payments

**Rows:** 100  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** Payment ledger for e-commerce transactions capturing payment attempts, status, gateway details, settlement and refund eligibility. It serves as the canonical source for payment events and reconciliation in the schema.

**Business Questions:**

- What is the total collected amount and count of payments by payment_mode or payment_gateway over a period?
- What percentage of payments are successful vs failed or pending, and how does that vary by gateway or mode?
- What is the average settlement lag (time between payment_ts and settlement_date) and settlement rate by gateway?
- How many payments are refund-eligible and what is their total amount?
- Which orders have payments with failed or pending status (to drive follow-ups / retries)?

**Key Columns:**

- **`payment_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Unique identifier for the payment attempt/record (string).*
- **`order_id`** (nvarchar(28), NULL) - 100 distinct values
  - *Reference to the order associated with the payment (string).*
- **`payment_ts`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the payment was initiated/recorded (stored as nvarchar).*
- **`amount`** (nvarchar(24), NULL) - 100 distinct values
  - *Monetary amount for the payment (stored as nvarchar; contains decimal numbers).*
- **`payment_mode`** (nvarchar(30), NULL) - 4 distinct values
  - *Mode of payment (enumeration: COD, NETBANKING, UPI, CARD).*
- **`payment_gateway`** (nvarchar(34), NULL) - 3 distinct values
  - *Payment gateway/provider used (e.g., Razorpay, Paytm, BankTransfer).*
- **`gateway_ref_no`** (nvarchar(28), NULL) - 100 distinct values
  - *Reference number from the payment gateway for this payment attempt (string).*
- **`status`** (nvarchar(24), NULL) - 3 distinct values
  - *Outcome status of the payment attempt (PENDING, FAILED, SUCCESS).*
- **`settlement_status`** (nvarchar(28), NULL) - 2 distinct values
  - *Whether the payment has been settled to the merchant (SETTLED or UNSETTLED).*
- **`settlement_date`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the payment was marked settled (stored as nvarchar).*
- *(... and 4 more columns)*

---

### ecom_product_events

**Rows:** 250  
**Columns:** 8  
**Primary Keys:** *None*  

**Purpose:** Records discrete product-related events on the e‑commerce platform (stock changes and price changes). It is an event log used to understanding when and why product attributes (stock or price) changed and who/what triggered those changes.

**Business Questions:**

- Which SKUs experienced the most BACK_IN_STOCK, OUT_OF_STOCK or PRICE_DROP events in a given date range?
- How did frequency of PRICE_DROP events vary over time (daily/weekly) and which agent (triggered_by) initiated most price changes?
- Which SKUs had frequent inventory fluctuations (OUT_OF_STOCK / BACK_IN_STOCK) and when did those events occur?
- Are price drops followed by spikes in orders/sales (requires joining with sales/orders tables)?
- Which automated agent (pricing_bot, inventory_bot, system) is responsible for the majority of events and how does that vary by SKU?

**Key Columns:**

- **`event_id`** (nvarchar(28), NULL) - 250 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for each product event record (string). Appears to be unique per row in the sample (high cardinality).*
- **`sku`** (nvarchar(22), NULL) - 7 distinct values
  - *Product SKU associated with the event. Low cardinality in the sample (7 distinct SKUs); common join key to product-related tables.*
- **`event_ts`** (nvarchar(48), NULL) - 250 distinct values ⚠️ HIGH CARDINALITY
  - *Timestamp when the event logically occurred (stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format in the sample). High cardinality.*
- **`event_type`** (nvarchar(36), NULL) - 3 distinct values
  - *Type of product event. Low cardinality with values in the sample: BACK_IN_STOCK, PRICE_DROP, OUT_OF_STOCK.*
- **`old_value`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Previous value of the changed attribute (intended for price or inventory level). In the current sample, column is 100% NULL which indicates either not populated or deprecated.*
- **`new_value`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *New value after the change (intended for price or inventory level). Like old_value, currently 100% NULL in the sample.*
- **`triggered_by`** (nvarchar(36), NULL) - 3 distinct values
  - *Agent that triggered the event. Low cardinality with typical values 'system', 'pricing_bot', 'inventory_bot'.*
- **`created_at`** (nvarchar(48), NULL) - 250 distinct values ⚠️ HIGH CARDINALITY
  - *Timestamp when the event record was created in the system (stored as nvarchar). High cardinality and likely close to event_ts but may differ when events are ingested after occurrence.*

---

### ecom_product_wise_sales

**Rows:** 21,300  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Daily product-level ecommerce sales snapshot. Each row captures sales metrics (orders, customers, quantity, gross/net amounts, fees, discounts, taxes) for a given product and date. Used for reporting, trend analysis, and feeding downstream KPIs.

**Business Questions:**

- Which products drove the most net sales over a given date range?
- How did daily gross sales and net sales trend for a particular product last month?
- Which products have the highest average quantity per order or highest discount rates?
- What is the contribution of delivery_fee and tax_amount to total costs across products?
- Which days had anomalous sales (spikes/dips) for top SKUs?

**Key Columns:**

- **`date`** (nvarchar(30), NULL) - 710 distinct values ⚠️ HIGH CARDINALITY
  - *Calendar date for the sales snapshot. Stored as nvarchar(30) but values appear in YYYY-MM-DD format (max len 10).*
- **`product_id`** (nvarchar(22), NULL) - 10 distinct values
  - *SKU or product identifier. nvarchar(22). Low cardinality (~10 distinct) in this table snapshot.*
- **`total_orders`** (nvarchar(46), NULL) - 21,300 distinct values ⚠️ HIGH CARDINALITY
  - *Total number of orders for the product on the date. Stored as nvarchar; likely integer values but may contain punctuation or decimals.*
- **`total_customers`** (nvarchar(46), NULL) - 21,300 distinct values ⚠️ HIGH CARDINALITY
  - *Count of distinct customers who bought the product on that date. Stored as nvarchar but represents integer counts.*
- **`total_qty_kg`** (nvarchar(46), NULL) - 21,300 distinct values ⚠️ HIGH CARDINALITY
  - *Total quantity sold in kilograms for the product on that date. Stored as nvarchar; numeric float/decimal semantics expected.*
- **`gross_sales`** (nvarchar(46), NULL) - 21,300 distinct values ⚠️ HIGH CARDINALITY
  - *Gross sales amount (pre-discount, pre-tax) for the product on that date. Stored as nvarchar; currency/numeric values expected.*
- **`discount_amount`** (nvarchar(46), NULL) - 21,300 distinct values ⚠️ HIGH CARDINALITY
  - *Total discount amount applied for the product on that date. Stored as nvarchar; numeric/currency expected.*
- **`delivery_fee`** (nvarchar(46), NULL) - 21,300 distinct values ⚠️ HIGH CARDINALITY
  - *Total delivery fees collected (or charged) for the product on that date. Stored as nvarchar; currency numeric expected.*
- **`tax_amount`** (nvarchar(46), NULL) - 21,300 distinct values ⚠️ HIGH CARDINALITY
  - *Total tax amount for the product on that date. Stored as nvarchar; numeric/currency expected.*
- **`net_sales`** (nvarchar(46), NULL) - 21,300 distinct values ⚠️ HIGH CARDINALITY
  - *Net sales amount after discounts, taxes, and delivery fees (final revenue) for the product on that date. Stored as nvarchar; currency numeric expected.*

---

### ecom_ratings_summary

**Rows:** 100  
**Columns:** 6  
**Primary Keys:** *None*  

**Purpose:** This table stores summarized e-commerce product rating metrics (one row per rating summary record) used to report product-level average rating, review counts, and timestamps for last review and last update. It is intended as a lightweight summary view of product ratings for reporting, dashboards, and quick lookups.

**Business Questions:**

- Which SKUs have the highest average rating and how many reviews do they have?
- Which SKUs have the most total reviews and what are their average ratings?
- Which products have not received any recent reviews (stale last_review_ts) or have old summary updates (updated_at)?
- Is there a relationship between total_reviews (popularity) and avg_rating (quality)?
- What are the top N SKUs by weighted rating (e.g., avg_rating weighted by total_reviews) in the last 30 days?

**Key Columns:**

- **`rating_summary_id`** (nvarchar(28), NULL) - 100 distinct values
  - *Unique identifier for the rating summary record (string). Appears distinct across the current dataset and is likely used to identify each summary row.*
- **`sku`** (nvarchar(22), NULL) - 7 distinct values
  - *Stock-keeping unit identifier for the product this rating summary pertains to.*
- **`avg_rating`** (nvarchar(18), NULL) - 72 distinct values
  - *Average rating value for the SKU's reviews, stored as nvarchar. Values appear as floating numbers (e.g., '4.5300000000000002').*
- **`total_reviews`** (nvarchar(14), NULL) - 56 distinct values
  - *Total number of reviews contributing to the avg_rating, stored as nvarchar but representing an integer count (max length 2 in sample).*
- **`last_review_ts`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp of the most recent review included in this summary, stored as nvarchar with format 'YYYY-MM-DD HH:MM:SS'.*
- **`updated_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the rating summary record was last updated, stored as nvarchar with format 'YYYY-MM-DD HH:MM:SS'.*

---

### ecom_refunds

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Holds refund events for e-commerce orders: one row per refund transaction capturing when the refund was requested/processed, its amount, mode, status and reason. It is used to analyze refund volume, reasons, processing outcomes and to reconcile with orders and payments.

**Business Questions:**

- What is the total refunded amount and number of refunds over a time window (daily/weekly/monthly)?
- Which reasons contribute most to refunds and how do they trend over time (Quality Issue vs Order Cancelled vs Customer Return)?
- What proportion of refunds are completed vs initiated vs failed and how much money is in each status?
- Which orders or payments have multiple refunds and what is the aggregate refunded amount per order?
- How does refund mode (ACCOUNT_CREDIT vs PG_REFUND) impact refund success rates and processing times?

**Key Columns:**

- **`refund_id`** (nvarchar(24), NULL) - 50 distinct values
  - *Unique identifier for the refund transaction (string).*
- **`order_id`** (nvarchar(28), NULL) - 39 distinct values
  - *Identifier of the order associated with the refund (string).*
- **`payment_id`** (nvarchar(26), NULL) - 39 distinct values
  - *Payment transaction identifier associated with the refunded payment (string).*
- **`refund_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp string when the refund event occurred (stored as nvarchar).*
- **`refund_amount`** (nvarchar(24), NULL) - 50 distinct values
  - *Monetary amount refunded (stored as nvarchar containing decimal values).*
- **`refund_mode`** (nvarchar(38), NULL) - 2 distinct values
  - *Mode used for the refund (enum-like string) — e.g., ACCOUNT_CREDIT or PG_REFUND.*
- **`gateway_ref_no`** (nvarchar(30), NULL) - 50 distinct values
  - *Payment gateway reference number for refunds (string from payment gateway).*
- **`status`** (nvarchar(28), NULL) - 3 distinct values
  - *Current processing status of the refund: COMPLETED, INITIATED, or FAILED.*
- **`processed_by`** (nvarchar(34), NULL) - 1 distinct values
  - *Actor/team that processed the refund (string); currently constant 'finance_team'.*
- **`processed_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp string when the refund was processed (stored as nvarchar).*
- *(... and 2 more columns)*

---

### ecom_return_items

**Rows:** 60  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Represents individual items within returned orders for the ecommerce returns pipeline. Each row is one returned item instance capturing identifiers (return_item_id, return_id, order_item_id), product reference (sku), quantity, inspection status/timestamp, restockability, disposition decision and optional notes.

**Business Questions:**

- Which SKUs generate the most returned items and what are their dispositions (RESTOCK/DISCARD/RETURN_TO_SUPPLIER)?
- What proportion of returned items are restockable, and does that vary by SKU or disposition?
- How many items per return (return_id) on average and which returns contain the largest quantities?
- What percentage of return items are inspected and what is the distribution of inspection timestamps (to measure inspection throughput)?
- Which order items (order_item_id) are most frequently returned (repeat returns) and how many times?

**Key Columns:**

- **`return_item_id`** (nvarchar(26), NULL) - 60 distinct values
  - *Unique identifier for each return item row. Appears to be unique across the table (60 distinct values).*
- **`return_id`** (nvarchar(26), NULL) - 29 distinct values
  - *Identifier linking this item to the parent return record. Many items can belong to a single return (29 distinct on 60 rows).*
- **`order_item_id`** (nvarchar(24), NULL) - 53 distinct values
  - *Identifier of the original order line / item that was returned (links to order line / order item tables).*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product SKU code of the returned item. Low cardinality (10 distinct) with skew (top sku ~20%).*
- **`qty`** (nvarchar(14), NULL) - 10 distinct values
  - *Returned quantity for the item. Stored as nvarchar but contains integer-like values (common values 7,6,10,2,4).*
- **`inspected_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *Flag indicating whether the returned item has been inspected. Values stored as text '1' or '0' (76.7% '1').*
- **`inspected_at`** (nvarchar(48), NULL) - 60 distinct values
  - *Timestamp when the item inspection occurred. Stored as nvarchar and appears to be ISO-like datetime strings (distinct values for all rows).*
- **`restockable_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *Flag indicating whether the returned item can be restocked into inventory. Textual '1'/'0' with ~53% '1'.*
- **`disposition`** (nvarchar(46), NULL) - 3 distinct values
  - *Categorical outcome for the returned item: DISCARD, RESTOCK, RETURN_TO_SUPPLIER (3 distinct).*
- **`notes`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Free-text notes about the return item. In this dataset notes is 100% null.*

---

### ecom_reviews

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Stores customer product reviews captured from the e-commerce channel. Each row represents one review instance with text, rating, timestamps and metadata; used to analyze product sentiment, quality, and customer feedback trends.

**Business Questions:**

- Which products (sku) have the highest and lowest average rating?
- How have review volumes and average ratings changed over time (daily/weekly/monthly)?
- Which reviews received the most helpful votes and who wrote them?
- What proportion of reviews are verified purchases and is there a rating difference between verified and non-verified reviews?
- Which reviews are negative (low rating / negative text) and have not been responded to by support?

**Key Columns:**

- **`review_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Surrogate identifier for each review record.*
- **`customer_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Identifier of the customer who submitted the review.*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product stock-keeping unit associated with the reviewed item.*
- **`rating`** (nvarchar(12), NULL) - 3 distinct values
  - *Customer numeric rating for the product (stored as nvarchar, values like '3','4','5').*
- **`title`** (nvarchar(36), NULL) - 4 distinct values
  - *Short headline/title provided by the reviewer summarizing the review.*
- **`review_text`** (nvarchar(86), NULL) - 4 distinct values
  - *The free-text body of the review where customers provide details about their experience.*
- **`review_ts`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the review was authored by the customer (stored as nvarchar in ISO-like format).*
- **`verified_purchase_flag`** (nvarchar(18), NULL) - 1 distinct values
  - *Flag indicating whether the review is from a verified purchase (stored as nvarchar, current data shows '1' for all rows).*
- **`helpful_count`** (nvarchar(14), NULL) - 21 distinct values
  - *Count of 'helpful' votes for the review (stored as nvarchar but numeric values present).*
- **`responded_by`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Identifier of staff/agent who responded to the review (currently 100% NULL).*
- *(... and 2 more columns)*

---

### ecom_sales_daily

**Rows:** 2,130  
**Columns:** 15  
**Primary Keys:** *None*  

**Purpose:** Daily aggregated e-commerce sales metrics by order channel. It appears to be a lightly processed daily rollup that captures counts (orders, customers), quantities (kg), monetary metrics (gross, discount, delivery, tax, net) and ingestion metadata. Its role in the schema is as a daily summary table used for reporting, dashboards and quick trend queries across order channels.

**Business Questions:**

- How do gross, discount, and net sales trend daily and by channel over a given period?
- Which order channel (Website, Mobile App, WhatsApp) generates the highest average order value or highest net sales per day/week?
- What is the relationship between total_qty_kg shipped and net sales (kg per unit revenue) over time?
- How do discounts and delivery fees impact net sales and margin estimates over time?
- Are there anomalous days with unusually high delivery fees, tax amounts, or discount rates that require investigation?

**Key Columns:**

- **`date`** (nvarchar(30), NULL) - 710 distinct values ⚠️ HIGH CARDINALITY
  - *Report date for the daily aggregate; stored as nvarchar in yyyy-mm-dd format (max length 10).*
- **`order_channel`** (nvarchar(30), NULL) - 3 distinct values
  - *Channel through which the orders were placed (Website, Mobile App, WhatsApp). nvarchar with low cardinality (3).*
- **`total_orders`** (nvarchar(16), NULL) - 286 distinct values ⚠️ HIGH CARDINALITY
  - *Daily count of orders for the date and channel; stored as nvarchar (integers up to 3 digits).*
- **`total_customers`** (nvarchar(16), NULL) - 257 distinct values ⚠️ HIGH CARDINALITY
  - *Number of distinct customers interacting / ordering on that date and channel; stored as nvarchar.*
- **`total_qty_kg`** (nvarchar(22), NULL) - 2,100 distinct values ⚠️ HIGH CARDINALITY
  - *Total quantity sold in kilograms for the date and channel; stored as nvarchar representing decimal numbers.*
- **`gross_sales`** (nvarchar(26), NULL) - 2,130 distinct values ⚠️ HIGH CARDINALITY
  - *Total gross sales (before discounts/tax/fees) for the date and channel; stored as nvarchar decimal-like strings.*
- **`discount_amount`** (nvarchar(24), NULL) - 2,121 distinct values ⚠️ HIGH CARDINALITY
  - *Total discount amount applied for the date and channel; stored as nvarchar decimal-like strings.*
- **`delivery_fee`** (nvarchar(24), NULL) - 2,113 distinct values ⚠️ HIGH CARDINALITY
  - *Total delivery fees charged/collected for the date and channel; stored as nvarchar decimals.*
- **`tax_amount`** (nvarchar(24), NULL) - 2,116 distinct values ⚠️ HIGH CARDINALITY
  - *Total tax collected for the date and channel; nvarchar decimal.*
- **`net_sales`** (nvarchar(46), NULL) - 2,130 distinct values ⚠️ HIGH CARDINALITY
  - *Reported net sales for the date and channel; stored as nvarchar decimal-like string. Likely equals gross - discount + delivery + tax or some variation — needs reconciliation.*
- *(... and 5 more columns)*

---

### ecom_sales_monthly

**Rows:** 36  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Monthly e-commerce sales rollup by order channel. This table stores pre-aggregated monthly metrics (orders, customers, quantities and monetary amounts) per order channel and month for the year 2024. It is intended for reporting, trend analysis and quick KPI lookups without joining raw transaction tables.

**Business Questions:**

- How did net sales trend month-over-month across the year 2024 for each order channel?
- Which order channel contributed the most to gross_sales and net_sales each month and overall in 2024?
- What is the month with highest total_qty_kg and how does that relate to total_orders across channels?
- What are month-over-month percentage changes in total_orders and total_customers by channel?
- What is the average order value (gross_sales / total_orders) and average customer spend (gross_sales / total_customers) by channel per month?

**Key Columns:**

- **`year`** (nvarchar(18), NULL) - 1 distinct values
  - *Calendar year for the monthly rollup. Stored as nvarchar and all rows show 2024 in the sample.*
- **`month`** (nvarchar(14), NULL) - 12 distinct values
  - *Month number (1..12) for the rollup, stored as nvarchar.*
- **`order_channel`** (nvarchar(30), NULL) - 3 distinct values
  - *Channel through which orders were placed (e.g., Mobile App, Website, WhatsApp). Low cardinality categorical field.*
- **`total_orders`** (nvarchar(18), NULL) - 35 distinct values
  - *Total number of orders in that month for the channel, stored as nvarchar (integer semantics).*
- **`total_customers`** (nvarchar(18), NULL) - 35 distinct values
  - *Number of unique customers who ordered in that month for the channel (stored as nvarchar).*
- **`total_qty_kg`** (nvarchar(26), NULL) - 36 distinct values
  - *Total quantity sold in kilograms for the month/channel, stored as nvarchar with decimal precision.*
- **`gross_sales`** (nvarchar(28), NULL) - 36 distinct values
  - *Total gross sales amount (pre-discount) for the month/channel, stored as nvarchar with decimals.*
- **`discount_amount`** (nvarchar(26), NULL) - 36 distinct values
  - *Total discounts given in the month/channel (monetary), stored as nvarchar.*
- **`delivery_fee`** (nvarchar(26), NULL) - 36 distinct values
  - *Total delivery fees collected in the month/channel, stored as nvarchar.*
- **`tax_amount`** (nvarchar(26), NULL) - 36 distinct values
  - *Total tax collected for the month/channel, stored as nvarchar.*
- *(... and 2 more columns)*

---

### ecom_sales_yearly

**Rows:** 3  
**Columns:** 11  
**Primary Keys:** *None*  

**Purpose:** Aggregated yearly e-commerce sales metrics broken down by order channel. This table appears to store pre-aggregated KPIs (orders, customers, quantities, and financial metrics) for each year × order_channel combination and is intended for reporting and trend analysis at a high level.

**Business Questions:**

- How do gross sales, net sales and total orders compare across order channels for the year?
- What is the average order value (gross and net) per channel for the year?
- What percent of gross sales is taken up by discounts, tax and delivery fees per channel?
- Which channel delivered the highest quantity (kg) sold and how does that compare to revenue share?
- Has customer count or orders concentration shifted between channels for this year (channel mix)?

**Key Columns:**

- **`year`** (nvarchar(18), NULL) - 1 distinct values
  - *Calendar year for the aggregated metrics (stored as nvarchar).*
- **`order_channel`** (nvarchar(30), NULL) - 3 distinct values
  - *Sales channel label (e.g., 'Mobile App', 'Website', 'WhatsApp').*
- **`total_orders`** (nvarchar(20), NULL) - 3 distinct values
  - *Total number of orders in the year for the channel (stored as nvarchar).*
- **`total_customers`** (nvarchar(20), NULL) - 3 distinct values
  - *Count of distinct customers who transacted in the year for the channel (stored as nvarchar).*
- **`total_qty_kg`** (nvarchar(28), NULL) - 3 distinct values
  - *Total quantity sold in kilograms for the year and channel (stored as nvarchar with decimals).*
- **`gross_sales`** (nvarchar(30), NULL) - 3 distinct values
  - *Gross sales amount (pre-discount, pre-tax) for the year and channel (stored as nvarchar with decimals).*
- **`discount_amount`** (nvarchar(28), NULL) - 3 distinct values
  - *Total discounts applied (monetary) for the year and channel (stored as nvarchar).*
- **`delivery_fee`** (nvarchar(28), NULL) - 3 distinct values
  - *Total delivery fees collected or charged for the year and channel (stored as nvarchar).*
- **`tax_amount`** (nvarchar(28), NULL) - 3 distinct values
  - *Total tax collected/recorded for the year and channel (stored as nvarchar).*
- **`net_sales`** (nvarchar(30), NULL) - 3 distinct values
  - *Net sales amount for the year and channel (likely gross minus discounts plus/minus fees/taxes) stored as nvarchar.*
- *(... and 1 more columns)*

---

### ecom_search_keywords

**Rows:** 100  
**Columns:** 6  
**Primary Keys:** *None*  

**Purpose:** This table captures search keyword records for the e-commerce site: each row links a search keyword to measured metrics (search_volume, conversion_rate), the top-selling SKU for that keyword, and a created_at timestamp. It is primarily an analytics/marketing table used to evaluate keyword performance, discover product demand signals from search, and prioritize SEO/merchandising.

**Business Questions:**

- Which keywords generate the highest total search volume and which of those have the highest conversion rates?
- Which SKUs are most frequently the top result for search terms and how do their associated conversion rates compare?
- How has search volume and conversion rate for a given keyword changed over time (trend) based on created_at timestamps?
- Which low-volume keywords have unusually high conversion rates (opportunity keywords)?
- What are the top-performing keywords to prioritize for SEO or paid bids (high search volume and high conversion)?

**Key Columns:**

- **`keyword_id`** (nvarchar(26), NULL) - 100 distinct values
  - *A unique identifier for the keyword record (string). Acts as a row identifier for this table's records.*
- **`keyword`** (nvarchar(38), NULL) - 9 distinct values
  - *The search term or keyword string people used (e.g., 'potato', 'organic veg').*
- **`search_volume`** (nvarchar(18), NULL) - 100 distinct values
  - *The number of searches (numeric) for the keyword during the captured period, stored as nvarchar.*
- **`conversion_rate`** (nvarchar(20), NULL) - 97 distinct values
  - *Conversion rate for the keyword (likely percent or ratio), stored as nvarchar with decimal values.*
- **`top_sku`** (nvarchar(22), NULL) - 7 distinct values
  - *The SKU identifier for the product most associated with this keyword (string).*
- **`created_at`** (nvarchar(48), NULL) - 100 distinct values
  - *The timestamp when the keyword record was captured, stored as nvarchar in 'YYYY-MM-DD hh:mm:ss' format.*

---

### ecom_ticket

**Rows:** 100  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Stores customer support tickets raised via the e-commerce platform; tracks ticket metadata (who, when, what, status, priority) and links to customers and orders. Used for support operations, reporting and root-cause analysis.

**Business Questions:**

- How many tickets are open, in-progress, resolved or closed over a given period?
- What is the distribution of ticket priority (HIGH/MEDIUM/LOW) and which agents handle the most high-priority tickets?
- What is the average time to resolution for resolved tickets (updated_at - created_at) and how does it vary by assigned_to or priority?
- Which customers or orders generate the most tickets in a time window?
- What are the top ticket subjects/reasons (e.g., Delivery Delay, Refund Query) and their proportions?

**Key Columns:**

- **`ticket_id`** (nvarchar(30), NULL) - 100 distinct values
  - *Unique identifier for the ticket (string). Appears distinct per row but not declared as a primary key.*
- **`customer_id`** (nvarchar(26), NULL) - 60 distinct values
  - *Identifier of the customer who raised the ticket (string).*
- **`subject`** (nvarchar(44), NULL) - 4 distinct values
  - *Short categorical reason for the ticket (e.g., Delivery Delay, Order Issue). Low cardinality (4 distinct).*
- **`description`** (nvarchar(60), NULL) - 4 distinct values
  - *Longer text explaining the customer's complaint (string) — often repeated consistent phrases in this dataset.*
- **`status`** (nvarchar(32), NULL) - 4 distinct values
  - *Ticket lifecycle state (OPEN, IN_PROGRESS, RESOLVED, CLOSED). Low cardinality (4).*
- **`priority`** (nvarchar(22), NULL) - 3 distinct values
  - *Priority assigned to the ticket (LOW, MEDIUM, HIGH) — very low cardinality.*
- **`created_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the ticket was created stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*
- **`updated_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp for the last update to the ticket stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*
- **`order_id`** (nvarchar(26), NULL) - 53 distinct values
  - *Order identifier associated with the ticket (string). Nullable; moderate cardinality.*
- **`assigned_to`** (nvarchar(40), NULL) - 3 distinct values
  - *Username/role of the agent handling the ticket (ops_manager, support_agent_1, support_agent_2). Very low cardinality.*

---

### ecom_ticket_messages

**Rows:** 293  
**Columns:** 7  
**Primary Keys:** *None*  

**Purpose:** Holds individual messages (conversation rows) for e-commerce support tickets. Each row represents one message in a ticket thread, capturing who sent it, when it was sent, the message text, and any attachment reference. It is used to analyze ticket conversation patterns, response times, and message content.

**Business Questions:**

- How many messages are exchanged per ticket (average, median, distribution)?
- What is the distribution of senders (support vs customer) across messages and per ticket?
- What are the most frequent message texts/templates and their proportions?
- What is the average time between consecutive messages on a ticket (response time)?
- Which tickets have the most messages (longest conversations)?

**Key Columns:**

- **`ticket_message_id`** (nvarchar(30), NULL) - 293 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for each message row (string).*
- **`ticket_id`** (nvarchar(30), NULL) - 100 distinct values
  - *Identifier for the support ticket to which the message belongs (string).*
- **`message_ts`** (nvarchar(48), NULL) - 293 distinct values ⚠️ HIGH CARDINALITY
  - *Timestamp when the message was sent (stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format).*
- **`sender`** (nvarchar(26), NULL) - 2 distinct values
  - *Role of the sender (categorical): typically 'support' or 'customer'.*
- **`message_text`** (nvarchar(68), NULL) - 4 distinct values
  - *Text content of the message. In this snapshot it contains a few common templates.*
- **`attachment_url`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *URL or reference to any attachment included with the message (string). Currently all values are null in the sample.*
- **`created_at`** (nvarchar(48), NULL) - 293 distinct values ⚠️ HIGH CARDINALITY
  - *Timestamp when the message row was created in the system (stored as nvarchar). May differ from message_ts if events are delayed.*

---

### ecom_vendors

**Rows:** 50  
**Columns:** 11  
**Primary Keys:** *None*  

**Purpose:** Master vendor reference for the e-commerce system: stores vendor identifiers, contact and tax details, categorization, location and lifecycle status. Used as a lookup for payments, orders, contracts and reporting about vendors.

**Business Questions:**

- How many vendors do we have overall and by status (ACTIVE vs INACTIVE)?
- What is the distribution of vendors by vendor_category and by city?
- Which vendors lack valid tax identifiers (missing gst_no or pan_no)?
- Provide contact details for all ACTIVE vendors in a given city or category.
- Which vendor partners should be excluded from procurement due to INACTIVE status?

**Key Columns:**

- **`vendor_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Unique identifier for the vendor (string code like 'ECOMV3001').*
- **`vendor_name`** (nvarchar(70), NULL) - 49 distinct values
  - *Human-readable vendor name.*
- **`vendor_category`** (nvarchar(30), NULL) - 5 distinct values
  - *Categorical classification of vendor (Ad Agency, Courier, Influencer, Marketing, Tech).*
- **`phone`** (nvarchar(38), NULL) - 50 distinct values
  - *Vendor phone number (string, includes country code and formatting).*
- **`email`** (nvarchar(92), NULL) - 49 distinct values
  - *Vendor email address for contact and billing.*
- **`billing_address`** (nvarchar(110), NULL) - 50 distinct values
  - *Free-form billing address (street, area, postal code).*
- **`gst_no`** (nvarchar(40), NULL) - 50 distinct values
  - *Vendor GST (tax) registration number.*
- **`pan_no`** (nvarchar(30), NULL) - 50 distinct values
  - *Vendor PAN (permanent account number) for tax/identity.*
- **`city`** (nvarchar(32), NULL) - 9 distinct values
  - *City portion of vendor address (normalized to a short token).*
- **`status`** (nvarchar(26), NULL) - 2 distinct values
  - *Lifecycle state of vendor (ACTIVE or INACTIVE).*
- *(... and 1 more columns)*

---

### ecom_wishlist

**Rows:** 100  
**Columns:** 6  
**Primary Keys:** *None*  

**Purpose:** Customer wishlist items captured by the e-commerce system. Each row represents a single item that a customer has added to their wishlist, along with when it was added and whether it was flagged as a priority. The table supports personalization, product interest analytics, and cross-referencing with orders and product catalogs.

**Business Questions:**

- Which products (SKUs) are most commonly added to wishlists?
- How many unique customers have added items to their wishlist in a given time range?
- What proportion of wishlist items are marked as priority?
- Which customers have the most high-priority wishlist items (potential targets for campaigns)?
- How long after adding an item to wishlist do customers typically purchase it? (requires join to orders/order_items)

**Key Columns:**

- **`wishlist_id`** (nvarchar(28), NULL) - 100 distinct values
  - *Surrogate identifier for each wishlist record (nvarchar(28)). In this dataset it appears unique per row (100 distinct values). Example top values include WISH04001..WISH04005.*
- **`customer_id`** (nvarchar(26), NULL) - 65 distinct values
  - *Identifier for the customer who added the wishlist item (nvarchar(26)). 65 distinct values in 100 rows - indicates some customers add multiple items. Top customers: CUST1058, CUST1066, CUST1083, CUST1081, CUST1018.*
- **`sku`** (nvarchar(22), NULL) - 7 distinct values
  - *Product SKU code added to the wishlist (nvarchar(22)). Very low cardinality: 7 distinct SKUs; skewed toward a few popular SKUs (TOM001 20%, POT002 16%, CAR004 15%, ONI003 13%, APP009 12%).*
- **`added_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp (nvarchar(48)) when the item was added to the wishlist. Stored as text in format like '2025-10-05 02:46:01'. Distinct for all rows in sample (100 distinct).*
- **`priority_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *String flag (nvarchar(20)) indicating whether the wishlist item is a priority. Values observed are '0' (54%) and '1' (46%).*
- **`notes`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Free-text field for any note associated with the wishlist item (nvarchar(16)). In this dataset the column is 100% NULL, indicating not used.*

---

### inventory_items

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Raw inventory items ledger capturing received batches of items with stock, batch, supplier and timestamp/cost metadata. Likely used as ingestion/raw source for inventory, expiry/ageing and costing analyses within the wider retail/fulfillment schema.

**Business Questions:**

- Which SKUs or item names have the largest total_stock_units in inventory?
- What batches are expiring within the next N days (near-expiry) and what is their total stock?
- Which supplier supplies the most stock (units) and what is their average cost_per_unit?
- What was the average cost_per_unit over time for a given SKU or supplier?
- When were specific batches received and how old is inventory by batch (ageing since received_at or mfg_date)?

**Key Columns:**

- **`item_id`** (nvarchar(24), NULL) - 100 distinct values
  - *Unique identifier for this inventory row / inventory item instance (string). Appears unique per row in this dataset.*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product SKU code (text) identifying the product model/variant. Low cardinality (~10 distinct).*
- **`name`** (nvarchar(58), NULL) - 10 distinct values
  - *Human-readable product name/description corresponding to the sku.*
- **`total_stock_units`** (nvarchar(18), NULL) - 97 distinct values
  - *Quantity of stock units available in this inventory row stored as text (numeric semantic).*
- **`batch_id`** (nvarchar(28), NULL) - 99 distinct values
  - *Batch identifier for the received goods (string). Mostly unique per row (99 distinct).*
- **`received_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the items were received into inventory; stored as text in yyyy-mm-dd hh:mm:ss format.*
- **`expiry_date`** (nvarchar(30), NULL) - 29 distinct values
  - *Expiry date of the batch/item in yyyy-mm-dd format but stored as text. Lower cardinality (~29 distinct values).*
- **`supplier`** (nvarchar(52), NULL) - 3 distinct values
  - *Name of the supplier/vendor providing the batch. Very low cardinality (3 suppliers).*
- **`cost_per_unit`** (nvarchar(22), NULL) - 100 distinct values
  - *Unit cost for the inventory row stored as text with decimal precision (e.g., '111.63').*
- **`mfg_date`** (nvarchar(30), NULL) - 68 distinct values
  - *Manufacture date for the batch in yyyy-mm-dd format stored as text.*
- *(... and 2 more columns)*

---

### order_items

**Rows:** 217  
**Columns:** 14  
**Primary Keys:** *None*  

**Key Columns:**

- **`order_item_id`** (nvarchar(24), NULL) - 217 distinct values ⚠️ HIGH CARDINALITY
- **`order_id`** (nvarchar(28), NULL) - 217 distinct values ⚠️ HIGH CARDINALITY
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
- **`product_name`** (nvarchar(58), NULL) - 10 distinct values
- **`variant_id`** (nvarchar(30), NULL) - 10 distinct values
- **`qty_units`** (nvarchar(14), NULL) - 20 distinct values
- **`qty_kg`** (nvarchar(14), NULL) - 20 distinct values
- **`unit_price`** (nvarchar(16), NULL) - 10 distinct values
- **`line_total`** (nvarchar(18), NULL) - 102 distinct values
- **`tax_amount`** (nvarchar(20), NULL) - 102 distinct values
- *(... and 4 more columns)*

---

### pos_daily_sales_summary

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Daily aggregated point-of-sale summary records per store/date. It captures precomputed daily metrics (transactions, sales, tax, refunds, avg transaction value) and metadata for each summary row. Intended for reporting, trend analysis, and high-level KPI checks rather than transaction-level queries.

**Business Questions:**

- What were daily total sales, tax and refunds by store for the last N days?
- Which store had the highest average transaction value or highest total transactions on a given day?
- How have total sales and refunds trended week-over-week or month-over-month per store?
- What is the refund rate (refunds / total_sales) or tax rate (total_tax / total_sales) per store or overall?
- Are there outlier dates (very high/low sales or avg_txn_value) that need investigation?

**Key Columns:**

- **`summary_id`** (nvarchar(24), NULL) - 50 distinct values
  - *Unique identifier for each daily summary row (e.g., 'SUM1000').*
- **`store_id`** (nvarchar(36), NULL) - 4 distinct values
  - *Identifier of the physical POS store (e.g., 'STORE_AHD_001').*
- **`date`** (nvarchar(30), NULL) - 24 distinct values
  - *Date of the summary (stored as nvarchar, format appears 'YYYY-MM-DD').*
- **`total_txns`** (nvarchar(16), NULL) - 46 distinct values
  - *Total number of transactions recorded for the store on the date (stored as nvarchar).*
- **`total_sales`** (nvarchar(28), NULL) - 50 distinct values
  - *Sum of sales (currency) for the store on the date; stored as nvarchar and contains decimal values.*
- **`total_tax`** (nvarchar(24), NULL) - 50 distinct values
  - *Total tax collected on the day's sales for the store (stored as nvarchar decimals).*
- **`total_refunds`** (nvarchar(24), NULL) - 50 distinct values
  - *Total monetary value of refunds issued that day for the store (stored as nvarchar decimals).*
- **`avg_txn_value`** (nvarchar(24), NULL) - 50 distinct values
  - *Average transaction value for the day (stored as nvarchar decimal). May be precomputed as total_sales / total_txns or calculated externally.*
- **`created_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the summary row was created (stored as nvarchar, appears 'YYYY-MM-DD HH:MM:SS').*
- **`notes`** (nvarchar(36), NULL) - 1 distinct values
  - *Free-text note about the row; currently constant 'Daily summary'.*

---

### pos_inventory_adjustments

**Rows:** 50  
**Columns:** 11  
**Primary Keys:** *None*  

**Purpose:** Records individual point-of-sale inventory adjustments (manual corrections, shrinkage, damage) at store + SKU level. Serves as an audit trail for inventory changes and a source for analysis of inventory accuracy, reasons for adjustments, and operator behavior.

**Business Questions:**

- Which SKUs and stores contribute most to inventory shrinkage (sum of negative qty_change grouped by SKU/store)?
- Which users make the most adjustments and which users approve the most adjustments (counts and avg qty_change)?
- Are there adjustments where inventory_after does not equal inventory_before + qty_change (potential data quality or process issues)?
- What are the top reasons for adjustments and how much quantity is attributed to each reason over a period?
- How do adjustment volumes and magnitudes evolve over time (daily/weekly trends) for specific stores or SKUs?

**Key Columns:**

- **`adjustment_id`** (nvarchar(24), NULL) - 50 distinct values
  - *Unique identifier for the inventory adjustment record (text).*
- **`pos_sku`** (nvarchar(30), NULL) - 10 distinct values
  - *SKU identifier used by POS for the product affected by the adjustment.*
- **`store_id`** (nvarchar(36), NULL) - 4 distinct values
  - *Identifier of the store where the adjustment occurred.*
- **`adjustment_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the adjustment was performed (stored as nvarchar).*
- **`qty_change`** (nvarchar(16), NULL) - 19 distinct values
  - *Quantity change applied by the adjustment (signed integer stored as text). Negative values indicate decreases (e.g., shrinkage), positive values indicate additions.*
- **`reason`** (nvarchar(54), NULL) - 3 distinct values
  - *Categorical reason for the adjustment (e.g., Shrinkage, Stock Count Correction, Damage).*
- **`adjusted_by`** (nvarchar(22), NULL) - 3 distinct values
  - *Identifier of the user/operator who made the adjustment (text user id).*
- **`approval_by`** (nvarchar(22), NULL) - 3 distinct values
  - *Identifier of the approver of the adjustment (text user id).*
- **`inventory_before`** (nvarchar(16), NULL) - 48 distinct values
  - *Inventory count recorded before the adjustment (stored as text, integer-like).*
- **`inventory_after`** (nvarchar(16), NULL) - 50 distinct values
  - *Inventory count after the adjustment (stored as text, integer-like).*
- *(... and 1 more columns)*

---

### pos_loyalty_redemptions

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Records individual point-redemption events at point-of-sale: which customer redeemed loyalty points, which POS transaction they applied it to, how many points were used, the monetary discount granted, when and where the redemption occurred, who created the record and the approval reference. Serves as the ledger of loyalty redemptions for POS analytics, audits and reconciliation with POS transactions and customer profiles.

**Business Questions:**

- How much discount (total and average) has been given through loyalty redemptions over a period?
- Which customers redeem loyalty points most frequently and which generate the largest total discount?
- How many redemptions and what value of discounts occur per store or per creator (staff member)?
- What is the time distribution of redemptions (hourly/daily/monthly trends)?
- Are there anomalous redemptions (very high discount_amount or loyalty_points_used) that require investigation?

**Key Columns:**

- **`redemption_id`** (nvarchar(22), NULL) - 50 distinct values
  - *Unique identifier for a loyalty redemption event (string).*
- **`customer_id`** (nvarchar(26), NULL) - 39 distinct values
  - *Identifier of the customer who redeemed loyalty points (string, references customer master).*
- **`pos_txn_id`** (nvarchar(28), NULL) - 40 distinct values
  - *POS transaction identifier associated with the redemption (string).*
- **`loyalty_points_used`** (nvarchar(16), NULL) - 49 distinct values
  - *Number of loyalty points consumed in the redemption (stored as nvarchar, numeric content).*
- **`discount_amount`** (nvarchar(22), NULL) - 50 distinct values
  - *Monetary value of discount applied for the redemption (stored as nvarchar containing decimal values).*
- **`redeemed_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the redemption occurred (stored as nvarchar, sample format 'YYYY-MM-DD HH:MM:SS').*
- **`store_id`** (nvarchar(36), NULL) - 4 distinct values
  - *Identifier of the store where redemption happened (string, low cardinality).*
- **`created_by`** (nvarchar(22), NULL) - 3 distinct values
  - *Identifier of the user/terminal that created the redemption record (string, low cardinality).*
- **`approval_id`** (nvarchar(22), NULL) - 49 distinct values
  - *Reference identifier for approval/authorization tied to the redemption (string, near-unique).*
- **`notes`** (nvarchar(46), NULL) - 1 distinct values
  - *Free-text notes for the redemption; in sample data this appears constant ('Loyalty redemption').*

---

### pos_product_wise_sales

**Rows:** 21,930  
**Columns:** 7  
**Primary Keys:** *None*  

**Purpose:** Pos-level product-wise daily sales snapshot. Each row records sales metrics (quantity, gross, discount, tax, net) for a product on a date. It appears to be an ingest/raw staging table holding point-of-sale aggregated metrics before normalization or joining to masters.

**Business Questions:**

- What is the daily net sales and quantity sold per product over a given date range?
- Which products contribute most to gross sales, net sales, or volume in a period?
- How much discount and tax are being applied per product and how do they change over time?
- What are weekly/monthly trends in quantity (kg) and revenue for each product?
- Are there discrepancies between gross, discounts, tax and net (data quality check) for given dates/products?

**Key Columns:**

- **`date`** (nvarchar(30), NULL) - 731 distinct values ⚠️ HIGH CARDINALITY
  - *The calendar date for which the product-level sales metrics are reported. Stored as nvarchar but values appear in YYYY-MM-DD format.*
- **`product_id`** (nvarchar(22), NULL) - 10 distinct values
  - *Identifier for the product sold (text). Appears to be a product SKU/code (e.g., ONI003).*
- **`total_qty_kg`** (nvarchar(46), NULL) - 21,930 distinct values ⚠️ HIGH CARDINALITY
  - *Total quantity sold in kilograms for the product on the date. Stored as nvarchar; values represent weight in kg.*
- **`gross_sales`** (nvarchar(46), NULL) - 21,930 distinct values ⚠️ HIGH CARDINALITY
  - *Total gross sales amount (before discounts/taxes) for the product on the date. Stored as nvarchar string representing monetary value.*
- **`discount_amount`** (nvarchar(46), NULL) - 21,930 distinct values ⚠️ HIGH CARDINALITY
  - *Total discount given on gross sales for the product on the date. Stored as text but represents monetary value.*
- **`tax_amount`** (nvarchar(46), NULL) - 21,930 distinct values ⚠️ HIGH CARDINALITY
  - *Total tax applied to sales for the product on the date. Stored as nvarchar string representing tax amount.*
- **`net_sales`** (nvarchar(46), NULL) - 21,930 distinct values ⚠️ HIGH CARDINALITY
  - *Net sales amount after discounts and taxes for the product on the date. Stored as nvarchar string representing monetary value.*

---

### pos_products

**Rows:** 13  
**Columns:** 15  
**Primary Keys:** *None*  

**Purpose:** Catalog of point-of-sale products for a specific store ingestion (raw POS product snapshot). It contains SKU identifiers, PLU codes, display name, unit-of-measure, POS price, tax and stock metrics and a last-updated timestamp. Likely used as the canonical POS product feed for POS reporting, inventory checks and price lookups.

**Business Questions:**

- What items are currently below their reorder point and need restocking?
- What is the current POS price list for the store and how many items are in each UoM?
- When was each product last updated in the POS feed?
- How many active products are listed in this POS snapshot and which ones have null or missing fields?
- What is the on-hand stock quantity per SKU (for inventory check) and which SKUs are low?

**Key Columns:**

- **`pos_sku`** (nvarchar(30), NULL) - 10 distinct values
  - *POS-specific SKU identifier (store-level product key used in the point-of-sale).*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Canonical SKU (likely product-level identifier without store suffix).*
- **`store_id`** (nvarchar(36), NULL) - 1 distinct values
  - *Identifier of the store this POS snapshot belongs to.*
- **`plucode`** (nvarchar(22), NULL) - 10 distinct values
  - *Price Look-Up code (PLU) used for certain product types (often produce), represented here as text (appears with .0 suffix).*
- **`name`** (nvarchar(54), NULL) - 10 distinct values
  - *Display name of the product as shown on POS (human-readable product title).*
- **`uom`** (nvarchar(18), NULL) - 3 distinct values
  - *Unit of measure for the SKU (e.g., 'kg', '250g', '500g').*
- **`pos_price`** (nvarchar(20), NULL) - 10 distinct values
  - *Price of the product in POS (as captured in the feed) stored as text (e.g., '185.0').*
- **`tax_rate`** (nvarchar(18), NULL) - 1 distinct values
  - *Tax rate applicable to the product as text (appears constant as '5.0000000000000003').*
- **`stock_qty`** (nvarchar(20), NULL) - 10 distinct values
  - *On-hand stock quantity for the SKU in POS (stored as text, e.g., '186.0').*
- **`reorder_point`** (nvarchar(18), NULL) - 9 distinct values
  - *Configured threshold quantity at which the product should be reordered (text).*
- *(... and 5 more columns)*

---

### pos_products_sales

**Rows:** 10  
**Columns:** 5  
**Primary Keys:** *None*  

**Purpose:** Raw point-of-sale (POS) product-level sales snapshot. Each row records sales-related dollar amounts for a product SKU. This table appears to be an ingestion or staging table (zuna_seed_raw) holding per-SKU financial metrics (gross, discounts, tax, net) likely exported from POS or ETL pipeline before normalization.

**Business Questions:**

- What is the total gross sales, total discounts, total tax, and total net sales for each SKU?
- Which SKUs have the highest gross sales and which have the highest discount amount?
- What is the effective discount or tax rate by SKU (discount/gross, tax/gross) in the provided snapshot?
- Are there any SKUs where net sales exceed gross sales (indicating data quality issues)?
- How do per-SKU gross, discount, tax, and net sales rank (top-N) across the dataset?

**Key Columns:**

- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product identifier (SKU) from POS/system. nvarchar(22) in raw snapshot; values like 'APP009', 'BRN007'.*
- **`Gross Sales`** (nvarchar(30), NULL) - 10 distinct values
  - *Total gross sales amount for the SKU (raw nvarchar). Represents pre-discount, pre-tax sales value in currency but stored as text.*
- **`Discount Amount`** (nvarchar(28), NULL) - 10 distinct values
  - *Total discount amount applied to the SKU (raw nvarchar). Monetary value stored as text.*
- **`Tax Amount`** (nvarchar(28), NULL) - 10 distinct values
  - *Tax charged on the SKU (raw nvarchar). Monetary tax value stored as text.*
- **`Net Sales`** (nvarchar(30), NULL) - 10 distinct values
  - *Net sales amount after discounts and tax adjustments for the SKU (raw nvarchar). Expected to represent Gross - Discount +/− Tax depending on reporting convention; stored as text.*

---

### pos_returns

**Rows:** 50  
**Columns:** 11  
**Primary Keys:** *None*  

**Purpose:** Records of point-of-sale return events: one row per returned SKU line capturing which POS transaction it came from, when the return occurred and was recorded, quantity, reason, refund amount, who processed it and simple flags (approval required, restock). Used to analyze return volume, refund cost and operational handling of returns at POS.

**Business Questions:**

- What is the total number of returns and total refund amount over a date range?
- Which SKUs generate the most return refunds and quantities?
- What are the most common return reasons and their share of total refunds?
- Which POS users/processors handle the most returns and what are their average refund amounts?
- What percentage of returns required approval or were restocked, and how has that changed over time?

**Key Columns:**

- **`pos_return_id`** (nvarchar(22), NULL) - 50 distinct values
  - *Unique identifier for the return line (POS return event id).*
- **`pos_txn_id`** (nvarchar(28), NULL) - 34 distinct values
  - *Identifier of the POS transaction the return belongs to (original sale transaction id).*
- **`return_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when the return occurred (string formatted timestamp).*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product SKU for the returned item.*
- **`qty`** (nvarchar(12), NULL) - 5 distinct values
  - *Quantity of the SKU returned on this return line (stored as string).*
- **`reason`** (nvarchar(40), NULL) - 3 distinct values
  - *Categorical reason for the return (e.g., Wrong Item, Customer Return, Damaged).*
- **`refund_amount`** (nvarchar(22), NULL) - 50 distinct values
  - *Monetary refund issued for the return line (stored as string/float-like text).*
- **`processed_by`** (nvarchar(22), NULL) - 3 distinct values
  - *Identifier of the POS user/operator who processed the return.*
- **`approval_required_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *Binary flag (string '0'/'1') indicating whether this return required managerial/approval workflow.*
- **`restock_flag`** (nvarchar(20), NULL) - 2 distinct values
  - *Binary flag (string '0'/'1') indicating whether the returned item was restocked into inventory.*
- *(... and 1 more columns)*

---

### pos_sales_daily

**Rows:** 2,193  
**Columns:** 13  
**Primary Keys:** *None*  

**Purpose:** Daily point-of-sale (POS) sales metrics at the store level. Each row appears to represent aggregated daily metrics for a specific store (bills, quantity in kg, sales, discounts, tax, net sales) as ingested from a raw source.

**Business Questions:**

- How have net sales trended day-over-day or month-over-month for each store?
- Which store has the highest average ticket (gross or net) and how does that change over time?
- What is the total gross, discount and tax per period (day/week/month) and discount as a percentage of gross?
- How many bills and total quantity (kg) are sold per store per period (capacity / throughput metrics)?
- Are there anomalies (days with unusually high discounts, tax, or sales per kg) that require investigation?

**Key Columns:**

- **`date`** (nvarchar(30), NULL) - 731 distinct values ⚠️ HIGH CARDINALITY
  - *Reported calendar date for the aggregated daily metrics. Stored as nvarchar(30) but contents follow YYYY-MM-DD (max length 10).*
- **`store_id`** (nvarchar(36), NULL) - 3 distinct values
  - *Identifier for the POS store (e.g. STORE_AHD_001). Low cardinality (3 stores in dataset).*
- **`total_bills`** (nvarchar(16), NULL) - 111 distinct values
  - *Count of bills/transactions for the store on that date. Stored as nvarchar but values represent small integers (max length 3).*
- **`total_qty_kg`** (nvarchar(22), NULL) - 2,130 distinct values ⚠️ HIGH CARDINALITY
  - *Total quantity sold in kilograms for the store on that date. Stored as nvarchar; high-cardinality decimals present.*
- **`gross_sales`** (nvarchar(26), NULL) - 2,192 distinct values ⚠️ HIGH CARDINALITY
  - *Gross sales amount (before discounts/tax?) for the day and store; stored as nvarchar with many distinct decimal values.*
- **`discount_amount`** (nvarchar(24), NULL) - 2,159 distinct values ⚠️ HIGH CARDINALITY
  - *Total discount amount applied for the store on that date. Stored as nvarchar; high-cardinality decimals.*
- **`tax_amount`** (nvarchar(24), NULL) - 2,157 distinct values ⚠️ HIGH CARDINALITY
  - *Total tax collected for the store on that date. Stored as nvarchar with decimal-like values.*
- **`net_sales`** (nvarchar(46), NULL) - 2,192 distinct values ⚠️ HIGH CARDINALITY
  - *Net sales amount for the day and store (presumably gross - discounts + tax or another definition). Stored as nvarchar and high-cardinality decimals.*
- **`created_at`** (nvarchar(48), NULL) - 1 distinct values
  - *Ingestion timestamp for the row. Stored as nvarchar(48) and appears constant (single distinct value present).*
- **`Unnamed: 9`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Completely empty column (100% null). Likely an artifact from source CSV/ingestion.*
- *(... and 3 more columns)*

---

### pos_sales_monthly

**Rows:** 36  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Monthly Point-of-Sale (POS) sales aggregates per store. This table stores one row per store per month summarizing bills, quantities, gross/discount/tax/net amounts and an ingestion timestamp. It is intended as an analytical summary layer for monthly reporting and comparisons.

**Business Questions:**

- How do gross, discount, tax and net sales trend across months for each store in 2024?
- Which store has the highest average bill (net_sales / total_bills) in a given month or across the year?
- What is the monthly total quantity sold (kg) and how does it correlate with net sales per store?
- How much of gross sales is given away as discounts and how does discount percent vary month-to-month?
- Which months show the largest month-over-month net sales growth or decline for each store?

**Key Columns:**

- **`year`** (nvarchar(18), NULL) - 1 distinct values
  - *Reporting year for the monthly aggregate (stored as nvarchar). In this dataset all values are '2024'.*
- **`month`** (nvarchar(14), NULL) - 12 distinct values
  - *Reporting month as a string (1-12). Represents the month of the aggregate row.*
- **`store_id`** (nvarchar(34), NULL) - 3 distinct values
  - *Identifier for the store where sales occurred (e.g., STORE_AHD_01).*
- **`total_bills`** (nvarchar(18), NULL) - 34 distinct values
  - *Total number of bills (transactions) in that store-month (stored as nvarchar integer-like).*
- **`total_qty_kg`** (nvarchar(26), NULL) - 36 distinct values
  - *Total quantity sold in kilograms for the store-month (stored as nvarchar, decimal-like).*
- **`gross_sales`** (nvarchar(28), NULL) - 36 distinct values
  - *Total gross sales amount (before discounts/taxes) for the store-month (stored as nvarchar decimal-like string).*
- **`discount_amount`** (nvarchar(26), NULL) - 36 distinct values
  - *Total discounts applied for the store-month (stored as nvarchar decimal-like).*
- **`tax_amount`** (nvarchar(26), NULL) - 36 distinct values
  - *Total tax collected for the store-month (stored as nvarchar decimal-like).*
- **`net_sales`** (nvarchar(28), NULL) - 36 distinct values
  - *Net sales amount for the store-month (after discounts and taxes or as defined by the business) stored as nvarchar decimal-like.*
- **`created_at`** (nvarchar(48), NULL) - 1 distinct values
  - *Ingestion or snapshot timestamp (stored as nvarchar). In this dataset the value is constant across rows.*

---

### pos_sales_yearly

**Rows:** 3  
**Columns:** 9  
**Primary Keys:** *None*  

**Purpose:** Annual aggregated POS sales metrics per store. This table holds yearly rollups (billed transactions, quantities, gross/discount/tax/net values) for physical stores and is intended for reporting and high-level trend analysis.

**Business Questions:**

- Which stores had the highest net sales for the year?
- What is the average bill value per store for the year?
- Which store had the largest total quantity sold (kg) this year?
- What is the overall discount rate and tax rate across stores for the year?
- Are these yearly rollups consistent with monthly/daily POS rollups (reconciliation)?

**Key Columns:**

- **`year`** (nvarchar(18), NULL) - 1 distinct values
  - *Calendar year for the aggregated metrics (stored as nvarchar). Represents the year these rollups belong to (e.g., '2024').*
- **`store_id`** (nvarchar(34), NULL) - 3 distinct values
  - *Identifier for the physical store where sales were made (string like 'STORE_AHD_01').*
- **`total_bills`** (nvarchar(20), NULL) - 3 distinct values
  - *Total number of bills/transactions for the store during the year, stored as nvarchar (integer-like).*
- **`total_qty_kg`** (nvarchar(28), NULL) - 3 distinct values
  - *Total quantity sold in kilograms for the store during the year (numeric-like string, may contain decimals).*
- **`gross_sales`** (nvarchar(30), NULL) - 3 distinct values
  - *Gross sales amount (pre-discount, pre-tax) for the store for the year, stored as a numeric string with decimals.*
- **`discount_amount`** (nvarchar(28), NULL) - 3 distinct values
  - *Total discount amount applied to sales for the store during the year (string containing decimal).*
- **`tax_amount`** (nvarchar(28), NULL) - 3 distinct values
  - *Total tax collected/applied for the store during the year (string with decimal).*
- **`net_sales`** (nvarchar(30), NULL) - 3 distinct values
  - *Net sales amount after discounts and tax adjustments for the store for the year (string numeric).*
- **`created_at`** (nvarchar(48), NULL) - 1 distinct values
  - *Ingestion or record creation timestamp for the row (stored as nvarchar). In sample data it appears constant and likely represents when the rollup was generated.*

---

### pos_shift_closures

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** POS shift closure records: one row per closed shift capturing terminal, user (cashier), start/end timestamps, monetary totals (sales, cash/card), refunds and cash reconciliation. Used for end-of-shift reconciliation, cashier performance and terminal utilization reporting.

**Business Questions:**

- Which cashier (user_id) generated the highest total sales over a period of time?
- Which terminal has the most frequent cash-count discrepancies (expected_cash != counted_cash)?
- What is the average shift duration per terminal and per user?
- How much cash and card were collected across all shifts in a given date range?
- Which shifts had refunds above a set threshold and who operated them?

**Key Columns:**

- **`shift_id`** (nvarchar(34), NULL) - 50 distinct values
  - *Unique identifier for a closed shift (string).*
- **`terminal_id`** (nvarchar(30), NULL) - 4 distinct values
  - *Identifier for the POS terminal where the shift ran (string).*
- **`user_id`** (nvarchar(22), NULL) - 3 distinct values
  - *Identifier of the user/cashier who closed the shift (string).*
- **`shift_start_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Shift start timestamp recorded as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*
- **`shift_end_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Shift end timestamp recorded as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*
- **`total_sales`** (nvarchar(26), NULL) - 50 distinct values
  - *Total sales amount for the shift stored as a numeric value in nvarchar.*
- **`cash_collected`** (nvarchar(26), NULL) - 50 distinct values
  - *Amount of cash collected during the shift stored as nvarchar.*
- **`card_collected`** (nvarchar(26), NULL) - 50 distinct values
  - *Amount collected by card for the shift (string).*
- **`refunds_amt`** (nvarchar(22), NULL) - 50 distinct values
  - *Total refunds processed during the shift stored as a string numeric.*
- **`expected_cash`** (nvarchar(26), NULL) - 50 distinct values
  - *System-calculated expected cash amount at shift close (string).*
- *(... and 2 more columns)*

---

### pos_stores

**Rows:** 4  
**Columns:** 5  
**Primary Keys:** *None*  

**Purpose:** A master/reference table of point-of-sale (POS) store locations and their last / first connectivity timestamps. It is used to identify stores by store_id and provide basic geographic (city/region) and operational (first_active_date, last_online) metadata for POS-related analyses.

**Business Questions:**

- Which stores are currently online or were last online within a given interval (e.g., last 7 days)?
- How many stores exist per city or region and which stores belong to each city/region?
- Which stores were activated within a given date range (first_active_date) and what's their tenure?
- Which stores have not been online recently (stale offline stores) to target support or check hardware?)
- Are there inconsistent or missing geographic entries (city vs region mismatches) that need cleaning?

**Key Columns:**

- **`store_id`** (nvarchar(36), NULL) - 4 distinct values
  - *A textual identifier for each POS store (e.g., 'STORE_AHD_001'). Intended to be the canonical key for a store.*
- **`city`** (nvarchar(28), NULL) - 4 distinct values
  - *City where the store is located (human-readable name like 'Ahmedabad').*
- **`region`** (nvarchar(28), NULL) - 4 distinct values
  - *Higher-level geographic label (region) for the store. In the sample data region values match city values, but region can represent broader area or division.*
- **`first_active_date`** (nvarchar(48), NULL) - 4 distinct values
  - *Timestamp when the store first became active/registered. Currently stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*
- **`last_online`** (nvarchar(48), NULL) - 4 distinct values
  - *Timestamp when the store last connected or was observed online. Stored as nvarchar in 'YYYY-MM-DD HH:MM:SS' format.*

---

### pos_sync_log

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Log of Point-of-Sale (POS) synchronization attempts from terminals to a central system. Each row records a sync event (attempt) including timestamps, counts of records exchanged, status, errors and retry attempts. Used to monitor reliability and throughput of POS syncs and to troubleshoot failed syncs.

**Business Questions:**

- What is the overall sync success rate and how does it change over time?
- Which terminals have the highest failure rate or highest average retry_count?
- What are the common error messages and how many syncs are impacted by each?
- How many records are being sent/received per terminal per day and are there trends or anomalies?
- When was the last successful sync per terminal and which terminals are overdue for a successful sync?

**Key Columns:**

- **`sync_id`** (nvarchar(26), NULL) - 50 distinct values
  - *Identifier for the sync attempt or batch. Appears unique per row in sample (50 distinct).*
- **`terminal_id`** (nvarchar(30), NULL) - 4 distinct values
  - *Identifier of the POS terminal that initiated the sync (e.g., 'TERM-001-2'). Low cardinality with skew toward a primary terminal.*
- **`sync_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp of the sync event (ISO-like string). Represents when the sync occurred or was reported from the terminal.*
- **`sync_status`** (nvarchar(24), NULL) - 2 distinct values
  - *Outcome of the sync attempt (e.g., SUCCESS or FAILED). Low cardinality (2 values in sample).*
- **`records_sent`** (nvarchar(16), NULL) - 41 distinct values
  - *Number of records the terminal reported it sent to the central system for this sync (stored as string).*
- **`records_received`** (nvarchar(16), NULL) - 43 distinct values
  - *Number of records the central system acknowledged or returned to the terminal (stored as string).*
- **`error_message`** (nvarchar(36), NULL) - 1 distinct values ⚠️ 58.0% NULL
  - *Text describing the failure reason when sync_status is FAILED. Largely NULL in sample; single non-null value 'Network error'.*
- **`retry_count`** (nvarchar(12), NULL) - 4 distinct values
  - *Number of retry attempts for this sync (stored as string). Low cardinality values (0-3) in sample.*
- **`last_success_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp of the last successful sync for the terminal or for this sync context (ISO-like string). Useful to know the last healthy state.*
- **`created_at`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp when this log row was created in the database or ingestion time (ISO-like string).*

---

### pos_terminals

**Rows:** 8  
**Columns:** 11  
**Primary Keys:** *None*  

**Purpose:** Inventory of point-of-sale (POS) terminals: identity, location, assignment, software/version and recent connectivity metadata. It is a device registry used to manage terminals across stores and to relate terminals to transactions, shifts and operational users.

**Business Questions:**

- How many terminals are deployed per store and what are their identifiers?
- Which terminals have not checked in within a given time window (potentially offline)?
- Which software versions are running on terminals and which stores still need upgrades?
- What are the geolocations of our terminals (for mapping/region coverage)?
- Which user (operator) is assigned to each terminal and when was each terminal provisioned?

**Key Columns:**

- **`terminal_id`** (nvarchar(30), NULL) - 4 distinct values
  - *Logical identifier for the POS terminal (tenant-specific id like TERM-001-2).*
- **`store_id`** (nvarchar(36), NULL) - 4 distinct values
  - *Identifier of the store where the terminal is located (e.g., STORE_AHD_001).*
- **`terminal_code`** (nvarchar(32), NULL) - 8 distinct values
  - *Human-friendly code for the terminal within a store (e.g., STORE_AH-T1).*
- **`device_serial`** (nvarchar(26), NULL) - 8 distinct values
  - *Hardware serial number of terminal device (vendor-provided SN).*
- **`pos_software_version`** (nvarchar(22), NULL) - 1 distinct values
  - *POS application version installed on the terminal (text).*
- **`assigned_user_id`** (nvarchar(22), NULL) - 3 distinct values
  - *Identifier of the user/operator assigned to the terminal (e.g., PU1001).*
- **`last_online_ts`** (nvarchar(48), NULL) - 8 distinct values
  - *Timestamp (as string) when the terminal last checked in or was seen online (format: 'YYYY-MM-DD HH:MI:SS').*
- **`status`** (nvarchar(22), NULL) - 1 distinct values
  - *Operational status of the terminal (e.g., ACTIVE, INACTIVE).*
- **`location_lat`** (nvarchar(28), NULL) - 8 distinct values
  - *Latitude of terminal location stored as text (decimal string).*
- **`location_long`** (nvarchar(28), NULL) - 8 distinct values
  - *Longitude of terminal location stored as text (decimal string).*
- *(... and 1 more columns)*

---

### pos_transaction_lines

**Rows:** 125  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Represents individual POS transaction lines (items) sold in point-of-sale transactions. Each row is one line item on a POS receipt containing SKU, quantity, pricing, tax, batch and creation timestamp. It is a detailed sales activity table used to compute revenue, tax, SKU-level sales and inventory/batch traceability.

**Business Questions:**

- Which SKUs generated the most revenue and units sold in this dataset?
- What is total revenue and tax collected for the recorded POS lines over a given time range?
- Which batches were sold and how many units per batch (batch traceability)?
- What is the average unit price and average line_total per SKU?
- How many line items are associated with each POS transaction (lines per receipt)?

**Key Columns:**

- **`pos_line_id`** (nvarchar(18), NULL) - 125 distinct values
  - *Identifier for the POS transaction line; appears unique per row and represents the line-level id on a receipt.*
- **`pos_txn_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Identifier of the parent POS transaction/receipt containing this line. Multiple lines map to the same transaction.*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Stock keeping unit code for the product sold on this line. Low cardinality with a few SKUs dominating.*
- **`qty`** (nvarchar(14), NULL) - 10 distinct values
  - *Quantity sold on the line. Stored as nvarchar but appears integer-like (small ints).*
- **`unit_price`** (nvarchar(16), NULL) - 10 distinct values
  - *Unit price applied for the line. Stored as string but numeric-like (several repeated values).*
- **`line_total`** (nvarchar(18), NULL) - 54 distinct values
  - *Total amount for the line (qty * unit_price minus discounts plus taxes if included). Stored as a string; many distinct values.*
- **`discount_amt`** (nvarchar(12), NULL) - 1 distinct values
  - *Discount amount applied on the line. In this dataset it is consistently '0' for all rows.*
- **`tax_amt`** (nvarchar(18), NULL) - 54 distinct values
  - *Tax amount applied to the line. Stored as string with decimal values and occasional floating-string artifacts (e.g., '4.7999999999999998').*
- **`variant_info`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Holds variant-level metadata about the product (e.g., size, color). In this dataset the column is 100% null.*
- **`expiry_date`** (nvarchar(16), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Expiry date associated with this line's product batch (if applicable). Currently 100% null in this dataset.*
- *(... and 2 more columns)*

---

### pos_transactions

**Rows:** 50  
**Columns:** 15  
**Primary Keys:** *None*  

**Purpose:** Point-of-sale transactions raw table capturing individual POS sales events and their basic financial and operational attributes. It serves as the canonical ingest of POS transaction headers for downstream reporting, reconciliation, and joins to line-level sales, terminals, users and shift metadata.

**Business Questions:**

- What is the total and average transaction value by day/week/month?
- How much sales (sum txn_total) did each terminal or POS user generate in a time range?
- What is the distribution of payment modes (CASH/UPI/CARD) and associated totals?
- How much tax was collected by day and by payment_mode?
- How many transactions were completed/failed and what is the sync status to downstream systems?

**Key Columns:**

- **`pos_txn_id`** (nvarchar(28), NULL) - 50 distinct values
  - *Unique identifier for the POS transaction (transaction header ID).*
- **`terminal_id`** (nvarchar(30), NULL) - 4 distinct values
  - *Identifier of the POS terminal where the transaction was processed.*
- **`pos_user_id`** (nvarchar(22), NULL) - 3 distinct values
  - *Identifier of the POS operator/cashier who processed the transaction.*
- **`txn_ts`** (nvarchar(48), NULL) - 50 distinct values
  - *Timestamp of the transaction event (string in ISO-like format).*
- **`txn_type`** (nvarchar(18), NULL) - 1 distinct values
  - *Category of the transaction (e.g., SALE, REFUND).*
- **`txn_total`** (nvarchar(22), NULL) - 49 distinct values
  - *Total monetary amount for the transaction (stored as string, includes subtotal, taxes, discounts).*
- **`tax_total`** (nvarchar(44), NULL) - 49 distinct values
  - *Monetary tax amount charged for the transaction (stored as string).*
- **`discount_total`** (nvarchar(12), NULL) - 1 distinct values
  - *Total discount applied to the transaction (stored as string). In sample it's constant '0'.*
- **`payment_mode`** (nvarchar(18), NULL) - 3 distinct values
  - *Mode of payment used (e.g., CASH, UPI, CARD).*
- **`external_txn_ref`** (nvarchar(28), NULL) - 50 distinct values
  - *External payment or gateway reference associated with the transaction. Useful for reconciliation with external systems.*
- *(... and 5 more columns)*

---

### pos_users

**Rows:** 3  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** This table stores point-of-sale (POS) user / staff records (cashiers, supervisors) including identifiers, contact details, assigned store, status and basic activity timestamps. It is a reference/master table for POS user identities used by transaction and shift systems across the POS-related schema.

**Business Questions:**

- How many POS users exist by role and by store?
- Which POS users have not logged in in the last N days (identify inactive staff)?
- When were POS users added (new hires) over a chosen date range?
- Which users are active vs inactive and what is the headcount per store?
- What are contact details (phone/email) for POS users in a specific store or role?

**Key Columns:**

- **`pos_user_id`** (nvarchar(22), NULL) - 3 distinct values
  - *Unique identifier for the POS user (employee/staff) within the POS system.*
- **`name`** (nvarchar(34), NULL) - 3 distinct values
  - *Full human-readable name of the POS user.*
- **`role`** (nvarchar(30), NULL) - 2 distinct values
  - *User role or job function at the POS (e.g., Cashier, Supervisor).*
- **`phone`** (nvarchar(38), NULL) - 3 distinct values
  - *Contact phone number for the POS user, stored as a string (includes country code).*
- **`email`** (nvarchar(58), NULL) - 3 distinct values
  - *User's email address used for notifications and identity contact.*
- **`store_id`** (nvarchar(36), NULL) - 3 distinct values
  - *Identifier of the store the POS user is assigned to (likely links to pos_stores table).*
- **`active_flag`** (nvarchar(18), NULL) - 1 distinct values
  - *Flag indicating whether the user is active (sample uses '1'); stored as a string.*
- **`created_at`** (nvarchar(48), NULL) - 3 distinct values
  - *Datetime string when the POS user record was created (format YYYY-MM-DD HH:MM:SS in sample).*
- **`last_login`** (nvarchar(48), NULL) - 3 distinct values
  - *Datetime string of the user's most recent login to the POS system (format YYYY-MM-DD HH:MM:SS in sample).*
- **`pin_hash`** (nvarchar(138), NULL) - 3 distinct values
  - *Hashed representation of the user's PIN; sensitive credential data (hash).*

---

### pos_vendors

**Rows:** 40  
**Columns:** 9  
**Primary Keys:** *None*  

**Purpose:** Master/reference list of point-of-sale (POS) vendors used by the application. Stores vendor identifiers, contact details, location, tax identifier and business category. Intended to support lookups, reporting and joins against transactional tables (purchases, returns, vendor invoices) to attribute activity to vendors.

**Business Questions:**

- How many vendors are registered in each city?
- What is the distribution of vendors by business_type (e.g., Equipment Repair vs Hardware)?
- Which vendors do we have contact information for and which have missing phone/email?
- Which vendors are located in a given city (e.g., Gandhinagar) and what are their GST numbers?
- Are there potential duplicate vendors by name or GST number in the master list?

**Key Columns:**

- **`vendor_id`** (nvarchar(26), NULL) - 40 distinct values
  - *Alphanumeric identifier for the vendor (system-level vendor code).*
- **`vendor_name`** (nvarchar(82), NULL) - 40 distinct values
  - *Human-readable vendor name/business name.*
- **`phone`** (nvarchar(38), NULL) - 40 distinct values
  - *Vendor contact phone number, stored as text (includes country code/formatting).*
- **`email`** (nvarchar(96), NULL) - 40 distinct values
  - *Vendor contact email address.*
- **`address`** (nvarchar(102), NULL) - 40 distinct values
  - *Full mailing/street address for the vendor (one free-form text field).*
- **`city`** (nvarchar(32), NULL) - 9 distinct values
  - *City where the vendor is located (categorical, low cardinality).*
- **`gst_no`** (nvarchar(40), NULL) - 40 distinct values
  - *Vendor GST (tax) number, stored as text.*
- **`business_type`** (nvarchar(44), NULL) - 5 distinct values
  - *Categorical description of the vendor's business (e.g., Equipment Repair, Hardware).*
- **`created_at`** (nvarchar(48), NULL) - 1 distinct values
  - *Timestamp when the vendor record was created, stored as nvarchar rather than datetime. Observed to be identical for all rows in this snapshot.*

---

### product_inventory

**Rows:** 40  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Product-level inventory snapshot per centre. Contains inventory identifiers, product SKU, storage location (centre), quantities (units and kg), reserved and available balances, replenishment parameters (reorder point, lead time, safety stock), expiry timestamp and storage temperature. Supports inventory management, replenishment decisioning and expiry/temperature compliance checks.

**Business Questions:**

- Which SKUs at which centres are below their reorder point and need replenishment?
- What is the total available stock (kg and units) per SKU and per centre?
- Which inventory items will expire within X days (or are already expired)?
- How much of available stock is reserved vs free per SKU/centre?
- Are any items stored at incorrect temperatures or do certain centres have only cold-storage SKUs?

**Key Columns:**

- **`inventory_id`** (nvarchar(50), NULL) - 40 distinct values
  - *Unique identifier for an inventory record (combination of sku and centre/lot).*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product SKU code representing the product/variant.*
- **`centre_id`** (nvarchar(64), NULL) - 4 distinct values
  - *Human-readable name of the centre/warehouse/collection point holding the inventory.*
- **`qty_units`** (nvarchar(18), NULL) - 38 distinct values
  - *Quantity expressed in discrete units (stored as nvarchar).*
- **`qty_kg`** (nvarchar(18), NULL) - 40 distinct values
  - *Quantity expressed in kilograms (stored as nvarchar).*
- **`reserved_stock`** (nvarchar(16), NULL) - 38 distinct values
  - *Quantity reserved (units or kg depending on schema context) and not available for allocation (stored as nvarchar).*
- **`available_stock`** (nvarchar(18), NULL) - 40 distinct values
  - *Quantity immediately available for new allocations (stored as nvarchar).*
- **`reorder_point`** (nvarchar(14), NULL) - 33 distinct values
  - *Configured threshold below which a reorder should be triggered (stored as nvarchar).*
- **`lead_time_days`** (nvarchar(12), NULL) - 3 distinct values
  - *Supplier/fulfilment expected lead time in days (stored as nvarchar).*
- **`safety_stock_kg`** (nvarchar(14), NULL) - 31 distinct values
  - *Configured safety stock level (in kg), used to absorb demand/lead-time variability (stored as nvarchar).*
- *(... and 2 more columns)*

---

### product_pricing

**Rows:** 100  
**Columns:** 9  
**Primary Keys:** *None*  

**Purpose:** Holds time-ranged pricing records for products (by SKU). Each row defines a price_per_unit, minimum order quantity and validity window (start_ts - end_ts) for a SKU. It appears to be a raw / staging table capturing price versions rather than a normalized canonical price table.

**Business Questions:**

- What is the active price for a given SKU at a specific timestamp (e.g., now)?
- How has the unit price for SKU X changed over the last 6 months?
- Which SKUs have overlapping price validity windows or gaps in pricing?
- What is the distribution of minimum order quantities by SKU and how does min_order_qty correlate with price tiers?
- How many price updates were made by the pricing team in a given period (using created_at)?

**Key Columns:**

- **`price_id`** (nvarchar(34), NULL) - 100 distinct values
  - *Unique identifier for the pricing record / price version. Appears to be distinct per row (e.g., 'PR-APP009-1').*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product stock keeping unit — the key used to associate a price record with a product.*
- **`start_ts`** (nvarchar(48), NULL) - 100 distinct values
  - *Start of the validity window for the price record. Stored as nvarchar but contains timestamp-like values (YYYY-MM-DD HH:MM:SS).*
- **`end_ts`** (nvarchar(48), NULL) - 100 distinct values
  - *End of the validity window for the price record. Stored as nvarchar but contains timestamp-like values.*
- **`price_per_unit`** (nvarchar(22), NULL) - 100 distinct values
  - *Unit price for the record. Stored as nvarchar but contains decimal numeric values (e.g., '156.65').*
- **`currency`** (nvarchar(16), NULL) - 1 distinct values
  - *Currency code for the price value (ISO code like 'INR'). Here it's constant (INR).*
- **`min_order_qty`** (nvarchar(14), NULL) - 3 distinct values
  - *Minimum order quantity required for this price record (stored as string but small integer-like values: 1,5,10).*
- **`created_by`** (nvarchar(36), NULL) - 1 distinct values
  - *Identifier of the user/system that created the pricing record (here 'pricing_admin' for all rows).*
- **`created_at`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the price record was created (stored as nvarchar but contains timestamp-like strings).*

---

### product_sales

**Rows:** 10  
**Columns:** 6  
**Primary Keys:** *None*  

**Purpose:** This table appears to be a raw, product-level sales snapshot keyed by SKU. It contains monetary metrics (gross sales, discounts, delivery fees, tax and net sales) for products. It is likely a staging or seed/raw import used for downstream reporting, validation, or ETL into canonical product-sales tables.

**Business Questions:**

- Which SKUs generated the highest gross sales in the sample?
- What is the discount amount and discount percentage by SKU (Discount / Gross Sales)?
- How much of total charges come from delivery fees and tax per SKU?
- Does Net Sales match the expected computed value (e.g., Gross - Discount +/- Delivery Fee +/- Tax)?
- Which SKUs have inconsistent or unparsable numeric fields that need data cleaning?

**Key Columns:**

- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product stock-keeping unit identifier. nvarchar(22) with actual max length 6 in this sample; 10 distinct values in 10 rows.*
- **`Gross Sales`** (nvarchar(30), NULL) - 10 distinct values
  - *Reported gross sales amount for the SKU, stored as text (nvarchar). Values have decimals and large magnitudes.*
- **`Discount`** (nvarchar(28), NULL) - 10 distinct values
  - *Total discount applied to the SKU, stored as text (nvarchar). Contains decimal values.*
- **`Delivery Fee`** (nvarchar(28), NULL) - 10 distinct values
  - *Delivery fee amount attributed to the SKU, stored as text (nvarchar).*
- **`Tax`** (nvarchar(28), NULL) - 10 distinct values
  - *Tax amount applied to the SKU, stored as text (nvarchar).*
- **`Net Sales`** (nvarchar(30), NULL) - 10 distinct values
  - *Reported net sales amount for the SKU, stored as text (nvarchar). Expected to be a derivation of the other monetary fields but exact formula is not documented here.*

---

### product_variants

**Rows:** 20  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Holds product variant level master data for SKUs (different pack sizes / loose vs packed) including identifiers, unit/weight metadata, barcodes and pricing. Serves as the canonical lookup for variant attributes used by inventory, pricing and sales tables in the schema.

**Business Questions:**

- What variants exist for a given SKU and what are their pack sizes and weights?
- What is the retail vs wholesale price for each product variant and what is the price spread?
- How many active variants use each unit-of-measure (uom) and what pack sizes are most common?
- Which variants are missing barcodes or have inconsistent weight/pricing data?
- Which variants were added in a given time period (based on created_at)?

**Key Columns:**

- **`variant_id`** (nvarchar(24), NULL) - 20 distinct values
  - *Unique identifier for the variant (string). Appears to uniquely identify each row in sample.*
- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Product-level SKU that groups multiple variants (short product code).*
- **`variant_name`** (nvarchar(32), NULL) - 2 distinct values
  - *Human-readable variant label (e.g., 'Loose', 'Packed 500g'). Low cardinality in sample.*
- **`variant_sku`** (nvarchar(44), NULL) - 20 distinct values
  - *Compound SKU including product SKU and variant descriptor (e.g., APP009-LOOSE). Unique per variant.*
- **`uom`** (nvarchar(18), NULL) - 3 distinct values
  - *Unit of measure for the variant (e.g., 'kg', '250g', '500g').*
- **`units_per_pack`** (nvarchar(16), NULL) - 2 distinct values
  - *Number of units per pack (string representation of numeric, e.g., '0.5', '1.0').*
- **`weight_kg`** (nvarchar(16), NULL) - 2 distinct values
  - *Weight of the variant in kilograms (stored as string, e.g., '0.5', '1.0').*
- **`barcode`** (nvarchar(30), NULL) - 20 distinct values
  - *Machine-readable barcode assigned to the variant (string).*
- **`price_retail`** (nvarchar(20), NULL) - 20 distinct values
  - *Retail price for the variant stored as nvarchar (contains numeric-like strings with floating artifacts).*
- **`price_wholesale`** (nvarchar(20), NULL) - 10 distinct values
  - *Wholesale price for the variant (nvarchar storing numeric-like values).*
- *(... and 2 more columns)*

---

### products

**Rows:** 10  
**Columns:** 16  
**Primary Keys:** *None*  

**Purpose:** Product master / catalog feed containing SKU-level product attributes used to describe items sold across channels. It appears to be a raw ingestion table (zuna_seed_raw) that provides descriptive metadata (names, weights, categorization, storage and shelf-life) which downstream systems (pricing, inventory, sales) can join to.

**Business Questions:**

- Which SKUs are perishable and what are their shelf-life distributions?
- How many unique products exist by product_type, category and subcategory?
- Which products require cold storage (based on storage_temp_c) and should be handled differently in logistics?
- Which SKUs are missing HS codes or default images (data quality gaps)?
- What is the mapping of SKU to pack sizes and weights for packaging and freight planning?

**Key Columns:**

- **`sku`** (nvarchar(22), NULL) - 10 distinct values
  - *Stock Keeping Unit identifier for the product (alphanumeric code). Appears unique per row in this sample.*
- **`product_name`** (nvarchar(58), NULL) - 10 distinct values
  - *Human-readable product title (e.g., 'Apple - Kinnaur (1kg)').*
- **`product_type`** (nvarchar(28), NULL) - 2 distinct values
  - *High-level type of product (e.g., 'Vegetable', 'Fruit'). Low cardinality.*
- **`category`** (nvarchar(36), NULL) - 1 distinct values
  - *Broad category label (in this snapshot always 'Fresh Produce').*
- **`subcategory`** (nvarchar(46), NULL) - 10 distinct values
  - *More granular classification of the product (e.g., 'Apple', 'Bitter Gourd').*
- **`brand`** (nvarchar(34), NULL) - 1 distinct values
  - *Brand name for the product (here 'Daily Greens').*
- **`uom`** (nvarchar(18), NULL) - 3 distinct values
  - *Unit of measure for the SKU (e.g., 'kg', '250g', '500g').*
- **`gross_weight_kg`** (nvarchar(16), NULL) - 2 distinct values
  - *Gross weight of the packaged product in kg (stored as nvarchar).*
- **`net_weight_kg`** (nvarchar(16), NULL) - 2 distinct values
  - *Net product weight (without packaging) in kg (stored as nvarchar).*
- **`pack_size`** (nvarchar(12), NULL) - 1 distinct values
  - *Count of units per pack (string, constant '1' in sample).*
- *(... and 6 more columns)*

---

### returns

**Rows:** 40  
**Columns:** 13  
**Primary Keys:** *None*  

**Purpose:** Records of product returns initiated against orders. Each row captures a return request lifecycle (request, approval, pickup scheduling, centre receipt, refund and credit note linkage). The table is a raw ingest (all columns are nvarchar) intended to be joined with orders, credit notes, return items and invoices for business analytics and operational reporting.

**Business Questions:**

- How many returns were created in a given date range and how are they distributed by reason_code and status?
- What is the total and average refund_amount for returns (and by reason_code or status)?
- Which approvers processed the most returns and what are their approval rates or average refund amounts?
- What are the average times from request_ts -> pickup_scheduled_ts -> received_at_centre_ts (operational latency) for completed returns?
- Which orders have multiple returns (and how many returns per order)?

**Key Columns:**

- **`return_id`** (nvarchar(26), NULL) - 40 distinct values
  - *Unique identifier for the return request (string).*
- **`order_id`** (nvarchar(26), NULL) - 35 distinct values
  - *Identifier of the order associated with the return.*
- **`request_ts`** (nvarchar(48), NULL) - 40 distinct values
  - *Timestamp when the return was requested (stored as nvarchar in ISO-like format).*
- **`reason_code`** (nvarchar(42), NULL) - 4 distinct values
  - *Categorical reason for the return (e.g., QUALITY, WRONG_ITEM, NOT_AS_DESCRIBED, DAMAGED).*
- **`requested_items_json`** (nvarchar(14), NULL) - 1 distinct values
  - *JSON field that should list items requested for return; in this sample it contains '[]' for all rows.*
- **`status`** (nvarchar(28), NULL) - 4 distinct values
  - *Lifecycle status of the return (REQUESTED, APPROVED, REJECTED, COMPLETED).*
- **`approved_by`** (nvarchar(34), NULL) - 2 distinct values ⚠️ 52.5% NULL
  - *Identifier of the approver (ops_manager, quality_head) or NULL if not approved.*
- **`pickup_scheduled_ts`** (nvarchar(48), NULL) - 40 distinct values
  - *Timestamp when the pickup for the return was scheduled (string).*
- **`received_at_centre_ts`** (nvarchar(48), NULL) - 40 distinct values
  - *Timestamp when returned items were received at the central processing centre (string).*
- **`refund_amount`** (nvarchar(24), NULL) - 40 distinct values
  - *Monetary amount refunded for the return, stored as a string representing a decimal number.*
- *(... and 3 more columns)*

---

### shipments

**Rows:** 100  
**Columns:** 14  
**Primary Keys:** *None*  

**Purpose:** This table stores shipment-level records for orders: one row per physical shipment describing carrier, tracking, dates, status, weight, charge and timestamps. It is used for logistics and delivery performance analysis and for reconciling shipment costs with orders.

**Business Questions:**

- What is the on-time delivery rate by carrier and pickup centre?
- Which carriers or pickup centres have the highest average shipping charge and shipping charge per kg?
- How many shipments are currently OUT_FOR_DELIVERY, IN_TRANSIT, PICKED or DELIVERED?
- What is the distribution of delivery delays (actual - expected) and how many shipments are overdue?
- Which orders have shipments missing an actual_delivery_date (possible delivery exceptions)?

**Key Columns:**

- **`shipment_id`** (nvarchar(26), NULL) - 100 distinct values
  - *Unique identifier for the shipment record (string).*
- **`order_id`** (nvarchar(28), NULL) - 100 distinct values
  - *Identifier of the related order (string).*
- **`carrier_id`** (nvarchar(48), NULL) - 3 distinct values
  - *Logical carrier identifier (e.g., 'LocalCourier', 'ThirdPartyLogistics', 'InHouseFleet').*
- **`tracking_no`** (nvarchar(28), NULL) - 100 distinct values
  - *Carrier tracking number assigned to the physical shipment.*
- **`shipment_date`** (nvarchar(48), NULL) - 100 distinct values
  - *Timestamp when the shipment was dispatched (stored as text in 'YYYY-MM-DD HH:MM:SS' format).*
- **`expected_delivery_date`** (nvarchar(48), NULL) - 100 distinct values
  - *Planned delivery timestamp (text).*
- **`actual_delivery_date`** (nvarchar(48), NULL) - 59 distinct values
  - *Timestamp when the shipment was actually delivered (text). Contains many nulls for undelivered or in-transit shipments.*
- **`shipment_status`** (nvarchar(42), NULL) - 4 distinct values
  - *Current lifecycle state of the shipment (OUT_FOR_DELIVERY, IN_TRANSIT, PICKED, DELIVERED).*
- **`pickup_centre_id`** (nvarchar(64), NULL) - 2 distinct values
  - *Identifier/name of the pickup/dispatch centre handling the shipment (e.g., 'Surat Distribution Centre').*
- **`package_weight_kg`** (nvarchar(20), NULL) - 99 distinct values
  - *Package weight recorded in kilograms, stored as text (numeric-like values).*
- *(... and 4 more columns)*

---


---

*Report generated on 2026-01-09 00:00:40*
