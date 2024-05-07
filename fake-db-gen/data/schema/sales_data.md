| Column | Type | Description |
| --- | --- | --- |
| SaleID | INT | Unique identifier for each sale transaction |
| CustomerID | INT | ID of the customer making the purchase |
| ProductID | INT | ID of the product sold |
| SaleDate | DATE | Date when the sale occurred |
| Quantity | INT | Number of products sold |
| TotalAmount | DECIMAL(10,2) | Total amount of the transaction |
| PaymentMethod | VARCHAR(50) | Method used for payment (Credit card, PayPal, etc.) |
| SaleStatus | VARCHAR(50) | Status of the sale (Completed, Refunded, etc.) |
| ShippingAddress | VARCHAR(200) | Address to which the products are shipped |
| BillingAddress | VARCHAR(200) | Address used for billing purposes |
| ShippingMethod | VARCHAR(50) | Method of shipping (Standard, Express, etc.) |
| TrackingNumber | VARCHAR(50) | Tracking number for shipment |
| DeliveryStatus | VARCHAR(50) | Status of product delivery (Delivered, Pending, etc.) |
| PromotionsApplied | VARCHAR(100) | Promotions applied to the sale |
| TaxAmount | DECIMAL(10,2) | Amount of tax applied to the transaction |
| DiscountAmount | DECIMAL(10,2) | Amount of discount applied to the transaction |
| GiftMessage | TEXT | Any gift message included with the purchase |
| PaymentStatus | VARCHAR(50) | Status of payment (Paid, Pending, Failed, etc.) |
| PaymentDate | DATE | Date when the payment was processed |
| PaymentReference | VARCHAR(50) | Reference number for the payment transaction |
| PaymentGateway | VARCHAR(50) | Gateway used for processing the payment |
| InvoiceNumber | VARCHAR(50) | Invoice number for the sale |
| ReturnRequested | BOOLEAN | Whether a return has been requested for the sale |
| ReturnReason | VARCHAR(100) | Reason provided for requesting a return |
| ReturnApproved | BOOLEAN | Whether the return request has been approved |
| ReturnProcessed | BOOLEAN | Whether the return has been processed |
| ReturnDate | DATE | Date when the return was processed |
| RefundAmount | DECIMAL(10,2) | Amount refunded for the return |
| RefundMethod | VARCHAR(50) | Method used for refund (Credit card, PayPal, etc.) |
| RefundStatus | VARCHAR(50) | Status of the refund process (Completed, Pending) |
| RefundDate | DATE | Date when the refund was processed |
| RefundReference | VARCHAR(50) | Reference number for the refund transaction |