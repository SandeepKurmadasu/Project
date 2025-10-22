from abc import ABC, abstractmethod

from course_management.interactors.dtos import UserDTO,CreateUserDTO,UpdateUserDTO,CreateUserEnrollmentDTO

class UserStorageInterface(ABC):
    @abstractmethod
    def create_user(self):
        pass