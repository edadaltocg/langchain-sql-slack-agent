| Column | Type | Description |
| --- | --- | --- |
| ExpenseID | INT | Unique identifier for each expense record |
| EmployeeID | INT | ID of the employee who made the expense |
| TripID | INT | Associated trip ID for the expense |
| Date | DATE | Date when the expense was incurred |
| Category | VARCHAR(50) | Category of the expense (Travel, Food, etc.) |
| Amount | DECIMAL(10,2) | Amount of the expense |
| Currency | VARCHAR(10) | Currency in which the expense was made |
| PaymentMethod | VARCHAR(50) | Method used for payment (Credit card, Cash) |
| Description | VARCHAR(200) | Detailed description of the expense |
| Receipt | BOOLEAN | Whether a receipt was provided |
| Approved | BOOLEAN | Whether the expense has been approved |
| ApprovalDate | DATE | Date when the expense was approved |
| TaxDeductible | BOOLEAN | If the expense is tax deductible |
| Vendor | VARCHAR(100) | Vendor from whom the expense was purchased |
| Location | VARCHAR(100) | Location where the expense was incurred |
| ProjectCode | VARCHAR(50) | Code for the project related to the expense |
| Reimbursed | BOOLEAN | If the expense has been reimbursed |
| ReimbursementDate | DATE | Date when the expense was reimbursed |
| Notes | TEXT | Any additional notes about the expense |
| AttachmentPath | VARCHAR(255) | Path to any attachments related to the expense |