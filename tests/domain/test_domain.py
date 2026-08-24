from blueprint_forge import (
    Question,
    Knowledge,
    Reasoning,
)

from tests.factories.DataFactories import (
    QuestionDataFactory,
    QuestionWithoutKnowledgeDataFactory,
    QuestionWithoutWorksheetPathDataFactory,
    ReasoningDataFactory,
)

def test_Question_from_dict_create_successful():
    # Setup
    data = QuestionDataFactory()
    question_id, question_data = next(iter(data.items()))

    # Execution
    question = Question.from_dict(
        id=question_id,
        data=question_data
        )

    # Verification
    assert question.id == question_id
    assert question.question == question_data["question"]
    assert question.summary == question_data["summary"]

    assert isinstance(question.reasoning, Reasoning)
    assert question.reasoning.status == question_data["reasoning"]["status"]
    assert question.reasoning.worksheet_path == question_data["reasoning"]["worksheet_path"]

    assert isinstance(question.knowledge, Knowledge)
    assert question.knowledge.type == question_data["knowledge"]["type"]
    assert question.knowledge.path == question_data["knowledge"]["path"]

    assert question.prerequisites == question_data["prerequisites"]

def test_question_from_dict_none_knowledge_section_generation():
    # Setup
    data = QuestionDataFactory(knowledge=None)
    question_id, question_data = next(iter(data.items()))

    # Execution
    question = Question.from_dict(
        id=question_id,
        data=question_data
        )

    # Verification
    assert question.id == question_id
    assert question.question == question_data["question"]
    assert question.summary == question_data["summary"]

    assert isinstance(question.reasoning, Reasoning)
    assert question.reasoning.status == question_data["reasoning"]["status"]
    assert question.reasoning.worksheet_path == question_data["reasoning"]["worksheet_path"]

    assert question.knowledge == None

    assert question.prerequisites == question_data["prerequisites"]

def test_question_from_dict_absent_knowledge_section_generation():
    # Setup
    data = QuestionWithoutKnowledgeDataFactory()
    question_id, question_data = next(iter(data.items()))

    # Execution
    question = Question.from_dict(
        id=question_id,
        data=question_data
        )

    # Verification
    assert question.id == question_id
    assert question.question == question_data["question"]
    assert question.summary == question_data["summary"]

    assert isinstance(question.reasoning, Reasoning)
    assert question.reasoning.status == question_data["reasoning"]["status"]
    assert question.reasoning.worksheet_path == question_data["reasoning"]["worksheet_path"]

    assert question.knowledge == None

    assert question.prerequisites == question_data["prerequisites"]

def test_question_from_dict_absent_worksheet_path_generation():
    # Setup
        data = QuestionWithoutWorksheetPathDataFactory()

        question_id, question_data = next(iter(data.items()))
    
        # Execution
        question = Question.from_dict(
            id=question_id,
            data=question_data
            )

        # Verification
        assert question.id == question_id
        assert question.question == question_data["question"]
        assert question.summary == question_data["summary"]
    
        assert isinstance(question.reasoning, Reasoning)
        assert question.reasoning.status == question_data["reasoning"]["status"]
        assert question.reasoning.worksheet_path == None
    
        assert isinstance(question.knowledge, Knowledge)
        assert question.knowledge.type == question_data["knowledge"]["type"]
        assert question.knowledge.path == question_data["knowledge"]["path"]
    
        assert question.prerequisites == question_data["prerequisites"]

def test_question_from_dict_none_worksheet_path_generation():
    # Setup
        data = QuestionDataFactory(
            reasoning=ReasoningDataFactory(
                worksheet_path=None
            )
        )

        question_id, question_data = next(iter(data.items()))
    
        # Execution
        question = Question.from_dict(
            id=question_id,
            data=question_data
            )

        # Verification
        assert question.id == question_id
        assert question.question == question_data["question"]
        assert question.summary == question_data["summary"]
    
        assert isinstance(question.reasoning, Reasoning)
        assert question.reasoning.status == question_data["reasoning"]["status"]
        assert question.reasoning.worksheet_path == None
    
        assert isinstance(question.knowledge, Knowledge)
        assert question.knowledge.type == question_data["knowledge"]["type"]
        assert question.knowledge.path == question_data["knowledge"]["path"]
    
        assert question.prerequisites == question_data["prerequisites"]