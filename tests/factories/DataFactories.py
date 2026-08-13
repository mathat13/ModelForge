import factory
from faker import Faker

fake = Faker()

class ReasoningDataFactory(factory.DictFactory):
    status = "complete"
    worksheet_path = "reasoning/worksheets/test.md"

class KnowledgeDataFactory(factory.DictFactory):
    type = "adr"
    path = "knowledge/adrs/test.md"

def prerequisites_for(node_id: str) -> list[str]:
    number = int(node_id.split("_")[1])

    return [
        f"node_{i}"
        for i in range(max(0, number - 3), number)
    ]

class QuestionDataFactory(factory.DictFactory):
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

class QuestionWithoutKnowledgeDataFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        question_id = next(iter(values))
        values[question_id].pop("knowledge", None)

        return values

class QuestionWithoutWorksheetPathDataFactory(QuestionDataFactory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        values = super()._build(model_class, *args, **kwargs)

        question_id = next(iter(values))
        values[question_id]["reasoning"].pop("worksheet_path", None)

        return values