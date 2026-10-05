import pytest
from app.services.assessment_service import AssessmentService
from app.repositories.assessment_repository import AssessmentRepository
from app.database.connection import DatabaseConnection, init_db


@pytest.fixture
def test_db(tmp_path):
    test_db_path = str(tmp_path / "test_arch.db")
    init_db(test_db_path)
    db_conn = DatabaseConnection(test_db_path)
    return db_conn


def test_dependency_flow(test_db):
    """
    Validates architectural flow:
    Controller -> AssessmentService -> AssessmentFactory -> Assessment -> Repository -> Database
    """
    repo = AssessmentRepository(db_connection_factory=test_db.get_connection)
    service = AssessmentService(assessment_repo=repo)

    # Service calls Factory Method -> Creates Domain Entity -> Calculates Polymorphically -> Saves via Repository
    result = service.conduct_assessment(
        user_id=1,
        assessment_type="CRAFT",
        total_score=2,
        assessment_id=1
    )

    assert result.id is not None
    assert result.risk_level == "HIGH"

    # Verify data in repository
    conn = test_db.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assessment_results WHERE id = ?", (result.id,))
        row = cursor.fetchone()
        assert row is not None
        assert row["total_score"] == 2
        assert row["risk_level"] == "HIGH"
    finally:
        conn.close()
