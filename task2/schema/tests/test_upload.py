from pathlib import Path

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

TEST_PDF_1 = Path(
    "storage/uploads/test_1.pdf"
)

TEST_PDF_2 = Path(
    "storage/uploads/test_2.pdf"
)

TEST_PDF_3 = Path(
    "storage/uploads/test_3.pdf"
)

TEST_PNG = Path(
    "storage/uploads/test_1.png"
)

TEST_BLANK_PNG = Path(
    "storage/uploads/test_blank.png"
)

TEST_JPEG = Path(
    "storage/uploads/test_jpg.jpeg"
)

def test_single_pdf_upload():

    with open(TEST_PDF_1, "rb") as pdf:

        response = client.post(
            "/upload",
            files={
                "files": (
                    TEST_PDF_1.name,
                    pdf,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


def test_multiple_valid_uploads():

    with (
        open(TEST_PDF_1, "rb") as pdf1,
        open(TEST_PDF_2, "rb") as pdf2
    ):

        response = client.post(
            "/upload",
            files=[
                (
                    "files",
                    (
                        TEST_PDF_1.name,
                        pdf1,
                        "application/pdf"
                    )
                ),
                (
                    "files",
                    (
                        TEST_PDF_2.name,
                        pdf2,
                        "application/pdf"
                    )
                )
            ]
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


def test_maximum_allowed_uploads():

    with (
        open(TEST_PDF_1, "rb") as pdf1,
        open(TEST_PDF_2, "rb") as pdf2,
        open(TEST_PDF_3, "rb") as pdf3
    ):

        response = client.post(
            "/upload",
            files=[
                (
                    "files",
                    (
                        TEST_PDF_1.name,
                        pdf1,
                        "application/pdf"
                    )
                ),
                (
                    "files",
                    (
                        TEST_PDF_2.name,
                        pdf2,
                        "application/pdf"
                    )
                ),
                (
                    "files",
                    (
                        TEST_PDF_3.name,
                        pdf3,
                        "application/pdf"
                    )
                )
            ]
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

def test_more_than_maximum_uploads():

    files = []

    for i in range(4):

        pdf = open(
            f"storage/uploads/test_{(i % 3) + 1}.pdf",
            "rb"
        )

        files.append(
            (
                "files",
                (
                    f"test_{i}.pdf",
                    pdf,
                    "application/pdf"
                )
            )
        )

    response = client.post(
        "/upload",
        files=files
    )

    for _, (_, pdf, _) in files:
        pdf.close()

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "error"

def test_unsupported_extension():

    invalid_file = Path(
        "storage/uploads/test_invalid.txt"
    )

    with open(invalid_file, "rb") as txt:

        response = client.post(
            "/upload",
            files={
                "files": (
                    invalid_file.name,
                    txt,
                    "text/plain"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "error"

def test_missing_file():

    response = client.post(
        "/upload"
    )

    assert response.status_code == 422

def test_empty_filename():

    response = client.post(
        "/upload",
        files={
            "files": (
                "",
                b"dummy content",
                "application/pdf"
            )
        }
    )

    assert response.status_code in [200, 422]

def test_png_upload():

    with open(TEST_PNG, "rb") as image:

        response = client.post(
            "/upload",
            files={
                "files": (
                    TEST_PNG.name,
                    image,
                    "image/png"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert data["files"][0]["text_file"] is not None

    assert data["files"][0]["characters"] >= 0


def test_jpeg_upload():

    with open(TEST_JPEG, "rb") as image:

        response = client.post(
            "/upload",
            files={
                "files": (
                    TEST_JPEG.name,
                    image,
                    "image/jpeg"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert data["files"][0]["text_file"] is not None

    assert data["files"][0]["characters"] >= 0


def test_blank_image_upload():

    with open(TEST_BLANK_PNG, "rb") as image:

        response = client.post(
            "/upload",
            files={
                "files": (
                    TEST_BLANK_PNG.name,
                    image,
                    "image/png"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert data["files"][0]["text_file"] is not None

    assert data["files"][0]["characters"] >= 0