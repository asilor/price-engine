# Price Engine

Price Engine periodically tracks millions of product prices accross multiple retailers and shows for every product variation in the selected region the list prices offered by every retailer sorted from lowest to highest.

The prices vary depending on the product variant (iPhone 16 128GB vs iPhone 16 256GB), the region (France, Spain, Germany, etc) and the retailer (Amazon, PcComponentes, Tradeinn, etc). Pricetracker takes that into account and stores in a timeseries database the price for every unique combination of variant_id, region_id, retailer_id. Prices are checked by a script running on a Docker container that is triggered by a Cron Job, which can be activated at the desired frequency (ex: every hour).

<img width="1215" alt="Screenshot 2025-01-29 at 12 47 10" src="https://github.com/user-attachments/assets/41d4d71d-4149-4a99-9a5e-e9e95bac864d" />

Based on competitor prices calculates optimal prices for every product variant in every available region and periodically updates them in an ecommerce via API.
