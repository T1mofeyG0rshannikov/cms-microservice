class UserWithEmailAlreadyExists(Exception):
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


class UserProductAlreadyExists(Exception):
    pass


class LinkOrConnectedRequired(Exception):
    pass


class CantAddLike(Exception):
    pass


class LikeAlreadyExists(Exception):
    pass


class IdeaNotFound(Exception):
    pass


class SocialChannelAlreadyExists(Exception):
    pass


class InvalidJwtToken(Exception):
    pass


class UserNotAdmin(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class InvalidPassword(Exception):
    pass
