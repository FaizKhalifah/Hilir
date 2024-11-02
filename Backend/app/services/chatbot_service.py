class ChatbotService:
    @staticmethod
    def generate_chatbot_prompt(parent_message, mental_health_issues):
        issues_list = ", ".join([issue["name"] for issue in mental_health_issues])

        prompt = (
            f"The following conversation is to assist a parent whose child has the following mental health issues: {issues_list}. "
            "The child is 8 years old. Respond to the parent's question with empathy, providing practical advice or support related to the child’s specific needs.\n\n"
            f"Parent's Message: {parent_message}\n\n"
            "Chatbot Response:\n"
        )
        
        return prompt
