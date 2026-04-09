import pytest
from hypothesis import given, strategies as st
from src.validators import validate_title, validate_email, validate_password, validate_deadline

# ==========================================
# 1. PARAMETERIZED TESTS (MELIPATGANDAKAN TEST CASE)
# ==========================================

# Menghasilkan 5 Test Case Valid Email
@pytest.mark.parametrize("valid_email", [
    "leo@kampus.com", 
    "LEO.A@kampus.co.id", 
    "123@numbers.org", 
    "a@b.c", 
    "mahasiswa_it@univ.edu"
])
def test_email_valid_cases(valid_email):
    assert validate_email(valid_email) == valid_email.lower()

# Menghasilkan 7 Test Case Invalid Email
@pytest.mark.parametrize("invalid_email", [
    "", "   ", None, "emailtanpa-at", "a@.com", "@domain.com", "ada spasi@mail.com"
])
def test_email_invalid_cases(invalid_email):
    with pytest.raises(ValueError):
        validate_email(invalid_email)

# Menghasilkan 4 Test Case Valid Password
@pytest.mark.parametrize("valid_pw", ["rahasia123", "P@ssw0rdPanjangBanget", "12345678", "        "])
def test_password_valid_cases(valid_pw):
    assert validate_password(valid_pw) == valid_pw

# Menghasilkan 5 Test Case Invalid Password
@pytest.mark.parametrize("invalid_pw", ["", None, "1234567", "pendek", " "])
def test_password_invalid_cases(invalid_pw):
    with pytest.raises(ValueError, match="minimal 8 karakter"):
        validate_password(invalid_pw)

# Menghasilkan 6 Test Case Invalid Title
@pytest.mark.parametrize("invalid_title", [
    "", "   ", None, 123, True, "a" * 201
])
def test_title_invalid_cases(invalid_title):
    with pytest.raises(ValueError):
        validate_title(invalid_title)

# Menghasilkan 5 Test Case Deadline
@pytest.mark.parametrize("deadline_input, expected_error", [
    ("31-12-2026", True),  # Format salah
    ("2026/12/31", True),  # Format salah
    ("Not a date", True),  # String ngawur
    ("2026-02-30", True),  # Tanggal tidak valid di kalender
    ("", False)            # Kosong boleh (None)
])
def test_deadline_edge_cases(deadline_input, expected_error):
    if expected_error:
        with pytest.raises(ValueError):
            validate_deadline(deadline_input)
    else:
        assert validate_deadline(deadline_input) is None

# ==========================================
# 2. PROPERTY-BASED TESTING (PBT) - HYPOTHESIS
# ==========================================

@given(st.text(alphabet=[" ", "\t", "\n"], min_size=1))
def test_pbt_whitespace_title_rejected(invalid_title):
    with pytest.raises(ValueError, match="tidak boleh kosong"):
        validate_title(invalid_title)

@given(st.text(min_size=201))
def test_pbt_long_title_rejected(long_title):
    with pytest.raises(ValueError, match="maksimal 200 karakter"):
        validate_title(long_title)