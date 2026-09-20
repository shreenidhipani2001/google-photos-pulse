# 📋 Google Photos Graduation Project: Remaining Scope & Roadmap (`left.md`)

This document provides a thorough, point-wise breakdown of everything remaining to complete the Google Photos Product Management Graduation Project based on the original problem statement, evaluation criteria, and case study objectives.

---

## 📌 Executive Status: Where We Are Now

| Component | Status | Description |
| :--- | :--- | :--- |
| **1. Discovery & Telemetry Dashboard** |  **COMPLETED** | **Photos Review Pulse**: 96,926 cleaned substantive reviews across 13 platforms, 14 complaint themes, sentiment donut, star ratings, dual-axis timeline (2018–2026), keyword explorer, and interactive review table. |
| **2. Cleaned Data Assets** |  **COMPLETED** | Master CSV (49.3 MB) and Excel (20.3 MB) with < 8 words and emoji spam removed; safety backups created; 30 episodic test cases; 35-item photo catalog. |
| **3. AI RAG Retrieval Engine** |  **COMPLETED** | Pure-Python vector retrieval (`PureTfidfVectorizer`), episodic query expansion, multimodal OCR & visual description similarity matching, zero-DLL compatibility. |
| **4. Primary User Research & Personas** | ⏳ **PENDING** | Qualitative user interviews, user surveys, user journey mapping, and persona synthesis. |
| **5. Evaluator "Before vs. After" Solution Prototype** | ⏳ **PENDING** | Direct side-by-side comparison illustrating what changed, the exact problem solved, and the final production UX provided to the customer. |
| **6. 10-Slide Executive Presentation Deck** | ⏳ **PENDING** | Formal PM case study slide deck with narrative, telemetry data, architecture, edge cases, and business impact. |

---

## 🔍 Task-by-Task Breakdown of Remaining Deliverables

---

### PART 1: Primary User Research & Behavioral Insights
*Objective: Complement the secondary telemetry (96,926 app reviews) with direct primary qualitative and quantitative data.*

- [ ] **1.1 User Interview Synthesis (Qualitative Fieldwork)**:
  - Conduct/document 5–8 user interview transcripts across core demographic segments.
  - Formulate structured interview protocol questions:
    - *"Describe the last time you spent more than 5 minutes searching for a specific photo."*
    - *"What exact details did you remember, and what did you type into the search bar?"*
    - *"What did the search results show, and what was your emotional reaction when it failed?"*
  - Extract verbatim user quotes highlighting the **"Semantic Recall Gap"** (e.g., recalling sensory details like lighting, mood, weather, or relative occasions instead of file dates or filenames).

- [ ] **1.2 Quantitative User Survey (Pain Point Validation)**:
  - Survey dataset of 50–100 responses ranking retrieval frustrations:
    - Frequency of vague memory searches per week.
    - Percentage of searches abandoned due to zero or irrelevant results.
    - Top forgotten vs. remembered attributes (validating the 88% visual/emotional recall vs. 12% exact date recall data).

- [ ] **1.3 User Personas (3 Archetypes)**:
  - **Persona A: "The Caregiver / Parent"** (Needs to find medical prescriptions, vaccination slips, baby milestones by relative time *"when she had high fever last rainy season"*).
  - **Persona B: "The Visual Explorer / Traveler"** (Recalls aesthetics, colors, weather, atmospheres *"that yellow sunset beach cafe with bamboo chairs in Goa"*).
  - **Persona C: "The Power Professional / Document Hunter"** (Searches receipts, whiteboards, parking slips, handwritten notes with partial OCR memory).

- [ ] **1.4 Customer Journey Map ("Current Broken Search" vs. "Future Episodic Search")**:
  - Step-by-step emotional curve from trigger → attempt 1 (failed keyword) → attempt 2 (frustrated scrolling) → abandonment vs. AI RAG guided retrieval.

---

### PART 2: Publicly Accessible Solution Prototype & Evaluator Workflow
*Objective: Build an evaluator-friendly interface that clearly showcases what changed, what we are solving, and the final customer experience.*

- [ ] **2.1 "Before vs. After" Evaluator Comparison Panel**:
  - Create a dedicated evaluation tab: **"⚖️ Solution Comparison: Before vs. After"**.
  - **Left Side (Legacy Google Photos Search)**:
    - Simulates current production behavior (exact keyword matching on EXIF dates/filenames).
    - Demonstrates failure on vague queries (e.g., query *"medicine for fever last winter"* returns *0 results* because EXIF metadata only stores `IMG_20250114.jpg` without symptom labels).
  - **Right Side (Episodic AI Search Assistant - Our Solution)**:
    - Demonstrates the 3-stage RAG pipeline:
      1. *Episodic Query Expander* maps *"fever"* → *Paracetamol, thermometer, medicine box, pharmacy*.
      2. *Multimodal Vector Matcher* retrieves candidate photos via OCR text and visual scene descriptions.
      3. *Confidence Score & Match Card* displays the photo with confidence percentage and matched clues highlighted.

