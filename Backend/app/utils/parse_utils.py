import re

# app/utils/parse_utils.py

def parse_exercises(response_json):
    """
    Parse exercises from Gemini API response with improved robustness for different formats.
    """
    exercises_text = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    
    # Split into sections, handling both numbered and unnumbered formats
    sections = []
    
    # Try splitting by numbered format first (1., 2., 3.)
    numbered_sections = re.split(r'\d+\.\s+', exercises_text)
    if len(numbered_sections) > 1:
        sections = numbered_sections[1:]  # Skip the first empty split
    else:
        # Try splitting by "## " or "**Title**" if numbered format isn't found
        sections = [s for s in re.split(r'(?:##\s*|(?=\*\*Title\*\*))', exercises_text) if s.strip()]

    exercises = []
    
    for section in sections:
        exercise = {}
        
        # More flexible patterns to match different possible formats
        title_pattern = r'\*\*Title\*\*:?\s*([^\n]+)'
        description_pattern = r'\*\*Description\*\*:?\s*([^\n]+(?:\n(?!\*\*)[^\n]+)*)'
        id_pattern = r'\*\*Mental_health_issue_id\*\*:?\s*(\d+)'
        
        # Extract title
        title_match = re.search(title_pattern, section, re.IGNORECASE)
        if title_match:
            exercise["title"] = title_match.group(1).strip()
        
        # Extract description
        description_match = re.search(description_pattern, section, re.IGNORECASE)
        if description_match:
            exercise["description"] = description_match.group(1).strip()
        
        # Extract mental health issue ID
        id_match = re.search(id_pattern, section, re.IGNORECASE)
        if id_match:
            exercise["mental_health_issue_id"] = int(id_match.group(1))
        
        # Only add complete exercises
        if all(key in exercise for key in ["title", "description", "mental_health_issue_id"]):
            exercises.append(exercise)
    
    return exercises
