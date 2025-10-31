class DocumentNotReadyError(Exception):
    """Документ не готов к отправке: отсутствуют метаданные, шаблон или ревизии."""
    pass

class DocumentAlreadyArchivedError(Exception):
    """Попытка архивировать уже архивированный документ."""
    pass

class DocumentRestoreError(Exception):
    """Попытка восстановить документ, который не находится в архиве."""
    pass

class ReportReviewerNotAssignedError(Exception):
    """Попытка действия с рецензентом, который не назначен на отчёт."""
    pass

class ReportChartNotFoundError(Exception):
    """Попытка удалить диаграмму, которая не найдена в отчёте."""
    pass

class EmailFormatError(Exception):
    """Неверный формат электронной почты."""
    pass

class PhoneNumberFormatError(Exception):
    """Неверный формат номера телефона."""
    pass

class EmailFormatError(Exception):
    """Неверный формат электронной почты."""
    pass

class SecurityQuestionEmptyError(Exception):
    """Контрольный вопрос не может быть пустым."""
    pass

class MetadataTagConflictError(Exception):
    """Попытка добавить тег, который уже существует."""
    pass

class MetadataEncryptionError(Exception):
    """Ошибка при попытке включить шифрование без указания метода."""
    pass

class MetadataDecryptionError(Exception):
    """Ошибка при попытке расшифровать нешифрованные метаданные."""
    pass

class MetadataKeywordNotFoundError(Exception):
    """Попытка удалить ключевое слово, которого нет в метаданных."""
    pass

class ArchiveDocumentNotFoundError(Exception):
    """Документ не найден в архиве."""
    pass

class ArchiveAlreadyContainsDocumentError(Exception):
    """Попытка добавить документ, который уже находится в архиве."""
    pass