- [ ] **2.2 Pre-loaded Evaluator Benchmark Test Suite (5 Instant Scenarios)**:
  - Provide clickable 1-click test scenarios so evaluators can test instantly without typing:
    - **Scenario 1 (Medical / Health)**: *"Medicine box when I was sick with fever"* → Retrieves Paracetamol nightstand photo via OCR.
    - **Scenario 2 (Travel / Scenery)**: *"Sunset beach with blue chairs in Goa"* → Retrieves Anjuna beach photo via scene descriptors.
    - **Scenario 3 (Financial / Receipt)**: *"Dinner receipt from Italian restaurant downtown"* → Retrieves restaurant bill via OCR total.
    - **Scenario 4 (Document / Handwritten)**: *"Grandma's handwritten chocolate chip cookie recipe"* → Retrieves notebook scan.
    - **Scenario 5 (Automotive / Parking)**: *"Where did I park my car on level 3?"* → Retrieves garage ticket photo.

- [ ] **2.3 Edge Case & Fallback Workflow Demonstration**:
  - Implement and visualize the 5 mitigation mechanisms defined in `gemini-code-1789927520637.md`:
    - **EC-01 Zero Memory Anchors**: Guided clarification prompts (asking *"Was it indoors or outdoors?"*).
    - **EC-02 Contradictory Clues**: Constraint relaxation alerting user (*"Delhi doesn't have a beach, but here are Goa beach photos"*).
    - **EC-03 Corrupted/Missing EXIF**: Fallback to OCR and visual semantic tags.
    - **EC-04 Multi-Asset Ambiguity**: Clustered candidate carousel.
    - **EC-05 Code-switching / Hinglish**: Semantic cross-lingual retrieval (*"dawai ki photo jo pichle saal li thi"*).

- [ ] **2.4 Final Customer-Facing UI Design Mockups**:
  - High-fidelity interactive UI screens showing how this feature lives inside the native Google Photos mobile app:
    - The new **"Ask Google Photos"** conversational search bar with Material Design 3 clue chips.
    - Interactive thumbnail inspection drawer with highlighted OCR bounding boxes.
    - Privacy & on-device processing trust indicators.

---

### PART 3: 10-Slide Executive Presentation Deck (PPT)
*Objective: A complete, structured pitch deck for presentation to evaluators, faculty, and product leadership.*

- [ ] **Slide 1: Title & Executive Summary**
  - Project Title: *Google Photos Episodic Search: Bridging the Human Memory Gap*.
  - Problem overview, product vision, and team/author info.
- [ ] **Slide 2: The Problem: The "Semantic Recall Gap"**
  - Human cognitive recall (88% visual/emotional cues) vs. database metadata (EXIF dates/filenames).
  - Voice of customer verbatim complaints.
- [ ] **Slide 3: Market Telemetry & Secondary Research**
  - Key findings from 96,926 cleaned reviews across 13 platforms.
  - Search & AI failure rate (31.8% negativity), Play Store vs. App Store divergence.
- [ ] **Slide 4: Primary User Research & Personas**
  - Key insights from user interviews and survey data.
  - Introduction of the 3 user personas and journey map friction points.
- [ ] **Slide 5: Product Vision & Solution Architecture**
  - High-level system diagram: User query → Query expansion → Multimodal embeddings → RAG generation.
  - Privacy-preserving on-device vs. cloud hybrid processing model.
- [ ] **Slide 6: Product Demo: The Evaluator Prototype**
  - Screenshots / walkthrough of the live prototype.
  - Before (0 results) vs. After (accurate retrieval with reasoning).
- [ ] **Slide 7: Technical Implementation & RAG Pipeline**
  - TF-IDF / embedding similarity, OCR integration, and confidence scoring algorithms.
- [ ] **Slide 8: Edge Cases, Guardrails & Trust & Safety**
  - Detailed mitigation of hallucinations, contradictory queries, and zero-anchor inputs.
- [ ] **Slide 9: Product Metrics, KPIs & Success Framework**
  - North Star Metric: *Successful Episodic Retrieval Rate (SERR)*.
  - Secondary KPIs: Search Abandonment Rate, Time-to-Retrieval (TTR), CSAT.
- [ ] **Slide 10: Rollout Roadmap, GTM & Future Scope**
  - Phase 1 (Alpha testing on device), Phase 2 (Gemini Nano on Pixel), Phase 3 (Global Google Photos rollout).

---

### PART 4: Verification & Final Polish
- [ ] Deploy the complete application to GitHub and Streamlit Community Cloud.
- [ ] Verify live public URL access across desktop and mobile devices.
- [ ] Package all documentation, presentation slides, and dataset files into a final graduation project submission folder.
