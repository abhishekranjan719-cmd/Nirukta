# Database Schema Analysis Report

**Database:** `raw_data_db`  
**Schema:** `zuna_etl`  
**Analyzed:** 2026-01-09T10:43:02.289233  
**Analyzer Version:** 2.0  

## Executive Summary

- **Tables:** 86
- **Total Rows:** 12,013
- **High Cardinality Threshold:** 200

### Overall Assessment

- **Quality:** Good
- **Normalization:** mixed
- **NL2SQL Suitability:** Good

**Summary:** The schema is comprehensive and well organized for retail/e‑commerce + B2B operations, with clear transactional tables for orders, inventory, shipments, payments and numerous aggregate summary tables. Some tables are highly normalized with explicit foreign keys, while others include denormalized JSON fields and several tables lack explicit primary keys which reduces consistency. Overall it supports broad analytics but would benefit from consistent PK/FK metadata and avoidance of ad‑hoc JSON blobs for easier querying and NL2SQL mapping.

## 📝 Schema Description

This is a multi‑channel retail and logistics schema covering both B2B and e‑commerce domains plus POS; it models customers, products, orders, inventory, fulfillment/shipments, invoices/payments, returns/refunds and operational KPIs. Key entities include customer master tables (b2b_customers, ecom_customers), order systems (b2b_orders, ecom_orders, order_items, b2b_order_lines), product/inventory (products, b2b_products, product_inventory, inventory_items, product_variants), logistics (b2b_dispatches, shipments, shipment tracking events), and financials (b2b_invoices, ecom_payments, refunds, credit notes). The overall model is a hybrid OLTP/OLAP layout: normalized transactional tables capture events and relationships while precomputed daily/monthly/yearly sales and product sales tables provide analytics-ready aggregates. This enables analyses such as channel/store/product sales trends, inventory and replenishment planning, fulfillment performance (on‑time rates, tracking events), returns and refund cost analysis, and coupon/promotion effectiveness. Top 5 business questions that can be answered: 1) What are revenue and margin trends by channel, store and product over time? 2) Which SKUs are low on stock or approaching expiry and require reorder or transfer? 3) What are on‑time delivery and fulfillment failure rates by carrier/centre and their impact on customer satisfaction? 4) What are return/refund drivers and the financial impact by product, reason and customer segment? 5) How effective are coupons and promotions (conversion, average order lift, redemption vs. expected)?

### Table Relationships

**Central/Fact Tables:** `ecom_orders`, `b2b_orders`, `order_items`, `b2b_order_lines`, `products`, `b2b_products`, `product_inventory`, `inventory_items`, `shipments`, `b2b_dispatches`, `b2b_invoices`, `ecom_payments`, `returns / refunds`  
**Lookup/Dimension Tables:** `ecom_customers`, `b2b_customers`, `pos_stores`, `pos_terminals`, `product_variants`, `delivery_slots`, `b2b_sales_agents`, `b2b_vendor_partners`, `ecom_coupons`, `pos_vendors`  

Orders (ecom_orders, b2b_orders) are the primary transactional facts and link to customer masters. Order line/detail tables (order_items, b2b_order_lines) connect orders to products/skus, which in turn join to inventory tables (product_inventory, inventory_items) for stock and batch information. Fulfillment is modeled via shipments and dispatches with tracking/event tables allowing time‑series joins for performance metrics. Financial flow is represented by invoices, payments, credit notes and refunds tied back to orders and customers, enabling revenue and cash analyses. Aggregate summary tables (daily/monthly/yearly sales, product_wise_sales, pos_sales_daily) provide fast analytics paths; common analytical joins are order -> order_items -> product -> inventory -> shipment -> payment -> customer, supporting sales, supply‑chain and finance reporting. Note: several tables lack explicit PKs and a few fields are stored as JSON blobs which complicates automated relationship discovery and NL2SQL mapping without metadata enrichment.

## 🚨 Data Quality Issues (NL2SQL Risks)

### ❌ Wrong Table Selection Risks (24 issues)

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

9. **Table:** `b2b_events_stream`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_events_stream

10. **Table:** `b2b_picking_batches`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_picking_batches

11. **Table:** `b2b_portal_api_clients`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_portal_api_clients

12. **Table:** `b2b_shipment_tracking_events`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to b2b_shipment_tracking_events

13. **Table:** `delivery_status`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to delivery_status

14. **Table:** `ecom_activity_log`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_activity_log

15. **Table:** `ecom_coupon_usage`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_coupon_usage

16. **Table:** `ecom_frequently_bought`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_frequently_bought

17. **Table:** `ecom_ticket_messages`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_ticket_messages

18. **Table:** `ecom_wishlist`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to ecom_wishlist

19. **Table:** `pos_returns`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_returns

20. **Table:** `pos_shift_closures`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_shift_closures

21. **Table:** `pos_transaction_lines`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_transaction_lines

22. **Table:** `pos_transactions`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_transactions

23. **Table:** `pos_users`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to pos_users

24. **Table:** `product_pricing`
   - *Issue:* Missing primary key makes table harder to identify uniquely
   - *Fix:* Add PRIMARY KEY constraint to product_pricing

### ❌ Wrong Column Selection Risks (124 issues)

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
   - *Found in tables:* `b2b_kpi_daily_snapshots`, `b2b_product_sales`, `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `pos_product_wise_sales`, `pos_products_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`, `product_sales`
   - *Issue:* Column 'gross_sales' exists in 16 tables: b2b_kpi_daily_snapshots, b2b_product_sales, b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, pos_product_wise_sales, pos_products_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly, product_sales
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
   - *Found in tables:* `b2b_orders`, `b2b_product_sales`, `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_orders`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `order_items`, `pos_product_wise_sales`, `pos_products_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'tax_amount' exists in 17 tables: b2b_orders, b2b_product_sales, b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_orders, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, order_items, pos_product_wise_sales, pos_products_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

56. **Column:** `discount_amount`
   - *Found in tables:* `b2b_orders`, `b2b_product_sales`, `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_orders`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `order_items`, `pos_loyalty_redemptions`, `pos_product_wise_sales`, `pos_products_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'discount_amount' exists in 18 tables: b2b_orders, b2b_product_sales, b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_orders, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, order_items, pos_loyalty_redemptions, pos_product_wise_sales, pos_products_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly
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

67. **Column:** `net_sales`
   - *Found in tables:* `b2b_product_sales`, `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `pos_product_wise_sales`, `pos_products_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`, `product_sales`
   - *Issue:* Column 'net_sales' exists in 15 tables: b2b_product_sales, b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, pos_product_wise_sales, pos_products_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly, product_sales
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

68. **Column:** `product_id`
   - *Found in tables:* `b2b_product_wise_sales`, `ecom_product_wise_sales`, `pos_product_wise_sales`
   - *Issue:* Column 'product_id' exists in 3 tables: b2b_product_wise_sales, ecom_product_wise_sales, pos_product_wise_sales
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

69. **Column:** `total_qty_kg`
   - *Found in tables:* `b2b_product_wise_sales`, `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `pos_product_wise_sales`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'total_qty_kg' exists in 12 tables: b2b_product_wise_sales, b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly, ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, pos_product_wise_sales, pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

70. **Column:** `plucode`
   - *Found in tables:* `b2b_products`, `pos_products`
   - *Issue:* Column 'plucode' exists in 2 tables: b2b_products, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

71. **Column:** `uom`
   - *Found in tables:* `b2b_products`, `pos_products`, `product_variants`, `products`
   - *Issue:* Column 'uom' exists in 4 tables: b2b_products, pos_products, product_variants, products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

72. **Column:** `pos_price`
   - *Found in tables:* `b2b_products`, `pos_products`
   - *Issue:* Column 'pos_price' exists in 2 tables: b2b_products, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

73. **Column:** `tax_rate`
   - *Found in tables:* `b2b_products`, `pos_products`
   - *Issue:* Column 'tax_rate' exists in 2 tables: b2b_products, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

74. **Column:** `stock_qty`
   - *Found in tables:* `b2b_products`, `pos_products`
   - *Issue:* Column 'stock_qty' exists in 2 tables: b2b_products, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

75. **Column:** `reorder_point`
   - *Found in tables:* `b2b_products`, `pos_products`, `product_inventory`
   - *Issue:* Column 'reorder_point' exists in 3 tables: b2b_products, pos_products, product_inventory
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

76. **Column:** `updated_at`
   - *Found in tables:* `b2b_products`, `ecom_cart_items`, `ecom_coupons`, `ecom_orders`, `ecom_payment_status_log`, `ecom_ratings_summary`, `ecom_ticket`, `inventory_items`, `pos_products`
   - *Issue:* Column 'updated_at' exists in 9 tables: b2b_products, ecom_cart_items, ecom_coupons, ecom_orders, ecom_payment_status_log, ecom_ratings_summary, ecom_ticket, inventory_items, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

77. **Column:** `photo_url`
   - *Found in tables:* `b2b_quality_inspections`, `delivery_status`
   - *Issue:* Column 'photo_url' exists in 2 tables: b2b_quality_inspections, delivery_status
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

78. **Column:** `return_id`
   - *Found in tables:* `b2b_returns`, `ecom_return_items`, `returns`
   - *Issue:* Column 'return_id' exists in 3 tables: b2b_returns, ecom_return_items, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

79. **Column:** `received_at`
   - *Found in tables:* `b2b_returns`, `inventory_items`
   - *Issue:* Column 'received_at' exists in 2 tables: b2b_returns, inventory_items
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

80. **Column:** `reason_code`
   - *Found in tables:* `b2b_returns`, `returns`
   - *Issue:* Column 'reason_code' exists in 2 tables: b2b_returns, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

81. **Column:** `refund_amount`
   - *Found in tables:* `b2b_returns`, `ecom_refunds`, `pos_returns`, `returns`
   - *Issue:* Column 'refund_amount' exists in 4 tables: b2b_returns, ecom_refunds, pos_returns, returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

82. **Column:** `disposition`
   - *Found in tables:* `b2b_returns`, `ecom_return_items`
   - *Issue:* Column 'disposition' exists in 2 tables: b2b_returns, ecom_return_items
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

83. **Column:** `agent_id`
   - *Found in tables:* `b2b_sales_agents`, `ecom_acquisition_agents`
   - *Issue:* Column 'agent_id' exists in 2 tables: b2b_sales_agents, ecom_acquisition_agents
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

84. **Column:** `phone`
   - *Found in tables:* `b2b_sales_agents`, `b2b_vendor_partners`, `ecom_acquisition_agents`, `ecom_customers`, `ecom_vendors`, `pos_users`, `pos_vendors`
   - *Issue:* Column 'phone' exists in 7 tables: b2b_sales_agents, b2b_vendor_partners, ecom_acquisition_agents, ecom_customers, ecom_vendors, pos_users, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

85. **Column:** `region`
   - *Found in tables:* `b2b_sales_agents`, `pos_stores`
   - *Issue:* Column 'region' exists in 2 tables: b2b_sales_agents, pos_stores
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

86. **Column:** `join_date`
   - *Found in tables:* `b2b_sales_agents`, `ecom_acquisition_agents`
   - *Issue:* Column 'join_date' exists in 2 tables: b2b_sales_agents, ecom_acquisition_agents
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

87. **Column:** `customer_type`
   - *Found in tables:* `b2b_sales_daily`, `b2b_sales_monthly`, `b2b_sales_yearly`
   - *Issue:* Column 'customer_type' exists in 3 tables: b2b_sales_daily, b2b_sales_monthly, b2b_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

88. **Column:** `year`
   - *Found in tables:* `b2b_sales_monthly`, `b2b_sales_yearly`, `ecom_sales_monthly`, `ecom_sales_yearly`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'year' exists in 6 tables: b2b_sales_monthly, b2b_sales_yearly, ecom_sales_monthly, ecom_sales_yearly, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

89. **Column:** `month`
   - *Found in tables:* `b2b_sales_monthly`, `ecom_sales_monthly`, `pos_sales_monthly`
   - *Issue:* Column 'month' exists in 3 tables: b2b_sales_monthly, ecom_sales_monthly, pos_sales_monthly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

90. **Column:** `gps_lat`
   - *Found in tables:* `b2b_shipment_tracking_events`, `delivery_status`
   - *Issue:* Column 'gps_lat' exists in 2 tables: b2b_shipment_tracking_events, delivery_status
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

91. **Column:** `gps_long`
   - *Found in tables:* `b2b_shipment_tracking_events`, `delivery_status`
   - *Issue:* Column 'gps_long' exists in 2 tables: b2b_shipment_tracking_events, delivery_status
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

92. **Column:** `vendor_id`
   - *Found in tables:* `b2b_vendor_partners`, `ecom_vendors`, `pos_vendors`
   - *Issue:* Column 'vendor_id' exists in 3 tables: b2b_vendor_partners, ecom_vendors, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

93. **Column:** `vendor_name`
   - *Found in tables:* `b2b_vendor_partners`, `ecom_vendors`, `pos_vendors`
   - *Issue:* Column 'vendor_name' exists in 3 tables: b2b_vendor_partners, ecom_vendors, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

94. **Column:** `gst_no`
   - *Found in tables:* `b2b_vendor_partners`, `ecom_vendors`, `pos_vendors`
   - *Issue:* Column 'gst_no' exists in 3 tables: b2b_vendor_partners, ecom_vendors, pos_vendors
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

95. **Column:** `shipment_id`
   - *Found in tables:* `delivery_status`, `shipments`
   - *Issue:* Column 'shipment_id' exists in 2 tables: delivery_status, shipments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

96. **Column:** `device_type`
   - *Found in tables:* `ecom_browsing_history`, `ecom_carts`
   - *Issue:* Column 'device_type' exists in 2 tables: ecom_browsing_history, ecom_carts
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

97. **Column:** `cart_id`
   - *Found in tables:* `ecom_cart_items`, `ecom_carts`
   - *Issue:* Column 'cart_id' exists in 2 tables: ecom_cart_items, ecom_carts
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

98. **Column:** `qty`
   - *Found in tables:* `ecom_cart_items`, `ecom_return_items`, `pos_returns`, `pos_transaction_lines`
   - *Issue:* Column 'qty' exists in 4 tables: ecom_cart_items, ecom_return_items, pos_returns, pos_transaction_lines
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

99. **Column:** `added_at`
   - *Found in tables:* `ecom_cart_items`, `ecom_wishlist`
   - *Issue:* Column 'added_at' exists in 2 tables: ecom_cart_items, ecom_wishlist
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

100. **Column:** `variant_id`
   - *Found in tables:* `ecom_cart_items`, `order_items`, `product_variants`
   - *Issue:* Column 'variant_id' exists in 3 tables: ecom_cart_items, order_items, product_variants
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

101. **Column:** `total_amount`
   - *Found in tables:* `ecom_carts`, `ecom_orders`
   - *Issue:* Column 'total_amount' exists in 2 tables: ecom_carts, ecom_orders
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

102. **Column:** `coupon_code`
   - *Found in tables:* `ecom_carts`, `ecom_coupons`, `ecom_orders`
   - *Issue:* Column 'coupon_code' exists in 3 tables: ecom_carts, ecom_coupons, ecom_orders
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

103. **Column:** `coupon_id`
   - *Found in tables:* `ecom_coupon_usage`, `ecom_coupons`
   - *Issue:* Column 'coupon_id' exists in 2 tables: ecom_coupon_usage, ecom_coupons
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

104. **Column:** `description`
   - *Found in tables:* `ecom_coupons`, `ecom_ticket`
   - *Issue:* Column 'description' exists in 2 tables: ecom_coupons, ecom_ticket
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

105. **Column:** `last_login`
   - *Found in tables:* `ecom_customers`, `pos_users`
   - *Issue:* Column 'last_login' exists in 2 tables: ecom_customers, pos_users
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

106. **Column:** `title`
   - *Found in tables:* `ecom_notifications`, `ecom_reviews`
   - *Issue:* Column 'title' exists in 2 tables: ecom_notifications, ecom_reviews
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

107. **Column:** `shipping_charge`
   - *Found in tables:* `ecom_orders`, `shipments`
   - *Issue:* Column 'shipping_charge' exists in 2 tables: ecom_orders, shipments
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

108. **Column:** `gateway_ref_no`
   - *Found in tables:* `ecom_payments`, `ecom_refunds`
   - *Issue:* Column 'gateway_ref_no' exists in 2 tables: ecom_payments, ecom_refunds
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

109. **Column:** `processed_by`
   - *Found in tables:* `ecom_payments`, `ecom_refunds`, `pos_returns`
   - *Issue:* Column 'processed_by' exists in 3 tables: ecom_payments, ecom_refunds, pos_returns
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

110. **Column:** `total_customers`
   - *Found in tables:* `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`
   - *Issue:* Column 'total_customers' exists in 4 tables: ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

111. **Column:** `delivery_fee`
   - *Found in tables:* `ecom_product_wise_sales`, `ecom_sales_daily`, `ecom_sales_monthly`, `ecom_sales_yearly`, `product_sales`
   - *Issue:* Column 'delivery_fee' exists in 5 tables: ecom_product_wise_sales, ecom_sales_daily, ecom_sales_monthly, ecom_sales_yearly, product_sales
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

112. **Column:** `order_item_id`
   - *Found in tables:* `ecom_return_items`, `order_items`
   - *Issue:* Column 'order_item_id' exists in 2 tables: ecom_return_items, order_items
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

113. **Column:** `ticket_id`
   - *Found in tables:* `ecom_ticket`, `ecom_ticket_messages`
   - *Issue:* Column 'ticket_id' exists in 2 tables: ecom_ticket, ecom_ticket_messages
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

114. **Column:** `expiry_date`
   - *Found in tables:* `inventory_items`, `pos_transaction_lines`
   - *Issue:* Column 'expiry_date' exists in 2 tables: inventory_items, pos_transaction_lines
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

115. **Column:** `product_name`
   - *Found in tables:* `order_items`, `products`
   - *Issue:* Column 'product_name' exists in 2 tables: order_items, products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

116. **Column:** `store_id`
   - *Found in tables:* `pos_daily_sales_summary`, `pos_inventory_adjustments`, `pos_loyalty_redemptions`, `pos_products`, `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`, `pos_stores`, `pos_terminals`, `pos_users`
   - *Issue:* Column 'store_id' exists in 10 tables: pos_daily_sales_summary, pos_inventory_adjustments, pos_loyalty_redemptions, pos_products, pos_sales_daily, pos_sales_monthly, pos_sales_yearly, pos_stores, pos_terminals, pos_users
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

117. **Column:** `total_sales`
   - *Found in tables:* `pos_daily_sales_summary`, `pos_shift_closures`
   - *Issue:* Column 'total_sales' exists in 2 tables: pos_daily_sales_summary, pos_shift_closures
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

118. **Column:** `pos_sku`
   - *Found in tables:* `pos_inventory_adjustments`, `pos_products`
   - *Issue:* Column 'pos_sku' exists in 2 tables: pos_inventory_adjustments, pos_products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

119. **Column:** `pos_txn_id`
   - *Found in tables:* `pos_loyalty_redemptions`, `pos_returns`, `pos_transaction_lines`, `pos_transactions`
   - *Issue:* Column 'pos_txn_id' exists in 4 tables: pos_loyalty_redemptions, pos_returns, pos_transaction_lines, pos_transactions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

120. **Column:** `total_bills`
   - *Found in tables:* `pos_sales_daily`, `pos_sales_monthly`, `pos_sales_yearly`
   - *Issue:* Column 'total_bills' exists in 3 tables: pos_sales_daily, pos_sales_monthly, pos_sales_yearly
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

121. **Column:** `shift_id`
   - *Found in tables:* `pos_shift_closures`, `pos_transactions`
   - *Issue:* Column 'shift_id' exists in 2 tables: pos_shift_closures, pos_transactions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

122. **Column:** `terminal_id`
   - *Found in tables:* `pos_shift_closures`, `pos_sync_log`, `pos_terminals`, `pos_transactions`
   - *Issue:* Column 'terminal_id' exists in 4 tables: pos_shift_closures, pos_sync_log, pos_terminals, pos_transactions
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

123. **Column:** `pos_user_id`
   - *Found in tables:* `pos_transactions`, `pos_users`
   - *Issue:* Column 'pos_user_id' exists in 2 tables: pos_transactions, pos_users
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

124. **Column:** `storage_temp_c`
   - *Found in tables:* `product_inventory`, `products`
   - *Issue:* Column 'storage_temp_c' exists in 2 tables: product_inventory, products
   - *Risk:* NL2SQL may select wrong table when filtering/grouping by this column

### ❌ Wrong Filter Condition Risks (40 issues)

1. **Column:** `b2b_credit_notes.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

2. **Column:** `b2b_kpi_daily_snapshots.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

3. **Column:** `b2b_payments.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

4. **Column:** `b2b_price_list.price_list_id`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(50)`
   - ❌ *Wrong:* `WHERE price_list_id > 100`
   - ✅ *Correct:* `WHERE CAST(price_list_id AS DECIMAL) > 100`
   - *Fix:* Convert b2b_price_list.price_list_id to appropriate numeric type

5. **Column:** `b2b_price_list.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

6. **Column:** `b2b_quality_inspections.rejection_reason`
   - *Issue:* High NULL percentage (68.0%)
   - *Fix:* Handle NULLs explicitly: WHERE rejection_reason IS NOT NULL

7. **Column:** `b2b_quality_inspections.photo_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE photo_url IS NOT NULL

8. **Column:** `b2b_quality_inspections.remarks`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE remarks IS NOT NULL

9. **Column:** `b2b_shipment_tracking_events.scan_photo_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE scan_photo_url IS NOT NULL

10. **Column:** `b2b_shipment_tracking_events.status_note`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE status_note IS NOT NULL

11. **Column:** `delivery_status.updated_by`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(50)`
   - ❌ *Wrong:* `WHERE updated_by > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(updated_by AS DATE) > '2024-01-01'`
   - *Fix:* Convert delivery_status.updated_by to DATE or DATETIME type

12. **Column:** `delivery_status.photo_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE photo_url IS NOT NULL

13. **Column:** `delivery_status.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

14. **Column:** `ecom_activity_log.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

15. **Column:** `ecom_cart_items.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

16. **Column:** `ecom_carts.abandoned_at`
   - *Issue:* High NULL percentage (59.0%)
   - *Fix:* Handle NULLs explicitly: WHERE abandoned_at IS NOT NULL

17. **Column:** `ecom_frequently_bought.last_updated`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(50)`
   - ❌ *Wrong:* `WHERE last_updated > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(last_updated AS DATE) > '2024-01-01'`
   - *Fix:* Convert ecom_frequently_bought.last_updated to DATE or DATETIME type

18. **Column:** `ecom_payment_status_log.response_body`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE response_body IS NOT NULL

19. **Column:** `ecom_payment_status_log.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

20. **Column:** `ecom_payments.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

21. **Column:** `ecom_product_events.old_value`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE old_value IS NOT NULL

22. **Column:** `ecom_product_events.new_value`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE new_value IS NOT NULL

23. **Column:** `ecom_refunds.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

24. **Column:** `ecom_return_items.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

25. **Column:** `ecom_reviews.responded_by`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE responded_by IS NOT NULL

26. **Column:** `ecom_reviews.response_text`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE response_text IS NOT NULL

27. **Column:** `ecom_ticket_messages.attachment_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE attachment_url IS NOT NULL

28. **Column:** `ecom_wishlist.notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE notes IS NOT NULL

29. **Column:** `pos_products.active_flag`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE active_flag IS NOT NULL

30. **Column:** `pos_shift_closures.discrepancies_note`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE discrepancies_note IS NOT NULL

31. **Column:** `pos_sync_log.error_message`
   - *Issue:* High NULL percentage (58.0%)
   - *Fix:* Handle NULLs explicitly: WHERE error_message IS NOT NULL

32. **Column:** `pos_transaction_lines.variant_info`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE variant_info IS NOT NULL

33. **Column:** `pos_transaction_lines.expiry_date`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE expiry_date IS NOT NULL

34. **Column:** `pos_transactions.cashier_note`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE cashier_note IS NOT NULL

35. **Column:** `product_pricing.price_id`
   - *Issue:* Numeric column stored as text/varchar
   - *Current Type:* `nvarchar(50)`
   - ❌ *Wrong:* `WHERE price_id > 100`
   - ✅ *Correct:* `WHERE CAST(price_id AS DECIMAL) > 100`
   - *Fix:* Convert product_pricing.price_id to appropriate numeric type

36. **Column:** `products.hs_code`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE hs_code IS NOT NULL

37. **Column:** `products.default_image_url`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE default_image_url IS NOT NULL

38. **Column:** `returns.approved_by`
   - *Issue:* High NULL percentage (52.5%)
   - *Fix:* Handle NULLs explicitly: WHERE approved_by IS NOT NULL

39. **Column:** `returns.resolution_notes`
   - *Issue:* High NULL percentage (100.0%)
   - *Fix:* Handle NULLs explicitly: WHERE resolution_notes IS NOT NULL

40. **Column:** `shipments.last_update`
   - *Issue:* Date column stored as text/varchar
   - *Current Type:* `nvarchar(50)`
   - ❌ *Wrong:* `WHERE last_update > '2024-01-01'`
   - ✅ *Correct:* `WHERE CAST(last_update AS DATE) > '2024-01-01'`
   - *Fix:* Convert shipments.last_update to DATE or DATETIME type

### ❌ Wrong Join Condition Risks (88 issues)

1. **Column:** `b2b_contracts.customer_id`
   - *Issue:* FK relationship exists but may lack index
   - *Fix:* Ensure index exists on b2b_contracts.customer_id for join performance

2. **Column:** `b2b_credit_notes.invoice_id`
   - *Issue:* FK relationship exists but may lack index
   - *Fix:* Ensure index exists on b2b_credit_notes.invoice_id for join performance

3. **Column:** `b2b_customer_addresses.customer_id`
   - *Issue:* FK relationship exists but may lack index
   - *Fix:* Ensure index exists on b2b_customer_addresses.customer_id for join performance

4. **Column:** `b2b_dispatches.order_id`
   - *Issue:* FK relationship exists but may lack index
   - *Fix:* Ensure index exists on b2b_dispatches.order_id for join performance

5. **Column:** `b2b_invoices.customer_id`
   - *Issue:* FK relationship exists but may lack index
   - *Fix:* Ensure index exists on b2b_invoices.customer_id for join performance

6. **Column:** `b2b_invoices.order_id`
   - *Issue:* FK relationship exists but may lack index
   - *Fix:* Ensure index exists on b2b_invoices.order_id for join performance

