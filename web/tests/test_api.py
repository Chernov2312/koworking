__all__ = ()
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth_and_get_free_rooms_flow(ac: AsyncClient):
    register_payload = {
        'username': 'ivanov_dev',
        'password1': 'SecretPass123',
        'password2': 'SecretPass123',
        'role': 'employee',
    }
    reg_response = await ac.post('/auth/register', json=register_payload)
    assert reg_response.status_code == 200
    assert reg_response.json()['username'] == 'ivanov_dev'

    login_data = {'username': 'ivanov_dev', 'password': 'SecretPass123'}
    login_response = await ac.post('/token', data=login_data)
    assert login_response.status_code == 200

    token_json = login_response.json()
    assert 'access_token' in token_json
    token = token_json['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    check_free_payload = {'date_for': '2026-06-29'}
    rooms_response = await ac.post(
        '/booking/free',
        json=check_free_payload,
        headers=headers,
    )
    assert rooms_response.status_code == 200

    rooms_data = rooms_response.json()
    assert len(rooms_data) > 0
    assert 'slots' in rooms_data[0]
    assert len(rooms_data[0]['slots']) > 0


@pytest.mark.asyncio
async def test_double_booking_protection(ac: AsyncClient):
    await ac.post(
        '/auth/register',
        json={
            'username': 'employee_1',
            'password1': 'SecurePass1',
            'password2': 'SecurePass1',
        },
    )
    login_res = await ac.post(
        '/token',
        data={'username': 'employee_1', 'password': 'SecurePass1'},
    )
    assert login_res.status_code == 200
    headers = {'Authorization': f'Bearer {login_res.json()["access_token"]}'}

    check_free_payload = {'date_for': '2026-06-29'}
    rooms_res = await ac.post(
        '/booking/free',
        json=check_free_payload,
        headers=headers,
    )
    assert rooms_res.status_code == 200

    real_slot_id = rooms_res.json()[0]['slots'][0]['id']

    booking_payload = {'booked_for': '2026-06-29', 'slot_id': real_slot_id}

    res1 = await ac.post(
        '/booking/create_booking',
        json=booking_payload,
        headers=headers,
    )
    assert res1.status_code == 200

    res2 = await ac.post(
        '/booking/create_booking',
        json=booking_payload,
        headers=headers,
    )
    assert res2.status_code == 400
    assert (
        res2.json()['detail'] == 'Этот'
        ' временной слот уже забронирован на указанную дату'
    )


@pytest.mark.asyncio
async def test_employee_cannot_delete_foreign_booking(ac: AsyncClient):
    await ac.post(
        '/auth/register',
        json={
            'username': 'user_a',
            'password1': 'SecurePass1',
            'password2': 'SecurePass1',
        },
    )
    login_a = await ac.post(
        '/token',
        data={'username': 'user_a', 'password': 'SecurePass1'},
    )
    assert login_a.status_code == 200
    headers_a = {'Authorization': f'Bearer {login_a.json()["access_token"]}'}

    check_free_payload = {'date_for': '2026-06-29'}
    rooms = await ac.post(
        '/booking/free',
        json=check_free_payload,
        headers=headers_a,
    )
    assert rooms.status_code == 200

    slot_id = rooms.json()[0]['slots'][0]['id']

    booking_res = await ac.post(
        '/booking/create_booking',
        json={'booked_for': '2026-06-29', 'slot_id': slot_id},
        headers=headers_a,
    )
    assert booking_res.status_code == 200
    booking_id = booking_res.json()['id']

    await ac.post(
        '/auth/register',
        json={
            'username': 'user_b',
            'password1': 'SecurePass1',
            'password2': 'SecurePass1',
        },
    )
    login_b = await ac.post(
        '/token',
        data={'username': 'user_b', 'password': 'SecurePass1'},
    )
    assert login_b.status_code == 200
    headers_b = {'Authorization': f'Bearer {login_b.json()["access_token"]}'}

    delete_payload = {'id': booking_id}
    delete_res = await ac.post(
        '/booking/delete_booking',
        json=delete_payload,
        headers=headers_b,
    )

    assert delete_res.status_code == 403
    assert (
        delete_res.json()['detail'] == 'У вас нет прав'
        ' чтобы удалять данную бронь'
    )
