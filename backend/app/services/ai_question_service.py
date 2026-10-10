class AIQuestionService:

    def generate_question(
        self,
        topic: str,
        difficulty: str,
        question_number: int,
    ) -> str:

        if topic.lower() == "python":

            questions = [
                "Tell me about your experience with Python.",
                "What are the main differences between a list and a tuple in Python?",
                "Explain Python decorators and where they are used.",
                "What is the difference between deep copy and shallow copy in Python?",
                "How does exception handling work in Python?"
            ]

            return questions[
                question_number % len(questions)
            ]


        return f"Explain the basics of {topic}."