7. **Column:** `b2b_order_allocations.order_line_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `b2b_order_lines`
   - *Fix:* Add FK constraint or clarify relationship in documentation

8. **Column:** `b2b_order_allocations.inventory_id`
   - *Issue:* Potential FK column without constraint
   - *Potential References:* `inventory_items`, `pos_inventory_adjustments`, `product_inventory`
   - *Fix:* Add FK constraint or clarify relationship in documentation

9. **Column:** `b2b_order_allocations.order_id`
   - *Issue:* FK relationship exists but may lack index
   - *Fix:* Ensure index exists on b2b_order_allocations.order_id for join performance

10. **Column:** `b2b_order_events.order_id`
   - *Issue:* FK relationship exists but may lack index
   - *Fix:* Ensure index exists on b2b_order_events.order_id for join performance

### ❌ Wrong Aggregation Risks (92 issues)

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

5. **Multi-level Columns:** `taxable_value`, `tax_amount`
   - *Tables:* `b2b_invoices`, `b2b_orders`
   - *Issue:* Similar columns in related tables may cause confusion
   - *Risk:* NL2SQL may aggregate at wrong level or double-count
   - *Fix:* Clarify whether to sum at b2b_invoices or b2b_orders level

6. **Column:** `b2b_invoices.total_tax`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_tax directly, avoid SUM(total_tax)

7. **Multi-level Columns:** `total_tax`, `tax_amount`
   - *Tables:* `b2b_invoices`, `b2b_orders`
   - *Issue:* Similar columns in related tables may cause confusion
   - *Risk:* NL2SQL may aggregate at wrong level or double-count
   - *Fix:* Clarify whether to sum at b2b_invoices or b2b_orders level

8. **Column:** `b2b_kpi_daily_snapshots.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

9. **Column:** `b2b_kpi_daily_snapshots.total_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_kg directly, avoid SUM(total_kg)

10. **Column:** `b2b_kpi_daily_snapshots.avg_delivery_time_min`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use avg_delivery_time_min directly, avoid SUM(avg_delivery_time_min)

11. **Column:** `b2b_order_lines.line_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use line_total directly, avoid SUM(line_total)

12. **Column:** `b2b_orders.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

13. **Column:** `b2b_picking_batches.total_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_kg directly, avoid SUM(total_kg)

14. **Column:** `b2b_product_sales.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

15. **Column:** `b2b_product_wise_sales.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

16. **Column:** `b2b_product_wise_sales.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

17. **Column:** `b2b_product_wise_sales.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

18. **Column:** `b2b_sales_daily.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

19. **Column:** `b2b_sales_daily.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

20. **Column:** `b2b_sales_daily.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

21. **Column:** `b2b_sales_monthly.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

22. **Column:** `b2b_sales_monthly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

23. **Column:** `b2b_sales_monthly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

24. **Column:** `b2b_sales_yearly.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

25. **Column:** `b2b_sales_yearly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

26. **Column:** `b2b_sales_yearly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

27. **Column:** `ecom_carts.total_items`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_items directly, avoid SUM(total_items)

28. **Column:** `ecom_carts.total_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_amount directly, avoid SUM(total_amount)

29. **Column:** `ecom_coupon_usage.discount_given`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_given directly, avoid SUM(discount_given)

30. **Multi-level Columns:** `discount_given`, `tax_amount`
   - *Tables:* `ecom_coupon_usage`, `ecom_orders`
   - *Issue:* Similar columns in related tables may cause confusion
   - *Risk:* NL2SQL may aggregate at wrong level or double-count
   - *Fix:* Clarify whether to sum at ecom_coupon_usage or ecom_orders level

31. **Multi-level Columns:** `discount_given`, `discount_type`
   - *Tables:* `ecom_coupon_usage`, `ecom_coupons`
   - *Issue:* Similar columns in related tables may cause confusion
   - *Risk:* NL2SQL may aggregate at wrong level or double-count
   - *Fix:* Clarify whether to sum at ecom_coupon_usage or ecom_coupons level

32. **Column:** `ecom_coupons.discount_type`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_type directly, avoid SUM(discount_type)

33. **Column:** `ecom_coupons.discount_value`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_value directly, avoid SUM(discount_value)

34. **Column:** `ecom_coupons.max_discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use max_discount_amount directly, avoid SUM(max_discount_amount)

35. **Column:** `ecom_customer_addresses.country`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use country directly, avoid SUM(country)

36. **Column:** `ecom_customer_segmentation.avg_order_value`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use avg_order_value directly, avoid SUM(avg_order_value)

37. **Column:** `ecom_orders.total_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_amount directly, avoid SUM(total_amount)

38. **Column:** `ecom_orders.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

39. **Column:** `ecom_payment_status_log.retry_count`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use retry_count directly, avoid SUM(retry_count)

40. **Column:** `ecom_product_wise_sales.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

41. **Column:** `ecom_product_wise_sales.total_customers`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_customers directly, avoid SUM(total_customers)

42. **Column:** `ecom_product_wise_sales.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

43. **Column:** `ecom_product_wise_sales.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

44. **Column:** `ecom_ratings_summary.rating_summary_id`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use rating_summary_id directly, avoid SUM(rating_summary_id)

45. **Column:** `ecom_ratings_summary.avg_rating`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use avg_rating directly, avoid SUM(avg_rating)

46. **Column:** `ecom_ratings_summary.total_reviews`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_reviews directly, avoid SUM(total_reviews)

47. **Column:** `ecom_reviews.helpful_count`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use helpful_count directly, avoid SUM(helpful_count)

48. **Column:** `ecom_sales_daily.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

49. **Column:** `ecom_sales_daily.total_customers`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_customers directly, avoid SUM(total_customers)

50. **Column:** `ecom_sales_daily.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

51. **Column:** `ecom_sales_daily.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

52. **Column:** `ecom_sales_monthly.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

53. **Column:** `ecom_sales_monthly.total_customers`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_customers directly, avoid SUM(total_customers)

54. **Column:** `ecom_sales_monthly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

55. **Column:** `ecom_sales_monthly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

56. **Column:** `ecom_sales_yearly.total_orders`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_orders directly, avoid SUM(total_orders)

57. **Column:** `ecom_sales_yearly.total_customers`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_customers directly, avoid SUM(total_customers)

58. **Column:** `ecom_sales_yearly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

59. **Column:** `ecom_sales_yearly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

60. **Column:** `inventory_items.total_stock_units`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_stock_units directly, avoid SUM(total_stock_units)

61. **Column:** `order_items.line_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use line_total directly, avoid SUM(line_total)

62. **Multi-level Columns:** `tax_amount`, `tax_amount`
   - *Tables:* `order_items`, `ecom_orders`
   - *Issue:* Similar columns in related tables may cause confusion
   - *Risk:* NL2SQL may aggregate at wrong level or double-count
   - *Fix:* Clarify whether to sum at order_items or ecom_orders level

63. **Column:** `order_items.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

64. **Multi-level Columns:** `discount_amount`, `tax_amount`
   - *Tables:* `order_items`, `ecom_orders`
   - *Issue:* Similar columns in related tables may cause confusion
   - *Risk:* NL2SQL may aggregate at wrong level or double-count
   - *Fix:* Clarify whether to sum at order_items or ecom_orders level

65. **Column:** `pos_daily_sales_summary.summary_id`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use summary_id directly, avoid SUM(summary_id)

66. **Column:** `pos_daily_sales_summary.total_txns`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_txns directly, avoid SUM(total_txns)

67. **Column:** `pos_daily_sales_summary.total_sales`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_sales directly, avoid SUM(total_sales)

68. **Column:** `pos_daily_sales_summary.total_tax`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_tax directly, avoid SUM(total_tax)

69. **Column:** `pos_daily_sales_summary.total_refunds`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_refunds directly, avoid SUM(total_refunds)

70. **Column:** `pos_daily_sales_summary.avg_txn_value`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use avg_txn_value directly, avoid SUM(avg_txn_value)

71. **Column:** `pos_loyalty_redemptions.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

72. **Column:** `pos_product_wise_sales.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

73. **Column:** `pos_product_wise_sales.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

74. **Column:** `pos_products_sales.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

75. **Column:** `pos_sales_daily.total_bills`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_bills directly, avoid SUM(total_bills)

76. **Column:** `pos_sales_daily.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

77. **Column:** `pos_sales_daily.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

78. **Column:** `pos_sales_monthly.total_bills`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_bills directly, avoid SUM(total_bills)

79. **Column:** `pos_sales_monthly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

80. **Column:** `pos_sales_monthly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

81. **Column:** `pos_sales_yearly.total_bills`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_bills directly, avoid SUM(total_bills)

82. **Column:** `pos_sales_yearly.total_qty_kg`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_qty_kg directly, avoid SUM(total_qty_kg)

83. **Column:** `pos_sales_yearly.discount_amount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amount directly, avoid SUM(discount_amount)

84. **Column:** `pos_shift_closures.total_sales`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use total_sales directly, avoid SUM(total_sales)

85. **Column:** `pos_shift_closures.counted_cash`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use counted_cash directly, avoid SUM(counted_cash)

86. **Column:** `pos_sync_log.retry_count`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use retry_count directly, avoid SUM(retry_count)

87. **Column:** `pos_transaction_lines.line_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use line_total directly, avoid SUM(line_total)

88. **Column:** `pos_transaction_lines.discount_amt`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_amt directly, avoid SUM(discount_amt)

89. **Column:** `pos_transactions.txn_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use txn_total directly, avoid SUM(txn_total)

90. **Column:** `pos_transactions.tax_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use tax_total directly, avoid SUM(tax_total)

91. **Column:** `pos_transactions.discount_total`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount_total directly, avoid SUM(discount_total)

92. **Column:** `product_sales.discount`
   - *Issue:* Pre-aggregated column name suggests already computed value
   - *Risk:* Aggregating this column again (SUM/AVG) may cause double-counting
   - *Fix:* Use discount directly, avoid SUM(discount)

## 💡 Recommendations

*No recommendations available.*

## 📊 Table Details

### b2b_contracts

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** `contract_id`  

**Purpose:** Stores B2B customer contract metadata (contract identifiers, linked customer, term dates, applicable SKUs, pricing and discount rules, delivery windows, penalties, status and creation timestamp). It represents the canonical contract definitions used to apply pricing and operational constraints across sales, invoicing and fulfillment processes.

**Business Questions:**

- Which contracts are currently active for a given customer or SKU?
- How many contracts (and which pricing models) are in PENDING, ACTIVE or EXPIRED status?
- What is the total minimum committed monthly volume across active contracts over a time window?
- Which SKUs are covered by contracts for a given customer or region (requires joining customer address)?
- Are there overlapping contracts for the same customer (contract term overlap) and what operational windows apply?

**Foreign Keys:**

- `customer_id` → `b2b_customers.customer_id`

**Key Columns:**

- **`contract_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for each B2B contract (primary key).*
- **`customer_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the customer that the contract applies to (foreign key to b2b_customers).*
- **`start_date`** (datetime2, NULL) - 50 distinct values
  - *Contract start timestamp indicating when terms become effective.*
- **`end_date`** (datetime2, NULL) - 50 distinct values
  - *Contract end timestamp when terms expire (can be null if open-ended).*
- **`sku_list_json`** (nvarchar(50), NULL) - 47 distinct values
  - *Semi-structured JSON (stored as nvarchar) containing a list/array of SKUs covered by the contract.*
- **`pricing_model`** (nvarchar(50), NULL) - 3 distinct values
  - *Nominal pricing approach used by the contract (e.g., Dynamic, Fixed, Tiered).*
- **`min_monthly_volume`** (decimal(18,4), NULL) - 48 distinct values
  - *Numeric minimum committed monthly volume for the contract (decimal(18,4)).*
- **`discount_schema_json`** (nvarchar(50), NULL) - 1 distinct values
  - *JSON blob describing discount rules/schema for the contract (currently identical across rows in this dataset).*
- **`delivery_windows_json`** (nvarchar(50), NULL) - 1 distinct values
  - *JSON describing permitted delivery windows for the contract (e.g., days and times). Currently appears constant across rows.*
- **`penalty_terms`** (nvarchar(50), NULL) - 1 distinct values
  - *Text describing penalty terms for breaches (e.g., late delivery penalty); currently identical text for all rows.*
- *(... and 2 more columns)*

---

### b2b_credit_notes

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** `credit_note_id`  

**Purpose:** Stores credit and debit notes issued against B2B invoices. Each row represents a single credit/debit note with metadata about issuance, approval, reason, status and linkage to the originating invoice and any related return.

**Business Questions:**

- What is the total value and count of credit notes vs debit notes over a given period?
- Which reasons (Damage / Price Adjustment / Return) account for the largest credit note amounts?
- How long does approval take on average (approved_at - issued_at) and are there outliers?
- Which issuers/approvers create or approve the largest volume/value of credit notes?
- How many credit notes are VOID vs ISSUED vs APPLIED and what amounts do they represent?

**Foreign Keys:**

- `invoice_id` → `b2b_invoices.invoice_id`

**Key Columns:**

- **`credit_note_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Primary key: unique identifier for each credit/debit note (e.g. CN17001).*
- **`invoice_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Foreign key reference to the originating invoice (e.g. INV13001). Nullable if a note isn't tied to an invoice.*
- **`note_type`** (nvarchar(50), NULL) - 2 distinct values
  - *Type of note: CREDIT or DEBIT (two categories).*
- **`amount`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary value of the credit/debit note (decimal(18,4)).*
- **`reason`** (nvarchar(50), NULL) - 3 distinct values
  - *Business reason for the note (Damage, Price Adjustment, Return).*
- **`issued_by`** (nvarchar(50), NULL) - 50 distinct values
  - *Name of the user who issued the credit/debit note.*
- **`issued_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the note was issued (datetime2).*
- **`approved_by`** (nvarchar(50), NULL) - 50 distinct values
  - *Name of the user who approved the credit/debit note.*
- **`approved_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the note was approved (datetime2).*
- **`related_return_id`** (nvarchar(50), NULL) - 30 distinct values
  - *If the credit note is tied to a return, this is the return identifier (e.g. RET15025). Nullable.*
- *(... and 2 more columns)*

---

### b2b_customer_addresses

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** `address_id`  

**Purpose:** Stores B2B customer postal and geolocation address records. Each row is a physical address (billing/shipping/location) associated with a business customer. It supports customer lookup, delivery planning, geospatial analysis and joining to orders/shipments/contacts across the ETL schema.

**Business Questions:**

- How many addresses does each B2B customer have and which customers have multiple addresses?
- What is the distribution of customer addresses by city and pincode?
- Which addresses are missing secondary address details (addr_line2) or other fields?
- Which addresses fall within a geographic bounding box or near a given coordinate (for delivery planning)?
- Which customers have addresses in a specific city or pincode (for regional promotions or logistics)?

**Foreign Keys:**

- `customer_id` → `b2b_customers.customer_id`

**Key Columns:**

- **`address_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for the address record (primary key).*
- **`customer_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Foreign key linking the address to a b2b customer (zuna_etl.b2b_customers.customer_id).*
- **`addr_line1`** (nvarchar(50), NULL) - 48 distinct values
  - *Primary address text (street, building number, road name).*
- **`addr_line2`** (nvarchar(50), NULL) - 4 distinct values
  - *Secondary address line (landmark, locality note); many repeated limited values and some NULLs.*
- **`city`** (nvarchar(50), NULL) - 10 distinct values
  - *City name for the address (regional segmentation).*
- **`state`** (nvarchar(50), NULL) - 1 distinct values
  - *State name for the address (all rows contain 'Gujarat' in this dataset).*
- **`pincode`** (bigint, NULL) - 50 distinct values
  - *Numeric postal code (regional postal index) for routing and grouping.*
- **`country`** (nvarchar(50), NULL) - 1 distinct values
  - *Country name for the address (all rows contain 'India').*
- **`latitude`** (decimal(18,4), NULL) - 50 distinct values
  - *Latitude of the address for geospatial calculations (decimal(18,4)).*
- **`longitude`** (decimal(18,4), NULL) - 50 distinct values
  - *Longitude of the address for geospatial calculations (decimal(18,4)).*

---

### b2b_customers

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** `customer_id`  

**Purpose:** Master B2B customer directory used by the ETL schema to store customer attributes, contact details, credit and billing/delivery pointers. Acts as the central customer reference for sales, invoicing, orders and reporting processes.

**Business Questions:**

- How many customers do we have overall and by account_type / customer_segment?
- What is the total and average credit_limit exposure by customer_segment or account_type?
- Which sales reps have the most customers assigned?
- What is the distribution of payment_terms_days across our customers?
- When were customers onboarded (created_at) — how many new customers per month?

**Key Columns:**

- **`customer_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Surrogate natural identifier for each B2B customer (primary key).*
- **`name`** (nvarchar(50), NULL) - 39 distinct values
  - *Business/trading name of the customer.*
- **`account_type`** (nvarchar(50), NULL) - 4 distinct values
  - *Categorical type of account (Retailer, Wholesale, Hotel/Catering, Exporter).*
- **`gst_number`** (nvarchar(50), NULL) - 50 distinct values
  - *Tax registration number (GST) for the customer; appears unique per row.*
- **`primary_contact_name`** (nvarchar(50), NULL) - 50 distinct values
  - *Name of the primary contact person at the customer.*
- **`primary_contact_phone`** (nvarchar(50), NULL) - 50 distinct values
  - *Phone number of the primary contact (often includes country code).*
- **`email`** (nvarchar(54), NULL) - 50 distinct values
  - *Primary contact email address for the customer.*
- **`billing_address_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Pointer to the customer's billing address record (address id).*
- **`delivery_address_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Pointer to the customer's delivery/shipping address record.*
- **`customer_segment`** (nvarchar(50), NULL) - 3 distinct values
  - *Business-assigned customer tiering (Tier-1, Tier-2, Tier-3).*
- *(... and 4 more columns)*

---

### b2b_dispatches

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** `dispatch_id`  

**Purpose:** Records of outbound dispatches for B2B orders: each row represents a dispatch event (physical shipment) tied to an order. It is used to track scheduling, actual dispatch times, vehicle/driver allocation, carrier partner, freight cost, tracking info and basic metadata about creation and handling.

**Business Questions:**

- What percentage of dispatches are DELIVERED vs IN_TRANSIT vs SCHEDULED?
- What is the on-time dispatch rate (actual_dispatch_ts <= scheduled_dispatch_ts) for the last month?
- Which drivers or vehicles have handled the most dispatches in a period?
- What is total and average freight cost by carrier_partner_id or by dispatch_status?
- Which dispatches lack tracking numbers or have missing actual_dispatch_ts (possible exceptions)?

**Foreign Keys:**

- `order_id` → `b2b_orders.order_id`

**Key Columns:**

- **`dispatch_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for the dispatch event (primary key).*
- **`order_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Reference to the originating B2B order (FK -> b2b_orders.order_id).*
- **`vehicle_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the vehicle assigned to the dispatch.*
- **`driver_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the driver assigned to the dispatch.*
- **`carrier_partner_id`** (nvarchar(50), NULL) - 2 distinct values
  - *Identifier for the carrier partner (logistics provider) responsible for the dispatch.*
- **`scheduled_dispatch_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Planned dispatch timestamp stored as nvarchar(50) (appears in 'YYYY-MM-DD hh:mm:ss' format).*
- **`actual_dispatch_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Actual dispatch timestamp recorded (stored as nvarchar(50) but contains datetime-like strings).*
- **`seal_no`** (nvarchar(50), NULL) - 50 distinct values
  - *Seal number applied to the consignment/container for security/integrity tracking.*
- **`dispatch_status`** (nvarchar(50), NULL) - 3 distinct values
  - *Current lifecycle status of the dispatch (SCHEDULED, IN_TRANSIT, DELIVERED).*
- **`freight_amount`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary freight cost charged for the dispatch (decimal(18,4)).*
- *(... and 4 more columns)*

---

### b2b_events_stream

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** An event stream table capturing domain events (order, inventory, shipment) coming from multiple source systems into the B2B ETL layer. It is used to track event occurrence, processing status, retry behavior, and to drive downstream processing or analytics.

**Business Questions:**

- How many events of each event_type (ORDER_CREATED, SHIPMENT_CREATED, INVENTORY_UPDATED) arrived in a given date range?
- What proportion of events have been processed vs unprocessed and what is the average processing latency?
- Which aggregate_ids (orders/shipments/inventory) are generating the most retries or failed processing attempts?
- How do event volumes and processing success differ by source_system (B2B_PORTAL vs ERP)?
- Which partitions (partition_key) or time windows contain the largest number of unprocessed events that need replay?

**Key Columns:**

- **`event_uuid`** (nvarchar(50), NULL) - 50 distinct values
  - *Unique identifier for the event in the stream (string). Currently distinct for each row in the sample.*
- **`event_ts`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the domain event occurred (source event time).*
- **`aggregate_type`** (nvarchar(50), NULL) - 3 distinct values
  - *Category of the domain object the event pertains to (e.g., inventory, order, shipment).*
- **`aggregate_id`** (nvarchar(50), NULL) - 31 distinct values
  - *Identifier of the domain aggregate instance (e.g., order id like B2BORD4008). Likely maps to ids in domain tables depending on aggregate_type.*
- **`event_type`** (nvarchar(50), NULL) - 3 distinct values
  - *Concrete event name/type (INVENTORY_UPDATED, ORDER_CREATED, SHIPMENT_CREATED) — a higher fidelity event label.*
- **`payload_json`** (nvarchar(50), NULL) - 1 distinct values
  - *JSON payload for the event content. In the current sample this column contains only '{}' (empty JSON).*
- **`source_system`** (nvarchar(50), NULL) - 2 distinct values
  - *Origin system of the event (e.g., B2B_PORTAL, ERP).*
- **`processed_flag`** (bit, NULL) - 2 distinct values
  - *Boolean flag indicating whether the event has been processed by downstream consumers.*
- **`processed_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the event was processed by the consumer (nullable if not processed).*
- **`retry_count`** (decimal(18,4), NULL) - 4 distinct values
  - *Number of retry attempts for processing the event. Stored as decimal(18,4) but acts like a small integer in practice.*
- *(... and 2 more columns)*

---

### b2b_invoices

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** `invoice_id`  

**Purpose:** Holds invoice-level financial and lifecycle data for B2B transactions. Used to record invoice identifiers, links to orders and customers, monetary amounts (taxable, tax components, total), invoice lifecycle dates (invoice_date, due_date, created_at) and status. Acts as the canonical invoice ledger for reporting, collections and downstream reconciliations.

**Business Questions:**

- What is the total invoiced amount and total tax over a time range (day/week/month/quarter)?
- Which customers have the highest invoice amounts or outstanding overdue invoices?
- How many invoices are in each status (PAID, ISSUED, OVERDUE) and how much value does each status represent?
- What is the aging profile of outstanding invoices (past due buckets) as of a given date?
- What is the average taxable_value, tax rate (total_tax/taxable_value) and invoice_amount by customer or over time?

**Foreign Keys:**

- `customer_id` → `b2b_customers.customer_id`
- `order_id` → `b2b_orders.order_id`

**Key Columns:**

- **`invoice_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for each invoice (nvarchar). Acts as the primary key for the table.*
- **`order_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier of the order associated with the invoice; nullable (FK to b2b_orders.order_id).*
- **`invoice_number`** (nvarchar(50), NULL) - 50 distinct values
  - *Business-facing invoice number string (may include formatting like INV-200000); not necessarily unique but likely unique in practice.*
- **`invoice_date`** (datetime2, NULL) - 50 distinct values
  - *The date/time when the invoice was issued (datetime2).*
- **`due_date`** (datetime2, NULL) - 50 distinct values
  - *The date when payment for the invoice is due (datetime2).*
- **`customer_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the customer billed on the invoice (FK to b2b_customers.customer_id).*
- **`taxable_value`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary base amount subject to tax (decimal(18,4)).*
- **`igst`** (bigint, NULL) - 1 distinct values
  - *Integrated GST component (bigint). In this dataset igst is constant 0.*
- **`cgst`** (decimal(18,4), NULL) - 50 distinct values
  - *Central GST component for the invoice (decimal(18,4)).*
- **`sgst`** (decimal(18,4), NULL) - 50 distinct values
  - *State GST component for the invoice (decimal(18,4)).*
- *(... and 4 more columns)*

---

### b2b_kpi_daily_snapshots

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** `snapshot_id`  

**Purpose:** Daily snapshot of B2B operational KPIs per centre. Captures daily aggregated metrics (orders, weight, sales, returns, wastage, delivery performance) used for trend analysis, reporting, and SLA monitoring.

**Business Questions:**

- How have gross sales trended over time for each centre?
- Which centres consistently meet on-time delivery targets and what are their average delivery times?
- What is the returns and wastage trend (kg) and how does it relate to total_kg?
- What days had unusually high or low total_orders or gross_sales (anomalies)?
- What is the average orders and sales per centre for a given date range?

**Key Columns:**

- **`snapshot_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for each daily KPI snapshot row (primary key).*
- **`centre_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Identifier for the operational centre/location the snapshot belongs to.*
- **`date`** (datetime2, NULL) - 41 distinct values
  - *The business date the snapshot covers (snapshot date). Stored as datetime2 but likely represents a date-only value at midnight.*
- **`total_orders`** (decimal(18,4), NULL) - 31 distinct values
  - *Aggregated count of orders for the centre on that date (stored as decimal(18,4) rather than integer).*
- **`total_kg`** (decimal(18,4), NULL) - 50 distinct values
  - *Total weight (kg) of goods handled/sold at the centre on that date.*
- **`gross_sales`** (decimal(18,4), NULL) - 50 distinct values
  - *Total gross sales (monetary amount) for the centre on that date.*
- **`returns_kg`** (decimal(18,4), NULL) - 50 distinct values
  - *Total weight (kg) of returns for the centre on that date.*
- **`wastage_kg`** (decimal(18,4), NULL) - 50 distinct values
  - *Weight (kg) of wastage (loss/spoilage) recorded for the centre on that date.*
- **`avg_delivery_time_min`** (bigint, NULL) - 46 distinct values
  - *Average delivery time in minutes for deliveries from the centre on that date.*
- **`on_time_pct`** (decimal(18,4), NULL) - 50 distinct values
  - *Percentage of deliveries that were on-time for the centre on that date (stored as decimal, likely 0-100 scale).*
- *(... and 2 more columns)*

---

### b2b_order_allocations

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** `allocation_id`  

**Purpose:** Records inventory allocations made against B2B orders (per order line / inventory item). Captures how much inventory (kg and units) was allocated, when, by whom, expiry and release metadata, and why allocations were made. Serves as the bridge between orders and inventory for allocation, reservation, and release workflows.

**Business Questions:**

- What is the total allocated quantity (kg and units) per day / week / month?
- Which orders or order lines have active allocations and how much inventory is reserved for them?
- Which inventory items are most frequently allocated or experiencing shortages?
- Which allocators (users) allocate the most volume and what are their release/expiry patterns?
- How long do allocations remain active before release (allocation lifecycle / aging)?

**Foreign Keys:**

- `order_id` → `b2b_orders.order_id`

**Key Columns:**

- **`allocation_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for each allocation record (primary key).*
- **`order_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier of the B2B order this allocation belongs to (FK to b2b_orders).*
- **`order_line_id`** (nvarchar(50), NULL) - 34 distinct values
  - *Identifier of the specific order line the allocation is against (links to b2b_order_lines).*
- **`inventory_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier of the inventory record (stock item / location) used to satisfy the allocation.*
- **`allocated_qty_kg`** (decimal(18,4), NULL) - 50 distinct values
  - *Quantity reserved/allocated in kilograms (decimal(18,4)).*
