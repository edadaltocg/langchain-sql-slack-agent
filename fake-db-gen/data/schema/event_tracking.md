| Column | Type | Description |
| --- | --- | --- |
| EventID | INT | Unique identifier for each event |
| CustomerID | INT | ID of the customer involved in the event |
| EventType | VARCHAR(50) | Type of event (Page Visit, Download, Signup, etc.) |
| EventDate | TIMESTAMP | Timestamp when the event occurred |
| EventDetails | TEXT | Additional details about the event |
| Device | VARCHAR(50) | Device used for the event (Mobile, Desktop, etc.) |
| Location | VARCHAR(100) | Location of the customer during the event |
| SessionID | VARCHAR(100) | Unique session identifier for the event |
| BrowsingDuration | INT | Duration in seconds the customer spent during the event |
| EntryPage | VARCHAR(255) | URL of the entry page for the event |
| ExitPage | VARCHAR(255) | URL of the exit page for the event |
| ReferrerURL | VARCHAR(255) | URL of the referrer site |
| IPaddress | VARCHAR(50) | IP address of the customer during the event |
| Browser | VARCHAR(50) | Browser used by the customer |
| OS | VARCHAR(50) | Operating system of the device used |
| ClicksCount | INT | Number of clicks made during the event |
| PageViewsCount | INT | Number of page views during the event |
| Conversion | BOOLEAN | Whether the event led to a conversion |
| ConversionType | VARCHAR(50) | Type of conversion (Purchase, Subscription, etc.) |
| UserID | INT | Internal user ID linked to the customer |
| InteractionsDetails | TEXT | Details of interactions during the event |
| GeoLocation | VARCHAR(100) | Geographical location based on IP address |
| Timezone | VARCHAR(50) | Local timezone of the event |
| Language | VARCHAR(50) | Language preference detected during the event |
| IsMobile | BOOLEAN | Whether the event was on a mobile device |
| IsNewVisitor | BOOLEAN | Whether the visitor was new to the site |
| EngagementLevel | VARCHAR(50) | Level of engagement during the event (High, Medium, Low) |
| ActionsPerformed | TEXT | Description of any actions performed during the event |
| LeadGenerationSuccess | BOOLEAN | Whether the event successfully generated a lead |