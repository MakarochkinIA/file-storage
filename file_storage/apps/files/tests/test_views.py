import io


def test_upload_and_download_round_trip(api_client):
    payload = b"hello world" * 1_000  # 11 kB – spans several chunks

    # ---- upload -------------------------------------------------------
    upload_resp = api_client.post(
        "/api/v1/files/upload/",
        data={"file": io.BytesIO(payload)},
    )
    assert upload_resp.status_code == 201
    uid = upload_resp.data["uid"]
    print(uid)

    # ---- download -----------------------------------------------------
    download_resp = api_client.get(f"/api/v1/files/download/{uid}/")
    assert download_resp.status_code == 200
    assert b''.join(download_resp.streaming_content) == payload