- **`allocated_qty_units`** (bigint, NULL) - 43 distinct values
  - *Quantity reserved/allocated in units (bigint).*
- **`allocated_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the allocation was made (datetime2).*
- **`allocated_by`** (nvarchar(50), NULL) - 50 distinct values
  - *Name or identifier of the person/system that performed the allocation.*
- **`expiry_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Expiration timestamp for the allocation (stored as nvarchar). Likely indicates when reservation expires if not converted to an order release or consumed.*
- **`status`** (nvarchar(50), NULL) - 2 distinct values
  - *Allocation lifecycle status (e.g., ACTIVE, RELEASED). Low-cardinality indicator of whether allocation is currently holding inventory.*
- *(... and 2 more columns)*

---

### b2b_order_events

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** `event_id`  

**Purpose:** Event-level audit trail for lifecycle changes and actions on B2B orders. Each row records a discrete event (status change, allocation, pick, dispatch, etc.) tied to an order and actors/system that generated the event. Used for operational monitoring, auditing, and event-driven analytics in the B2B order pipeline.

**Business Questions:**

- How many events of each event_type occurred in a given date range?
- Which orders have unprocessed events or a backlog of events?
- What is the typical time between CREATED and DISPATCHED events per order?
- Which users (event_by) or source_systems generate the most events or errors?
- What are the most common status transitions (prev_status -> new_status)?

**Foreign Keys:**

- `order_id` → `b2b_orders.order_id`

**Key Columns:**

- **`event_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for this event (primary key).*
- **`order_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier of the order this event relates to (FK to b2b_orders.order_id).*
- **`event_type`** (nvarchar(50), NULL) - 6 distinct values
  - *Categorical type of the event (CREATED, ALLOCATED, PICKED, DISPATCHED, CONFIRMED, etc.).*
- **`event_ts`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the event occurred (event source time).*
- **`event_by`** (nvarchar(50), NULL) - 50 distinct values
  - *Human or system actor who triggered the event (user name or service name).*
- **`prev_status`** (nvarchar(50), NULL) - 3 distinct values
  - *Status of the order prior to this event.*
- **`new_status`** (nvarchar(50), NULL) - 3 distinct values
  - *Status of the order after this event.*
- **`details_json`** (nvarchar(50), NULL) - 1 distinct values
  - *JSON payload with event-specific details. Currently appears to contain '{}' in sample.*
- **`source_system`** (nvarchar(50), NULL) - 3 distinct values
  - *Origin system that produced the event (ERP, MOBILE_APP, PORTAL, etc.).*
- **`ip_address`** (nvarchar(50), NULL) - 50 distinct values
  - *IP address of the actor/system at the time of the event (string).*
- *(... and 2 more columns)*

---

### b2b_order_lines

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** `order_line_id`  

**Purpose:** Order line-level detail for B2B orders: each row is a single line item on an order, containing product (sku), quantities, pricing, allocation and routing metadata. It is the transactional source for item-level sales, inventory allocation and fulfillment analytics.

**Business Questions:**

- What is total revenue and quantity sold per SKU or item_description over a time period?
- Which warehouses are fulfilling the most kg/units or revenue and which allocations/batches are most used?
- Are there lines with promised_by delays relative to created_at (lead time) or missing promises?
- What is average unit price and variance per SKU or batch?
- Which order lines have special remarks (e.g., Prewashed) and how do they impact price or quantity?

**Foreign Keys:**

- `sku` → `b2b_products.sku`
- `order_id` → `b2b_orders.order_id`

**Key Columns:**

- **`order_line_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Primary key: unique identifier for each order line.*
- **`order_id`** (nvarchar(50), NULL) - 32 distinct values
  - *Identifier of the parent order (links to orders table).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Stock-keeping unit code for the product on the line (links to products table).*
- **`item_description`** (nvarchar(50), NULL) - 10 distinct values
  - *Human-readable description of the item (likely derived from product master).*
- **`qty_units`** (bigint, NULL) - 45 distinct values
  - *Quantity measured in units (integer bigint).*
- **`qty_kg`** (decimal(18,4), NULL) - 47 distinct values
  - *Quantity measured in kilograms (decimal 18,4).*
- **`unit_price`** (decimal(18,4), NULL) - 50 distinct values
  - *Price per unit (decimal).*
- **`line_total`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary total for the order line (decimal) — revenue contribution for the line.*
- **`allocation_id`** (nvarchar(50), NULL) - 33 distinct values
  - *Identifier for the inventory allocation attempt/reservation that served this line.*
- **`promised_by`** (nvarchar(50), NULL) - 50 distinct values
  - *Promised delivery/due timestamp stored as nvarchar (contains datetime-like strings).*
- *(... and 4 more columns)*

---

### b2b_orders

**Rows:** 71  
**Columns:** 15  
**Primary Keys:** `order_id`  

**Purpose:** This table stores B2B order-level records. It is a central sales/orders fact for business customers capturing order identifiers, timestamps, financials (gross, discount, tax, net), fulfillment metadata (pickup centre, priority), channel and status. It is used for revenue, order lifecycle, fulfillment and customer-level analyses and acts as a hub for joins to customers, order lines, invoices, dispatches and related operational tables.

**Business Questions:**

- What is the total gross/net revenue and average order value in a date range?
- How many orders were placed per order_channel and what are their average net_amounts?
- Which pickup centres have the highest volume and value of orders?
- What proportion of orders are CANCELLED vs PLACED/DELIVERED by time period?
- How many URGENT priority orders were placed and what is their average fulfillment value?

**Foreign Keys:**

- `customer_id` → `b2b_customers.customer_id`

**Key Columns:**

- **`order_id`** (nvarchar(50), NOT NULL) - 71 distinct values
  - *Unique identifier for each B2B order (primary key).*
- **`external_order_code`** (nvarchar(50), NULL) - 71 distinct values
  - *Order code used by external systems (mapping/reference to external ERP/partner).*
- **`customer_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the customer who placed the order; FK to b2b_customers (nullable).*
- **`order_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp when the order was placed, stored as nvarchar string (format appears 'YYYY-MM-DD HH:MM:SS').*
- **`requested_delivery_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Requested delivery datetime by the customer, stored as nvarchar string (ISO-like format).*
- **`order_channel`** (nvarchar(50), NULL) - 4 distinct values
  - *Channel via which the order was placed (WhatsApp, Email, Phone, Sales Rep).*
- **`order_status`** (nvarchar(50), NULL) - 5 distinct values
  - *Current lifecycle status of the order (PLACED, CANCELLED, CONFIRMED, DISPATCHED, DELIVERED).*
- **`currency`** (nvarchar(50), NULL) - 1 distinct values
  - *Currency code for monetary fields (three-letter ISO). Currently all rows are 'INR'.*
- **`gross_amount`** (decimal(18,4), NULL) - 50 distinct values
  - *Order gross amount (decimal(18,4)) before discounts and taxes.*
- **`tax_amount`** (decimal(18,4), NULL) - 1 distinct values
  - *Tax component of the order (decimal). Current data shows 0 for all rows.*
- *(... and 5 more columns)*

---

### b2b_payments

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** `payment_id`  

**Purpose:** Records payment events for B2B invoices: one row per payment (successful, pending, failed) with amount, timing, payment method and reconciliation metadata. It is used to reconcile receipts against invoices and to analyze payment behavior and cash collection.

**Business Questions:**

- What is the total payment amount and count by day/week/month?
- Which payment modes contribute most to collected amount and which have higher failure rates?
- What percentage of payments are reconciled and what is the average reconciliation lag (reconciled_at - payment_ts)?
- Which customers have the highest payment volume or most failed payments?
- How many payments are pending or failed over a period and how do they correlate with payment_mode or bank_ref_no?

**Foreign Keys:**

- `invoice_id` → `b2b_invoices.invoice_id`

**Key Columns:**

- **`payment_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Surrogate/unique identifier for the payment record (primary key).*
- **`invoice_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier of the invoice this payment is applied to (FK to b2b_invoices).*
- **`customer_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the customer who made/received the payment.*
- **`payment_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp when payment was initiated/recorded, stored as nvarchar (text) in table.*
- **`amount`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary amount of the payment (decimal(18,4)).*
- **`payment_mode`** (nvarchar(50), NULL) - 4 distinct values
  - *Method used for the payment (CHEQUE, RTGS, UPI, NEFT).*
- **`bank_ref_no`** (nvarchar(50), NULL) - 50 distinct values
  - *Bank or gateway reference number for the payment (trace/transaction id).*
- **`status`** (nvarchar(50), NULL) - 3 distinct values
  - *Outcome/status of the payment: SUCCESS, PENDING, FAILED.*
- **`reconciled_flag`** (bit, NULL) - 2 distinct values
  - *Boolean indicating whether the payment has been reconciled to accounting/bank records (bit).*
- **`reconciled_at`** (datetime2, NULL) - 50 distinct values
  - *Datetime when the payment was reconciled (datetime2).*
- *(... and 2 more columns)*

---

### b2b_picking_batches

**Rows:** 50  
**Columns:** 13  
**Primary Keys:** *None*  

**Purpose:** Records picking batch metadata for B2B order fulfilment: who picked, where and when the batch was created/started/finished, counts of expected vs actual lines, weight, routing and priority. Used for operational monitoring, efficiency analysis and linking picking activity to downstream dispatch/shipment/order data.

**Business Questions:**

- Which centres have the highest average pick duration and how does that vary by transport_priority?
- Which pickers consistently meet or exceed expected_lines (actual_lines >= expected_lines)?
- How does total_kg per batch vary by route_id or transport_priority?
- What percentage of batches are COMPLETED vs IN_PROGRESS in the last 7/30/90 days?
- Are there systemic differences in pick performance (duration, accuracy) between centres or routes?

**Key Columns:**

- **`picking_batch_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Unique identifier for each picking batch (string).*
- **`centre_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Identifier of the fulfilment centre or warehouse where the batch was picked.*
- **`picker_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the picker (employee) who performed the batch.*
- **`created_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the picking batch record was created in the system.*
- **`started_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when picking for the batch actually started.*
- **`finished_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when picking for the batch finished.*
- **`status`** (nvarchar(50), NULL) - 3 distinct values
  - *Lifecycle state of the picking batch (CREATED / IN_PROGRESS / COMPLETED).*
- **`expected_lines`** (bigint, NULL) - 10 distinct values
  - *Number of order lines expected to be picked in the batch (planned count).*
- **`actual_lines`** (bigint, NULL) - 10 distinct values
  - *Number of order lines actually picked in the batch (observed count).*
- **`total_kg`** (decimal(18,4), NULL) - 50 distinct values
  - *Total weight (kilograms) of items in the picking batch (decimal).*
- *(... and 3 more columns)*

---

### b2b_portal_api_clients

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Houses API client credentials and metadata for B2B portal integrations. Records credentials (hashed), authorization scope, rate limits, creation and usage timestamps, and an active flag so the system can authenticate and manage external integrations per customer.

**Business Questions:**

- How many API clients are currently active vs inactive?
- Which API clients have not been used in the last N days (stale clients)?
- How many clients are assigned to each rate_limit tier (100/200/500)?
- How many API clients were created over time (daily/weekly cohorts)?
- Which customers have API clients and are any customers without active clients?

**Key Columns:**

- **`api_client_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Unique identifier for the API client/application. Serves as the logical ID used to reference a client in logs and joins.*
- **`customer_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the customer/account that owns this API client. Links the client to a customer record.*
- **`api_key_hash`** (nvarchar(96), NULL) - 50 distinct values
  - *Hash of the client's API key used for authentication. Stored as opaque hashed value for security.*
- **`secret_hash`** (nvarchar(60), NULL) - 50 distinct values
  - *Hashed secret associated with the API client (secondary credential). Stored hashed for security.*
- **`allowed_ips_json`** (nvarchar(50), NULL) - 1 distinct values
  - *JSON array listing allowed client IPs or IP ranges for this client. In this dataset it is always an empty array ([]).*
- **`rate_limit`** (bigint, NULL) - 3 distinct values
  - *Numeric rate-limit tier assigned to the client (requests per unit time). Low cardinality: typical values 100, 200, 500.*
- **`scopes_json`** (nvarchar(50), NULL) - 1 distinct values
  - *JSON array of permission scopes granted to this client (e.g., ["orders","inventory"]). Currently identical for all rows.*
- **`created_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the API client was created (datetime2).*
- **`last_used`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp or marker indicating when the client was last used. Stored as nvarchar(50) in this schema, though values look like ISO datetimes.*
- **`active_flag`** (bit, NULL) - 2 distinct values
  - *Boolean indicating whether the API client is active (True) or deactivated (False).*

---

### b2b_price_list

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** `price_list_id`  

**Purpose:** This table stores B2B price list entries that define per-unit prices (and minimum order quantities) for SKUs either for specific customers or for customer groups, with explicit validity windows (start and end timestamps). It is used to determine what price applies to an order/customer at a given time and to maintain historical price records.

**Business Questions:**

- What price(s) are defined for SKU X for customer Y or customer group Z during date D?
- Which customers have special prices (different from the standard/customer group price) for a given SKU?
- How has the price_per_unit for SKU X changed over time (price history)?
- Which price list entries are currently active (as of now) or will become active within a date range?
- Which SKUs have minimum order quantities greater than a threshold, and for which customers?

**Foreign Keys:**

- `sku` → `b2b_products.sku`
- `customer_id` → `b2b_customers.customer_id`

**Key Columns:**

- **`price_list_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Primary key identifier for a price list entry (unique per row).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Product SKU to which the price entry applies; FK to b2b_products.sku.*
- **`customer_id`** (nvarchar(50), NULL) - 34 distinct values
  - *Customer identifier for whom the price was set; FK to b2b_customers.customer_id. Nullable — absence implies customer_group or general price.*
- **`customer_group`** (nvarchar(50), NULL) - 2 distinct values
  - *Customer group classification for which this price applies (e.g., RETAIL or WHOLESALE).*
- **`start_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Validity start timestamp for the price entry, stored as an nvarchar (ISO-like datetime string).*
- **`end_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Validity end timestamp for the price entry, stored as an nvarchar (ISO-like datetime string).*
- **`price_per_unit`** (decimal(18,4), NULL) - 50 distinct values
  - *Decimal price per unit (currency indicated in currency column).*
- **`currency`** (nvarchar(50), NULL) - 1 distinct values
  - *Currency code for price_per_unit (e.g., INR).*
- **`min_order_qty`** (decimal(18,4), NULL) - 40 distinct values
  - *Minimum quantity required to place an order at this price (decimal).*
- **`created_by`** (nvarchar(50), NULL) - 1 distinct values
  - *User who created the price_list entry (audit field).*
- *(... and 2 more columns)*

---

### b2b_product_sales

**Rows:** 10  
**Columns:** 5  
**Primary Keys:** `sku`  

**Purpose:** Aggregated B2B product-level sales metrics for each SKU. This table appears to be an ETL-level snapshot that stores per-SKU monetary measures (gross sales, discounts, tax, and net sales) and is intended for reporting, KPI calculations, and downstream joins to product master or order-detail tables to enrich or filter results.

**Business Questions:**

- Which SKUs account for the top X% of net sales (SKU Pareto / top contributors)?
- What is the discount rate (discount_amount / gross_sales) and which SKUs have the highest discount rates?
- Which SKUs have the largest tax amounts relative to gross sales (tax_amount / gross_sales)?
- How do gross_sales, discounts and taxes contribute to net_sales per SKU and how do they rank by net_sales?
- Which SKUs should be prioritized for pricing or promotion reviews based on low net margin (inferred from high discounts relative to gross)?

**Key Columns:**

- **`sku`** (nvarchar(50), NOT NULL) - 10 distinct values
  - *Stock Keeping Unit identifier for the product. Serves as the primary key in this table and the natural key to link to product master and transactional tables.*
- **`gross_sales`** (decimal(18,4), NULL) - 10 distinct values
  - *Total gross monetary sales for the SKU (pre-discounts and before applying tax semantics used in downstream reporting). Stored as decimal(18,4).*
- **`discount_amount`** (decimal(18,4), NULL) - 10 distinct values
  - *Total discounts (monetary amount) applied to the SKU. Stored as decimal(18,4).*
- **`tax_amount`** (decimal(18,4), NULL) - 10 distinct values
  - *Total tax collected or applied for the SKU. Stored as decimal(18,4).*
- **`net_sales`** (decimal(18,4), NULL) - 10 distinct values
  - *Net sales (monetary) for the SKU after accounting for discounts/taxes according to the ETL logic. Stored as decimal(18,4). Represents the end metric for revenue reporting at SKU level.*

---

### b2b_product_wise_sales

**Rows:** 731  
**Columns:** 8  
**Primary Keys:** `date`  

**Purpose:** Time-series product-level sales metrics for B2B channel. Each row captures daily aggregated metrics (orders, quantity, sales, discounts, tax, net) for a product on a specific date. It is used for trend analysis, KPI computation and downstream joins to product and order metadata for enrichment.

**Business Questions:**

- How has daily net sales for product TOM001 changed over the last year?
- What is the weekly/monthly trend in quantity sold (kg) and number of orders for this product?
- What is the effective discount rate and how much revenue is lost to discounts over a time period?
- How do gross sales, discounts and tax reconcile to net sales day-by-day and are there anomalies?
- Are there days with unusually high average order size (kg per order) that require operational follow-up?

**Key Columns:**

- **`date`** (datetime2, NOT NULL) - 731 distinct values
  - *The business date for the aggregated row (datetime2). Acts as the primary key in this table; each row represents metrics for this date.*
- **`product_id`** (nvarchar(50), NULL) - 1 distinct values
  - *Identifier for the product (nvarchar(50)). In the snapshot this is effectively a single product (TOM001). Column is nullable in DDL but dataset shows consistent value.*
