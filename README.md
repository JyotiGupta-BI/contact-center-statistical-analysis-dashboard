# Contact Center Operational Analytics

An end-to-end **Contact Center Operational Analytics** project using Python and Streamlit to analyze operational performance, workforce-related metrics, customer satisfaction, resolution outcomes, root causes, and management actions.

The project uses a structured contact-center dataset containing **5,000 calls across 8 agents and 5 contact topics over a 90-day period**.

The objective was not just to build a dashboard, but to answer business questions that a contact-center operations or workforce-management team could use for performance review and decision-making.

---

## Project Objective

The analysis was designed to answer ten business questions:

1. What is the overall performance of the contact center?
2. How consistent is operational performance?
3. How has performance changed over time?
4. How does performance vary across agents?
5. Which contact topics present operational challenges?
6. What factors are associated with customer satisfaction?
7. What factors are associated with call resolution?
8. Why do some calls take longer to handle?
9. Can available operational variables predict low customer satisfaction?
10. What actions should management consider based on the findings?

---

## Dataset

The dataset contains the following fields:

* Call ID
* Agent
* Date
* Time
* Topic
* Answered (Y/N)
* Resolved
* Speed of Answer
* Average Talk Duration
* Satisfaction Rating

### Dataset Coverage

| Metric                               |        Value |
| ------------------------------------ | -----------: |
| Total Calls                          |        5,000 |
| Agents                               |            8 |
| Topics                               |            5 |
| Analysis Period                      | Jan–Mar 2021 |
| Answered Calls                       |        4,054 |
| Unanswered Calls                     |          946 |
| Overall Answer Rate                  |       81.08% |
| Overall Resolution Rate              |       72.92% |
| Resolution Rate Among Answered Calls |       89.94% |
| Average Speed of Answer              |    67.52 sec |
| Average Talk Duration                |   224.92 sec |
| Average Satisfaction                 |     3.40 / 5 |

---

## Analytical Approach

The project follows this workflow:

**Raw Excel Data → Python Analysis → Excel Analytical Outputs → Streamlit Application → Management Presentation**

### 1. Data Preparation

Python was used to:

* Load and inspect the raw dataset
* Validate data types and missing values
* Convert date fields for time-based analysis
* Convert call duration into seconds for numerical analysis
* Separate answered and unanswered calls where appropriate
* Create analytical measures required for the business questions

Operational metrics such as talk duration, speed of answer and satisfaction were analyzed using **answered calls**, avoiding the distortion that would occur if unanswered calls were included in measures that require interaction data.

---

## Business Analysis

### Q1 — Overall Contact Center Performance

**Analysis type:** Descriptive Statistics

The overall KPI analysis established the baseline performance of the operation.

Key measures included:

* Call volume
* Answer rate
* Resolution rate
* Speed of answer
* Talk duration
* Customer satisfaction

The contact center handled **5,000 calls**, with an **81.08% answer rate** and **72.92% overall resolution rate**.

---

### Q2 — Performance Consistency

**Analysis type:** Descriptive Statistics / Variability Analysis

Variability was examined using:

* Mean
* Standard deviation
* Variance
* Median
* Quartiles
* Percentiles

For Speed of Answer:

* Mean: **67.52 sec**
* Median: **68 sec**
* P90: **114 sec**
* P95: **120 sec**
* Maximum: **125 sec**

This analysis helps identify whether average performance adequately represents the operational experience or whether a portion of calls experiences materially longer response times.

---

### Q3 — Performance Over Time

**Analysis type:** Trend Analysis

Monthly performance was compared across January, February and March.

The analysis showed:

* Call volume declined after January.
* Answer rate declined from **82.11% in January to 80.32% in February**, with a slight recovery to **80.71% in March**.
* Resolution rate followed a similar pattern.
* Customer satisfaction declined from **3.45 in January to 3.37 in March**.
* Average Speed of Answer remained relatively stable at approximately 67–68 seconds.

One important observation was that the decline in satisfaction occurred despite relatively stable response time, indicating that response time alone does not explain the customer-experience movement.

---

### Q4 — Agent Performance

**Analysis type:** Comparative Analysis

Agent-level performance was reviewed across:

* Call volume
* Answer rate
* Resolution
* Speed of Answer
* Talk duration
* Customer satisfaction

The analysis focuses on identifying performance variation while recognizing that agent comparisons should be interpreted alongside **call mix and topic complexity**.

---

### Q5 — Topic Analysis

**Analysis type:** Comparative Analysis / Root Cause Analysis

The five contact topics were compared across:

* Call volume
* Resolution
* Talk duration
* Customer satisfaction

Topic-level analysis showed more visible variation in resolution and handling time than some of the agent-level comparisons.

**Streaming** had the lowest resolution rate among answered calls at approximately **88.43%**, while **Technical Support** was approximately **91.43%**.

This indicates that topic-specific complexity, process dependencies or resolution barriers are areas worth investigating.

---

### Q6 — Customer Satisfaction Drivers

**Analysis type:** Driver Analysis

The analysis examined whether operational variables were associated with customer satisfaction.

Variables included:

* Speed of Answer
* Talk Duration
* Resolution
* Topic
* Agent

Correlation analysis showed approximately:

* Speed of Answer vs Satisfaction: **0.001**
* Talk Duration vs Satisfaction: **0.000**

These results indicate that the available response-time and talk-duration variables showed **little observable linear association** with satisfaction in this dataset.

Topic and agent-level satisfaction differences were also relatively small.

