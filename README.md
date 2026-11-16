# Dishank Jain · AI Engineer

I build Python applications for search, document extraction, and product recommendations. In my support systems, one question shapes the design: **how do you know the assistant retrieved the right answer?**

[Connect on LinkedIn](https://www.linkedin.com/in/dishankjain25/)

## Start with the code

| Project | What to look for |
| --- | --- |
| [Zigly PawSupport](https://github.com/Dishank25/ZiglyPawSupport) | A FastAPI assistant that checks curated FAQs before generating a response. The [offline evaluation runner](https://github.com/Dishank25/ZiglyPawSupport/blob/main/evaluation/run_evaluation.py) tests whether the router selected the expected FAQ ID. |
| [SupportPilot](https://github.com/Dishank25/supportpilot) | A smaller implementation of retrieval-augmented support. Follow a request through the [chat endpoint](https://github.com/Dishank25/supportpilot/blob/main/main.py) to see how intent classification, ChromaDB retrieval, and a confidence threshold determine whether the system answers. |

## Other engineering work

- **Document extraction.** Built a FastAPI service that turns veterinary PDFs into structured pet, treatment, and follow-up records. It validates the extracted fields before exporting them to Excel.
- **Product recommendations.** Compared purchase frequency and order quantity in a collaborative filtering model. I used cosine similarity to find customers with related purchase histories and excluded products each customer had already bought.
- **Vision prototype.** Used GPT-4o Vision to identify pet breeds from uploaded photos. The API checks the image and the model’s JSON response and returns an unknown result when confidence is low.

**Tools I use:** Python, FastAPI, Pydantic, ChromaDB, pandas, NumPy, scikit-learn, and Git.
