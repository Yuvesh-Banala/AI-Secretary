from summarizer import summarize_email

sample_email = """
Hey Yuvesh, just a reminder that our project presentation is due Friday at 2 PM.
Please make sure the slides are updated and the demo is working by tomorrow afternoon.
"""

summary = summarize_email(sample_email)
print("Summary:", summary)