- **`total_orders`** (decimal(18,4), NULL) - 720 distinct values
  - *Aggregated count/measure of orders for the product on the date (stored as decimal(18,4) rather than integer).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 730 distinct values
  - *Total quantity sold in kilograms for the product on the date (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 731 distinct values
  - *Gross sales amount before discounts and taxes for the product on that date (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 730 distinct values
  - *Total discount applied to the product sales on that date (decimal(18,4)).*
- **`tax_amount`** (decimal(18,4), NULL) - 731 distinct values
  - *Total tax charged on the product sales on that date (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 731 distinct values
  - *Net sales amount after discounts and taxes for the product on that date (decimal(18,4)).*

---

### b2b_products

**Rows:** 10  
**Columns:** 10  
**Primary Keys:** `sku`  

**Purpose:** Catalog of B2B products with pricing, tax, unit-of-measure and simple inventory metadata. Serves as the canonical product master for B2B workflows (pricing, inventory checks, reorder signals, reporting).

**Business Questions:**

- Which products are below their reorder point and need replenishment?
- What are current POS prices and tax rates for each SKU (to compute tax-inclusive price)?
- How many active SKUs exist and how are they distributed by UOM?
- Which products were updated in the last X days?
- What is the total on-hand stock across all SKUs or by UOM?

**Key Columns:**

- **`sku`** (nvarchar(50), NOT NULL) - 10 distinct values
  - *Primary product identifier (alphanumeric code used as the table's primary key).*
- **`plucode`** (bigint, NULL) - 10 distinct values
  - *Numeric PLU/code commonly used at POS systems; alternative product identifier (bigint).*
- **`name`** (nvarchar(50), NULL) - 10 distinct values
  - *Human-readable product name/description.*
- **`uom`** (nvarchar(50), NULL) - 3 distinct values
  - *Unit of measure (e.g., kg, 250g, 500g).*
- **`pos_price`** (decimal(18,4), NULL) - 10 distinct values
  - *Point-of-sale price for the product (decimal with 4 fractional digits).*
- **`tax_rate`** (decimal(18,4), NULL) - 1 distinct values
  - *Applicable tax rate for the product (decimal). In this sample it is constant at 0.05.*
- **`stock_qty`** (decimal(18,4), NULL) - 10 distinct values
  - *On-hand stock quantity for the SKU (decimal to allow fractional units).*
- **`reorder_point`** (bigint, NULL) - 9 distinct values
  - *Reorder threshold for the SKU (bigint) — if stock_qty <= reorder_point, consider reordering.*
- **`active_flag`** (bit, NULL) - 1 distinct values
  - *Boolean flag indicating if the product is active/available for sale.*
- **`updated_at`** (datetime2, NULL) - 10 distinct values
  - *Timestamp of the last update to the product record (datetime2).*

---

### b2b_quality_inspections

**Rows:** 50  
**Columns:** 14  
**Primary Keys:** `inspection_id`  

**Purpose:** Records individual quality inspection events performed on B2B order batch items / order lines. Each row is a single inspection performed by an inspector at a timestamp, capturing measured temperature, visual score, microbial test result, an acceptance decision, any rejection reason and corrective action, and creation metadata. The table supports product quality monitoring, operational compliance, and root-cause analysis for returns/spoilage/corrective actions.

**Business Questions:**

- What is the overall acceptance rate of inspected batch items and how has it trended over time?
- Which inspectors have the highest rejection rates or lowest average visual_score?
- What proportion of rejected inspections cite spoilage and what corrective actions follow (Dispose, Discount, Repack)?
- Is there a relationship between measured temperature (temp_c) and acceptance_flag or visual_score?
- Which orders/order lines lead to repeated rejections (when joined to order/order_line tables) and may need supplier or handling interventions?

**Key Columns:**

- **`inspection_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for each quality inspection event (primary key).*
- **`batch_item_id`** (nvarchar(50), NULL) - 30 distinct values
  - *Identifier for the batch item being inspected (likely links to a specific item in a picking/packing batch).*
- **`order_line_id`** (nvarchar(50), NULL) - 32 distinct values
  - *Identifier of the order line associated with the inspected item (maps to order line records).*
- **`inspector_id`** (nvarchar(50), NULL) - 49 distinct values
  - *Identifier of the inspector who performed the inspection.*
- **`inspection_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp when the inspection occurred; stored as nvarchar but values appear to be datetime strings.*
- **`temp_c`** (decimal(18,4), NULL) - 48 distinct values
  - *Measured temperature in Celsius at inspection time (decimal(18,4)).*
- **`visual_score`** (bigint, NULL) - 30 distinct values
  - *Quantitative visual inspection score (bigint) representing appearance or quality rating.*
- **`acceptance_flag`** (bit, NULL) - 2 distinct values
  - *Boolean flag indicating whether the inspected item was accepted (True) or rejected (False).*
- **`rejection_reason`** (nvarchar(50), NULL) - 1 distinct values ⚠️ 68.0% NULL
  - *Categorical reason for rejection (e.g., 'Spoilage'); heavily null where acceptance_flag is true or not rejected.*
- **`photo_url`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Intended to store URL to inspection photo but currently typed as decimal(18,4) and 100% null in this dataset.*
- *(... and 4 more columns)*

---

### b2b_returns

**Rows:** 50  
**Columns:** 13  
**Primary Keys:** `return_id`  

**Purpose:** Records B2B return transactions. Each row represents a return request/fulfillment tied to an order and customer, including timing, disposition, inspection metadata and financial adjustment (refund/credit note). It is used to track return volume, reasons, costs and operational handling.

**Business Questions:**

- How many returns were requested / received in a given period, and how many were completed, approved or rejected?
- What is the total and average refund amount and total returned weight (qty_kg) over a period or by return reason?
- What are the most common reason_codes and dispositions, and how do they change over time?
- What is the average time (hours/days) between requested_at and received_at for returns, and which returns are outliers?
- Which inspectors processed the most returns and what were their average refund amounts / dispositions?

**Foreign Keys:**

- `order_id` → `b2b_orders.order_id`

**Key Columns:**

- **`return_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for the return record (primary key). Example pattern: 'RET#####'.*
- **`order_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier of the order associated with the return. FK to zuna_etl.b2b_orders.order_id. Pattern example: 'B2BORD####'. Nullable.*
- **`customer_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for the customer who initiated/owned the return. Pattern example: 'CUST####'. Nullable.*
- **`requested_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the return was requested by the customer or recorded in the system (datetime2).*
- **`received_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the returned goods were received by the warehouse/inspector (datetime2).*
- **`return_status`** (nvarchar(50), NULL) - 4 distinct values
  - *Categorical status of the return lifecycle (e.g., REQUESTED, APPROVED, REJECTED, COMPLETED).*
- **`reason_code`** (nvarchar(50), NULL) - 4 distinct values
  - *Categorical reason for the return (EXCESS_QUANTITY, QUALITY, DAMAGED, WRONG_ITEM).*
- **`qty_kg`** (decimal(18,4), NULL) - 50 distinct values
  - *Returned quantity measured in kilograms (decimal(18,4)).*
- **`refund_amount`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary refund issued for the return (decimal(18,4)).*
- **`credit_note_id`** (nvarchar(50), NULL) - 33 distinct values
  - *Identifier of the credit note issued for the return, if any (links to b2b_credit_notes).*
- *(... and 3 more columns)*

---

### b2b_sales_agents

**Rows:** 60  
**Columns:** 10  
**Primary Keys:** `agent_id`  

**Purpose:** Master list of B2B sales agents used by the application to attribute sales, commissions and to join to transactional tables (orders, contracts, payments). It provides agent identity, contact info, region and specialization and basic operational metadata (status, join and created timestamps).

**Business Questions:**

- How many active vs inactive B2B sales agents are there and how are they distributed by region?
- What is the average, min and max commission rate by specialization or region?
- How many agents joined each month/quarter (cohort) and what is the trend in hiring?
- Which agents are missing contact details (phone or email) and need data clean-up?
- What is the regional split of agent headcount for workforce planning?

**Key Columns:**

- **`agent_id`** (nvarchar(50), NOT NULL) - 60 distinct values
  - *Unique identifier for each sales agent (primary key). Stored as nvarchar up to 50 but actual max length ~9.*
- **`name`** (nvarchar(50), NULL) - 60 distinct values
  - *Full name of the agent for display and human identification.*
- **`phone`** (nvarchar(50), NULL) - 60 distinct values
  - *Agent contact phone number stored as string (includes country code formatting).*
- **`email`** (nvarchar(52), NULL) - 60 distinct values
  - *Agent email address used for notifications and identification.*
- **`region`** (nvarchar(50), NULL) - 8 distinct values
  - *Geographic region or city the agent is assigned to (e.g., Vadodara, Ahmedabad).*
- **`specialization`** (nvarchar(50), NULL) - 4 distinct values
  - *Agent's market specialization (Caterer, HORECA, Retail Chain, Wholesale).*
- **`commission_rate_pct`** (decimal(18,4), NULL) - 57 distinct values
  - *Commission rate for the agent expressed as percentage stored as decimal(18,4) (e.g., 3.2300 means 3.23%).*
- **`join_date`** (datetime2, NULL) - 59 distinct values
  - *Date the agent joined (datetime2). Represents tenure/cohort entry.*
- **`status`** (nvarchar(50), NULL) - 2 distinct values
  - *Operational status of the agent (ACTIVE/INACTIVE).*
- **`created_at`** (datetime2, NULL) - 60 distinct values
  - *Timestamp when the agent record was created in the system (datetime2).*

---

### b2b_sales_daily

**Rows:** 731  
**Columns:** 9  
**Primary Keys:** `date`  

**Purpose:** Daily aggregated B2B sales metrics at the customer_type level. It appears to be a pre-aggregated, time-series table used for reporting and KPI calculations (sales, discounts, tax, quantities and order counts) on a per-day basis.

**Business Questions:**

- How have daily net sales trended over the last N days and what is the week-over-week/month-over-month growth?
- What is the average daily order count and quantity (kg) for a given period, and are there days with anomalous spikes/dips?
- How much discount was given and what percentage of gross sales do discounts represent over a selected time window?
- What is the daily tax collected and how does it vary proportionally with gross sales?
- Can we compute rolling averages and detect outlier days for gross_sales, net_sales, or total_qty_kg?

**Key Columns:**

- **`date`** (datetime2, NOT NULL) - 731 distinct values
  - *The date for the aggregated metrics (datetime2). Each row corresponds to a single distinct date value.*
- **`customer_type`** (nvarchar(50), NULL) - 1 distinct values
  - *Customer segment/type for which the daily metrics are aggregated (nvarchar(50)). In this snapshot the column contains a single value 'HORECA'.*
- **`total_orders`** (decimal(18,4), NULL) - 26 distinct values
  - *Number of orders aggregated for the date and customer_type (decimal(18,4) although it represents a count).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 727 distinct values
  - *Total quantity sold in kilograms for the date and customer_type (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 731 distinct values
  - *Gross sales amount (before discounts/taxes) for the date and customer_type (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 728 distinct values
  - *Total discounts applied for the date and customer_type (decimal(18,4)).*
- **`tax_amount`** (decimal(18,4), NULL) - 731 distinct values
  - *Tax collected for the date and customer_type (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 731 distinct values
  - *Net sales amount after discounts and tax adjustments for the date and customer_type (decimal(18,4)).*
- **`created_at`** (datetime2, NULL) - 1 distinct values
  - *ETL load timestamp when this row (or the dataset) was created/loaded (datetime2). In this snapshot it has a single constant value (one ETL run time).*

---

### b2b_sales_monthly

**Rows:** 12  
**Columns:** 10  
**Primary Keys:** `month`, `year`  

**Purpose:** Monthly aggregated B2B sales metrics (one row per year+month+customer_type) used as a pre-aggregated reporting table to quickly surface month-level KPIs for B2B channels.

**Business Questions:**

- How did gross and net sales evolve month-over-month during 2024 for B2B (HORECA)?
- What is the average order size (value and quantity) per month?
- What were the monthly discount and tax amounts and their rates relative to gross sales?
- Which month had the highest total_qty_kg or total_orders in 2024?
- What is the month-over-month percentage change in net_sales or gross_sales?

**Key Columns:**

- **`year`** (bigint, NOT NULL) - 1 distinct values
  - *Calendar year for the monthly aggregate (bigint). Serves as the high-level time partition key.*
- **`month`** (bigint, NOT NULL) - 12 distinct values
  - *Numeric month (1-12) representing the calendar month of the aggregate (bigint).*
- **`customer_type`** (nvarchar(50), NULL) - 1 distinct values
  - *Categorical descriptor of the customer segment for the aggregated row (nvarchar(50)). Present data contains 'HORECA' only.*
- **`total_orders`** (decimal(18,4), NULL) - 12 distinct values
  - *Total number of B2B orders in the month (decimal to allow fractional stored values but semantically integer count).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 12 distinct values
  - *Total quantity sold in kilograms for the month (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 12 distinct values
  - *Total gross sales (pre-discount, pre-tax) for the month (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 12 distinct values
  - *Total discount value applied in the month (decimal(18,4)).*
- **`tax_amount`** (decimal(18,4), NULL) - 12 distinct values
  - *Total tax collected or applied for the month (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 12 distinct values
  - *Net sales for the month after discounts/taxes as stored in the snapshot (decimal(18,4)).*
- **`created_at`** (datetime2, NULL) - 1 distinct values
  - *Timestamp when this row/snapshot was created in the ETL (datetime2). Present data shows a single refresh timestamp.*

---

### b2b_sales_yearly

**Rows:** 1  
**Columns:** 9  
**Primary Keys:** `year`  

**Purpose:** This is an annual aggregated sales summary for B2B customers (yearly granularity). It stores pre-aggregated metrics (orders, quantity, gross/discount/tax/net sales) per year and customer_type and appears to be an ETL-produced snapshot (created_at). Its role is to provide fast, read-optimized answers to high-level questions about yearly B2B sales and to serve as a reconciliation / rollup layer against more granular tables (monthly/daily/orders).

**Business Questions:**

- What were the total net sales and gross sales for B2B customers in year X?
- How many B2B orders and how much quantity (kg) were sold in year X for a given customer_type?
- What is the discount amount and discount percentage relative to gross sales for the year?
- How did net sales change year-over-year (requires multiple rows/years)?
- When was this yearly sales snapshot generated (ETL run time)?

**Key Columns:**

- **`year`** (bigint, NOT NULL) - 1 distinct values
  - *The calendar year for the aggregated metrics (bigint). Acts as the primary key for the row(s).*
- **`customer_type`** (nvarchar(50), NULL) - 1 distinct values
  - *Categorical label for the customer segment (nvarchar(50)), e.g., 'HORECA'. May be NULL.*
- **`total_orders`** (decimal(18,4), NULL) - 1 distinct values
  - *Aggregated count of orders (decimal(18,4) stored as numeric — though conceptually an integer count).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 1 distinct values
  - *Aggregated quantity sold in kilograms (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 1 distinct values
  - *Total gross sales amount before discounts and taxes (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 1 distinct values
  - *Total discounts applied in the period (decimal(18,4)).*
- **`tax_amount`** (decimal(18,4), NULL) - 1 distinct values
  - *Total taxes charged for the period (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 1 distinct values
  - *Net sales amount after discounts and taxes (decimal(18,4)). Likely the final revenue metric used in reporting.*
- **`created_at`** (datetime2, NULL) - 1 distinct values
  - *ETL snapshot timestamp indicating when this row was created/updated (datetime2). Not a transaction date for sales — metadata for the snapshot.*

---

### b2b_shipment_tracking_events

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Stores individual shipment tracking events for B2B dispatches — timestamped location/status updates (picked, loaded, in_transit, out_for_delivery, delivered) for dispatches. Used to reconstruct shipment timelines, audit scans, and link location/device/actor information to a dispatch.

**Business Questions:**

- What is the average time from LOADED to DELIVERED per dispatch or per route?
- Which dispatches are currently OUT_FOR_DELIVERY or IN_TRANSIT and what are their last-known GPS coordinates?
- Which scanners (scanned_by) or devices generate the most events and are there anomalies (many events in short time)?
- How many events of each event_type occur per day/week and are there location hotspots (location_name) with more delays?
- For a given dispatch_id, what is the ordered timeline of events and the timestamp of the last event?

**Foreign Keys:**

- `dispatch_id` → `b2b_dispatches.dispatch_id`

**Key Columns:**

- **`tracking_event_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Unique identifier for each tracking event (string).*
- **`dispatch_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier of the dispatch this event belongs to (foreign key to b2b_dispatches.dispatch_id).*
- **`event_ts`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the tracking event occurred (datetime2).*
- **`event_type`** (nvarchar(50), NULL) - 5 distinct values
  - *Categorical event type describing the tracking state (DELIVERED, LOADED, IN_TRANSIT, OUT_FOR_DELIVERY, PICKED).*
- **`gps_lat`** (decimal(18,4), NULL) - 50 distinct values
  - *Latitude of the event's GPS capture (decimal(18,4)).*
- **`gps_long`** (decimal(18,4), NULL) - 49 distinct values
  - *Longitude of the event's GPS capture (decimal(18,4)).*
- **`scanned_by`** (nvarchar(50), NULL) - 50 distinct values
  - *Name or identifier of the person who scanned the shipment/event (string).*
- **`scan_photo_url`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Intended to store a photo URL for the scan (currently defined as decimal(18,4) but 100% nulls — likely mis-typed; should be nvarchar).*
- **`location_name`** (nvarchar(50), NULL) - 10 distinct values
  - *Human-readable location name associated with the event (city/town or facility).*
- **`status_note`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Freely-typed status note for the event (intended to be text) — currently decimal(18,4) and 100% NULL in snapshot, indicating schema mismatch or unused field.*
- *(... and 2 more columns)*

---

### b2b_vendor_partners

**Rows:** 45  
**Columns:** 10  
**Primary Keys:** `vendor_id`  

**Purpose:** Master list of B2B vendor partner records. Stores vendor identifiers and contact/metadata used by procurement, logistics, billing and partner-management processes across the B2B ecosystem.

**Business Questions:**

- How many vendors do we have by service type (Transport, Logistics, Quality Inspection, etc.)?
- Which cities have the highest concentration of vendor partners?
- How many vendors are on each credit_terms bucket (NET 7/15/30)?
- Which vendors (vendor_id/vendor_name) provide a given service_type or operate in a given city?
- Are there vendors missing GST numbers or contact details that need remediation?

**Key Columns:**

- **`vendor_id`** (nvarchar(50), NOT NULL) - 45 distinct values
  - *Unique identifier for each vendor partner (string). Designated primary key.*
- **`vendor_name`** (nvarchar(51), NULL) - 45 distinct values
  - *Display name of the vendor partner.*
- **`service_type`** (nvarchar(50), NULL) - 5 distinct values
  - *Categorical service classification for the vendor (e.g., Quality Inspection, Transport, Logistics Partner).*
- **`contact_name`** (nvarchar(50), NULL) - 45 distinct values
  - *Primary contact person's name for the vendor.*
- **`phone`** (nvarchar(50), NULL) - 45 distinct values
  - *Contact phone number for the vendor's primary contact (string to preserve formatting/country code).*
- **`email`** (nvarchar(63), NULL) - 45 distinct values
  - *Primary contact email for the vendor (string).*
- **`credit_terms`** (nvarchar(50), NULL) - 3 distinct values
  - *Payment terms offered to/used by the vendor (categorical: NET 7/15/30).*
- **`gst_no`** (bigint, NULL) - 45 distinct values
  - *Vendor GST number stored as bigint (tax identifier).*
- **`city`** (nvarchar(50), NULL) - 9 distinct values
  - *City where the vendor operates or is registered.*
- **`created_at`** (datetime2, NULL) - 1 distinct values
  - *Timestamp when the vendor record was created or loaded (datetime2).*

---

### delivery_slots

**Rows:** 80  
**Columns:** 8  
**Primary Keys:** `slot_id`  

**Purpose:** Represents delivery time slots available for order deliveries. Each row describes a unique slot (slot_id) for a specific date, start/end times, capacity and remaining availability for orders, associated with a fulfilment centre and the timestamp when the row was created. Used to manage and schedule order deliveries and to report utilization of delivery capacity.

**Business Questions:**

- Which delivery slots are available for a given date and centre?
- What is the utilization (filled orders) per slot / per centre / per date?
- Which centres have the most capacity on a given day or time window?
- What time windows are most frequently fully booked or under-utilized?
- What are the most recent changes to delivery slot definitions (new/updated slots)?

**Key Columns:**

- **`slot_id`** (nvarchar(50), NOT NULL) - 80 distinct values
  - *Unique identifier for the delivery slot (primary key).*
- **`date`** (datetime2, NULL) - 15 distinct values
  - *Date of the delivery slot (datetime2 stored, effectively a date representing the slot day).*
- **`start_time`** (nvarchar(50), NULL) - 5 distinct values
  - *Scheduled start time of the slot stored as nvarchar (formatted like '9:00', '11:00').*
- **`end_time`** (nvarchar(50), NULL) - 5 distinct values
  - *Scheduled end time of the slot stored as nvarchar (formatted like '13:00', '17:00').*
- **`capacity_orders`** (bigint, NULL) - 56 distinct values
  - *Total capacity (max orders) allowed for the slot (bigint).*
- **`available_orders`** (bigint, NULL) - 59 distinct values
  - *Remaining available order capacity for the slot (bigint).*
- **`centre_id`** (nvarchar(50), NULL) - 3 distinct values
  - *Human-readable identifier/name of the fulfilment centre or collection point (nvarchar).*
- **`created_at`** (datetime2, NULL) - 80 distinct values
  - *Timestamp when the slot row was created in the ETL process or system (datetime2).*

---

### delivery_status

**Rows:** 232  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Event-level delivery status log for shipments and orders. Each row records a delivery-related event (timestamped) including state (event_type/status), location, GPS coordinates and the operator who updated it. It is used to track the lifecycle of deliveries and to join delivery events back to orders/shipments for operational reporting and troubleshooting.

**Business Questions:**

- How many delivery attempts and what proportion failed vs delivered over a given period?
- What is the average time from LOADED to DELIVERED (or OUT_FOR_DELIVERY to DELIVERED) per city or per route?
- Which couriers/operators (updated_by) have the highest failure rates or longest resolution times?
- Which orders/shipments experienced FAILED_ATTEMPT events and what subsequent events occurred?
- Where (gps coordinates or city) are delivery failures concentrated?

**Foreign Keys:**

- `order_id` → `ecom_orders.order_id`

**Key Columns:**

- **`delivery_id`** (nvarchar(50), NULL) - 101 distinct values
  - *Identifier for the delivery event or logical delivery unit (string).*
- **`shipment_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Identifier for the shipment associated with the delivery event (string).*
- **`order_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Order identifier linking the delivery event to the original order (string). Foreign key to zuna_etl.ecom_orders.order_id.*
- **`event_ts`** (datetime2, NULL) - 232 distinct values
  - *Timestamp (datetime2) when the event occurred.*
- **`event_type`** (nvarchar(50), NULL) - 6 distinct values
  - *Type of delivery event (categorical): e.g., DELIVERED, IN_TRANSIT, OUT_FOR_DELIVERY, FAILED_ATTEMPT, LOADED, etc.*
- **`location`** (nvarchar(50), NULL) - 4 distinct values
  - *City/location name where the event occurred (string).*
- **`status`** (nvarchar(50), NULL) - 3 distinct values
  - *High-level delivery status classification (FAILED, IN_TRANSIT, DELIVERED).*
- **`updated_by`** (nvarchar(50), NULL) - 231 distinct values ⚠️ HIGH CARDINALITY
  - *Name or identifier of the operator/person/system who recorded the event (string). High cardinality.*
- **`gps_lat`** (decimal(18,4), NULL) - 228 distinct values
  - *Latitude coordinate where the event occurred (decimal(18,4)).*
- **`gps_long`** (decimal(18,4), NULL) - 232 distinct values
  - *Longitude coordinate where the event occurred (decimal(18,4)).*
- *(... and 2 more columns)*

---

### ecom_ab_test

**Rows:** 80  
**Columns:** 11  
**Primary Keys:** `test_id`  

**Purpose:** Holds meta-data and results for e-commerce A/B tests (experiments). Each row records one experiment's identity, variants, timing, status, winner and summary conversion metrics. Acts as the canonical experiment registry for analytics and product decisions.

**Business Questions:**

- How many experiments are currently RUNNING, COMPLETED, or CANCELLED?
- Which experiments resulted in variant A vs variant B winning and what is the distribution of wins?
- What is the average conversion rate for variant A and variant B across completed experiments?
- Which experiments ran during a given date range and how long did they run (duration)?
- Which tests had the largest absolute or relative difference between conversion_rate_a and conversion_rate_b?

**Key Columns:**

- **`test_id`** (nvarchar(50), NOT NULL) - 80 distinct values
  - *Unique identifier for each A/B test (primary key).*
- **`test_name`** (nvarchar(50), NULL) - 3 distinct values
  - *Human-readable name/classification of the experiment (e.g., Pricing Banner Test).*
- **`variant_a`** (nvarchar(50), NULL) - 1 distinct values
  - *Label for variant A in the test (usually 'Control').*
- **`variant_b`** (nvarchar(50), NULL) - 1 distinct values
  - *Label for variant B in the test (usually 'Treatment').*
- **`start_ts`** (nvarchar(50), NULL) - 80 distinct values
  - *Start timestamp of the experiment stored as nvarchar (e.g., '2025-08-04 15:17:40').*
- **`end_ts`** (nvarchar(50), NULL) - 80 distinct values
  - *End timestamp of the experiment stored as nvarchar (e.g., '2025-08-18 08:59:06').*
- **`status`** (nvarchar(50), NULL) - 3 distinct values
  - *Current lifecycle status of the test (RUNNING, CANCELLED, COMPLETED).*
- **`winner_variant`** (nvarchar(50), NULL) - 3 distinct values
  - *Recorded winner of the experiment: 'A', 'B', or 'NONE' (no winner or inconclusive).*
- **`conversion_rate_a`** (decimal(18,4), NULL) - 76 distinct values
  - *Summary conversion rate metric for variant A (decimal percentage, e.g., 0-100 or 0-1 depending on convention; stored as decimal(18,4)).*
- **`conversion_rate_b`** (decimal(18,4), NULL) - 75 distinct values
  - *Summary conversion rate metric for variant B (decimal(18,4)).*
- *(... and 1 more columns)*

---

### ecom_acquisition_agents

**Rows:** 55  
**Columns:** 9  
**Primary Keys:** `agent_id`  

**Purpose:** Repository of e-commerce customer acquisition agents (people/resources) used to acquire customers. Stores identity, contact, channel, geography, lifecycle timestamps and current active status. Supports attribution, channel performance, regional coverage, and agent-level reporting within the ecom analytics/operations ecosystem.

**Business Questions:**

- How many acquisition agents are active vs inactive and how has that changed over time (by join_date or created_at)?
- Which acquisition channels have the most agents and what is the geographic distribution of agents by area?
- Which agents joined within a specific date range (e.g., hires in Q1 2022)?
- Which channels or areas should be prioritized for recruiting more agents based on current agent counts?
- Is contact information available for each agent and which agents are missing phone or email?

**Key Columns:**

- **`agent_id`** (nvarchar(50), NOT NULL) - 55 distinct values
  - *Unique identifier for the acquisition agent (primary key).*
- **`name`** (nvarchar(50), NULL) - 55 distinct values
  - *Full name of the acquisition agent used for display and human-readable reports.*
- **`phone`** (nvarchar(50), NULL) - 55 distinct values
  - *Agent phone number (international format shown).*
- **`email`** (nvarchar(55), NULL) - 55 distinct values
  - *Agent email address used for notifications and login/communication.*
- **`acq_channel`** (nvarchar(50), NULL) - 5 distinct values
  - *Acquisition channel through which the agent recruits or operates (e.g., Social Media, Influencer, Referral).*
- **`area`** (nvarchar(50), NULL) - 9 distinct values
  - *Geographic area or city where the agent operates (e.g., Surat, Rajkot).*
- **`join_date`** (datetime2, NULL) - 55 distinct values
  - *Date the agent joined (onboarded). Stored as datetime2; often represents cohort membership.*
- **`status`** (nvarchar(50), NULL) - 2 distinct values
  - *Agent lifecycle status (ACTIVE or INACTIVE).*
- **`created_at`** (datetime2, NULL) - 55 distinct values
  - *Timestamp when the agent record was created in the system (ingestion/registration time).*

---

### ecom_activity_log

**Rows:** 200  
**Columns:** 8  
**Primary Keys:** *None*  

**Purpose:** Event / audit log for ecommerce operations. Tracks actions (CREATE/UPDATE/DELETE/STATUS_CHANGE) performed on entities (CUSTOMER, ORDER, PAYMENT, PRODUCT), who performed them, when, and source IP. Serves operational auditing, security monitoring, and behavioral analytics.

**Business Questions:**

- Which users or system actors performed the most DELETE or STATUS_CHANGE actions in the last 7/30 days?
- How many CREATE/UPDATE/DELETE actions happened per entity_type (ORDER/CUSTOMER/PAYMENT/PRODUCT) over a period?
- Which entity_ids (orders/customers) had the most status changes or deletions in the last month?
- From which IP addresses are most destructive actions (DELETE) being performed?
- When did a specific entity_id (e.g., EORD2073 or CUST1022) undergo CREATE, UPDATE, STATUS_CHANGE or DELETE and who performed them?

**Key Columns:**

- **`audit_id`** (nvarchar(50), NULL) - 200 distinct values
  - *Identifier for the audit event. nvarchar(50). Appears unique per row in the sample (distinct=200) but not enforced as PK.*
- **`entity_type`** (nvarchar(50), NULL) - 4 distinct values
  - *Type/category of the entity acted upon (PAYMENT, CUSTOMER, ORDER, PRODUCT). nvarchar(50) but low cardinality (4).*
- **`entity_id`** (nvarchar(50), NULL) - 126 distinct values
  - *Identifier of the entity instance the action targeted (e.g., CUST1022, EORD2086). nvarchar(50) with many distinct values (126).*
- **`action`** (nvarchar(50), NULL) - 4 distinct values
  - *Type of action performed on the entity: CREATE, UPDATE, DELETE, STATUS_CHANGE. nvarchar(50) with 4 distinct values.*
- **`action_ts`** (nvarchar(50), NULL) - 200 distinct values
  - *Timestamp (as text) when the action occurred in format 'YYYY-MM-DD HH:MM:SS'. Stored as nvarchar(50) not a native datetime.*
- **`performed_by`** (nvarchar(50), NULL) - 3 distinct values
  - *Actor who performed the action (system / support_agent / admin). nvarchar(50) with 3 distinct values.*
- **`ip_address`** (nvarchar(50), NULL) - 200 distinct values
  - *Source IP address of the action. nvarchar(50) but values look like IPv4 strings (max length 15). High cardinality.*
- **`notes`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Numeric notes field declared decimal(18,4) but contains 100% nulls in the sample. Possibly reserved for future numeric metadata or mis-typed column.*

---

### ecom_browsing_history

**Rows:** 300  
**Columns:** 9  
**Primary Keys:** `browse_id`  

**Purpose:** Stores event-level browsing interactions on the e-commerce site (searches, product views, category clicks) for analytics, product & UX optimization, and attribution.

**Business Questions:**

- Which referrer sources drive the most product views and searches?
- What are the top search queries and how do they convert to product views for specific SKUs?
- How does browsing activity vary by device type and time of day?
- Which customers have the most browsing events and which products are they viewing/searching for?
- What is the distribution of event types (SEARCH, VIEW_PRODUCT, CATEGORY_CLICK) over a given date range?

**Key Columns:**

- **`browse_id`** (nvarchar(50), NOT NULL) - 300 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for each browsing event (primary key).*
- **`customer_id`** (nvarchar(50), NULL) - 95 distinct values
  - *Logical customer identifier for the user who generated the event (may be NULL for anonymous sessions).*
- **`sku`** (nvarchar(50), NULL) - 7 distinct values
  - *Stock-keeping unit indicating the product referenced by the event (may be NULL for pure category/search events).*
- **`event_ts`** (datetime2, NULL) - 300 distinct values
  - *Timestamp when the browsing event occurred (event time).*
- **`event_type`** (nvarchar(50), NULL) - 3 distinct values
  - *Categorical field describing the kind of browsing event (e.g., SEARCH, VIEW_PRODUCT, CATEGORY_CLICK).*
- **`search_query`** (nvarchar(50), NULL) - 5 distinct values
  - *The search string entered by the user when event_type = SEARCH (may be NULL otherwise).*
- **`device_type`** (nvarchar(50), NULL) - 3 distinct values
  - *Client device type used for the event (ios, android, web).*
- **`referrer_source`** (nvarchar(50), NULL) - 4 distinct values
  - *Traffic source/referrer that brought the user to the site (e.g., FB Ads, Google, WhatsApp, Direct).*
- **`created_at`** (datetime2, NULL) - 300 distinct values
  - *Row insertion or ingestion timestamp (when the record was created in the ETL system).*

---

### ecom_cart_items

**Rows:** 150  
**Columns:** 10  
**Primary Keys:** `cart_item_id`  

**Purpose:** Stores line‑level items placed into e‑commerce carts. Each row represents a single cart item (sku/variant, quantity, price snapshot and reservation state) and is used to understand cart composition, item-level activity and pre-order/reservation behavior prior to checkout.

**Business Questions:**

- Which SKUs or variants are most frequently added to carts (top-of-cart items)?
- What is the distribution of quantities and price snapshots for cart items?
- How many items per cart do users typically add and which carts contain >N items?
- What proportion of cart items were marked reserved and how does reservation vary by SKU or time?
- When are items typically added/updated (daily/hourly trends) before checkout?

**Foreign Keys:**

- `cart_id` → `ecom_carts.cart_id`

**Key Columns:**

- **`cart_item_id`** (nvarchar(50), NOT NULL) - 150 distinct values
  - *Surrogate unique identifier for each cart line item (primary key).*
- **`cart_id`** (nvarchar(50), NULL) - 81 distinct values
  - *Identifier of the parent cart that the item belongs to (FK to ecom_carts).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Stock keeping unit code representing the product added to the cart (natural product key).*
- **`qty`** (decimal(18,4), NULL) - 10 distinct values
  - *Quantity of the SKU added to the cart for this cart item (decimal with 4 fractional digits).*
- **`added_at`** (datetime2, NULL) - 150 distinct values
  - *Timestamp when the cart item was first added to the cart.*
- **`updated_at`** (datetime2, NULL) - 150 distinct values
  - *Timestamp of the last update to the cart item (quantity change, reservation change, etc.).*
- **`reserved_flag`** (bit, NULL) - 2 distinct values
  - *Boolean flag indicating whether the item was reserved (e.g., held in inventory) when added to the cart.*
- **`price_at_add`** (bigint, NULL) - 10 distinct values
  - *Snapshot of the item's price when it was added to the cart (bigint).*
- **`variant_id`** (nvarchar(50), NULL) - 21 distinct values
  - *Identifier for the product variant associated with the cart item (e.g., size/color), complementary to sku.*
- **`notes`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Freeform or numeric notes related to the cart item. In the provided sample this column is numeric type and entirely NULL.*

---

### ecom_carts

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** `cart_id`  

**Purpose:** Represents shopping carts (active, checked-out or abandoned) captured by the e-commerce ETL. Each row is a cart instance tracked by cart_id with meta data about owner (customer_id), session, timing, value, coupon usage, device and abandonment status. It is used for customer behavior analysis, cart abandonment analysis and as a join source to cart items, orders and customers.

**Business Questions:**

- What percentage of carts are abandoned vs completed?
- What is the average total_amount and total_items by device_type or coupon_code?
- How does abandonment rate vary over time (daily/weekly) based on created_at or session?
- Which coupons are being used and what is the average cart value for each coupon?
- Which customers/sessions generate the highest cart totals and how many carts per customer exist?

**Foreign Keys:**

- `customer_id` → `ecom_customers.customer_id`

**Key Columns:**

- **`cart_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Unique identifier for the cart (primary key).*
- **`customer_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Identifier of the customer who owns the cart (nullable).*
- **`session_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Session identifier associated with the cart (nullable).*
- **`created_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp when the cart was created.*
- **`last_updated_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp of the last update to the cart (e.g., when items changed or status updated).*
- **`total_items`** (bigint, NULL) - 8 distinct values
  - *Total number of items in the cart (aggregate count of cart_items).*
- **`total_amount`** (decimal(18,4), NULL) - 100 distinct values
  - *Monetary total of the cart (decimal(18,4)).*
- **`coupon_code`** (nvarchar(50), NULL) - 2 distinct values
  - *Coupon code applied to the cart (nullable).*
- **`currency`** (nvarchar(50), NULL) - 1 distinct values
  - *Currency code for the cart monetary values (e.g., INR).*
- **`device_type`** (nvarchar(50), NULL) - 3 distinct values
  - *Device/platform used to create the cart (web/ios/android).*
- *(... and 2 more columns)*

---

### ecom_coupon_usage

**Rows:** 140  
**Columns:** 7  
**Primary Keys:** *None*  

**Purpose:** Records instances when coupons were applied to orders (coupon redemptions). It captures which coupon was used by which customer on which order, when it was applied, the discount amount given and when the usage row was created. In the schema it serves as the bridge between coupon definitions (ecom_coupons) and orders (ecom_orders) for coupon analytics and attribution.

**Business Questions:**

- How many times was each coupon redeemed in a given date range?
- What is the total and average discount provided by each coupon or across all coupons?
- Which customers redeem the most coupons and what is the average discount they receive?
- When (time-series) are coupons being applied most often (daily/weekly/monthly patterns)?
- Which orders used coupons and how much discount was applied per order (requires join to orders for order totals to compute relative discount)?

**Foreign Keys:**

- `coupon_id` → `ecom_coupons.coupon_id`
- `order_id` → `ecom_orders.order_id`

**Key Columns:**

- **`coupon_usage_id`** (nvarchar(50), NULL) - 120 distinct values
  - *Surrogate identifier for the coupon usage event (string).*
- **`coupon_id`** (nvarchar(50), NULL) - 54 distinct values
  - *Identifier of the coupon applied (foreign key to ecom_coupons).*
- **`customer_id`** (nvarchar(50), NULL) - 78 distinct values
  - *Identifier of the customer who applied the coupon (string, can be joined to ecom_customers).*
- **`order_id`** (nvarchar(50), NULL) - 84 distinct values
  - *Identifier of the order associated with the coupon application (foreign key to ecom_orders).*
- **`applied_ts`** (nvarchar(50), NULL) - 140 distinct values
  - *Timestamp string when the coupon was applied (stored as nvarchar).*
- **`discount_given`** (decimal(18,4), NULL) - 135 distinct values
  - *Monetary amount of discount applied for the usage event (decimal(18,4)).*
- **`created_at`** (datetime2, NULL) - 140 distinct values
  - *Datetime when this row was created in the ETL (datetime2).*

---

### ecom_coupons

**Rows:** 65  
**Columns:** 13  
**Primary Keys:** `coupon_id`  

**Key Columns:**

- **`coupon_id`** (nvarchar(50), NOT NULL) - 65 distinct values
- **`coupon_code`** (nvarchar(50), NULL) - 65 distinct values
- **`description`** (nvarchar(50), NULL) - 2 distinct values
- **`discount_type`** (nvarchar(50), NULL) - 2 distinct values
- **`discount_value`** (bigint, NULL) - 6 distinct values
- **`max_discount_amount`** (bigint, NULL) - 7 distinct values
- **`valid_from`** (datetime2, NULL) - 63 distinct values
- **`valid_to`** (datetime2, NULL) - 63 distinct values
- **`min_order_amount`** (bigint, NULL) - 6 distinct values
- **`usage_limit`** (bigint, NULL) - 4 distinct values
- *(... and 3 more columns)*

---

### ecom_customer_addresses

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** `address_id`  

**Purpose:** Stores customer postal and geolocation addresses for the e-commerce platform. Each row is one address belonging to a customer and is used for deliveries, analytics (geography, urban concentration), and customer-contact functions.

**Business Questions:**

- How many saved addresses does each customer have and which customers have multiple delivery locations?
- What is the distribution of customer addresses by city and by label (Home vs Work)?
- Which addresses are new in the last X days (recently added addresses) for outreach or fraud checks?
- What are the geographic clusters of customers (using latitude/longitude) to inform delivery zone planning?
- Which customers' addresses are near a given store or warehouse (proximity / nearest location)?

**Foreign Keys:**

- `customer_id` → `ecom_customers.customer_id`

**Key Columns:**

- **`address_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Unique identifier for the address (primary key).*
- **`customer_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Identifier of the customer who owns the address (FK to ecom_customers.customer_id).*
- **`label`** (nvarchar(50), NULL) - 2 distinct values
  - *Address label provided by the user (e.g., Home, Work).*
- **`addr_line1`** (nvarchar(50), NULL) - 98 distinct values
  - *Primary street address or building name for the address.*
- **`addr_line2`** (nvarchar(50), NULL) - 3 distinct values
  - *Secondary address detail (landmark or additional directions). Many repeated values and some nulls.*
- **`city`** (nvarchar(50), NULL) - 10 distinct values
  - *City of the address.*
- **`state`** (nvarchar(50), NULL) - 1 distinct values
  - *State of the address (constant: Gujarat).*
- **`pincode`** (bigint, NULL) - 99 distinct values
  - *Postal code / ZIP code for the address (numeric).*
- **`country`** (nvarchar(50), NULL) - 1 distinct values
  - *Country of the address (constant: India).*
- **`latitude`** (decimal(18,4), NULL) - 99 distinct values
  - *Latitude coordinate of the address for geolocation.*
- *(... and 2 more columns)*

---

### ecom_customer_segmentation

**Rows:** 100  
**Columns:** 7  
**Primary Keys:** `customer_id`  

**Purpose:** Stores one-row-per-customer segmentation metrics derived from transactional data (RFM segment, loyalty score, avg order value, purchase frequency, last purchase and create timestamps). Used to drive marketing, personalization, retention and analytics without re-computing base transactions each query.

**Business Questions:**

- How many customers are in each RFM segment and what is their average order value and loyalty score?
- Which customers are 'Champions' with high avg_order_value and high loyalty_score for VIP outreach?
- Which customers are 'Hibernating' or 'At Risk' and had last_purchase_date more than X days ago for re-engagement campaigns?
- What is the distribution of purchase_frequency across segments and which segments drive the highest revenue per order?
- How did the composition of RFM segments change for customers created in the last N months?

**Key Columns:**

- **`customer_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Unique identifier for each customer; logical primary key for this table (nvarchar up to 50, actual max length observed 8).*
- **`rfm_segment`** (nvarchar(50), NULL) - 4 distinct values
  - *Categorical RFM segment assigned to the customer (e.g., Champions, Regulars, At Risk, Hibernating). Low cardinality (4 distinct).*
- **`loyalty_score`** (bigint, NULL) - 59 distinct values
  - *Integer-like score (bigint) representing customer loyalty, derived from behavior/points. 59 distinct values observed.*
- **`avg_order_value`** (decimal(18,4), NULL) - 100 distinct values
  - *Average order value per customer (decimal(18,4)), pre-computed from transactional history.*
- **`purchase_frequency`** (decimal(18,4), NULL) - 84 distinct values
  - *Average purchase frequency metric per customer (decimal(18,4)), indicating how often a customer purchases over a period.*
- **`last_purchase_date`** (datetime2, NULL) - 100 distinct values
  - *Datetime of the customer's most recent purchase (datetime2). Used to measure recency.*
- **`created_at`** (datetime2, NULL) - 100 distinct values
  - *Datetime when this segmentation row or customer record was created (datetime2). Useful for cohorting by creation date or data lineage.*

---

### ecom_customers

**Rows:** 100  
**Columns:** 14  
**Primary Keys:** `customer_id`  

**Purpose:** Customer master for the e-commerce domain: stores identity, contact, demographic and engagement metadata for individual customers used by front-end, marketing, reporting and joins to transactional tables (orders, payments, addresses).

**Business Questions:**

- How many active vs inactive customers do we have and their language/gender breakdown?
- Which acquisition channels (source_channel) brought the most customers and what percent opted into marketing?
- What is the distribution of last login recency (e.g., active users in last 30/90 days)?
- What are the counts of customers by preferred_language and gender for targeted campaigns?
- Which customers lack email or phone contact information?

**Key Columns:**

- **`customer_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Surrogate natural identifier for a customer (primary key).*
- **`external_customer_code`** (nvarchar(50), NULL) - 100 distinct values
  - *Customer identifier from an external system (optional).*
- **`first_name`** (nvarchar(50), NULL) - 81 distinct values
  - *Customer given name.*
- **`last_name`** (nvarchar(50), NULL) - 90 distinct values
  - *Customer family name / surname.*
- **`email`** (nvarchar(50), NULL) - 100 distinct values
  - *Primary customer email address used for login and communication.*
- **`phone`** (nvarchar(50), NULL) - 100 distinct values
  - *Customer phone number, likely with country code and separators.*
- **`dob`** (nvarchar(50), NULL) - 100 distinct values
  - *Date of birth stored as nvarchar (format appears YYYY-MM-DD).*
- **`gender`** (nvarchar(50), NULL) - 3 distinct values
  - *Customer self-reported gender with low cardinality (Other/Male/Female).*
- **`created_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp when customer record was created (datetime2).*
- **`last_login`** (datetime2, NULL) - 100 distinct values
  - *Timestamp of the customer's last login (datetime2) — engagement metric.*
- *(... and 4 more columns)*

---

### ecom_frequently_bought

**Rows:** 100  
**Columns:** 5  
**Primary Keys:** *None*  

**Purpose:** Holds precomputed pairwise 'frequently bought together' relationships between SKUs for the e‑commerce domain. Each row represents a mapping (map_id) that links a base SKU (sku) to another SKU frequently bought with it (freq_with_sku), with an associated co_purchase_rate and a timestamp of the last update. This table is used to drive recommendations, cross-sell analyses, and product bundling heuristics across the ecom schema.

**Business Questions:**

- What are the top N SKUs most frequently bought with a given SKU (ranked by co_purchase_rate)?
- Which SKU pairs have the highest co-purchase rates across the catalog (potential bundling candidates)?
- How do co-purchase relationships change over time (requires snapshots or comparing last_updated across exports)?
- Which SKUs should be prioritized for cross-sell recommendations on product pages based on co_purchase_rate and recency?
- Are there low co_purchase_rate pairs that still appear frequently and might indicate pricing or inventory issues when combined with sales data?

**Key Columns:**

- **`map_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Unique identifier for the frequently-bought mapping record. Appears to be a mapping code (e.g., FRQ007001) and is unique per row in this snapshot.*
- **`sku`** (nvarchar(50), NULL) - 6 distinct values
  - *The base SKU for which we are listing frequently-bought-together products. Low cardinality in this table (6 distinct SKUs) and distribution is skewed toward a few top SKUs.*
- **`freq_with_sku`** (nvarchar(50), NULL) - 6 distinct values
  - *The SKU that is frequently purchased together with the base sku (the co-purchased partner SKU). Also low-cardinality and skewed.*
- **`co_purchase_rate`** (decimal(18,4), NULL) - 96 distinct values
  - *Numeric score (decimal(18,4)) representing the strength of the co-purchase relationship between sku and freq_with_sku. Higher values indicate stronger co-purchase propensity (rankable metric).*
- **`last_updated`** (nvarchar(50), NULL) - 100 distinct values
  - *Timestamp when the mapping was last refreshed. Stored as nvarchar(50) but appears to follow ISO-like 'YYYY-MM-DD HH:MM:SS' format in the data.*

---

### ecom_notifications

**Rows:** 150  
**Columns:** 9  
**Primary Keys:** `notification_id`  

**Purpose:** Stores outbound notifications (email, SMS, push) sent to customers, with message content, delivery status, and linkage to orders. Used for monitoring communication effectiveness, delivery reliability, and auditing notification history.

**Business Questions:**

- What is the delivery success rate (DELIVERED vs FAILED) overall and by notification_type (EMAIL/SMS/PUSH)?
- Which customers received the most notifications in a given period and what are their delivery outcomes?
- How many notifications are linked to orders and what is the distribution of delivery_status for order-related notifications?
- Which notification templates (title/message) lead to higher delivered rates or more order conversions?
- What are the hourly/daily patterns of sent notifications and peak sending times?

**Key Columns:**

- **`notification_id`** (nvarchar(50), NOT NULL) - 150 distinct values
  - *Unique identifier for each notification event. Primary key for the table.*
- **`customer_id`** (nvarchar(50), NULL) - 78 distinct values
  - *Identifier of the recipient customer (nullable).*
- **`notification_type`** (nvarchar(50), NULL) - 3 distinct values
  - *Channel used to send the notification (EMAIL, SMS, PUSH).*
- **`title`** (nvarchar(50), NULL) - 3 distinct values
  - *Notification subject or template title (e.g., 'Order Update', 'New Offer').*
- **`message`** (nvarchar(50), NULL) - 3 distinct values
  - *Content body (templated) of the notification message. Repeated values indicate standard templates.*
- **`sent_ts`** (nvarchar(50), NULL) - 150 distinct values
  - *Timestamp string representing when the notification was sent (stored as nvarchar).*
- **`delivery_status`** (nvarchar(50), NULL) - 3 distinct values
  - *Result of the send attempt (e.g., DELIVERED, FAILED, SENT).*
- **`linked_order_id`** (nvarchar(50), NULL) - 75 distinct values
  - *Optional reference to an order related to the notification (nullable).*
- **`created_at`** (datetime2, NULL) - 150 distinct values
  - *Datetime2 indicating when the notification record was created in the system (reliable datetime column).*

---

### ecom_orders

**Rows:** 601  
**Columns:** 19  
**Primary Keys:** `order_id`  

**Purpose:** Represents ecommerce orders (one row per order) and serves as the central fact table for order-level metrics (amounts, status, channel, timestamps). It is used to analyze sales, payments, fulfillment and campaign attribution and to join to customers, addresses, order lines and shipment tables.

**Business Questions:**

- What is total revenue (net_amount / total_amount) and order count by day/week/month and by channel?
- Which acquisition channels or campaigns produce the highest average order value and repeat customers?
- What are cancellation and refund rates by fulfillment centre, delivery slot or channel?
- How much discount and shipping cost is given per order and how do they affect net revenue?
- Which customers generate the most orders and revenue (when joined to customers)?

**Foreign Keys:**

- `customer_id` → `ecom_customers.customer_id`

**Key Columns:**

- **`order_id`** (nvarchar(50), NOT NULL) - 601 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for the order (primary key).*
- **`order_number`** (nvarchar(50), NULL) - 601 distinct values ⚠️ HIGH CARDINALITY
  - *Human-facing order reference (may include business-formatted sequence).*
- **`customer_id`** (nvarchar(50), NULL) - 98 distinct values
  - *Identifier for the customer who placed the order (FK to ecom_customers).*
- **`order_ts`** (nvarchar(50), NULL) - 463 distinct values ⚠️ HIGH CARDINALITY
  - *Timestamp of the order event stored as nvarchar (string representation of datetime).*
- **`channel`** (nvarchar(50), NULL) - 2 distinct values
  - *Sales channel through which the order was placed (e.g., Web, Mobile App).*
- **`order_status`** (nvarchar(50), NULL) - 6 distinct values
  - *Current lifecycle status of the order (PLACED, CONFIRMED, PACKED, SHIPPED, CANCELLED, etc.).*
- **`payment_status`** (nvarchar(50), NULL) - 3 distinct values
  - *Payment state of the order (PENDING, PAID, REFUNDED).*
- **`delivery_slot_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier for scheduled delivery slot for the order (links to delivery_slots table).*
- **`delivery_address_id`** (nvarchar(50), NULL) - 500 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier of the delivery address used for the order (likely links to customer address table).*
- **`total_amount`** (decimal(18,4), NULL) - 500 distinct values
  - *Gross order total before tax, discounts and shipping (decimal).*
- *(... and 9 more columns)*

---

### ecom_payment_status_log

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** `log_id`  

**Purpose:** Event / audit log of payment status transitions for e-commerce payments. Each row records a single status change attempt for a payment, including source of change, response from payment gateway, retry attempts, timestamps and processing flag. Used for debugging, monitoring payment reliability and retry behavior.

**Business Questions:**

- What percentage of payment status transitions end in FAILED vs PAID in a given date range?
- Which payment source (Manual vs PG Webhook) has higher failure rate or higher retry counts?
- How many retries are attempted on average before a payment becomes PAID or FAILED?
- Which response_code (200/402/500) is associated with most FAILED transitions?
- Which payments had multiple status changes (frequent toggling) and need manual review?

**Key Columns:**

- **`log_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Primary key for this log row; unique identifier for the payment status change event.*
- **`payment_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Identifier of the payment associated with this status change (natural join key to payments table).*
- **`status_before`** (nvarchar(50), NULL) - 3 distinct values
  - *Payment status before this change (enumerated values such as PENDING, PAID, INITIATED).*
- **`status_after`** (nvarchar(50), NULL) - 3 distinct values
  - *Payment status after this change (e.g., FAILED, PENDING, PAID).*
- **`updated_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp when the status update was recorded/occurred (datetime2).*
- **`source`** (nvarchar(50), NULL) - 2 distinct values
  - *Origin of the status update (e.g., Manual, PG Webhook).*
- **`response_code`** (bigint, NULL) - 3 distinct values
  - *Numeric response code from payment gateway or internal handling (HTTP-like codes such as 200, 402, 500).*
- **`response_body`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Intended to store the payment gateway response body but currently defined as decimal(18,4) and 100% NULL in dataset — likely incorrect type or unused.*
- **`retry_count`** (decimal(18,4), NULL) - 4 distinct values
  - *Number of retries attempted for this status change (stored as decimal but contains small integer values like 0-3).*
- **`processed_flag`** (bit, NULL) - 2 distinct values
  - *Boolean flag indicating whether the log event has been processed by downstream systems (bit).*
- *(... and 2 more columns)*

---

### ecom_payments

**Rows:** 100  
**Columns:** 14  
**Primary Keys:** `payment_id`  

**Purpose:** Stores one row per payment attempt / transaction for e-commerce orders. Tracks amount, timing, gateway, status and settlement details to enable reconciliation, payment-failure analysis and settlement reporting within the ecom domain.

**Business Questions:**

- What is the total payment amount and count by payment_mode and payment_gateway for a given date range?
- What percentage and count of payments are SUCCESS vs FAILED vs PENDING, and how does that vary by gateway?
- What is the total unsettled amount and number of UNSETTLED payments as of a given date?
- How long (median/average) does it take for payments to move from payment_ts to settlement_date (time-to-settlement)?
- Which orders have payments that are refund-eligible and what is the total potential refund exposure?

**Foreign Keys:**

- `order_id` → `ecom_orders.order_id`

**Key Columns:**

- **`payment_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Surrogate unique identifier for each payment transaction (primary key).*
- **`order_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Identifier of the order associated with the payment (FK to ecom_orders). Nullable.*
- **`payment_ts`** (nvarchar(50), NULL) - 100 distinct values
  - *Timestamp of the payment event stored as nvarchar (string). Values follow a 'YYYY-MM-DD HH:MM:SS' pattern.*
- **`amount`** (decimal(18,4), NULL) - 100 distinct values
  - *Monetary amount associated with the payment (decimal(18,4)).*
- **`payment_mode`** (nvarchar(50), NULL) - 4 distinct values
  - *High-level mode of payment (COD, NETBANKING, UPI, CARD).*
- **`payment_gateway`** (nvarchar(50), NULL) - 3 distinct values
  - *The payment processor/gateway used (e.g., Razorpay, Paytm, BankTransfer).*
- **`gateway_ref_no`** (nvarchar(50), NULL) - 100 distinct values
  - *Reference number returned by the gateway for the transaction (external id).*
- **`status`** (nvarchar(50), NULL) - 3 distinct values
  - *Execution status of the payment attempt (PENDING, FAILED, SUCCESS).*
- **`settlement_status`** (nvarchar(50), NULL) - 2 distinct values
  - *Shows whether the payment has been settled to the merchant (SETTLED or UNSETTLED).*
- **`settlement_date`** (datetime2, NULL) - 100 distinct values
  - *Datetime when the payment was settled (datetime2).*
- *(... and 4 more columns)*

---

### ecom_product_events

**Rows:** 250  
**Columns:** 8  
**Primary Keys:** `event_id`  

**Purpose:** Tracks discrete product-related events (stock and price changes) emitted by e‑commerce systems and bots. It is an audit/telemetry table used to analyze inventory and pricing lifecycle events for SKUs and to join with product/catalog/inventory tables for enrichment.

**Business Questions:**

- Which SKUs experienced the most product events in a given period?
- What is the breakdown of event types (BACK_IN_STOCK / PRICE_DROP / OUT_OF_STOCK) over time?
- Which agent (system, pricing_bot, inventory_bot) triggered the majority of events?
- What is the average latency between event_ts and created_at (ingestion delay)?
- For each SKU, what was the most recent event and when did it occur?

**Key Columns:**

- **`event_id`** (nvarchar(50), NOT NULL) - 250 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for each product event record (primary key).*
- **`sku`** (nvarchar(50), NULL) - 7 distinct values
  - *Product identifier / stock-keeping unit affected by the event.*
- **`event_ts`** (datetime2, NULL) - 250 distinct values
  - *Timestamp when the product event actually occurred (source event time).*
- **`event_type`** (nvarchar(50), NULL) - 3 distinct values
  - *Categorical type of the event (BACK_IN_STOCK, PRICE_DROP, OUT_OF_STOCK).*
- **`old_value`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Previous numeric value associated with the event (e.g., previous price or quantity). Currently populated entirely with NULLs.*
- **`new_value`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *New numeric value after the event (e.g., new price or resulting quantity). Currently populated entirely with NULLs.*
- **`triggered_by`** (nvarchar(50), NULL) - 3 distinct values
  - *Source or agent that triggered the event (system, pricing_bot, inventory_bot).*
- **`created_at`** (datetime2, NULL) - 250 distinct values
  - *Timestamp when the event record was inserted into this table (ingestion/recorded time).*

---

### ecom_product_wise_sales

**Rows:** 710  
**Columns:** 10  
**Primary Keys:** `date`  

**Purpose:** Daily product-level sales metrics for e-commerce, storing time series KPIs (orders, customers, quantities, and monetary metrics) for product-level reporting and trend analysis. It appears to be a daily snapshot of sales metrics for a product across time.

**Business Questions:**

- How have daily net sales trended over the last N days/weeks/months for the product?
- What is the average daily number of orders and customers, and how are they correlated with net sales?
- How much revenue is lost to discounts and what percentage of gross sales do discounts represent over a period?
- What is the average sold quantity (kg) per order or per customer and has it changed over time?
- How much of gross_sales is consumed by delivery fees and taxes over time (breakdown of components of net_sales)?

**Key Columns:**

- **`date`** (datetime2, NOT NULL) - 710 distinct values
  - *The date of the daily snapshot (datetime2). Values appear at midnight and represent the day for which the metrics apply.*
- **`product_id`** (nvarchar(50), NULL) - 1 distinct values
  - *Identifier for the product (nvarchar(50)). In this dataset it's constant ('TOM001'), indicating a single-product dataset.*
- **`total_orders`** (decimal(18,4), NULL) - 710 distinct values
  - *Aggregate count or sum representing total orders for the product on that date (stored as decimal(18,4)).*
- **`total_customers`** (decimal(18,4), NULL) - 709 distinct values
  - *Number of distinct customers associated with the product sales that day (decimal(18,4)). Likely an aggregate distinct count.*
- **`total_qty_kg`** (decimal(18,4), NULL) - 710 distinct values
  - *Total quantity sold in kilograms for the product on that date (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 710 distinct values
  - *Gross monetary sales for the product on that date before discounts, delivery fees, taxes (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 710 distinct values
  - *Total discount amount applied to product sales for the date (decimal(18,4)).*
- **`delivery_fee`** (decimal(18,4), NULL) - 710 distinct values
  - *Total delivery fees charged for the product on that date (decimal(18,4)). May be fees charged to customer or fees recognized as revenue depending on ETL semantics.*
- **`tax_amount`** (decimal(18,4), NULL) - 710 distinct values
  - *Total tax amount collected on product sales for the date (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 710 distinct values
  - *Net sales for the product on that date after discounts, delivery, and taxes - final recognized sales (decimal(18,4)).*

---

### ecom_ratings_summary

**Rows:** 7  
**Columns:** 6  
**Primary Keys:** `sku`  

**Key Columns:**

- **`rating_summary_id`** (nvarchar(50), NULL) - 7 distinct values
- **`sku`** (nvarchar(50), NOT NULL) - 7 distinct values
- **`avg_rating`** (decimal(18,4), NULL) - 7 distinct values
- **`total_reviews`** (bigint, NULL) - 7 distinct values
- **`last_review_ts`** (nvarchar(50), NULL) - 7 distinct values
- **`updated_at`** (datetime2, NULL) - 7 distinct values

---

### ecom_refunds

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** `refund_id`  

**Purpose:** Holds refund-level records for e-commerce orders. Each row represents one refund event (refund_id) with references to the original order and payment, timestamps, amounts, status and administrative metadata. It supports tracking refunds, reconciliation and refund-rate analytics.

**Business Questions:**

- What is the total refunded amount over a given period (day/week/month)?
- What proportion of refunds are ACCOUNT_CREDIT vs PG_REFUND and how does that vary by month?
- Which orders have the highest number/amount of refunds or repeat refunds?
- What is the breakdown of refund status (COMPLETED, INITIATED, FAILED) and trends over time?
- What are the top reasons for refunds and their associated average refund amounts?

**Foreign Keys:**

- `order_id` → `ecom_orders.order_id`

**Key Columns:**

- **`refund_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Surrogate identifier for the refund event, stored as nvarchar(50). Primary key (unique for each refund row).*
- **`order_id`** (nvarchar(50), NULL) - 39 distinct values
  - *Identifier of the order associated with the refund; nullable string and foreign key to ecom_orders.order_id.*
- **`payment_id`** (nvarchar(50), NULL) - 39 distinct values
  - *Identifier for the payment transaction associated with the refund, stored as nvarchar(50).*
- **`refund_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp of the refund event as a string (nvarchar). Appears to contain datetime-like values but stored as text.*
- **`refund_amount`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary amount refunded for the refund event (decimal(18,4)).*
- **`refund_mode`** (nvarchar(50), NULL) - 2 distinct values
  - *Method used to issue the refund (ACCOUNT_CREDIT or PG_REFUND). Low cardinality string column.*
- **`gateway_ref_no`** (nvarchar(50), NULL) - 50 distinct values
  - *Reference number assigned by payment gateway for the refund transaction (varchar).*
- **`status`** (nvarchar(50), NULL) - 3 distinct values
  - *Current state of the refund (COMPLETED, INITIATED, FAILED). Low cardinality with three values.*
- **`processed_by`** (nvarchar(50), NULL) - 1 distinct values
  - *Identifier of the team or user who processed the refund (all current values: finance_team).*
- **`processed_at`** (datetime2, NULL) - 50 distinct values
  - *Datetime when the refund was processed in the system (datetime2).*
- *(... and 2 more columns)*

---

### ecom_return_items

**Rows:** 60  
**Columns:** 10  
**Primary Keys:** `return_item_id`  

**Purpose:** Stores one row per returned item for e-commerce returns. Each record represents a specific item on a return (line-level), tracking quantity, inspection status, whether it can be restocked, and the final disposition. It is used to analyze return details, restocking decisions, and inspection outcomes.

**Business Questions:**

- Which SKUs generate the most returned quantity and how much of that quantity is restockable?
- What proportion of returned items are inspected and what are the typical inspection times?
- How are dispositions distributed (RESTOCK, DISCARD, RETURN_TO_SUPPLIER) overall and by SKU?
- Which returns (return_id) contain the largest quantity of returned items?
- How many items are restocked versus discarded over a given date range of inspection?

**Key Columns:**

- **`return_item_id`** (nvarchar(50), NOT NULL) - 60 distinct values
  - *Unique identifier for this returned item record (primary key).*
- **`return_id`** (nvarchar(50), NULL) - 29 distinct values
  - *Identifier for the overall return (a return can contain multiple return_item rows).*
- **`order_item_id`** (nvarchar(50), NULL) - 53 distinct values
  - *Identifier of the original order line / item that was returned (links returned item back to the order).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Stock Keeping Unit of the returned product; short product code used for product-level analytics.*
- **`qty`** (decimal(18,4), NULL) - 10 distinct values
  - *Quantity of units returned for this return item line (decimal with 4 decimal places).*
- **`inspected_flag`** (bit, NULL) - 2 distinct values
  - *Boolean flag indicating whether the returned item was inspected.*
- **`inspected_at`** (datetime2, NULL) - 60 distinct values
  - *Timestamp when the returned item inspection occurred.*
- **`restockable_flag`** (bit, NULL) - 2 distinct values
  - *Boolean flag indicating whether the inspected returned item can be restocked into inventory.*
- **`disposition`** (nvarchar(50), NULL) - 3 distinct values
  - *Categorical outcome assigned after inspection (e.g., RESTOCK, DISCARD, RETURN_TO_SUPPLIER).*
- **`notes`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Freeform notes or comments related to the return item. Column currently typed as decimal but observed to be 100% NULL—likely unused or mis-typed.*

---

### ecom_reviews

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** `review_id`  

**Purpose:** Customer product reviews for the e-commerce platform; stores review metadata, textual content, ratings, and minimal response/administrative fields. Used to measure product satisfaction, surface review text and titles, and link feedback to customers and SKUs.

**Business Questions:**

- Which SKUs have the most reviews and what are their average ratings?
- How has average rating (or review volume) changed over time (daily/weekly/monthly)?
- Which customers have submitted the most reviews and what are their typical ratings?
- What percentage of reviews are 4 or 5 stars versus 3 stars (overall and by SKU)?
- Which reviews are most helpful (highest helpful_count) and which titles/reviews are most common?

**Foreign Keys:**

- `customer_id` → `ecom_customers.customer_id`

**Key Columns:**

- **`review_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Unique identifier for each review (primary key).*
- **`customer_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Identifier of the customer who submitted the review; FK to ecom_customers.customer_id.*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Product SKU for the reviewed item.*
- **`rating`** (bigint, NULL) - 3 distinct values
  - *Numeric rating provided by the customer (bigint).*
- **`title`** (nvarchar(50), NULL) - 4 distinct values
  - *Short review title summarizing the customer's impression.*
- **`review_text`** (nvarchar(57), NULL) - 4 distinct values
  - *Full review text left by the customer; here appears templated with a few repeated phrases.*
- **`review_ts`** (nvarchar(50), NULL) - 100 distinct values
  - *Timestamp of the review as stored originally (nvarchar).*
- **`verified_purchase_flag`** (bit, NULL) - 1 distinct values
  - *Indicates whether the review is from a verified purchase (bit).*
- **`helpful_count`** (bigint, NULL) - 21 distinct values
  - *Number of customers who marked the review as helpful (bigint).*
- **`responded_by`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Intended to represent who responded to the review (likely user id) but currently typed decimal and contains 100% NULLs.*
- *(... and 2 more columns)*

---

### ecom_sales_daily

**Rows:** 710  
**Columns:** 11  
**Primary Keys:** `date`  

**Purpose:** Daily e-commerce sales summary aggregated at the date level for the Website order channel. It stores daily KPIs (orders, customers, quantities, revenue components and timestamps) used for reporting, trend analysis and aggregation to higher-level metrics.

**Business Questions:**

- How have gross sales and net sales trended day-by-day over a time window?
- What is the daily average order value (AOV) and how has it changed over time?
- What portion of gross sales is being lost to discounts and how does that vary daily?
- How many unique customers purchased per day and how does customer count correlate with orders?
- What is daily delivered weight (kg) and how does quantity relate to revenue and delivery/tax costs?

**Key Columns:**

- **`date`** (datetime2, NOT NULL) - 710 distinct values
  - *The calendar date for the aggregated daily metrics (datetime2, primary key). Represents the day the sales metrics belong to.*
- **`order_channel`** (nvarchar(50), NULL) - 1 distinct values
  - *The channel through which orders were placed (nvarchar(50)). In this table all rows are 'Website'.*
- **`total_orders`** (decimal(18,4), NULL) - 260 distinct values
  - *Total number of orders on that date (stored as decimal(18,4) though conceptually a count).*
- **`total_customers`** (decimal(18,4), NULL) - 218 distinct values
  - *Number of unique customers who purchased on that date (decimal stored).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 708 distinct values
  - *Total quantity shipped/sold on that date measured in kilograms (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 710 distinct values
  - *Total gross sales (revenue before discounts, fees and taxes) for the date (decimal monetary value).*
- **`discount_amount`** (decimal(18,4), NULL) - 710 distinct values
  - *Total discounts applied on that date (decimal monetary value).*
- **`delivery_fee`** (decimal(18,4), NULL) - 707 distinct values
  - *Total delivery fees collected on that date (decimal monetary value).*
- **`tax_amount`** (decimal(18,4), NULL) - 707 distinct values
  - *Total taxes charged on that date (decimal monetary value).*
- **`net_sales`** (decimal(18,4), NULL) - 710 distinct values
  - *Net sales for the date after discounts, fees and taxes (decimal monetary value).*
- *(... and 1 more columns)*

---

### ecom_sales_monthly

**Rows:** 12  
**Columns:** 12  
**Primary Keys:** `month`, `year`  

**Purpose:** Monthly aggregated e-commerce sales metrics for the Website channel. This table stores one row per year/month (monthly rollup) and is intended for reporting and trend analysis of orders, customers, quantities and monetary metrics at a monthly grain.

**Business Questions:**

- What were monthly gross and net sales for each month in 2024?
- How did total orders and total customers trend month-over-month and which month had highest orders?
- What is the average order value per month (gross_sales / total_orders) and how did it change?
- What was the total discount and delivery fee incurred each month and their share of gross sales?
- What are year-to-date totals for gross_sales, net_sales, and total_qty_kg for 2024?

**Key Columns:**

- **`year`** (bigint, NOT NULL) - 1 distinct values
  - *Calendar year for the monthly aggregate (integer/bigint). Part of the composite primary key.*
- **`month`** (bigint, NOT NULL) - 12 distinct values
  - *Calendar month number (1-12) for the aggregate. Second part of the composite primary key.*
- **`order_channel`** (nvarchar(50), NULL) - 1 distinct values
  - *Sales channel for the row (nvarchar(50)). In the sample data it's always 'Website'.*
- **`total_orders`** (decimal(18,4), NULL) - 12 distinct values
  - *Pre-aggregated total number of orders for the month (numeric stored as decimal(18,4)).*
- **`total_customers`** (decimal(18,4), NULL) - 12 distinct values
  - *Monthly total distinct customers (pre-aggregated, decimal(18,4)).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 12 distinct values
  - *Total quantity sold in kilograms for the month (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 12 distinct values
  - *Total gross sales (pre-discount) for the month (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 12 distinct values
  - *Total discounts applied for the month (decimal(18,4)).*
- **`delivery_fee`** (decimal(18,4), NULL) - 12 distinct values
  - *Total delivery fees charged in the month (decimal(18,4)).*
- **`tax_amount`** (decimal(18,4), NULL) - 12 distinct values
  - *Total tax collected for the month (decimal(18,4)).*
- *(... and 2 more columns)*

---

### ecom_sales_yearly

**Rows:** 1  
**Columns:** 11  
**Primary Keys:** `year`  

**Purpose:** Annual aggregated e-commerce sales metrics by year and order channel. It provides a pre-aggregated, year-level snapshot of orders, customers, quantities and monetary metrics to support high-level reporting and KPI calculations in the ETL layer.

**Business Questions:**

- What were the total/net/gross sales for a given year (or multiple years) and order channel?
- How many orders and unique customers did the business have in a given year, and what is the average order value?
- What proportion of revenue was given away as discounts or paid as delivery fees and taxes in a year?
- How does year-over-year net sales growth look (requires multiple rows / multiple years in table)?
- When was this yearly aggregate last generated (ETL run time) and is the snapshot up to date?

**Key Columns:**

- **`year`** (bigint, NOT NULL) - 1 distinct values
  - *Calendar year for the aggregated metrics. Primary key of the table representing the period of aggregation.*
- **`order_channel`** (nvarchar(50), NULL) - 1 distinct values
  - *The sales channel (e.g., Website, Mobile app, POS) for which the yearly aggregates are computed.*
- **`total_orders`** (decimal(18,4), NULL) - 1 distinct values
  - *Total number of orders (aggregated) for the year and channel. Stored as decimal(18,4) even though counts are typically integers, indicating it may be aggregated or averaged in upstream processing.*
- **`total_customers`** (decimal(18,4), NULL) - 1 distinct values
  - *Number of distinct customers captured in the year for the channel (stored as decimal(18,4) similar to total_orders).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 1 distinct values
  - *Total quantity sold in kilograms for the aggregated year and channel (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 1 distinct values
  - *Total gross revenue for the year before discounts, taxes and delivery fees (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 1 distinct values
  - *Total monetary value of discounts applied during the year (decimal(18,4)).*
- **`delivery_fee`** (decimal(18,4), NULL) - 1 distinct values
  - *Total delivery/shipping fees charged to customers in the year (decimal(18,4)).*
- **`tax_amount`** (decimal(18,4), NULL) - 1 distinct values
  - *Total tax collected on orders for the year (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 1 distinct values
  - *Net sales for the year after adjusting gross sales for discounts, delivery fees and taxes (decimal(18,4)).*
- *(... and 1 more columns)*

---

### ecom_search_keywords

**Rows:** 100  
**Columns:** 6  
**Primary Keys:** `keyword_id`  

**Purpose:** Holds recorded search keywords from an e-commerce/search analytics pipeline with per-keyword metrics (search volume, conversion rate) and the top associated SKU. Used to track keyword performance over time for SEO/SEM and merchandising decisions.

**Business Questions:**

- Which keywords generate the highest search volume over the recorded period?
- Which keywords have the highest conversion rate and are they also high-volume?
- Which SKU is most frequently the top SKU for high-converting or high-volume keywords?
- How has search volume or conversion rate for a given keyword changed over time?
- Which low-volume keywords have unexpectedly high conversion rates (potential niche opportunities)?

**Key Columns:**

- **`keyword_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Unique identifier for the keyword record (string). Primary key of the table.*
- **`keyword`** (nvarchar(50), NULL) - 9 distinct values
  - *The search term or keyword string (e.g., 'potato', 'organic veg').*
- **`search_volume`** (bigint, NULL) - 100 distinct values
  - *Numeric count indicating search volume or estimated searches for the keyword (bigint).*
- **`conversion_rate`** (decimal(18,4), NULL) - 97 distinct values
  - *Conversion rate for the keyword represented as a decimal (decimal(18,4)), likely a percentage value (e.g., 2.4800 meaning 2.48%).*
- **`top_sku`** (nvarchar(50), NULL) - 7 distinct values
  - *The SKU most associated with the keyword (string). Represents the top product shown or clicked for this keyword.*
- **`created_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp when this keyword metric record was recorded (datetime2).*

---

### ecom_ticket

**Rows:** 100  
**Columns:** 10  
**Primary Keys:** `ticket_id`  

**Purpose:** Records customer support tickets for the e-commerce system. Each row represents one ticket raised by a customer (optionally tied to an order), its current status/priority, timestamps, and which agent owns it. The table supports operational monitoring of support workload and basic customer-service analytics.

**Business Questions:**

- How many tickets are open / in progress / resolved over a given time range?
- Which agents have the highest number of high-priority tickets assigned?
- What is the average time to update or resolve tickets (created_at -> updated_at) by priority or subject?
- Which customers submit the most tickets and what issues do they report most often?
- How many tickets are linked to orders and which orders generate the most tickets?

**Foreign Keys:**

- `customer_id` → `ecom_customers.customer_id`

**Key Columns:**

- **`ticket_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Unique identifier for each support ticket (primary key).*
- **`customer_id`** (nvarchar(50), NULL) - 60 distinct values
  - *Identifier of the customer who raised the ticket; nullable if ticket not tied to a customer record.*
- **`subject`** (nvarchar(50), NULL) - 4 distinct values
  - *Categorized short subject of the ticket (e.g., Delivery Delay, Order Issue).*
- **`description`** (nvarchar(50), NULL) - 4 distinct values
  - *Short textual description of the issue. Often templated in this dataset.*
- **`status`** (nvarchar(50), NULL) - 4 distinct values
  - *Current lifecycle state of the ticket (OPEN, IN_PROGRESS, RESOLVED, CLOSED).*
- **`priority`** (nvarchar(50), NULL) - 3 distinct values
  - *Business priority assigned to the ticket (LOW, MEDIUM, HIGH).*
- **`created_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp when the ticket was created.*
- **`updated_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp of the last update to the ticket record.*
- **`order_id`** (nvarchar(50), NULL) - 53 distinct values
  - *References an order related to the ticket (nullable); ties ticket to a specific purchase or order event.*
- **`assigned_to`** (nvarchar(50), NULL) - 3 distinct values
  - *Identifier of the support agent or owner responsible for the ticket (e.g., ops_manager, support_agent_1).*

---

### ecom_ticket_messages

**Rows:** 293  
**Columns:** 7  
**Primary Keys:** *None*  

**Purpose:** Stores individual messages exchanged on support tickets (both customer and support messages). Acts as the conversation log for e-commerce tickets and is used to understand ticket timelines, response behavior, and message content.

**Business Questions:**

- How many messages are associated with each ticket and which tickets have the most messages?
- What is the distribution of messages by sender (support vs customer) and average messages per ticket by sender?
- What is the typical time between successive messages on a ticket (median/average response time) and support response latency?
- Which tickets had the most recent activity in a given date range (by created_at or message_ts)?
- What are the common message texts or patterns and how often do automated/common responses occur?

**Foreign Keys:**

- `ticket_id` → `ecom_ticket.ticket_id`

**Key Columns:**

- **`ticket_message_id`** (nvarchar(50), NULL) - 293 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for each ticket message (nvarchar(50)). Presently no PK constraint enforced in DDL.*
- **`ticket_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Identifier of the ticket to which the message belongs (foreign key to ecom_ticket.ticket_id). nvarchar(50).*
- **`message_ts`** (nvarchar(50), NULL) - 293 distinct values ⚠️ HIGH CARDINALITY
  - *Message timestamp stored as nvarchar(50) (format examples look like 'YYYY-MM-DD HH:MM:SS'). Represents when the message content was created/sent (may be same or different from created_at).*
- **`sender`** (nvarchar(50), NULL) - 2 distinct values
  - *Who sent the message (small set of values, e.g., 'support' or 'customer'). nvarchar(50) but only 2 distinct values observed.*
- **`message_text`** (nvarchar(50), NULL) - 4 distinct values
  - *Text body of the message (nvarchar(50)). In this dataset only 4 distinct messages are present; likely templated or truncated content.*
- **`attachment_url`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Intended to store a URL to an attachment; currently typed as decimal(18,4) and 100% NULL in the sample. Column appears mis-typed and unused.*
- **`created_at`** (datetime2, NULL) - 293 distinct values
  - *Row ingestion/creation timestamp (datetime2). Represents when the message row was created in the ETL or database.*

---

### ecom_vendors

**Rows:** 50  
**Columns:** 11  
**Primary Keys:** `vendor_id`  

**Purpose:** Master vendor reference for e-commerce/pos/B2B systems. Stores vendor identity, contact, tax identifiers, location and lifecycle status used to enrich transactions, payments, contracts and operational records across the schema.

**Business Questions:**

- How many vendors do we have by category and by city?
- How many vendors are ACTIVE vs INACTIVE, and which ones are inactive?
- Which vendors are missing or have malformed tax identifiers (GST/PAN) or contact info?
- List contact details (phone/email/billing address) for a specific vendor or set of vendors.
- Which vendors belong to a given category (e.g., Influencer) so we can target communications?

**Key Columns:**

- **`vendor_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for a vendor (logical primary key).*
- **`vendor_name`** (nvarchar(50), NULL) - 49 distinct values
  - *Human-readable name of the vendor.*
- **`vendor_category`** (nvarchar(50), NULL) - 5 distinct values
  - *Categorical classification of vendor (Ad Agency, Courier, Influencer, Marketing, Tech).*
- **`phone`** (nvarchar(50), NULL) - 50 distinct values
  - *Vendor contact phone number (country code + digits, spaces present).*
- **`email`** (nvarchar(61), NULL) - 49 distinct values
  - *Vendor contact email address.*
- **`billing_address`** (nvarchar(75), NULL) - 50 distinct values
  - *Vendor billing address (free-form).*
- **`gst_no`** (bigint, NULL) - 50 distinct values
  - *Vendor GST number stored as bigint (tax identifier).*
- **`pan_no`** (nvarchar(50), NULL) - 50 distinct values
  - *Vendor PAN (Permanent Account Number) as nvarchar (typical length ~10).*
- **`city`** (nvarchar(50), NULL) - 9 distinct values
  - *Vendor city (normalized to a small set; 9 distinct values present).*
- **`status`** (nvarchar(50), NULL) - 2 distinct values
  - *Lifecycle status of vendor: ACTIVE or INACTIVE.*
- *(... and 1 more columns)*

---

### ecom_wishlist

**Rows:** 100  
**Columns:** 6  
**Primary Keys:** *None*  

**Purpose:** Customer wishlist records for the e-commerce pipeline; captures which SKUs customers have added to their wishlist, when they added them, and whether they marked them as priority. Serves as a lightweight behavioral / intent dataset that can be joined to customer and product master tables to drive personalization, marketing, and inventory planning.

**Business Questions:**

- Which SKUs are most commonly added to wishlists (overall and in a given time window)?
- Which customers have the most items in their wishlist, and which customers have high-priority wishlist items?
- How many wishlist additions occurred per day / week / month, and are there temporal spikes tied to events or campaigns?
- Which priority wishlist items are yet to convert to purchases (requires join to orders/order_lines)?
- What proportion of customers add items to wishlists (requires join to customer base) and which segments are most engaged?

**Key Columns:**

- **`wishlist_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Unique identifier for the wishlist entry (nvarchar(50)). In this dataset it appears unique per row (distinct = 100) but there is no declared primary key constraint.*
- **`customer_id`** (nvarchar(50), NULL) - 65 distinct values
  - *Identifier for the customer who created the wishlist entry (nvarchar(50)). 65 distinct customers across 100 rows, nullable.*
- **`sku`** (nvarchar(50), NULL) - 7 distinct values
  - *Stock-keeping unit for the product added to the wishlist (nvarchar(50)). Low cardinality (7 distinct SKUs) with strong skew toward a few top SKUs.*
- **`added_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp (datetime2) when the SKU was added to the wishlist. Distinct for most rows (100 distinct values). Nullable.*
- **`priority_flag`** (bit, NULL) - 2 distinct values
  - *Boolean/bit indicating whether the wishlist item is marked as priority (bit). Distribution approximately 46% True, 54% False.*
- **`notes`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Decimal(18,4) column named 'notes' that is fully NULL in this dataset (100% nulls). Likely a legacy or mis-typed column; semantics unclear (could be rating, score, or notes placeholder).*

---

### inventory_items

**Rows:** 100  
**Columns:** 12  
**Primary Keys:** `item_id`  

**Purpose:** Inventory items ledger capturing per-item stock, batch, date, supplier and cost metadata. It is the canonical table for on-hand inventory details used for stock valuation, expiry/age tracking, and linking physical inventory to product master and downstream sales/returns records.

**Business Questions:**

- What is the total on-hand quantity and inventory value by SKU / product name?
- Which batches are expiring within the next N days and what quantities are at risk?
- How much stock did we receive in a given date range and from which suppliers?
- Which suppliers contribute the most stock and cost exposure?
- What is the average cost per unit by SKU and how does cost change over time?

**Key Columns:**

- **`item_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Unique identifier for each inventory item/record (primary key).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Stock keeping unit — product-level code mapping the inventory record to product/master data.*
- **`name`** (nvarchar(50), NULL) - 10 distinct values
  - *Human-readable product name associated with the inventory item.*
- **`total_stock_units`** (decimal(18,4), NULL) - 97 distinct values
  - *Quantity on hand for the inventory item (decimal, supports fractional units).*
- **`batch_id`** (nvarchar(50), NULL) - 99 distinct values
  - *Identifier for a received production/shipment batch for traceability.*
- **`received_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp when the inventory was received into stock (datetime2).*
- **`expiry_date`** (datetime2, NULL) - 29 distinct values
  - *Expiry date for the inventory item/batch (datetime2).*
- **`supplier`** (nvarchar(50), NULL) - 3 distinct values
  - *Name of the supplier who provided the inventory (categorical, 3 main suppliers).*
- **`cost_per_unit`** (decimal(18,4), NULL) - 100 distinct values
  - *Unit cost for the inventory item (decimal) used for valuation.*
- **`mfg_date`** (datetime2, NULL) - 68 distinct values
  - *Manufacturing/production date of the inventory item (datetime2).*
- *(... and 2 more columns)*

---

### order_items

**Rows:** 217  
**Columns:** 14  
**Primary Keys:** `order_item_id`  

**Purpose:** Represents individual items (line-level) on e-commerce orders. Each row is one ordered product/variant with quantity, pricing, tax, batch and timestamps. Used to compute revenue, quantities, fulfillment/picking metrics and to join order-level context from ecom_orders or product metadata from product tables.

**Business Questions:**

- What are the top-selling SKUs by units and by revenue in a given date range?
- How much revenue and tax did each order generate (requires grouping by order_id or joining to orders)?
- Which batches had the highest number of picked items or highest value of goods?
- What is the average unit price per SKU or variant and how has it changed over time?
- How long between item created_at and picked_at on average (fulfillment latency)?

**Foreign Keys:**

- `order_id` → `ecom_orders.order_id`

**Key Columns:**

- **`order_item_id`** (nvarchar(50), NOT NULL) - 217 distinct values ⚠️ HIGH CARDINALITY
  - *Unique identifier for the order line item (primary key).*
- **`order_id`** (nvarchar(50), NULL) - 217 distinct values ⚠️ HIGH CARDINALITY
  - *Identifier for the parent order (foreign key to ecom_orders.order_id).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Stock Keeping Unit — marketplace/product code identifying item family.*
- **`product_name`** (nvarchar(50), NULL) - 10 distinct values
  - *Human-readable product name for the line item.*
- **`variant_id`** (nvarchar(50), NULL) - 10 distinct values
  - *Identifier for a specific variant of the product (size, packaging, etc.).*
- **`qty_units`** (bigint, NULL) - 20 distinct values
  - *Quantity in countable units (e.g., number of packs or items).*
- **`qty_kg`** (decimal(18,4), NULL) - 20 distinct values
  - *Quantity expressed in kilograms (decimal with 4 decimal points).*
- **`unit_price`** (decimal(18,4), NULL) - 10 distinct values
  - *Price per unit (or per kg depending on item) at the time of order.*
- **`line_total`** (decimal(18,4), NULL) - 102 distinct values
  - *Total monetary value for the line (unit_price * quantity minus discounts plus taxes depending on business logic).*
- **`tax_amount`** (decimal(18,4), NULL) - 102 distinct values
  - *Tax charged for the line item.*
- *(... and 4 more columns)*

---

### pos_daily_sales_summary

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** `summary_id`  

**Purpose:** Daily aggregated point-of-sale (POS) metrics per store. Each row is a single-day summary for a store (or a single summary row) containing counts and monetary aggregates used by analytics, reporting and ETL validation.

**Business Questions:**

- Which stores had the highest total_sales over a given date range?
- How did average transaction value (avg_txn_value) trend over the last N days for each store?
- What percentage of sales is being refunded (total_refunds / total_sales) per store or day?
- Which days had unusually high transaction counts or sales (outlier detection) across stores?
- Is the ETL job running correctly (latest created_at per date) and when was each daily summary produced?

**Key Columns:**

- **`summary_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Surrogate/unique identifier for the daily summary row. Primary key of the table.*
- **`store_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Identifier for the POS store the summary applies to (logical store key).*
- **`date`** (datetime2, NULL) - 24 distinct values
  - *The date (day) that the summary covers. Stored as datetime2 but semantically a date (midnight times observed).*
- **`total_txns`** (decimal(18,4), NULL) - 46 distinct values
  - *Total number of transactions (stored as decimal) for the day/store summary. Represents transaction count.*
- **`total_sales`** (decimal(18,4), NULL) - 50 distinct values
  - *Total gross sales amount for the day and store (monetary value).*
- **`total_tax`** (decimal(18,4), NULL) - 50 distinct values
  - *Total tax amount collected for the day/store.*
- **`total_refunds`** (decimal(18,4), NULL) - 50 distinct values
  - *Total amount refunded to customers for the day/store.*
- **`avg_txn_value`** (decimal(18,4), NULL) - 50 distinct values
  - *Precomputed average transaction value for the day/store (probably total_sales / total_txns). Stored for convenience/fast read.*
- **`created_at`** (datetime2, NULL) - 50 distinct values
  - *ETL insertion or summary creation timestamp (when this summary row was written).*
- **`notes`** (nvarchar(50), NULL) - 1 distinct values
  - *Free-text notes for the summary row. In this dataset it is constant ('Daily summary').*

---

### pos_inventory_adjustments

**Rows:** 50  
**Columns:** 11  
**Primary Keys:** `adjustment_id`  

**Purpose:** Stores point-of-sale inventory adjustment events. Each row records a single manual/system adjustment to on‑hand inventory for a given POS SKU at a store, with who performed the adjustment, who approved it, the reason, inventory before/after, and timestamps. This table is used for reconciliation, shrinkage tracking, audit, and operational investigations.

**Business Questions:**

- Which SKUs and stores have the largest negative adjustments (shrinkage) over a period?
- What are the main reasons for adjustments and their counts/volumes (Shrinkage vs Damage vs Stock Count Correction)?
- Which users make or approve the most adjustments and what are their average adjustment sizes?
- Are there adjustments where inventory_after != inventory_before + qty_change (data integrity issues)?
- What is the time distribution/trend of adjustments (daily/hourly) and peak adjustment windows?

**Key Columns:**

- **`adjustment_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Surrogate unique identifier for the inventory adjustment event (primary key).*
- **`pos_sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Point-of-sale SKU identifier for the product adjusted.*
- **`store_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Identifier of the store where the adjustment occurred.*
- **`adjustment_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp of when the adjustment occurred as recorded (stored as nvarchar formatted like 'YYYY-MM-DD HH:MM:SS').*
- **`qty_change`** (bigint, NULL) - 19 distinct values
  - *Net change in inventory quantity caused by the adjustment; can be negative (removal) or positive (addition).*
- **`reason`** (nvarchar(50), NULL) - 3 distinct values
  - *Categorized reason for the adjustment (e.g., Shrinkage, Stock Count Correction, Damage).*
- **`adjusted_by`** (nvarchar(50), NULL) - 3 distinct values
  - *User identifier for the person who made the adjustment.*
- **`approval_by`** (nvarchar(50), NULL) - 3 distinct values
  - *User identifier for the approver of the adjustment.*
- **`inventory_before`** (bigint, NULL) - 48 distinct values
  - *Recorded on-hand inventory count for the SKU at the store immediately before the adjustment.*
- **`inventory_after`** (bigint, NULL) - 50 distinct values
  - *Recorded on-hand inventory count for the SKU at the store immediately after the adjustment.*
- *(... and 1 more columns)*

---

### pos_loyalty_redemptions

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** `redemption_id`  

**Purpose:** Records individual loyalty redemptions at POS: which customer redeemed points, how many points were used, the discount applied, when and where the redemption occurred, and audit attributes. Serves as the source of truth for loyalty redemptions and links loyalty behavior to transactions, stores and customers.

**Business Questions:**

- How many loyalty redemptions occurred in a given date range and how has that trended over time?
- What is the total and average discount amount and points redeemed per store or per customer?
- Which customers redeem the most loyalty points and what is the monetary value of their redemptions?
- How do redemptions correlate with POS transactions (e.g., percent of transactions that used loyalty) and which terminals/stores have the highest redemption rate?
- Are there unusual approval patterns or approvals that require investigation (e.g., approvals with unusually high discount amounts)?

**Key Columns:**

- **`redemption_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for each loyalty redemption record (primary key).*
- **`customer_id`** (nvarchar(50), NULL) - 39 distinct values
  - *Identifier of the customer who redeemed loyalty points; links to customer master data.*
- **`pos_txn_id`** (nvarchar(50), NULL) - 40 distinct values
  - *POS transaction identifier associated with the redemption; ties the redemption to a specific sale transaction.*
- **`loyalty_points_used`** (bigint, NULL) - 49 distinct values
  - *Number of loyalty points consumed in the redemption event.*
- **`discount_amount`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary discount applied due to loyalty redemption (decimal with 4 fractional digits).*
- **`redeemed_at`** (datetime2, NULL) - 50 distinct values
  - *Timestamp when the loyalty points were redeemed (datetime2).*
- **`store_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Identifier of the store/location where the redemption occurred.*
- **`created_by`** (nvarchar(50), NULL) - 3 distinct values
  - *Identifier for the user or process that created the redemption record (likely POS user).*
- **`approval_id`** (nvarchar(50), NULL) - 49 distinct values
  - *Identifier for an approval associated with the redemption (audit/manager approval reference).*
- **`notes`** (nvarchar(50), NULL) - 1 distinct values
  - *Free-text notes about the redemption; appears constant ('Loyalty redemption') in current snapshot.*

---

### pos_product_wise_sales

**Rows:** 731  
**Columns:** 7  
**Primary Keys:** `date`  

**Purpose:** Daily product-level point-of-sale (POS) sales metrics for (currently) a single product. It records date-stamped aggregated sales quantities and monetary measures (gross, discount, tax, net) at product granularity, supporting time-series and KPI calculations for that product in the ETL layer.

**Business Questions:**

- How does daily net sales for product TOM001 trend over time (day/week/month)?
- What is the average selling price per kg and how has it changed over time?
- Which dates had the largest discounts (absolute and percent) and how did that affect net sales?
- What share of gross sales is taken by tax and discount over a given period?
- What are 7-day and 30-day rolling averages of net_sales and total_qty_kg to smooth seasonality?

**Key Columns:**

- **`date`** (datetime2, NOT NULL) - 731 distinct values
  - *The date/time the aggregated metrics relate to. Stored as datetime2 (no timezone). In practice this appears to be one row per calendar date (time portion zeroed).*
- **`product_id`** (nvarchar(50), NULL) - 1 distinct values
  - *Identifier of the product for which metrics are recorded (nvarchar(50)). Currently only one distinct value (TOM001). Nullable in DDL but populated in data.*
- **`total_qty_kg`** (decimal(18,4), NULL) - 731 distinct values
  - *Total quantity sold for that product on the date, measured in kilograms (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 731 distinct values
  - *Gross monetary sales amount for that product on the date before discounts and taxes (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 731 distinct values
  - *Total discount applied to sales for that product on the date (decimal(18,4)).*
- **`tax_amount`** (decimal(18,4), NULL) - 731 distinct values
  - *Total tax collected for that product on the date (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 731 distinct values
  - *Net sales amount for that product on the date after discounts and including taxes (decimal(18,4)). Represents the final revenue recognized in this ETL table.*

---

### pos_products

**Rows:** 10  
**Columns:** 12  
**Primary Keys:** `sku`  

**Purpose:** POS product master for a single store extracted into the zuna_etl schema. It stores point-of-sale specific product identifiers (pos_sku), canonical SKU, pricing, tax, stock and replenishment info used by POS reporting, inventory reconciliation and simple merchandising/ordering decisions.

**Business Questions:**

- Which products are below their reorder point and need replenishment at the POS?
- What are the current POS prices for SKUs and how do they compare across other channels (after joining with product_pricing)?
- What is the available stock quantity for a given SKU or PLU code at this store?
- Which SKUs were updated within a specific time window (recent price/stock updates)?
- What products have the UOM kg vs smaller pack sizes (250g, 500g) for pack-size based promotions?

**Key Columns:**

- **`pos_sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Point-of-sale specific SKU code (POS-level item variant identifier). Often includes suffixes (e.g., size/pack) and is distinct per POS item.*
- **`sku`** (nvarchar(50), NOT NULL) - 10 distinct values
  - *Canonical SKU (business product identifier). Declared NOT NULL and acts as the logical primary key in this extract.*
- **`store_id`** (nvarchar(50), NULL) - 1 distinct values
  - *Store identifier for the POS extract (store location code). In this data extract there is only one distinct value.*
- **`plucode`** (decimal(18,4), NULL) - 10 distinct values
  - *Numeric PLU code often used by scale or POS devices to identify produce/weighed items.*
- **`name`** (nvarchar(50), NULL) - 10 distinct values
  - *Human-readable product name as presented in POS (may include pack/weight info).*
- **`uom`** (nvarchar(50), NULL) - 3 distinct values
  - *Unit of measure or pack-size for the POS item (e.g., kg, 250g, 500g).*
- **`pos_price`** (decimal(18,4), NULL) - 10 distinct values
  - *Current POS selling price for the item (per POS UOM).*
- **`tax_rate`** (decimal(18,4), NULL) - 1 distinct values
  - *Tax rate applied at POS for the item (decimal). In this extract it is constant at 0.05.*
- **`stock_qty`** (decimal(18,4), NULL) - 10 distinct values
  - *Current POS stock quantity for the item (in the unit indicated by uom).*
- **`reorder_point`** (decimal(18,4), NULL) - 9 distinct values
  - *Threshold quantity that triggers reorder for the POS item.*
- *(... and 2 more columns)*

---

### pos_products_sales

**Rows:** 10  
**Columns:** 5  
**Primary Keys:** `sku`  

**Purpose:** This table stores aggregated point-of-sale level sales metrics per product SKU. It appears to capture gross sales, discounts applied, tax amounts and resulting net sales for each SKU, intended for POS reporting, product performance and downstream analytics.

**Business Questions:**

- Which SKUs generated the highest net sales in the POS channel?
- What is the total gross sales, total discounts and total net sales across all SKUs?
- Which SKUs have the highest discount amounts or discount rates (discount as % of gross)?
- Are there SKUs where net_sales does not equal gross_sales - discount_amount (possible data quality issue)?
- What is the total tax collected per SKU and how does tax compare to gross/net sales?

**Key Columns:**

- **`sku`** (nvarchar(50), NOT NULL) - 10 distinct values
  - *Product identifier (SKU) used to attribute sales metrics to specific products. Declared nvarchar(50) but observed max length is 6 and all values are distinct in this sample.*
- **`gross_sales`** (decimal(18,4), NULL) - 10 distinct values
  - *Total gross sales amount for the SKU before discounts and (apparently) before removing discounts. Decimal(18,4) for monetary precision.*
- **`discount_amount`** (decimal(18,4), NULL) - 10 distinct values
  - *Total discount amount applied to the SKU at POS. Decimal(18,4).*
- **`tax_amount`** (decimal(18,4), NULL) - 10 distinct values
  - *Taxes collected for the SKU. Decimal(18,4). In the sample it appears stored separately and not included in net_sales calculation.*
- **`net_sales`** (decimal(18,4), NULL) - 10 distinct values
  - *Net sales amount for the SKU after discounts (observed = gross_sales - discount_amount). Decimal(18,4).*

---

### pos_returns

**Rows:** 50  
**Columns:** 11  
**Primary Keys:** *None*  

**Purpose:** Records point-of-sale return events processed by the POS system. Each row describes a single returned item instance (or line) with metadata needed to analyze return volume, financial impact (refunds), reason codes, handling staff and whether items were restocked or required approval. It is an operational/ETL staging table used for return analytics and reconciliation with sales/finance systems.

**Business Questions:**

- What is the total refunded amount for the period (daily/weekly/monthly)?
- Which SKUs generate the most returns (by count and refund amount)?
- What are the top reasons for returns and their contribution to refund totals?
- Which POS operators process the most returns or the highest refund amounts?
- How many returned items were restocked vs not restocked, and how does that affect inventory?

**Key Columns:**

- **`pos_return_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Unique identifier for the POS return event/line (string). In the sample each value appears distinct for each row.*
- **`pos_txn_id`** (nvarchar(50), NULL) - 34 distinct values
  - *Identifier of the original POS transaction associated with the return (string).*
- **`return_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp of the return event as stored by the POS system, currently as nvarchar (text).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Stock keeping unit code of the returned product (string).*
- **`qty`** (decimal(18,4), NULL) - 5 distinct values
  - *Quantity of units returned for this line (decimal but represents integer counts in practice).*
- **`reason`** (nvarchar(50), NULL) - 3 distinct values
  - *Categorical reason code for the return (e.g., Wrong Item, Customer Return, Damaged).*
- **`refund_amount`** (decimal(18,4), NULL) - 50 distinct values
  - *Monetary amount refunded for this return line (decimal).*
- **`processed_by`** (nvarchar(50), NULL) - 3 distinct values
  - *Identifier of the POS user/operator who processed the return (string).*
- **`approval_required_flag`** (bit, NULL) - 2 distinct values
  - *Boolean flag indicating whether managerial approval was required for the return (bit).*
- **`restock_flag`** (bit, NULL) - 2 distinct values
  - *Boolean flag indicating whether the returned item was restocked into inventory (bit).*
- *(... and 1 more columns)*

---

### pos_sales_daily

**Rows:** 2,193  
**Columns:** 9  
**Primary Keys:** `date`, `store_id`  

**Purpose:** Daily point-of-sale (POS) aggregated sales metrics per store. Each row represents a single store's consolidated daily performance (counts, quantities, and monetary measures) used for reporting, trend analysis, and rollups into higher-level reports.

**Business Questions:**

- How did net sales change by store over the last N days or months?
- Which store had the highest average gross sales per day in a given month?
- What is the daily trend of total quantity sold (kg) across all stores?
- What is the average discount amount and discount rate applied per store per period?
- How many bills (transactions) occurred per store per day and what is the average sale per bill?

**Key Columns:**

- **`date`** (datetime2, NOT NULL) - 731 distinct values
  - *The day for which the sales aggregates are reported (datetime2, stored at midnight). Acts as the time dimension for the aggregated metrics.*
- **`store_id`** (nvarchar(50), NOT NULL) - 3 distinct values
  - *Identifier for the store reporting the daily metrics (nvarchar(50); three distinct values in this dataset).*
- **`total_bills`** (decimal(18,4), NULL) - 111 distinct values
  - *Total number of bills/transactions for that store on that date (stored as decimal(18,4) though logically an integer count).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 2,130 distinct values
  - *Total quantity sold in kilograms for that store/day (decimal with high cardinality).*
- **`gross_sales`** (decimal(18,4), NULL) - 2,192 distinct values
  - *Total gross sales amount for the store on that date before discounts/taxes (decimal).*
- **`discount_amount`** (decimal(18,4), NULL) - 2,159 distinct values
  - *Total discounts applied on that date for the store (monetary amount as decimal).*
- **`tax_amount`** (decimal(18,4), NULL) - 2,157 distinct values
  - *Total tax collected for that store on that date (decimal).*
- **`net_sales`** (decimal(18,4), NULL) - 2,191 distinct values
  - *Final net sales amount for the store on that date (likely gross minus discounts plus tax or pre-calculated net metric).*
- **`created_at`** (datetime2, NULL) - 1 distinct values
  - *ETL/record creation timestamp (datetime2). In this dataset it is constant, indicating an ETL or load timestamp rather than row-level event time.*

---

### pos_sales_monthly

**Rows:** 36  
**Columns:** 10  
**Primary Keys:** `month`, `store_id`, `year`  

**Purpose:** Monthly aggregated point-of-sale (POS) sales metrics per store. This table stores one row per store-month (composite key: year, month, store_id) and is used as the canonical monthly summary for POS reporting and cross-channel comparisons.

**Business Questions:**

- Which store had the highest net sales in a given month?
- How did gross and net sales change month-over-month across stores for 2024?
- What is the total discount and tax amount given by store for the year-to-date?
- What is the average number of bills and average bill value (gross_sales/total_bills) by store for a selected period?
- What percentage share of total net sales does each store contribute for a selected month or year-to-date?

**Key Columns:**

- **`year`** (bigint, NOT NULL) - 1 distinct values
  - *Calendar year for the monthly aggregation (e.g., 2024). Part of the composite key identifying the row.*
- **`month`** (bigint, NOT NULL) - 12 distinct values
  - *Month number (1-12) for the aggregation. Part of the composite key with year and store_id.*
- **`store_id`** (nvarchar(50), NOT NULL) - 3 distinct values
  - *Identifier for the store (e.g., STORE_AHD_01). Part of composite key and primary store dimension for analysis.*
- **`total_bills`** (decimal(18,4), NULL) - 34 distinct values
  - *Number of bills/receipts issued in the month for the store. Numeric, stored as decimal(18,4) though logically integer counts.*
- **`total_qty_kg`** (decimal(18,4), NULL) - 36 distinct values
  - *Total quantity sold in kilograms for the store-month. Decimal(18,4).*
- **`gross_sales`** (decimal(18,4), NULL) - 36 distinct values
  - *Total gross sales (pre-discount and pre-tax) for the store-month. Decimal(18,4).*
- **`discount_amount`** (decimal(18,4), NULL) - 36 distinct values
  - *Total discount amount given in the month for the store. Decimal(18,4).*
- **`tax_amount`** (decimal(18,4), NULL) - 36 distinct values
  - *Total tax collected for the store-month. Decimal(18,4).*
- **`net_sales`** (decimal(18,4), NULL) - 36 distinct values
  - *Net sales after discounts and taxes (final revenue) for the store-month. Decimal(18,4).*
- **`created_at`** (datetime2, NULL) - 1 distinct values
  - *ETL or row insertion timestamp indicating when the row was created/last updated in the ETL process. Single distinct value in sample data.*

---

### pos_sales_yearly

**Rows:** 3  
**Columns:** 9  
**Primary Keys:** `store_id`, `year`  

**Purpose:** Annual aggregated point-of-sale metrics per store. Each row represents a store's summary for a specific year (financial/transactional aggregates such as bills, quantity, gross/discount/tax/net sales). Intended as a high-level reporting/analytics table and a rollup source for dashboards and cross-table joins to drill down to monthly/daily or transaction-level data.

**Business Questions:**

- Which stores generated the highest net sales in the year?
- What is the average bill value and average kg per bill per store for the year?
- What is the discount as a percentage of gross sales by store for the year?
- What proportion of company-wide yearly net sales is contributed by each store?
- Are gross -> net calculations consistent (gross - discount + tax = net) across stores for the year?

**Key Columns:**

- **`year`** (bigint, NOT NULL) - 1 distinct values
  - *Calendar or fiscal year for the summarized metrics. Stored as a bigint (numeric year value).*
- **`store_id`** (nvarchar(50), NOT NULL) - 3 distinct values
  - *Store identifier (nvarchar(50)). Logical primary-key component identifying the retail location.*
- **`total_bills`** (decimal(18,4), NULL) - 3 distinct values
  - *Total number of bills/receipts for the store in the year. Stored as decimal(18,4) though semantically an integer count (likely aggregated as SUM of counts).*
- **`total_qty_kg`** (decimal(18,4), NULL) - 3 distinct values
  - *Total quantity sold in kilograms for the store over the year (decimal(18,4)).*
- **`gross_sales`** (decimal(18,4), NULL) - 3 distinct values
  - *Total gross sales (pre-discount, pre-tax) for the store in the year (decimal(18,4)).*
- **`discount_amount`** (decimal(18,4), NULL) - 3 distinct values
  - *Total discounts given for the store during the year (decimal(18,4)).*
- **`tax_amount`** (decimal(18,4), NULL) - 3 distinct values
  - *Total tax collected/charged for the store in the year (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 3 distinct values
  - *Net sales after discounts and taxes for the store in the year (decimal(18,4)). Observed to follow net_sales = gross_sales - discount_amount + tax_amount.*
- **`created_at`** (datetime2, NULL) - 1 distinct values
  - *ETL or row insertion/update timestamp (datetime2) indicating when the row was created/loaded into the table.*

---

### pos_shift_closures

**Rows:** 50  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** Represents end-of-shift closure records for point-of-sale terminals. Each row summarizes a single shift (identifier, terminal, operator, start/end timestamps) and financial totals (sales, cash/card collected, refunds, expected vs counted cash). It is used to reconcile till balances and analyze shift-level performance.

**Business Questions:**

- Which terminals or users have the largest cash discrepancies (expected_cash - counted_cash) and how often?
- What is average and median total_sales per shift by terminal and by user over a selected date range?
- Which shifts had unusually high refunds relative to total_sales?
- What is the distribution of shift lengths and does shift duration correlate with sales?
- For a given terminal and date, what shifts occurred and what were their totals and discrepancies?

**Foreign Keys:**

- `terminal_id` → `pos_terminals.terminal_id`

**Key Columns:**

- **`shift_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Unique identifier for the shift closure record (string token like 'SHIFTCLS1000').*
- **`terminal_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Identifier of the POS terminal where the shift occurred (foreign key to pos_terminals).*
- **`user_id`** (nvarchar(50), NULL) - 3 distinct values
  - *POS user/operator identifier who closed the shift (e.g., PU1003).*
- **`shift_start_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Shift start timestamp recorded as nvarchar (sample format 'YYYY-MM-DD HH:MM:SS').*
- **`shift_end_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Shift end timestamp recorded as nvarchar (sample format 'YYYY-MM-DD HH:MM:SS').*
- **`total_sales`** (decimal(18,4), NULL) - 50 distinct values
  - *Total monetary sales recorded for the shift (decimal).*
- **`cash_collected`** (decimal(18,4), NULL) - 50 distinct values
  - *Amount of cash recorded as collected during the shift (decimal).*
- **`card_collected`** (decimal(18,4), NULL) - 50 distinct values
  - *Amount collected via card payments during the shift (decimal).*
- **`refunds_amt`** (decimal(18,4), NULL) - 50 distinct values
  - *Total refund amount processed during the shift (decimal).*
- **`expected_cash`** (decimal(18,4), NULL) - 50 distinct values
  - *Calculated amount of cash expected in the till at shift close (decimal), likely derived from sales/cash transactions and refunds.*
- *(... and 2 more columns)*

---

### pos_stores

**Rows:** 4  
**Columns:** 5  
**Primary Keys:** `store_id`  

**Key Columns:**

- **`store_id`** (nvarchar(50), NOT NULL) - 4 distinct values
- **`city`** (nvarchar(50), NULL) - 4 distinct values
- **`region`** (nvarchar(50), NULL) - 4 distinct values
- **`first_active_date`** (datetime2, NULL) - 4 distinct values
- **`last_online`** (nvarchar(50), NULL) - 4 distinct values

---

### pos_sync_log

**Rows:** 50  
**Columns:** 10  
**Primary Keys:** `sync_id`  

**Purpose:** Logs point-of-sale (POS) synchronization events from terminals to the ETL/system. Each row records one sync attempt including counts, status, timestamps, errors and retry behavior. It is used for operational monitoring, troubleshooting and basic ETL auditing.

**Business Questions:**

- What is the overall success rate of POS syncs over a given period?
- Which terminals are failing most often and require investigation?
- How many records are being transmitted per sync per terminal (average/median)?
- How many retries are typically required before success and are failures correlated with retry_count or specific error messages?
- When was the last successful sync for each terminal?

**Key Columns:**

- **`sync_id`** (nvarchar(50), NOT NULL) - 50 distinct values
  - *Unique identifier for a synchronization attempt (primary key).*
- **`terminal_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Identifier of the POS terminal that initiated the sync.*
- **`sync_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp of the sync attempt as stored (nvarchar containing datetime-like string).*
- **`sync_status`** (nvarchar(50), NULL) - 2 distinct values
  - *Outcome of the sync attempt (e.g., SUCCESS or FAILED).*
- **`records_sent`** (bigint, NULL) - 41 distinct values
  - *Number of records sent from the terminal in the sync (bigint).*
- **`records_received`** (bigint, NULL) - 43 distinct values
  - *Number of records the receiver acknowledged/processed (bigint).*
- **`error_message`** (nvarchar(50), NULL) - 1 distinct values ⚠️ 58.0% NULL
  - *Short error text explaining failure reason (nullable).*
- **`retry_count`** (decimal(18,4), NULL) - 4 distinct values
  - *Number of retries attempted for this sync (decimal(18,4) but small integer-like values).*
- **`last_success_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *Timestamp of the last successful sync for the terminal or sync_id context, stored as nvarchar datetime-like string.*
- **`created_at`** (datetime2, NULL) - 50 distinct values
  - *Record insertion timestamp in datetime2 representing when the log row was created in the system.*

---

### pos_terminals

**Rows:** 4  
**Columns:** 11  
**Primary Keys:** `terminal_id`  

**Purpose:** Registry of POS terminals (hardware/software) deployed at stores. It identifies terminals, links them to stores and users, tracks location, software version, last online timestamp and creation time. Serves as a master/lookup for attributing transactions, shifts and device-level telemetry to terminals.

**Business Questions:**

- Which terminals are installed at each store and what are their serial numbers?
- Which terminals are running an outdated or non-compliant POS software version?
- Which user is assigned to a specific terminal and how many terminals does each user manage?
- Which terminals have not come online recently (device health) based on last_online_ts?
- What are the geographic locations of terminals (for mapping or routing)?

**Foreign Keys:**

- `store_id` → `pos_stores.store_id`

**Key Columns:**

- **`terminal_id`** (nvarchar(50), NOT NULL) - 4 distinct values
  - *Surrogate/business key identifying the terminal (PK). Example values: TERM-001-1 ...*
- **`store_id`** (nvarchar(50), NULL) - 3 distinct values
  - *Foreign key linking terminal to the store where it is installed. Values reference pos_stores.store_id.*
- **`terminal_code`** (nvarchar(50), NULL) - 4 distinct values
  - *Human-readable terminal code often combining store shorthand and terminal label (e.g., STORE_AH-T1).*
- **`device_serial`** (nvarchar(50), NULL) - 4 distinct values
  - *Manufacturer serial number of the POS device (hardware identifier).*
- **`pos_software_version`** (nvarchar(50), NULL) - 1 distinct values
  - *Version string of POS software installed on the terminal (e.g., v3.2.1).*
- **`assigned_user_id`** (nvarchar(50), NULL) - 2 distinct values
  - *Identifier of the user (operator/technician) assigned responsibility for the terminal.*
- **`last_online_ts`** (nvarchar(50), NULL) - 4 distinct values
  - *Timestamp when the terminal was last seen online. Stored as nvarchar but contains datetime-like strings.*
- **`status`** (nvarchar(50), NULL) - 1 distinct values
  - *Operational state of the terminal (e.g., ACTIVE, INACTIVE, DECOMMISSIONED). Current data shows 'ACTIVE' for all rows.*
- **`location_lat`** (decimal(18,4), NULL) - 4 distinct values
  - *Latitude of the terminal's physical location (decimal with 4 fractional digits).*
- **`location_long`** (decimal(18,4), NULL) - 4 distinct values
  - *Longitude of the terminal's physical location (decimal with 4 fractional digits).*
- *(... and 1 more columns)*

---

### pos_transaction_lines

**Rows:** 125  
**Columns:** 12  
**Primary Keys:** *None*  

**Purpose:** This table stores individual point-of-sale (POS) transaction line items — one row per sold/returned item line. It is used to record SKU-level quantity, pricing, tax, batch and timing information for each POS transaction line and is intended to support sales analytics, financial reconciliation and inventory traceability.

**Business Questions:**

- What are total quantity sold and revenue (sum of line_total) per SKU for a given date range?
- Which SKUs generate the highest tax amount or highest average unit_price?
- Which batches had the most units sold (traceability by batch_id) and what revenue did they generate?
- What is the distribution of line-level quantities (qty) and common order sizes per transaction?
- Are there data quality issues: lines with missing variant_info or expiry_date, or non-zero discounts?

**Key Columns:**

- **`pos_line_id`** (nvarchar(50), NULL) - 125 distinct values
  - *Unique identifier for the transaction line (string). Appears unique for each row in this dataset.*
- **`pos_txn_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Identifier of the parent POS transaction for the line (string). Repeats across multiple lines belonging to the same transaction.*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Stock-keeping unit identifier for the product sold (string). Low cardinality with a few SKUs making up most rows.*
- **`qty`** (decimal(18,4), NULL) - 10 distinct values
  - *Quantity sold for the line (decimal). Can be whole numbers in practice but stored as decimal(18,4).*
- **`unit_price`** (decimal(18,4), NULL) - 10 distinct values
  - *Unit selling price applied to the line (decimal).*
- **`line_total`** (decimal(18,4), NULL) - 54 distinct values
  - *Total monetary amount for the line (decimal), generally qty * unit_price minus discounts plus taxes depending on definition.*
- **`discount_amt`** (bigint, NULL) - 1 distinct values
  - *Discount applied to the line (bigint). In this dataset the column is constant 0 for all rows.*
- **`tax_amt`** (decimal(18,4), NULL) - 54 distinct values
  - *Tax amount applied to the line (decimal).*
- **`variant_info`** (decimal(18,4), NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Field intended for variant attributes (stored as decimal in the DDL), but currently entirely NULL in this snapshot.*
- **`expiry_date`** (datetime2, NULL) - 0 distinct values ⚠️ 100.0% NULL
  - *Intended expiry/Best Before date for the batch/product line (datetime). Currently 100% NULL.*
- *(... and 2 more columns)*

---

### pos_transactions

**Rows:** 50  
**Columns:** 15  
**Primary Keys:** *None*  

**Purpose:** Records point-of-sale transaction headers (one row per POS transaction). It stores transactional metadata (ids, timestamps, amounts, payment mode, shift, status and sync flag) and is used as the source of truth for POS-level sales and operational reporting. In the schema it acts as the parent to transaction lines (pos_transaction_lines) and links terminals (pos_terminals) and users (pos_users) to transactions.

**Business Questions:**

- What are total sales, tax and average ticket by day / hour / terminal / cashier?
- How much revenue was collected by payment mode (CASH, UPI, CARD) over a period?
- Which terminals or shifts generate the highest txn_total and tax_total?
- Are there transactions that failed to sync or have abnormal/missing metadata?
- How many transactions and total sales are associated with each cashier (pos_user_id) in a time window?

**Foreign Keys:**

- `terminal_id` → `pos_terminals.terminal_id`

**Key Columns:**

- **`pos_txn_id`** (nvarchar(50), NULL) - 50 distinct values
  - *Unique identifier for the POS transaction (header level).*
- **`terminal_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Identifier of the POS terminal where the transaction originated.*
- **`pos_user_id`** (nvarchar(50), NULL) - 3 distinct values
  - *Identifier for the cashier / POS user who processed the transaction.*
- **`txn_ts`** (nvarchar(50), NULL) - 50 distinct values
  - *POS transaction timestamp as string (NVARCHAR); likely when transaction occurred.*
- **`txn_type`** (nvarchar(50), NULL) - 1 distinct values
  - *Type of transaction (e.g., SALE, REFUND). In sample data it's always 'SALE'.*
- **`txn_total`** (decimal(18,4), NULL) - 49 distinct values
  - *Total monetary amount for the transaction (decimal(18,4)).*
- **`tax_total`** (decimal(18,4), NULL) - 49 distinct values
  - *Total tax amount applied to the transaction (decimal(18,4)).*
- **`discount_total`** (decimal(18,4), NULL) - 1 distinct values
  - *Total discount applied to the transaction (decimal). In this sample it is always 0.0000.*
- **`payment_mode`** (nvarchar(50), NULL) - 3 distinct values
  - *Mode of payment (e.g., CASH, UPI, CARD).*
- **`external_txn_ref`** (nvarchar(50), NULL) - 50 distinct values
  - *External/payment processor reference or id for the transaction (string).*
- *(... and 5 more columns)*

---

### pos_users

**Rows:** 3  
**Columns:** 10  
**Primary Keys:** *None*  

**Purpose:** Holds point-of-sale (POS) user / staff records used to identify who operates POS terminals at stores. It stores identity (id, name), contact info, role, store assignment, authentication hash, and activity timestamps. Supports attribution of POS activity to users and basic user lifecycle reporting.

**Business Questions:**

- How many active POS users are there per store or overall?
- What is the distribution of roles (Cashier vs Supervisor) across stores?
- Which users have not logged in for X days (inactivity detection)?
- How many users were created in each month (onboarding trend)?
- Which user performed the most transactions / highest sales (when joined with transactions)?

**Key Columns:**

- **`pos_user_id`** (nvarchar(50), NULL) - 3 distinct values
  - *Unique identifier for a POS user (alphanumeric id like 'PU1001').*
- **`name`** (nvarchar(50), NULL) - 3 distinct values
  - *Human readable name of the POS user.*
- **`role`** (nvarchar(50), NULL) - 2 distinct values
  - *User role or job function at POS (e.g., Cashier, Supervisor).*
- **`phone`** (nvarchar(50), NULL) - 3 distinct values
  - *Contact phone number for the POS user, stored as string (includes country code).*
- **`email`** (nvarchar(50), NULL) - 3 distinct values
  - *User email address used for notifications and identification.*
- **`store_id`** (nvarchar(50), NULL) - 3 distinct values
  - *Identifier of the store where the POS user is assigned (e.g., 'STORE_AHD_001').*
- **`active_flag`** (bit, NULL) - 1 distinct values
  - *Boolean flag indicating whether the user account is active (bit).*
- **`created_at`** (datetime2, NULL) - 3 distinct values
  - *Timestamp when the POS user record was created (onboarded).*
- **`last_login`** (datetime2, NULL) - 3 distinct values
  - *Timestamp of the user's last successful login to the POS system.*
- **`pin_hash`** (nvarchar(96), NULL) - 3 distinct values
  - *Cryptographic hash of the user's PIN used for authentication (non-reversible).*

---

### pos_vendors

**Rows:** 40  
**Columns:** 9  
**Primary Keys:** `vendor_id`  

**Purpose:** Master catalog of point-of-sale vendors. Stores vendor identifiers and contact / classification information used by POS, ecom and B2B operations. Acts as the authoritative source for vendor metadata to join against transactional tables (orders, transactions, products, inventory, contracts).

**Business Questions:**

- How many vendors do we have and what are their contact details?
- What is the distribution of vendors by city and by business type?
- Which vendors are missing contact information (phone/email) or GST details?
- Which vendors supply the most orders/sales (when joined to order/transaction tables)?
- Which vendors are associated with specific product/contract/inventory records (joins to product_inventory, b2b_contracts, pos_orders)?

**Key Columns:**

- **`vendor_id`** (nvarchar(50), NOT NULL) - 40 distinct values
  - *Unique identifier for each vendor (primary key). Alphanumeric code like 'POSV1001'.*
- **`vendor_name`** (nvarchar(54), NULL) - 40 distinct values
  - *Human-readable name of the vendor/company.*
- **`phone`** (nvarchar(50), NULL) - 40 distinct values
  - *Vendor primary phone number (includes country code and formatting).*
- **`email`** (nvarchar(64), NULL) - 40 distinct values
  - *Vendor contact email address used for notifications and billing.*
- **`address`** (nvarchar(69), NULL) - 40 distinct values
  - *Free-form street address (mixed components: street, area, postal code).*
- **`city`** (nvarchar(50), NULL) - 9 distinct values
  - *City where the vendor is located (normalized to a modest set of values).*
- **`gst_no`** (bigint, NULL) - 40 distinct values
  - *Vendor GST (tax) number stored as bigint.*
- **`business_type`** (nvarchar(50), NULL) - 5 distinct values
  - *Categorical classification of the vendor's primary business (e.g., Equipment Repair, Hardware).*
- **`created_at`** (datetime2, NULL) - 1 distinct values
  - *Timestamp of vendor record creation (datetime2).*

---

### product_inventory

**Rows:** 40  
**Columns:** 12  
**Primary Keys:** `inventory_id`  

**Purpose:** Inventory snapshot per product SKU and distribution/collection centre. Tracks quantities (units and kg), reserved vs available stock, replenishment parameters (reorder point, lead time, safety stock), storage temperature requirement and expiry timestamp. Used by procurement, warehouse operations and replenishment planning.

**Business Questions:**

- Which SKUs and centres are below their reorder_point and need replenishment?
- What is the total available stock (units and kg) by SKU or by centre?
- Which inventory items are expiring within X days (near-expiry reporting)?
- How much reserved stock exists per SKU and how does it impact available stock?
- Which SKUs require cold storage (storage_temp_c) and what are their total quantities?

**Foreign Keys:**

- `sku` → `products.sku`

**Key Columns:**

- **`inventory_id`** (nvarchar(50), NOT NULL) - 40 distinct values
  - *Unique identifier for the inventory record (PK). Likely encodes SKU and centre in its value (e.g., INV-APP009-AHMEDABAD).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Product SKU code; foreign key to products.sku. Low cardinality (10 distinct across 40 rows).*
- **`centre_id`** (nvarchar(50), NULL) - 4 distinct values
  - *Human-readable centre name where inventory is stored (collection/packing/distribution/cold storage). Very low cardinality: 4 centres.*
- **`qty_units`** (bigint, NULL) - 38 distinct values
  - *Quantity measured in units (integer) present in the inventory record.*
- **`qty_kg`** (decimal(18,4), NULL) - 40 distinct values
  - *Quantity measured in kilograms (decimal(18,4)) for the inventory record.*
- **`reserved_stock`** (bigint, NULL) - 38 distinct values
  - *Units reserved for orders/allocations and therefore not available for new orders.*
- **`available_stock`** (bigint, NULL) - 40 distinct values
  - *Units currently available for sale/dispatch (after reservations).*
- **`reorder_point`** (bigint, NULL) - 33 distinct values
  - *Configured inventory level (units) at which replenishment should be triggered for the record.*
- **`lead_time_days`** (bigint, NULL) - 3 distinct values
  - *Expected supplier/fulfilment lead time in days for replenishing this SKU at this centre. Low cardinality (1-3 days).*
- **`safety_stock_kg`** (bigint, NULL) - 31 distinct values
  - *Safety buffer expressed in kilograms to protect against stockouts. Stored as bigint but name suggests kg.*
- *(... and 2 more columns)*

---

### product_pricing

**Rows:** 100  
**Columns:** 9  
**Primary Keys:** *None*  

**Purpose:** Price schedule / pricing master for products: records price per unit and minimum order quantity for a SKU over a time range. It is used to represent time-bound price offers or standard prices for items and to determine which price applies for a given date or period.

**Business Questions:**

- What price (price_per_unit) was active for SKU X at datetime Y?
- How has the price for SKU X changed over time (price history/timeseries)?
- Which SKUs have price intervals that overlap or have gaps in their pricing schedule?
- What is the distribution (min/avg/max) of price_per_unit per SKU or across all SKUs in a given period?
- What minimum order quantities are set across SKUs and how frequently each min_order_qty is used?

**Foreign Keys:**

- `sku` → `products.sku`

**Key Columns:**

- **`price_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Unique identifier for the pricing record (string). Represents a specific price interval/entry.*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Stock-keeping unit identifier linking price to a product (FK to zuna_etl.products.sku).*
- **`start_ts`** (nvarchar(50), NULL) - 100 distinct values
  - *Start timestamp for the price interval. Stored as nvarchar but represents a datetime string (e.g., '2024-10-30 10:10:00').*
- **`end_ts`** (nvarchar(50), NULL) - 100 distinct values
  - *End timestamp for the price interval. Stored as nvarchar but represents a datetime string; marks when the price stops being effective.*
- **`price_per_unit`** (decimal(18,4), NULL) - 100 distinct values
  - *Monetary price per unit for the SKU for the given interval (decimal(18,4)).*
- **`currency`** (nvarchar(50), NULL) - 1 distinct values
  - *Currency code for the price (NVARCHAR(50) but values show a single currency 'INR').*
- **`min_order_qty`** (decimal(18,4), NULL) - 3 distinct values
  - *Minimum order quantity required for the given price interval (decimal(18,4), but effectively integral values in data).*
- **`created_by`** (nvarchar(50), NULL) - 1 distinct values
  - *Identifier of the user/system that created the pricing record. Data shows a single value 'pricing_admin'.*
- **`created_at`** (datetime2, NULL) - 100 distinct values
  - *Timestamp when the pricing record was created (datetime2).*

---

### product_sales

**Rows:** 10  
**Columns:** 6  
**Primary Keys:** `sku`  

**Purpose:** A compact sales summary at the SKU level for the ETL layer. Stores monetary aggregates that describe sales performance per product SKU (gross sales, discounts, delivery fees, tax and reported net sales). Typically used for reporting, reconciling revenue components and joining back to master product metadata or other sales/ordering tables for enrichment.

**Business Questions:**

- Which SKUs generate the highest net sales?
- What is the total gross sales, total discounts, and resulting net sales across all SKUs?
- Which SKUs have the highest discount amount or highest discount as a percentage of gross?
- How much of gross sales is contributed by delivery fees and tax per SKU?
- Are net_sales values consistent with gross, discount, delivery_fee and tax (reconciliation / ETL validation)?

**Key Columns:**

- **`sku`** (nvarchar(50), NOT NULL) - 10 distinct values
  - *Unique product stock-keeping unit identifier for the summarized row. Declared nvarchar(50) but observed max length ~6; this is the primary key for the table.*
- **`gross_sales`** (decimal(18,4), NULL) - 10 distinct values
  - *Total gross sales amount for the SKU before discounts/fees/taxes (decimal(18,4)).*
- **`discount`** (decimal(18,4), NULL) - 10 distinct values
  - *Total discount amount applied to sales of the SKU (decimal(18,4)).*
- **`delivery_fee`** (decimal(18,4), NULL) - 10 distinct values
  - *Aggregate delivery or shipping fees collected (decimal(18,4)) tied to the SKU sales.*
- **`tax`** (decimal(18,4), NULL) - 10 distinct values
  - *Aggregate tax amount collected on sales of the SKU (decimal(18,4)).*
- **`net_sales`** (decimal(18,4), NULL) - 10 distinct values
  - *Reported net sales amount for the SKU (decimal(18,4)). This is the post-processed revenue figure as stored by the ETL — business definition (how it is derived from gross/discount/delivery/tax) must be confirmed with domain owners.*

---

### product_variants

**Rows:** 20  
**Columns:** 12  
**Primary Keys:** `variant_id`  

**Purpose:** Holds product variant level master data for SKUs (different pack sizes, units, weights, barcodes, and prices) used across pricing, inventory, and sales processes.

**Business Questions:**

- Which variants exist for a particular product (sku) and what are their pack sizes, weights and barcodes?
- What is the retail and wholesale price per variant and how do prices compare between variants of the same product?
- How many variants were created in a given time window (by created_at)?
- Which variants are active/inactive and which should be excluded from ordering or display?
- How do unit pack size and weight distributions look across variants (e.g., percent packed vs loose)?

**Foreign Keys:**

- `sku` → `products.sku`

**Key Columns:**

- **`variant_id`** (nvarchar(50), NOT NULL) - 20 distinct values
  - *Surrogate/primary identifier for the product variant (unique string).*
- **`sku`** (nvarchar(50), NULL) - 10 distinct values
  - *Product-level SKU that groups multiple variants (nullable). Foreign key to zuna_etl.products.sku.*
- **`variant_name`** (nvarchar(50), NULL) - 2 distinct values
  - *Human-friendly variant label (e.g., Loose, Packed 500g). Low cardinality.*
- **`variant_sku`** (nvarchar(50), NULL) - 20 distinct values
  - *Concatenated SKU for the variant (often product SKU plus variant suffix). Appears unique per row.*
- **`uom`** (nvarchar(50), NULL) - 3 distinct values
  - *Unit of measure for the variant (e.g., kg, 250g, 500g).*
- **`units_per_pack`** (decimal(18,4), NULL) - 2 distinct values
  - *Quantity represented by the variant pack (decimal), e.g., 1.0000 or 0.5000.*
- **`weight_kg`** (decimal(18,4), NULL) - 2 distinct values
  - *Weight of the variant in kilograms (decimal).*
- **`barcode`** (nvarchar(50), NULL) - 20 distinct values
  - *Barcode identifier for the variant (string). Likely unique per variant.*
- **`price_retail`** (decimal(18,4), NULL) - 20 distinct values
  - *Retail selling price for the variant (decimal).*
- **`price_wholesale`** (decimal(18,4), NULL) - 10 distinct values
  - *Wholesale price for the variant (decimal), used in B2B pricing and margin calculations.*
- *(... and 2 more columns)*

---

### products

**Rows:** 10  
**Columns:** 16  
**Primary Keys:** `sku`  

**Purpose:** Canonical product catalog for the ETL layer (zuna_etl). Holds master product attributes used across sales, inventory and order systems to describe SKUs, weights, packaging, perishability and handling characteristics.

**Business Questions:**

- Which products are perishable and require cold/ambient storage (based on is_perishable_flag and storage_temp_c)?
- Which SKUs have short shelf life (e.g., shelf_life_days <= X) and may need prioritized replenishment?
- How many SKUs exist by product_type and subcategory (catalog composition)?
- Which SKUs have a net or gross weight equal to a specified threshold (useful for shipping/packaging rules)?
- When was each product added to the catalog (created_at) and which are recent additions?

**Key Columns:**

- **`sku`** (nvarchar(50), NOT NULL) - 10 distinct values
  - *Unique product identifier (stock keeping unit). Primary key for this table.*
- **`product_name`** (nvarchar(50), NULL) - 10 distinct values
  - *Human-readable product description (e.g., 'Apple - Kinnaur (1kg)').*
- **`product_type`** (nvarchar(50), NULL) - 2 distinct values
  - *High-level product type/category such as 'Vegetable' or 'Fruit'.*
- **`category`** (nvarchar(50), NULL) - 1 distinct values
  - *Broad catalog category (e.g., 'Fresh Produce').*
- **`subcategory`** (nvarchar(50), NULL) - 10 distinct values
  - *Specific product family (e.g., 'Carrot', 'Cucumber', 'Apple').*
- **`brand`** (nvarchar(50), NULL) - 1 distinct values
  - *Manufacturer/brand for the product (e.g., 'Daily Greens').*
- **`uom`** (nvarchar(50), NULL) - 3 distinct values
  - *Unit of measure for the product (e.g., 'kg', '250g', '500g').*
- **`gross_weight_kg`** (decimal(18,4), NULL) - 2 distinct values
  - *Gross weight of the packaged product in kilograms (decimal).*
- **`net_weight_kg`** (decimal(18,4), NULL) - 2 distinct values
  - *Net weight (product-only) in kilograms (decimal).*
- **`pack_size`** (bigint, NULL) - 1 distinct values
  - *Number of units in one pack (bigint).*
- *(... and 6 more columns)*

---

### returns

**Rows:** 40  
**Columns:** 13  
**Primary Keys:** `return_id`  

**Purpose:** Records individual return transactions for orders: metadata about the return request, its lifecycle timestamps, categorical reasons/status, approval info, refund amounts and linkage to credit notes. Serves as the canonical returns log for analytical queries and joins to orders, credit notes and other sales/returns tables across schemas.

**Business Questions:**

- How many returns occurred and what is the total refund amount over a given period?
- What are the top reasons for returns and how do refund amounts vary by reason_code?
- What is the average time from request to received_at_centre (and other lifecycle intervals) and how does that vary by status or approver?
- Which orders have multiple return records and what is the refund exposure per order?
- What is the approval distribution and approval rate (REQUESTED -> APPROVED/REJECTED) and who approved most returns?

**Key Columns:**

- **`return_id`** (nvarchar(50), NOT NULL) - 40 distinct values
  - *Surrogate primary key identifying each return transaction (nvarchar PK).*
- **`order_id`** (nvarchar(50), NULL) - 35 distinct values
  - *Order identifier (nullable string) that this return is associated with; may correspond to different order tables across channels.*
- **`request_ts`** (nvarchar(50), NULL) - 40 distinct values
  - *Timestamp (stored as nvarchar) when the return request was created/submitted; appears in ISO-like 'YYYY-MM-DD HH:MM:SS' format.*
- **`reason_code`** (nvarchar(50), NULL) - 4 distinct values
  - *Categorical reason for the return (QUALITY, WRONG_ITEM, NOT_AS_DESCRIBED, DAMAGED).*
- **`requested_items_json`** (nvarchar(50), NULL) - 1 distinct values
  - *Intended to hold JSON with item-level details requested for return, stored as nvarchar but currently contains '[]' for all rows.*
- **`status`** (nvarchar(50), NULL) - 4 distinct values
  - *Lifecycle status of the return request (REQUESTED, APPROVED, REJECTED, COMPLETED).*
- **`approved_by`** (nvarchar(50), NULL) - 2 distinct values ⚠️ 52.5% NULL
  - *Identifier/role of the person who approved the return (nullable, two observed values: ops_manager, quality_head).*
- **`pickup_scheduled_ts`** (nvarchar(50), NULL) - 40 distinct values
  - *Scheduled timestamp for pickup collection (stored as nvarchar ISO-like string).*
- **`received_at_centre_ts`** (nvarchar(50), NULL) - 40 distinct values
  - *Timestamp when the returned item(s) were received at processing centre (stored as nvarchar).*
- **`refund_amount`** (decimal(18,4), NULL) - 40 distinct values
  - *Monetary refund amount issued for the return (decimal(18,4)).*
- *(... and 3 more columns)*

---

### shipments

**Rows:** 100  
**Columns:** 14  
**Primary Keys:** `shipment_id`  

**Purpose:** Represents shipments created for e-commerce orders. It stores shipment identifiers, linkage to orders, carrier and tracking information, shipment and delivery timestamps, status, pickup location, package metrics and shipping charges. The table is used for fulfillment, logistics analytics and reconciliation with orders.

**Business Questions:**

- What is the on-time delivery rate (actual_delivery_date <= expected_delivery_date) overall and by carrier?
- What is the average transit time (actual_delivery_date - shipment_date) by carrier, pickup centre, and over time?
- How do shipping charges vary with package weight and by carrier or pickup centre?
- Which orders have shipments that are delayed, pending delivery, or stuck in a particular status?
- What is the distribution of shipment statuses (IN_TRANSIT, OUT_FOR_DELIVERY, PICKED, DELIVERED) and counts by pickup centre or carrier?

**Foreign Keys:**

- `order_id` → `ecom_orders.order_id`

**Key Columns:**

- **`shipment_id`** (nvarchar(50), NOT NULL) - 100 distinct values
  - *Primary key. Unique identifier for each shipment record (nvarchar up to 50, observed max length 8). Examples: SHIP8001.*
- **`order_id`** (nvarchar(50), NULL) - 100 distinct values
  - *Foreign key linking a shipment to an order in ecom_orders (nvarchar up to 50). Distinct values ~100, nullable.*
- **`carrier_id`** (nvarchar(50), NULL) - 3 distinct values
  - *Identifier/name of carrier handling the shipment (nvarchar). Very low cardinality (3 values observed: LocalCourier, ThirdPartyLogistics, InHouseFleet).*
- **`tracking_no`** (nvarchar(50), NULL) - 100 distinct values
  - *Carrier-provided tracking number for the shipment (nvarchar). High cardinality — unique per shipment in practice.*
- **`shipment_date`** (datetime2, NULL) - 100 distinct values
  - *Timestamp when the shipment was dispatched or created (datetime2). Distinct across most rows.*
- **`expected_delivery_date`** (datetime2, NULL) - 100 distinct values
  - *Carrier-expected delivery timestamp (datetime2). Used as SLA target for deliveries.*
- **`actual_delivery_date`** (datetime2, NULL) - 59 distinct values
  - *Timestamp when the shipment was actually delivered (datetime2). Contains ~41% NULLs indicating pending or missing deliveries.*
- **`shipment_status`** (nvarchar(50), NULL) - 4 distinct values
  - *Current lifecycle status of the shipment (e.g., OUT_FOR_DELIVERY, IN_TRANSIT, PICKED, DELIVERED). Low cardinality (4 values).*
- **`pickup_centre_id`** (nvarchar(50), NULL) - 2 distinct values
  - *Name/ID of the pickup or distribution centre that handled the shipment (nvarchar). Very low cardinality observed (e.g., Surat Distribution Centre, Ahmedabad Collection Centre).*
- **`package_weight_kg`** (decimal(18,4), NULL) - 99 distinct values
  - *Declared weight of the package in kilograms (decimal(18,4)). Continuous variable with ~99 distinct values.*
- *(... and 4 more columns)*

---


---

*Report generated on 2026-01-09 11:23:30*
