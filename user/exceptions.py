class UserWithEmailAlredyExists(Exception):
    pass


class UserWithPhoneAlreadyExists(Exception):
    pass


class SingleSuperSponsorExistError(Exception):
    pass


class InvalidReferalLevel(Exception):
    pass


class InvalidSortedByField(Exception):
    pass


class UserIsNotReferral(Exception):
    pass


class UserDoesNotExist(Exception):
    pass
