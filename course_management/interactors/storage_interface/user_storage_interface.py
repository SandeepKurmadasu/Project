from abc import ABC, abstractmethod

from course_management.interactors.dtos import UserDTO,CreateUserDTO,UpdateUserDTO,CreateUserEnrollmentDTO

class UserStorageInterface(ABC):

    @abstractmethod
    def create_user(self,user_details : CreateUserDTO)->UserDTO:
        pass

    @abstractmethod
    def check_user_exists(self, user_id):
        pass