class DomainError(Exception):
    """ドメイン層の基底例外。"""


class NotFoundError(DomainError):
    """リソースが見つからない。"""


class ValidationError(DomainError):
    """入力またはビジネスルール違反。"""


class InsufficientBalanceError(ValidationError):
    """残高不足。"""


class PriceUnavailableError(DomainError):
    """価格が取得できない。"""
