| Column | Type | Description |
| --- | --- | --- |
| InteractionID | INT | Unique identifier for each interaction |
| CustomerID | INT | ID of the customer involved |
| CampaignID | INT | ID of the campaign associated with the interaction |
| InteractionType | VARCHAR(50) | Type of interaction (Email, Call, Meeting, etc.) |
| InteractionDate | DATE | Date of the interaction |
| Duration | INT | Duration of the interaction in minutes |
| Outcome | VARCHAR(100) | Outcome of the interaction (Positive, Negative, Neutral) |
| Notes | TEXT | Additional notes about the interaction |
| FollowUpRequired | BOOLEAN | If follow-up is required |
| FollowUpDate | DATE | Scheduled date for follow-up |
| AgentID | INT | ID of the agent who handled the interaction |
| SatisfactionScore | INT | Customer satisfaction score from the interaction |