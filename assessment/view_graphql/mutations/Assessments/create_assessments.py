import graphene

from assessment.view_graphql.types.error_types import InvalidAssessmentTypesError, InvalidPassPercentageError
from assessment.view_graphql.types.input_types import CreateAssessmentsInput
from assessment.view_graphql.types.response_types import CreateAssessmentsResponse
from assessment.view_graphql.types.types import AssessmentType, AssessmentListType
from assessment.interactors.assessment_interactor.create_assessments import CreateAssessmentsInteractor
from assessment.storages.assessment_storage import AssessmentStorage
from assessment.exceptions.custom_exceptions import (
    InvalidAssessmentTypesFound,
    AssessmentInvalidPassPercentage,
)
from assessment.interactors.dtos import CreateAssessmentDTO, AssessmentTypeEnum


class CreateAssessments(graphene.Mutation):
    class Arguments:
        params = CreateAssessmentsInput(required=True)

    Output = CreateAssessmentsResponse

    @staticmethod
    def mutate(root, info, params):

        try:
            interactor = CreateAssessmentsInteractor(
                assessment_storage=AssessmentStorage()
            )

            dto_list = []
            for a in params.assessments:
                dto_list.append(
                    CreateAssessmentDTO(
                        assessment_title=a.assessmentTitle,
                        assessment_type=AssessmentTypeEnum(a.assessmentType),
                        description=a.description,
                        topic_id=a.topic_id,
                        icon=a.icon,
                        no_of_questions=a.noOfQuestions,
                        attempts_limit=a.attemptsLimit,
                        pass_percentage=a.passPercentage,
                        easy_count=a.easyCount,
                        medium_count=a.mediumCount,
                        hard_count=a.hardCount,
                        estimate_duration_in_mins=a.estimateDurationInMins,
                    )
                )

            created = interactor.create_assessments(dto_list)

            return AssessmentListType(
                assessments=[
                    AssessmentType(
                        assessmentId=obj.assessment_id,
                        assessmentTitle=obj.assessment_title,
                        assessmentType=obj.assessment_type.value,
                        topic_id=obj.topic_id,
                        description=obj.description,
                        passMarks=obj.pass_marks,
                        icon=obj.icon,
                        noOfQuestions=obj.no_of_questions,
                        marks=obj.marks,
                        passPercentage=obj.pass_percentage,
                        easyCount=obj.easy_count,
                        mediumCount=obj.medium_count,
                        hardCount=obj.hard_count,
                        attemptsLimit=obj.attempts_limit,
                        estimateDurationInMins=obj.estimate_duration_in_mins,
                    )
                    for obj in created
                ]
            )


        except InvalidAssessmentTypesFound as e:
            return InvalidAssessmentTypesError(assessmentTypes=e.assessment_types)

        except AssessmentInvalidPassPercentage as e:
            return InvalidPassPercentageError(percentages=e.percentages)
