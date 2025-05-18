from datetime import datetime, timedelta

def test_create_rental(client):
    # First create a user and vehicle
    user_res = client.post("/users/", json={"name": "Test user 2", "contact": "test@example.com"})
    vehicle_res = client.post("/vehicles/", json={
        "name": "Test Car", "type": "Sedan", "registration_number": "TEST04233"
    })

    assert user_res.status_code == 200
    assert vehicle_res.status_code == 200

    user_id = user_res.json()["id"]
    vehicle_id = vehicle_res.json()["id"]

    rental_data = {
        "user_id": user_id,
        "vehicle_id": vehicle_id,
        "expected_return": (datetime.now() + timedelta(days=2)).isoformat()
    }

    response = client.post("/rentals/", json=rental_data)
    print("Rental creation error:", response.json())

    assert response.status_code == 200
    assert response.json()["vehicle_id"] == vehicle_id
    assert response.json()["user_id"] == user_id

def test_list_rentals(client):
    response = client.get("/rentals/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_rental_by_id(client):
    rentals = client.get("/rentals/").json()
    if rentals:
        rental_id = rentals[0]["id"]
        response = client.get(f"/rentals/{rental_id}")
        assert response.status_code == 200
        assert response.json()["id"] == rental_id

def test_return_rental(client):
    rentals = client.get("/rentals/").json()
    if rentals:
        rental_id = rentals[0]["id"]
        response = client.post(f"/rentals/{rental_id}/return")
        assert response.status_code == 200
        assert response.json()["actual_return"] is not None

def test_delete_rental(client):
    # Create a new rental to delete
    user_res = client.post("/users/", json={"name": "To Delete", "contact": "del@example.com"})
    vehicle_res = client.post("/vehicles/", json={
        "name": "Delete Car", "type": "Hatchback", "registration_number": "DEL14423"
    })
    rental_res = client.post("/rentals/", json={
        "user_id": user_res.json()["id"],
        "vehicle_id": vehicle_res.json()["id"],
        "expected_return": (datetime.now() + timedelta(days=1)).isoformat()
    })
    rental_id = rental_res.json()["id"]
    
    response = client.delete(f"/rentals/{rental_id}")
    assert response.status_code == 204
