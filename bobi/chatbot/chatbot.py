from chatterbot.logic import LogicAdapter

class CreateBudgetLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        """
        words = ['category', 'details', 'amount']
        if all(x in statement.text.split() for x in words)
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        # cant figure out how to link to my postgres db responses

        confidence = 1

        response_statement = Statement(text='I have recorded your spending as requested. Please proceed to /budget to view your records.')

        return confidence, response_statement


class ReadBudgetLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        """
        words = ['how', 'much', 'spend']
        if all(x in statement.text.split() for x in words)
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        confidence = 1

        response_statement = Statement(text='Look in your console to see the results.')

        return confidence, response_statement


class DestroyBudgetLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        """
        words = ['destroy', 'entry', 'id']
        if all(x in statement.text.split() for x in words)
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        confidence = 1

        response_statement = Statement(text='I have destroyed your entry as requested. Please proceed to /budget to view your records.')

        return confidence, response_statement