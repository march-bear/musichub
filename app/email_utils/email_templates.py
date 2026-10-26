import enum

from frozendict import frozendict


class EmailTemplate(enum.Enum):
    EMAIL_CONFIRMATION = frozendict(template="confirm", subject="Подтверждение адреса электронной почты")
