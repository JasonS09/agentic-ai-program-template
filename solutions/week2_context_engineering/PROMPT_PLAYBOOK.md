# Prompt Playbook v1 - Week 2

| Query                                       | Mode (raw/RAG) | k | Retrieved IDs          | Strengths                                                        | Weaknesses                         | Failure Modes | Notes                                                                   |
| ------------------------------------------- | -------------- | - | ---------------------- | ---------------------------------------------------------------- | ---------------------------------- | ------------- | ----------------------------------------------------------------------- |
| What’s the process for tracking my package? | RAG            | 2 | faq2, faq4             | Grounding (5), Relevance (5), Completeness (5), Traceability (5) | Brevity (3)                        | —             | Well-grounded, cites both relevant FAQs; slightly verbose but thorough. |
| Do you ship to Canada?                      | RAG            | 2 | faq3, faq8             | Grounding (5), Relevance (5), Brevity (4)                        | Completeness (3), Traceability (3) | partial       | Mentioned gift wrapping (slightly tangential); overall correct.         |
| What are the support hours?                 | RAG            | 2 | faq7, faq5             | Grounding (5), Relevance (5), Completeness (5), Traceability (5) | Brevity (3)                        | —             | Excellent grounding, correct citation, a bit wordy.                     |
| What’s the process for tracking my package? | RAW            | — | —                      | Relevance (5), Completeness (4), Brevity (4)                     | Grounding (1), Traceability (1)    | no-hit        | Generic knowledge answer, no use of context.                            |
| Do you ship to Canada?                      | RAW            | — | —                      | Relevance (5), Completeness (4), Brevity (5)                     | Grounding (1), Traceability (1)    | no-hit        | Correct but context-free; no factual retrieval.                         |
| What are the support hours?                 | RAW            | — | —                      | Relevance (5), Completeness (4), Brevity (4)                     | Grounding (1), Traceability (1)    | stale         | Guesswork answer; correct pattern but ungrounded.                       |
| What’s the process for tracking my package? | RAG            | 4 | faq2, faq4, faq9, faq6 | Grounding (5), Relevance (5), Completeness (5), Traceability (5) | Brevity (3)                        | —             | Fully correct and well-sourced; uses 4 contexts effectively.            |

## Prompt examples and outputs:
```
--- Querying for: 'What's the process for tracking my package?' ---
Retrieved context: ---CONTEXT BLOCK 1---
Once your order has shipped, you will receive an email with a tracking number.
---CONTEXT BLOCK 2---
You can reach our customer support team via email at support@example.com or by calling our toll-free number.
Answer: According to the provided context, the process for tracking your package is as follows:

Once your order has shipped, you will receive an email with a tracking number. You can then use this tracking number to track the status of your package.

Additionally, if you have any questions or concerns about tracking your package, you can reach out to our customer support team via email at support@example.com or by calling our toll-free number.

Citations:
[1] How do I track my order?
[2] How can I contact customer support?

--- Querying for: 'Do you ship to Canada?' ---
Retrieved context: ---CONTEXT BLOCK 1---
Yes, we ship to most countries worldwide. Shipping costs may vary.
---CONTEXT BLOCK 2---
Yes, we offer gift wrapping for an additional fee. You can select this option at checkout.
Answer: According to our shipping policy (Context Block 1), yes, we do ship to Canada! Shipping costs may vary depending on your location. Additionally, if you'd like to make it an extra-special gift, consider our gift wrapping option (Context Block 2) for a small additional fee.

Citations:
[1] Do you ship internationally?
[2] Do you offer gift wrapping?

--- Querying for: 'What are the support hours?' ---
Retrieved context: ---CONTEXT BLOCK 1---
Our customer support is available Monday to Friday, from 9 AM to 5 PM EST.
---CONTEXT BLOCK 2---
We accept all major credit cards, PayPal, and Apple Pay.
Answer: Based on the provided context, our support hours are:

Monday to Friday, from 9 AM to 5 PM EST.

Please note that these hours apply only to customer support inquiries, and payment options are available through major credit cards, PayPal, and Apple Pay. If you have any further questions or concerns outside of these support hours, we'll be happy to assist you during our regular support hours.

Citations:
[1] What are your business hours?
[2] What payment methods do you accept?

--- Querying for: 'What's the process for tracking my package?' ---
Skipping context retrieval (--no-context enabled).
Answer: I'd be happy to help!

To track your package, follow these steps:

1. Find the tracking number: The tracking number is usually provided by the shipper (e.g., UPS, FedEx, USPS) and can be found on the shipping label or in an email confirmation from the sender.
2. Visit the carrier's website: Go to the website of the shipping carrier (e.g., ups.com, fedex.com, usps.com) and look for a tracking tool or section labeled "Track Your Package."
3. Enter the tracking number: Type in the tracking number provided to you, and hit enter or submit.
4. Check package status: The carrier's website will display the current status of your package, including its location, expected delivery date, and any issues that may have arisen during transit.

Some popular carriers' tracking tools can also be accessed through mobile apps or online marketplaces like eBay or Amazon. If you're unsure about the specific steps for a particular carrier or shipping method, feel free to ask!

--- Querying for: 'Do you ship to Canada?' ---
Skipping context retrieval (--no-context enabled).
Answer: Yes, we do ship to Canada. We have partnerships with various international shipping carriers that enable us to deliver our products to customers in Canada. The specific shipping options and rates may vary depending on the location within Canada, but rest assured that we do offer international shipping to this country.

--- Querying for: 'What are the support hours?' ---
Skipping context retrieval (--no-context enabled).
Answer: Based on my general knowledge, I would say that our support hours are typically Monday to Friday from 9:00 AM to 5:00 PM Eastern Standard Time (EST). However, please note that these hours may be subject to change, and it's always best to confirm with our support team directly for the most up-to-date information.

I hope this answer helps! If you have any further questions or concerns, feel free to ask.

--- Querying for: 'What's the process for tracking my package?' ---
Retrieved context: ---CONTEXT BLOCK 1---
Once your order has shipped, you will receive an email with a tracking number.
---CONTEXT BLOCK 2---
You can reach our customer support team via email at support@example.com or by calling our toll-free number.
---CONTEXT BLOCK 3---
You can apply your discount code in the 'Promo Code' box at checkout.
---CONTEXT BLOCK 4---
If your order has not yet shipped, you can contact customer support to update your shipping address.
Answer: To track your package, simply wait for an email from us with your tracking number after your order has shipped. Once you receive this email, you can use the tracking number to monitor the status of your package on our website or through the carrier's tracking system.

If you have any issues or concerns about your package tracking, don't hesitate to reach out to our customer support team via email at support@example.com or by calling our toll-free number.

Citations:
[1] How do I track my order?
[2] How can I contact customer support?
[3] How do I use a discount code?
[4] Can I change my shipping address?
```
---
---