Therefore, improving response time alone should not automatically be assumed to improve customer satisfaction.

---

### Q7 — Resolution Drivers

**Analysis type:** Driver Analysis / Root Cause Analysis

Resolution performance was analyzed using answered calls to avoid the mechanical relationship between unanswered calls and unresolved outcomes.

Resolution rates varied by topic, with:

* Streaming: **88.43%**
* Payment related: **89.12%**
* Contract related: **89.86%**
* Admin Support: **90.94%**
* Technical Support: **91.43%**

The topic-level differences were more visible than the agent-level differences.

This suggests that process complexity, dependencies or topic-specific resolution barriers may warrant further investigation.

---

### Q8 — Talk Duration Root Cause Analysis

**Analysis type:** Root Cause / Driver Analysis

Average talk duration for answered calls was approximately:

**224.92 seconds**

Talk duration was analyzed across topics and agents.

The longest average topic handling times were observed in:

* Admin Support: ~228 sec
* Contract related: ~228 sec
* Streaming: ~228 sec

Payment-related calls had the lowest average talk duration at approximately **216 seconds**.

Speed of Answer and Talk Duration had an approximately zero correlation (**-0.003**), indicating that faster answering did not explain shorter conversations in this dataset.

This points toward call complexity and topic characteristics as areas for further investigation.

---

### Q9 — Predictive Analysis

**Analysis type:** Predictive Analytics

A Logistic Regression model was developed to test whether available operational variables could predict **low customer satisfaction**.

The model used:

* Speed of Answer
* Talk Duration
* Resolution
* Topic
* Agent

The model produced approximately:

* Accuracy: **47.3%**
* ROC-AUC: **0.46**

The model did not demonstrate useful predictive performance with the available variables.

Rather than overstating the result, the analysis identifies the limitation of the current dataset and highlights additional variables that could improve future predictive modelling.

Potential additional variables include:

* Call reason/sub-reason
* Transfer count
* Hold duration
* First Contact Resolution
* Repeat contact indicator
* Escalation
* Complaint indicator
* Customer segment
* Customer tenure
* Interaction quality

---

## Key Management Findings

The analysis produced several management-level observations:

### 1. Customer satisfaction declined while response time remained relatively stable

This suggests that response time alone is unlikely to explain the decline in customer satisfaction.

### 2. Topic-level differences require attention

Streaming showed the lowest resolution performance among answered calls.

### 3. Some topics require longer interactions

Admin Support, Contract-related and Streaming calls showed relatively higher average talk duration.

### 4. Agent comparisons require call-mix context

Differences between agents should not automatically be interpreted as individual performance gaps without considering the types and complexity of calls handled.

### 5. Current data is insufficient for reliable prediction

The predictive model demonstrated limited performance, highlighting the need for richer operational and customer-level data.

---

## Recommended Management Actions

Based on the analysis, the following areas were identified for management review:

1. Investigate the causes of lower resolution performance in Streaming-related contacts.
2. Review process dependencies and knowledge gaps for higher-duration topics.
3. Investigate the decline in customer satisfaction beyond Speed of Answer.
4. Compare agents within comparable topic/call-mix groups.
5. Capture additional operational variables to support stronger predictive and driver analysis.
6. Use topic-level trends and operational KPIs as part of regular performance reviews.

These are analytical recommendations based on the available dataset and are intended to guide further investigation rather than establish causality.

---

## Streamlit Application

The Streamlit application converts the analytical results into an interactive business-facing application.

The application provides sections for:

* Executive Overview
* Performance Trends
* Agent Performance
* Topic Analysis
* Customer Satisfaction
* Resolution Analysis
* Root Cause / Driver Analysis
* Predictive Analysis
* Management Actions

The objective is to make the analytical findings easier to explore through filters, KPI summaries and interactive visual analysis.

---

## Technology Stack

**Data & Analysis**

* Python
* Pandas
* NumPy
* Scikit-learn

**Application**

* Streamlit

**Data Source / Output**

* Microsoft Excel

**Analysis & Business Communication**

* Jupyter Notebook
* Microsoft Excel
* Microsoft PowerPoint

**Version Control / Deployment**

* GitHub
* Streamlit deployment

---

## Project Structure

```text
contact-center-operational-analytics/
│
├── data/
│   └── contact_center_data.xlsx
│
├── notebooks/
│   └── contact_center_analysis.ipynb
│
├── app/
│   └── streamlit_app.py
│
├── outputs/
│   └── analysis_results.xlsx
│
├── presentation/
│   └── management_review.pptx
│
├── README.md
└── requirements.txt
```

---

## What This Project Demonstrates

This project demonstrates an end-to-end approach to operational analytics:

**Business Problem Definition → Data Preparation → Descriptive Analysis → Trend Analysis → Comparative Analysis → Driver Analysis → Root Cause Analysis → Predictive Testing → Actionable Recommendations → Interactive Application → Management Communication**

The emphasis is on translating operational data into business questions, measurable findings and management actions rather than building a dashboard alone.

---

## Limitations

The dataset contains operational-level information but does not include several variables that are commonly useful for deeper contact-center analysis.

Therefore:

* Correlation does not establish causation.
* Agent comparisons should consider call mix.
* Predictive model performance is limited by available features.
* The management recommendations identify areas for investigation rather than proving specific root causes.

---

## Author

**Jyoti Gupta**

Business Operations & Analytics | CX & WFM Analysis | Operational Reporting | Process Improvement
