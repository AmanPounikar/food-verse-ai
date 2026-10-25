# 🥑 Food Verse AI - Multimodal Food Intelligence Agent
**Skill Wallet Capstone Project 3 • Food Science & AI Systems Engineering**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-emerald.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A production-ready, full-stack multimodal food intelligence platform built in Python and Streamlit. Food Verse AI bridges clinical nutritional science, computational food microbiology, commercial kitchen HACCP safety audits, and automated metabolic planning into a unified, zero-external-database intelligence system.

---

## 🌟 Core Pillars & Epics

### 1. ⚙️ Configuration & Persona Management
- **Multi-Engine Intelligence**: Seamless support for **Google Gemini** (`gemini-3.8-flash`, `gemini-2.5-flash`), **Groq** (`llama-3.3-70b-versatile`, `llama-3.2-11b-vision-preview`), and an **Offline Standalone Demonstration Engine**.
- **Zero-Barrier Demo Mode**: Automatically functions with rich, pre-loaded food science heuristics and synthetic visual test cases when no API key is provided.
- **Secure Key Handling**: Ingests keys via Streamlit sidebar password masks, environment variables, or `.streamlit/secrets.toml`.

### 2. 🥗 Tab 1 - Food Recognition & Nutrition Audit (Epic 2)
- **Multimodal Visual Ingestion**: Analyzes meal photos to detect dishes, culinary origins, and individual ingredients with confidence scores.
- **Precision Macronutrient Breakdown**: Calculates Calories (kcal), Protein (g), Carbohydrates (g), Total & Saturated Fats (g), Dietary Fiber (g), Sugars (g), and Sodium (mg).
- **Allergen Alerting System**: Automatic detection of Big 9 allergens (Dairy, Gluten, Eggs, Fish, Shellfish, Tree nuts, Peanuts, Wheat, Soy).
- **Composite Health Score (1-100)**: Nutri-Score inspired algorithmic rating with clinical dietary rationale.
- **Interactive Visualizations**: Dynamic Plotly caloric macro donut charts and exercise burn equivalents (Running, Cycling, Walking).

### 3. 🔬 Tab 2 - Food Freshness & Spoilage Diagnostic (Epic 3)
- **Perishable Diagnostic Scanner**: Computer vision analysis of fruits, vegetables, meats, dairy, and baked goods.
- **Microbial & Morphological Checks**: Evaluates surface texture turgidity, enzymatic discoloration, moisture desiccation/wrinkling, and fungal mycelium colonies (*Botrytis*, *Penicillium*).
- **Freshness Stage Classification**: Classifies items into `Fresh`, `Moderately Fresh`, or `Spoiled`.
- **Actionable Safety Verdict**: Explicit flags (`Safe to consume`, `Consume within 24h`, `Discard immediately`).
- **Preservation & Storage Protocol**: Optimal storage temperatures (°C), humidity targets, ethylene gas sensitivities, and freezing viability guidelines.

### 4. 🧑‍🍳 Tab 3 - Commercial Kitchen Hygiene & Food Safety Compliance (Epic 4)
- **Automated HACCP Inspection**: Scans commercial food prep lines, hot stations, and butchery areas.
- **Hygiene Vector Detection**:
  - PPE adherence: Chef hats, hairnets, beard restraints, and single-use nitrile gloves.
  - Cross-contamination: Proximity of raw animal proteins (poultry, beef) to ready-to-eat salads or porous surfaces.
  - Sanitization compliance: Chemical cleaner storage isolation and surface sanitization state.
- **HACCP Compliance Rating**: Computes an overall Kitchen Hygiene Compliance Score (%) and assigns letter grades (Grade A, Grade B, Grade C).
- **Itemized Violation Logs**: Flagged by severity (`CRITICAL`, `MAJOR`, `MINOR`) with mandatory corrective actions according to FDA Food Code standards.

