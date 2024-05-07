| Column | Type | Description |
| --- | --- | --- |
| AutomationID | INT | Unique identifier for each automation task |
| CampaignID | INT | ID of the associated marketing campaign |
| TriggerEvent | VARCHAR(100) | Event that triggers the automation |
| Action | VARCHAR(100) | Action taken by the automation (Send Email, Notify Sales) |
| Status | VARCHAR(50) | Current status of the automation (Active, Paused, Ended) |
| LastRun | TIMESTAMP | Last time the automation was executed |
| CreatedDate | DATE | Date when the automation was created |
| ModifiedDate | DATE | Date when the automation was last modified |
| CreatedBy | INT | User ID of the person who created the automation |
| ModifiedBy | INT | User ID of the person who last modified the automation |
| AutomationName | VARCHAR(100) | Name of the automation |
| Description | TEXT | Detailed description of the automation |
| TriggerConditions | TEXT | Conditions that trigger the automation |
| ActionDetails | TEXT | Detailed description of the action taken |
| ExecutionFrequency | VARCHAR(50) | How often the automation runs (Daily, Weekly, On Event) |
| NextRun | TIMESTAMP | Scheduled next run time for the automation |
| EndDate | DATE | Scheduled end date for the automation |
| Priority | INT | Priority level of the automation |
| ErrorHandling | VARCHAR(100) | How errors are handled during automation execution |
| NotificationSettings | TEXT | Settings for notifications related to the automation |
| ResultTracking | BOOLEAN | Whether results of the automation are tracked |
| ResultData | TEXT | Data collected from the results of the automation |
| FeedbackLoopEnabled | BOOLEAN | Whether a feedback loop is enabled for continuous improvement |
| Dependencies | VARCHAR(255) | Other automations or processes this depends on |
| Notes | TEXT | Additional notes about the automation |
| ImpactLevel | VARCHAR(50) | Estimated impact level of the automation (High, Medium, Low) |
| CustomerSegmentTargeted | VARCHAR(100) | Customer segment targeted by the automation |
| PerformanceMetrics | TEXT | Metrics used to measure the performance of the automation |
| IsActive | BOOLEAN | Whether the automation is currently active |