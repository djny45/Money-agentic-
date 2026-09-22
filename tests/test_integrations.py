from app.integrations.cpagrip import CPAGripClient

def test_cpagrip_json_feed_parser():
    body = '{"offers":[{"id":"42","name":"Example","link":"https://example.test","payout":"0.17","country":"IN"}]}'
    rows = CPAGripClient.parse_feed(body, "application/json")
    assert rows[0]["id"] == "42"
    assert rows[0]["payout"] == 0.17
    assert rows[0]["country"] == "IN"

def test_cpagrip_csv_feed_parser():
    body = "offer_id,title,url,payout,country\n7,Example,https://example.test,1.25,US\n"
    rows = CPAGripClient.parse_feed(body, "text/csv")
    assert rows[0]["id"] == "7"
    assert rows[0]["payout"] == 1.25

def test_cpagrip_empty_feed():
    assert CPAGripClient.parse_feed("", "application/json") == []