### 5. 👨‍🍳 Tab 4 - Smart Kitchen Recipe Assistant (Epic 4)
- **Zero-Waste Pantry Inventory**: Users select staple pantry ingredients or enter custom ingredients.
- **Culinary Synthesis Engine**: Crafts balanced, creative recipes utilizing existing inventory to minimize food waste.
- **Comprehensive Cooking Briefs**: Prep times, cook times, difficulty levels, macro profiles per serving, and step-by-step instructions.
- **Smart Substitution Matrix**: Provides drop-in ingredient swaps (e.g., silken tofu for eggs, Greek yogurt for sour cream) with chef culinary notes.

### 6. 🧬 Tab 5 - Personalized Precision Meal Planner (Epic 5)
- **Biometric Metabolic Profiling**: Inputs age, biological sex, height, weight, activity level, and dietary constraints (Vegan, Keto, Diabetic-Friendly, Mediterranean).
- **Scientific Caloric Math**: Computes Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) via the **Mifflin-St Jeor Equation**.
- **Target Macro Optimization**: Sets goal-adjusted caloric targets (fat loss deficit, muscle gain surplus) and macro gram distributions.
- **Adaptive 7-Day Schedule**: Full weekly matrix detailing Breakfast, Lunch, Dinner, and Snacks.
- **Consolidated Grocery Logistics**: Automatically aggregates weekly ingredients grouped by supermarket aisle (Produce, Proteins, Dairy, Pantry Staples) with 1-click text and JSON download.

---

## 🏗️ Project Architecture & Directory Structure

```
food/
├── .streamlit/
│   └── config.toml             # Custom theme colors (Emerald & Amber, Dark/Light harmonious)
├── modules/
│   ├── ai_engine.py            # Unified multimodal engine (Gemini, Groq, Standalone Demo)
│   ├── food_recognition.py     # Tab 1: Vision recognition & nutrition audit
│   ├── freshness_diagnostic.py # Tab 2: Spoilage diagnostics & preservation guides
│   ├── kitchen_hygiene.py      # Tab 3: HACCP safety inspection & violation logger
│   ├── recipe_assistant.py     # Tab 4: Pantry inventory synthesis & substitutions
│   ├── meal_planner.py         # Tab 5: Mifflin-St Jeor metabolic planner & grocery compiler
│   ├── sample_data.py          # Synthetic visual presets & sample generation
│   └── ui_components.py        # Modern CSS styles, metric cards, Plotly charts
├── app.py                      # Streamlit application entry point & navigation
├── requirements.txt            # Production dependencies
└── README.md                   # Comprehensive documentation
```

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.10 or higher
- `pip` or `conda`

### 1. Clone or Open Workspace
```bash
cd c:\Project\food
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🔑 API Key Configuration (Optional)

The application includes a built-in **Standalone Demonstration Mode** that requires zero API keys. To connect live frontier AI models:

### Option A: Via Streamlit UI
Enter your key directly into the password field in the sidebar.

### Option B: Local Environment Variables
```bash
# For Google Gemini
export GEMINI_API_KEY="AIzaSy..."

# For Groq
export GROQ_API_KEY="gsk_..."
```

### Option C: Streamlit Secrets (`.streamlit/secrets.toml`)
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "AIzaSy..."
GROQ_API_KEY = "gsk_..."
```

---

## ☁️ 1-Click Streamlit Community Cloud Deployment

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Connect your repository and select `app.py` as the main file path.
4. (Optional) In **Advanced Settings**, paste your `GEMINI_API_KEY` into the Secrets box.
5. Click **Deploy**! The app will spin up with 0 external database setup.

---

## 🧪 Scientific & Regulatory References

1. **Mifflin-St Jeor Equation**:
   - $\text{BMR (Men)} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age} + 5$
   - $\text{BMR (Women)} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age} - 161$
2. **HACCP (Hazard Analysis Critical Control Point)**:
   - FDA Food Code 2026 guidelines for physical separation of raw poultry/meat from ready-to-eat produce.
   - Temperature danger zone monitoring ($4^\circ\text{C}$ to $60^\circ\text{C}$).
3. **USDA FoodData Central & Nutri-Score**:
   - Algorithmic macro distribution and micronutrient density scoring for composite meal grading.
