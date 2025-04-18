To run:
1. Install packages in requirements.txt
2. Run `python3 cork_takehome.py`

The API will be served at localhost:5000. I tested post requests using Postman. Here's a sample request body:
```
{
    "tenant_id": "1",
    "user_id": "2",
    "origin": "Portland, Oregon, United States",
    "status": "fail",
    "date": "2025-04-18 15:00:00",
    "i_key": "bdc54cf7-37e3-4015-adf5-a34f905f082f"
}
```
