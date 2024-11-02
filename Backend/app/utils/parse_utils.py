import re


def parse_exercises(response_json):
  
    exercises_text = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    
    sections = []
    
    numbered_sections = re.split(r'\d+\.\s+', exercises_text)
    if len(numbered_sections) > 1:
        sections = numbered_sections[1:]  
    else:
        sections = [s for s in re.split(r'(?:##\s*|(?=\*\*Title\*\*))', exercises_text) if s.strip()]

    exercises = []
    
    for section in sections:
        exercise = {}
        

        title_pattern = r'\*\*Title\*\*:?\s*([^\n]+)'
        description_pattern = r'\*\*Description\*\*:?\s*([^\n]+(?:\n(?!\*\*)[^\n]+)*)'
        id_pattern = r'\*\*Mental_health_issue_id\*\*:?\s*(\d+)'
        

        title_match = re.search(title_pattern, section, re.IGNORECASE)
        if title_match:
            exercise["title"] = title_match.group(1).strip()
        

        description_match = re.search(description_pattern, section, re.IGNORECASE)
        if description_match:
            exercise["description"] = description_match.group(1).strip()
        
        id_match = re.search(id_pattern, section, re.IGNORECASE)
        if id_match:
            exercise["mental_health_issue_id"] = int(id_match.group(1))
        
        if all(key in exercise for key in ["title", "description", "mental_health_issue_id"]):
            exercises.append(exercise)
    
    return exercises
