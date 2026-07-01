from datetime import datetime, timedelta, UTC

from config.settings import (
    SESSION_TIMEOUT_MINUTES
)

from database.document_repository import (
    get_expired_sessions
)

from schema.utils.document_cleanup import delete_document_resources

def cleanup_expired_sessions():
    cutoff = (
        datetime.now(UTC)
        - timedelta(
            minutes=SESSION_TIMEOUT_MINUTES
        )
    )

    expired_documents = (
        get_expired_sessions(
            cutoff
        )
    )

    deleted = 0

    for document in expired_documents:

        delete_document_resources(
            document
        )

        deleted += 1

    return deleted
