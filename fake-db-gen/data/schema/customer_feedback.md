| Column | Type | Description |
| --- | --- | --- |
| FeedbackID | INT | Unique identifier for each feedback entry |
| CustomerID | INT | ID of the customer providing feedback |
| ProductID | INT | ID of the product related to the feedback |
| Rating | INT | Rating given by the customer (1-5 scale) |
| Comment | TEXT | Detailed comment or feedback from customer |
| DateReceived | DATE | Date when the feedback was received |
| ResponseSent | BOOLEAN | Whether a response has been sent to the customer |
| ResponseDate | DATE | Date when the response was sent |
| FeedbackChannel | VARCHAR(50) | Channel through which the feedback was received (Online, In-Store) |
| FollowUpNeeded | BOOLEAN | Whether follow-up action is needed |
| FollowUpDate | DATE | Scheduled date for follow-up action |
| FollowUpStatus | VARCHAR(50) | Status of follow-up (Pending, Completed) |
| CustomerSatisfactionLevel | VARCHAR(50) | Level of customer satisfaction (High, Medium, Low) |
| IssueResolved | BOOLEAN | Whether the customer's issue was resolved |
| ResolutionDetails | TEXT | Details about how the issue was resolved |
| AgentID | INT | ID of the agent who handled the feedback |
| FeedbackImportance | VARCHAR(50) | Importance level of the feedback (Critical, Moderate, Low) |
| InternalNotes | TEXT | Notes for internal use regarding the feedback |
| CustomerContactedAgain | BOOLEAN | Whether the customer was contacted again post-feedback |
| AdditionalCompensationOffered | DECIMAL(10,2) | Compensation amount offered, if any |
| CompensationAccepted | BOOLEAN | Whether the customer accepted the offered compensation |
| RelatedCampaignID | INT | ID of marketing campaign related to the feedback |
| ProductReturnInitiated | BOOLEAN | Whether a product return was initiated |
| ReturnReason | VARCHAR(100) | Reason for product return, if applicable |
| ProductReplacementOffered | BOOLEAN | Whether a product replacement was offered |
| ReplacementProductID | INT | ID of the replacement product offered |
| CustomerRetentionActions | VARCHAR(255) | Actions taken to retain the customer |