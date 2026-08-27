import factory
from faker import Faker

fake = Faker()

#--- Helper functions ---

def prerequisites_for(node_id: str) -> list[str]:
    number = int(node_id.split("_")[1])

    return [
        f"node_{i}"
        for i in range(max(0, number - 3), number)
    ]

#--- Base Factories ---

class ReasoningDataFactory(factory.DictFactory):
    status = "complete"
    worksheet_path = "reasoning/worksheets/test.md"

class KnowledgeDataFactory(factory.DictFactory):
    type = "adr"
    path = "knowledge/adrs/test.md"

class QuestionYamlFactory(factory.DictFactory):
    id = factory.Sequence(lambda n: f"node_{n}")

    question = "Test question"
    summary = "Test summary"

    reasoning = factory.LazyAttribute(
        lambda o: ReasoningDataFactory(
            worksheet_path=f"reasoning/worksheets/{o.id}.md"
        )
    )

    knowledge = factory.LazyAttribute(
        lambda o: KnowledgeDataFactory(
            path=f"knowledge/adrs/{o.id}.md"
        )
    )

    prerequisites = factory.LazyAttribute(
        lambda o: prerequisites_for(o.id)
    )

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        question_id = values.pop("id")

        return {
            question_id: values
        }

class QuestionDataFactory(factory.DictFactory):
    question = "Test question"
    summary = "Test summary"

    reasoning = factory.LazyFunction(
        lambda: ReasoningDataFactory(
        worksheet_path=f"reasoning/worksheets/question_id.md"
        )
    )

    knowledge = factory.LazyFunction(
        lambda: KnowledgeDataFactory(
            path=f"knowledge/adrs/question_id.md"
            )
    )

    prerequisites = factory.LazyFunction(
    lambda: ["node_1", "node_2"]
    )

#--- QuestionYaml derivatives ---

class QuestionYamlWithoutKnowledgeFactory(QuestionYamlFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        question_id = next(iter(values))
        values[question_id].pop("knowledge", None)

        return values

class QuestionYamlWithoutWorksheetPathFactory(QuestionYamlFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        question_id = next(iter(values))
        values[question_id]["reasoning"].pop("worksheet_path", None)

        return values

#--- QuestionData derivatives ---

class QuestionDataWithoutReasoningFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        values.pop("reasoning", None)

        return values

class QuestionDataWithoutReasoningStatusFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        values["reasoning"].pop("status", None)

        return values

class QuestionDataWithoutWorksheetPathFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        values["reasoning"].pop("worksheet_path", None)

        return values

class QuestionDataWithoutKnowledgeFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        values.pop("knowledge", None)

        return values

class QuestionDataWithoutKnowledgePathFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        values["knowledge"].pop("path", None)

        return values

class QuestionDataWithoutKnowledgeTypeFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        values["knowledge"].pop("type", None)

        return values
    
class QuestionDataWithoutQuestionFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        values.pop("question", None)

        return values

class QuestionDataWithoutSummaryFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        values.pop("summary", None)

        return values