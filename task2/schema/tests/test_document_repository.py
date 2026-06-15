from database.document_repository import (
    create_document,
    get_document,
    update_document,
    delete_document
)

def test_create_and_get_document():

    document_id = create_document(
        {
            "filename": "test.pdf",
            "characters": 100
        }
    )

    document = get_document(
        document_id
    )

    assert document is not None

    assert (
        document["filename"]
        == "test.pdf"
    )

    delete_document(
        document_id
    )

def test_update_document():

    document_id = create_document(
        {
            "filename": "old.pdf"
        }
    )

    update_document(
        document_id,
        {
            "filename": "new.pdf"
        }
    )

    document = get_document(
        document_id
    )

    assert (
        document["filename"]
        == "new.pdf"
    )

    delete_document(
        document_id
    )

def test_delete_document():

    document_id = create_document(
        {
            "filename": "delete.pdf"
        }
    )

    delete_document(
        document_id
    )

    document = get_document(
        document_id
    )

    assert document is None