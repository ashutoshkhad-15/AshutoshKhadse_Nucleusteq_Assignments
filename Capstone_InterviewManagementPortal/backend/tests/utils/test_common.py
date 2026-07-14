from src.enums.app_enums import UserRole
from src.utils.common import build_pagination_meta, build_success_response, get_user_role, has_role, normalize_search_term


def test_common_helpers():
    assert normalize_search_term("  test ") == "test"
    assert normalize_search_term(None) == ""
    assert build_pagination_meta(2, 10, 15) == {"page": 2, "limit": 10, "total_items": 15, "total_pages": 2}

    response = build_success_response("ok", {"x": 1}, {"page": 1})
    assert response.message == "ok"
    assert response.data == {"x": 1}
    assert response.meta == {"page": 1}

    assert get_user_role({"role": "HR"}) == UserRole.HR
    assert get_user_role({"role": UserRole.ADMIN}) == UserRole.ADMIN
    assert get_user_role({"role": "unknown"}) is None
    assert has_role({"role": "ADMIN"}, [UserRole.ADMIN, UserRole.HR]) is True
    assert has_role({"role": "INTERVIEWER"}, [UserRole.ADMIN]) is False

