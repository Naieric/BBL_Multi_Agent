# Example runs

Transcripts below are real output captured on 2026-07-26 against `gemini-3.6-flash`
and `gemini-embedding-001`. Nothing here is illustrative or hand-written.

---

## 1. Direct factual question

```
$ python main.py "What is the standard warranty period and what does it cover?"

--- Retrieved context ---
The standard hardware warranty on all Aurora Dynamics robots is 24 months from the date of delivery. The warranty covers manufacturing defects, drive motor failure, and battery capacity degradation below 70 percent of rated capacity. It does not cover collision damage, water ingress, or damage caused by operating the robot outside its rated temperature range.

An extended warranty is available for purchase within 90 days of delivery. The extended warranty adds 24 months of coverage beyond the standard period, for a total of 48 months, and costs 15 percent of the robot's original purchase price.

Aurora Dynamics operates a certified refurbishment program. Robots returned under exchange are reconditioned, re-certified to original specification, and resold at 65 percent of the new unit price. Refurbished robots carry a 12-month warranty rather than the standard 24 months.

--- Answer ---
The standard warranty period is 24 months from the date of delivery. It covers:

* Manufacturing defects
* Drive motor failure
* Battery capacity degradation below 70 percent of rated capacity
```

The retriever returned three related passages; the report generator answered from the
first and ignored the other two rather than padding the answer with them.

---

## 2. Question spanning two unrelated passages

```
$ python main.py "How much does the Halden X cost and how is Beacon licensed?"

--- Answer ---
The Halden X is priced at 58,000 euros per unit.

Beacon is licensed per robot at 90 euros per robot per month, billed annually.
```

Pricing and licensing live in different paragraphs of `knowledge_base.txt`. Semantic
retrieval pulled both.

---

## 3. Question the knowledge base cannot answer

```
$ python main.py "What is Aurora Dynamics' revenue for 2025 and who is the CEO?"

--- Answer ---
Based on the provided context, there is no information about Aurora Dynamics' revenue for 2025 or who the CEO is.
```

This is the important one. Aurora Dynamics is fictional, so a model answering from its
own knowledge would have to invent a CEO and a revenue figure. It declines instead.

---

## 4. Error paths

Missing API key:

```
$ python main.py "What is the warranty period?"
Error: GOOGLE_API_KEY is not set. Copy .env.example to .env and add your key from https://aistudio.google.com/apikey.
```

Invalid API key:

```
$ python main.py "What is the warranty period?"
Error calling the model: Error calling model 'gemini-3.6-flash' (INVALID_ARGUMENT): 400 INVALID_ARGUMENT. ... 'API key not valid. Please pass a valid API key.'
```

No question supplied:

```
$ python main.py ""
No question provided.
```

All three exit with status 1 and no traceback.

---

## 5. Tests

```
$ pytest tests
.....                                                                    [100%]
5 passed in 2.19s
```
