

def test_full_heart_pred(client):
    #create data to be used, 0 missing vals
    full_data = {
        "diseases": ["Heart"],
        "data": {"age": 22, "sex":1,"cp":0, "trestbps": 120,  "chol":180, "fbs":0,
                "restecg":0, "thalach":183, "exang":0, "oldpeak": 0, "slope":0, "ca":0, "thal":1}
    }

    response = client.post('prediction/feature', json=full_data)

    #Assert the response
    assert response.status_code == 200
    assert response.data

    # decode the JSON response to check its contents
    response_json = response.get_json()
    assert 'Heart' in response_json[0]
    val = response_json[0]['Heart']
    assert isinstance(val, float)


def test_missing_heart_pred(client):
    #create data to be used, 3 missing vals
    partial_data = {
        "diseases": ["Heart"],
        "data": {"age": 22, "sex":1,"cp":0, "trestbps": 120,  "chol":180, "fbs":0,
                "restecg":0, "thalach":183, "exang":0, "oldpeak": 0}
    }

    response = client.post('prediction/feature', json=partial_data)

    #Assert the response
    assert response.status_code == 200
    assert response.data

    # decode the JSON response to check its contents
    response_json = response.get_json()
    assert 'Heart' in response_json[0]
    val = response_json[0]['Heart']
    assert isinstance(val, float)


def test_half_heart_pred(client):
    #create data to be used, half missing vals
    half_data = {
        "diseases": ["Heart"],
        "data": {"age": 22, "sex":1,"cp":0, "trestbps": 120,  "chol":180, "fbs":0}
    }

    response = client.post('prediction/feature', json=half_data)

    #Assert the response
    assert response.status_code == 200
    assert response.data

    # decode the JSON response to check its contents
    response_json = response.get_json()
    assert 'Heart' in response_json[0]
    assert response_json[0]['Heart'] == 'Not enough features'


