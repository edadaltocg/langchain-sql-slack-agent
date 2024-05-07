| Column | Type | Description |
| --- | --- | --- |
| TripID | INT | Unique identifier for each trip |
| EmployeeID | INT | ID of the employee going on the trip |
| Destination | VARCHAR(100) | Main destination of the trip |
| Purpose | VARCHAR(100) | Purpose of the trip (Business, Conference) |
| StartDate | DATE | Start date of the trip |
| EndDate | DATE | End date of the trip |
| Status | VARCHAR(50) | Current status of the trip (Planned, Ongoing, Completed) |
| TotalBudget | DECIMAL(10,2) | Total budget allocated for the trip |
| AdvanceAmount | DECIMAL(10,2) | Advance amount given for the trip |
| ExpensesClaimed | DECIMAL(10,2) | Total expenses claimed till now |
| Department | VARCHAR(100) | Department organizing the trip |
| BookingReference | VARCHAR(50) | Booking reference number |
| Accommodation | VARCHAR(200) | Accommodation details for the trip |
| TransportMode | VARCHAR(50) | Primary mode of transport (Flight, Train, etc.) |
| ReportingManager | VARCHAR(100) | Manager to whom the trip is reported |
| ApprovalStatus | VARCHAR(50) | Approval status of the trip |
| ApprovalDate | DATE | Date when the trip was approved |
| Notes | TEXT | Any additional notes about the trip |
| AttachmentPath | VARCHAR(255) | Path to any attachments related to the trip |
| LastModified | TIMESTAMP | Last modification timestamp of the trip record |