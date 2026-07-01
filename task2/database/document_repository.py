from datetime import UTC, datetime

from bson import ObjectId

from database.connection import db

documents = db.documents

def create_document(data):

    result = documents.insert_one(
        data
    )

    return str(
        result.inserted_id
    )

def get_document(document_id):

    return documents.find_one(
        {
            "_id": ObjectId(document_id)
        }
    )

def get_old_documents(
    cutoff_date
):

    return list(
        documents.find(
            {
                "uploaded_at": {
                    "$lt": cutoff_date
                }
            }
        )
    )

def update_document(
    document_id,
    updates
):

    return documents.update_one(
        {
            "_id": ObjectId(document_id)
        },
        {
            "$set": updates
        }
    )

def delete_document(
    document_id
):

    return documents.delete_one(
        {
            "_id": ObjectId(document_id)
        }
    )

def get_expired_sessions(cutoff_time):
    return list(
        documents.find(
            {
                "last_accessed": {
                    "$lt": cutoff_time
                }
            }
        )
    )

def update_last_access(document_id):
    return documents.update_one(
        {
            "_id": ObjectId(document_id)
        },
        {
            "$set": {
                "last_accessed": datetime.now(UTC)
            }
        }
    )