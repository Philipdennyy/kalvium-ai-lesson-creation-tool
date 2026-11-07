# AI Lesson Creation Tool

An AI-powered lesson creation tool that researches educational resources, generates structured lessons, and validates them through two independent quality-control layers.

## Overview

The application takes a **Lesson Title** and **Learning Objective** and creates an AI-powered lesson suitable for a 45-minute learning session.

The workflow:

1. Researches relevant web sources.
2. Searches for relevant books.
3. Retrieves relevant YouTube videos.
4. Generates a structured lesson using Google Gemini.
5. Performs factual-accuracy validation.
6. Performs instructional-quality validation.
7. Allows the instructor to review and edit the lesson.
8. Applies QC recommendations to improve the lesson.
9. Provides a final preview and downloadable exports.

## Architecture

```text
Streamlit
    |
    v
Azure-hosted n8n
    |
    +---- Tavily Web Research
    |
    +---- Gemini Book Search Keyword
    |          |
    |          v
    |     Open Library
    |
    +---- YouTube Data API
    |
    v
Research Package
    |
    v
Gemini Lesson Generation
    |
    +---- QC 1: Research & Factual Accuracy
    |
    +---- QC 2: Instructional Quality
    |
    v
Streamlit Review & Editing
    |
    v
Gemini Revision Workflow
    |
    v
Final Lesson + Export
```

## Features

### AI Lesson Generation

The user provides:

- Lesson Title
- Learning Objective

The system generates a structured lesson containing:

- Explanations
- Examples
- Practical applications
- Learning activities
- Knowledge checks
- Time allocation for a 45-minute session
- Relevant references
- YouTube learning resources

### Research

The workflow uses three research sources:

- **Tavily** for web research
- **Open Library** for book research
- **YouTube Data API** for video research

Gemini identifies a focused topic or keyword for the Open Library search so that book research can adapt to different lesson topics.

### QC Layer 1 — Research & Factual Accuracy

A separate Gemini evaluation checks:

- Factual correctness
- Unsupported or misleading claims
- Source reliability and relevance
- Missing information
- Inconsistencies

It produces a separate factual-accuracy audit report with issues and suggested improvements.

### QC Layer 2 — Instructional Quality

A second independent Gemini evaluation checks:

- Alignment with the learning objective
- Clarity
- Structure
- Relevance
- Examples
- Practical applications
- Activities
- Knowledge checks
- 45-minute feasibility

It produces a separate instructional-quality audit report.

### Instructor Review

The instructor can:

- Review the generated lesson
- Edit the lesson
- Save edits
- Preview the final version
- Apply QC recommendations

### Export

The application provides three downloadable files:

- `final_lesson.md`
- `lesson_report.md`
- `lesson_project.json`

The lesson report includes the final lesson, research references, YouTube resources, and both QC reports.

## Technologies

- Python
- Streamlit
- n8n
- Google Gemini
- Tavily
- Open Library API
- YouTube Data API
- Azure

## Project Structure

```text
kalvium-ai-lesson-creation-tool/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── n8n/
│
├── data/
│
└── outputs/
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Philipdennyy/kalvium-ai-lesson-creation-tool.git
cd kalvium-ai-lesson-creation-tool
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the workflow

The n8n workflows require credentials for:

- Google Gemini
- Tavily
- YouTube Data API

Open Library search does not require an API key for the implementation used in this project.

The Streamlit application also requires the production webhook URLs for the lesson-generation and lesson-revision workflows.

Do not commit API keys or private credentials to the repository.

## Running the Application

Run:

```bash
streamlit run app.py
```

Then enter a lesson title and learning objective and click **Generate Lesson**.

## n8n Workflows

### Lesson Generation Workflow

The main workflow:

1. Receives the lesson title and learning objective.
2. Performs Tavily web research.
3. Generates a focused book-search keyword.
4. Searches Open Library.
5. Searches YouTube.
6. Combines the research into a research package.
7. Generates the lesson using Gemini.
8. Runs QC Layer 1.
9. Runs QC Layer 2.
10. Returns the result to Streamlit.

### Lesson Revision Workflow

The revision workflow receives:

- Current lesson
- Learning objective
- QC Layer 1 report
- QC Layer 2 report

Gemini uses these reports to improve the lesson while maintaining the learning objective and 45-minute structure.

## Error Handling

The application handles:

- Empty inputs
- Workflow failures
- Request timeouts
- Connection errors
- Invalid workflow responses

The application uses Streamlit session state to preserve generated content and instructor edits during the session.

Failed generation or revision operations can be retried.

## Testing

### Required Test

**Lesson Title**

```text
HTTP Requests and Responses
```

**Learning Objective**

```text
Explain GET and POST methods and distinguish between 2xx, 4xx, and 5xx response status categories.
```

### Additional Test

**Lesson Title**

```text
Database Normalization
```

**Learning Objective**

```text
Explain 1NF, 2NF, and 3NF and identify common data redundancy problems in relational databases.
```

These tests demonstrate that the research and generation workflow adapts to different lesson topics.

## Technical Decisions

### n8n

n8n was selected as the workflow orchestration layer because the application requires multiple sequential AI and research steps.

### Separate QC Layers

Factual accuracy and instructional quality are different evaluation dimensions, so they are handled by two separate Gemini evaluation steps.

### Open Library

Open Library was used for book research to provide a practical book-search source without depending on the Google Books API quota.

### Gemini

Gemini is used for:

- Book-search keyword generation
- Lesson generation
- Factual-accuracy QC
- Instructional-quality QC
- Lesson revision

### Streamlit

Streamlit provides a simple instructor-facing interface while allowing the project to focus on the AI workflow and research functionality.

## Limitations

- AI-generated content should still be reviewed by an instructor.
- Research quality depends on the retrieved sources.
- External API availability and rate limits can affect execution.
- The current implementation is intended as a functional demonstration and does not implement production-level authentication or multi-user persistence.

## External Resources

This project uses:

- Google Gemini
- Tavily
- Open Library
- YouTube Data API
- n8n
- Streamlit

These services are used for research, AI generation, validation, and workflow orchestration.