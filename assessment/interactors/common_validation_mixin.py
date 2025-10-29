from assessment.exceptions.custom_exceptions import DuplicateQuestionTextFound, UnexpectedQuestionTypeFound, \
    UnexpectedDifficultyFound, DuplicateQuestionIdsFound, QuestionNotFound
from assessment.interactors.dtos import CreateQuestionDTO, QuestionType, Difficulty
from assessment.interactors.storage_interface.question_storage_interface import QuestionStorageInterface


class ValidationMixIns:

    @staticmethod
    def check_duplicate_question_texts(questions: list[CreateQuestionDTO]):
        question_texts=[]
        for q in questions:
            if q.question_text:
                question_texts.append(q.question_text.strip())
        seen=set()
        duplicates=[]
        for text in question_texts:
            if text in seen and text not in duplicates:
                duplicates.append(text)
            else:
                seen.add(text)
        if duplicates:
            raise DuplicateQuestionTextFound(question_texts=duplicates)


    @staticmethod
    def check_invalid_question_type(questions: list[CreateQuestionDTO]):
        valid_types = [qt.value for qt in QuestionType]
        invalid_types = [
            q.question_type.value
            for q in questions
            if q.question_type.value not in valid_types
        ]
        if invalid_types:
            raise UnexpectedQuestionTypeFound(question_types=invalid_types)


    @staticmethod
    def check_invalid_difficulty(questions: list[CreateQuestionDTO]):
        valid_difficulties = [d.value for d in Difficulty]
        invalid_difficulties = [
            q.difficulty.value
            for q in questions
            if q.difficulty.value not in valid_difficulties
        ]
        if invalid_difficulties:
            raise UnexpectedDifficultyFound(difficulties=invalid_difficulties)

    @staticmethod
    def check_duplicate_question_ids(question_ids:list[str]):
        seen=set()
        duplicates=[]
        for q in question_ids:
            if q in seen and q not in duplicates:
                duplicates.append(q)
            else:
                seen.add(q)
        if duplicates:
            raise DuplicateQuestionIdsFound(question_ids=duplicates)

    @staticmethod
    def check_if_question_ids_exists_in_db(question_ids:list[str],question_storage: QuestionStorageInterface):
        existing_questions=question_storage.get_questions(question_ids)
        existing_ids={q.question_id for q in existing_questions}
        missing_ids=[qid for qid in question_ids if qid not in existing_ids]
        if missing_ids:
            raise QuestionNotFound(question_ids=missing_ids)



