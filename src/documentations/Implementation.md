# Implementation Steps

## 1. Data Preprocessing

**Objective**  
Convert raw ticket data into a clean, analysis-ready format.

### Steps
1. **File loading**</br>
Accepts `.txt` files with tab/comma delimiters. Uses `DataLoader`:

```python
def load_from_text(text_content: str) -> pd.DataFrame:
    # Detect delimiter (tab or comma)
    # Convert to DataFrame with error handling
```
2. **Data Cleaning:**
- Filters tickets by valid service categories (```HDW```, ```NET```, ```KAI```, etc.):
```python
valid_categories = ['HDW', 'NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD']
df = df[df['SERVICE_CATEGORY'].isin(valid_categories)]
```
- Converts date columns to datetime:
```python
df['ACCEPTANCE_TIME'] = pd.to_datetime(df['ACCEPTANCE_TIME'], errors='coerce')
```
- Calculates resolution time (hours):
```python
df['RESOLUTION_HOURS'] = (df['COMPLETION_TIME'] - df['ACCEPTANCE_TIME']).dt.total_seconds() / 3600
```
3. **Validation**
- Checks for required columns (```ORDER_NUMBER```, ```SERVICE_CATEGORY```, etc.)
- Drops rows with invalid dates
- Handles missing values with warnings

## 2. Category Mapping

**Objective** 
Map technical service categories to business-friendly product names.

### Steps
- **Define Product Mapping**
```python
category_map = {
    'KAI': 'Broadband',
    'NET': 'Broadband',
    'KAV': 'Voice',
    'KAD': 'TV',
    'GIGA': 'GIGA',
    'VOD': 'VOD',
    'HDW': 'Hardware'
}
```
- **Apply Mapping**
```python
df['PRODUCT'] = df['SERVICE_CATEGORY'].map(category_map)
```
- Handle Unknowns
```python
df['PRODUCT'] = df['PRODUCT'].fillna('Unknown')
```
- **Output**
Generates a DataFrame with new `PRODUCT` column. Preserves original `SERVICE_CATEGORY` for debugging

## 3. Summary Generation
**Objective:** Create AI-powered narrative summaries for each product category.

### Steps
- **Timeline Segmentation**: 
Splits tickets into 5 story sections using `TimelineAnalyzer`:
```python
def create_timeline_sections(df):
    if len(df) <= 10: 
        return _adaptive_split(df)  # Small dataset
    elif date_range <= 7 days:
        return _count_based_split(df)  # By ticket count
    else:
        return _time_based_split(df)  # By date ranges
```
- **Prompt Engineering:** Generates LLM prompts for each section:

```python 
Prompt: """
Analyze {product} tickets ({section_name} - {timeframe}).
Tickets: {ticket_numbers}

Focus on:
1. Problem patterns (e.g., "30% were WiFi issues")
2. Resolution effectiveness ("Most resolved within 2h")
3. Customer experience trends

Write 3-5 bullet points in business English.
"""
```
- **AI Summarization** Uses Ollama LLM via `AIService`
```python 
def generate_summary(prompt: str) -> str:
    llm = ChatOllama(model="gemma2:2b-instruct-q5_0")
    return llm.invoke(prompt).content
```
- **Output Formatting:** Structures results as:
```python
## Broadband Summary
### Initial Issues (Nov 1-3)
• 3 tickets (001-xxx, 002-xxx)
• Primary issue: WiFi connectivity (66% of tickets)
• Avg resolution time: 1.2 hours
```
## Key Technical Decisions
1. **Error Handling:**
Skips corrupt rows but logs warnings
</br>Shows user-friendly error messages in UI
2. **Performance:** Caches LLM responses for identical inputs</br>
Processes data in memory (no disk I/O after upload)
3. **Extensibility:** New categories can be added via category_map</br>Prompt templates are modular

