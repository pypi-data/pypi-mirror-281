# Libpresign

Single-purpose library created for generating AWS S3 presigned URLs fast.

Implemented in C++ using OpenSSL 3.1.

## Moto

Boto3 is heavy dependency if you just want to create a presigned URL. And it's famously slow.

## How to use

```python3
import libpresign

libpresign.get(
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "region-1",
    "bucket-name", 
    "object-key.txt",
    3600,  # Expiration time in seconds
)
```
Output
```text
'https://bucket.s3.amazonaws.com/object-key.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=creds1%2F20230711%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Date=20230711T125101Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=5c5a2e2858261266db950e4912fb12ffcd5d0bcf40d873bf9fe209ee789f6c86'
```

### Function signature
```python3
def get(
    access_key_id: str,
    secret_access_key: str,
    region: Optional[str],  # defaults to "us-east-1"
    bucket: str,
    key: str,
    expires: Optional[str], # defaults to 3600 (1h)
):
    ...
```

## Comparison to boto3

### Test case

Generate 10 000 presigned URLs. Compare execution times

### Results
```text
┌────────────────────────┬────────┬────────────┐
│ library                │ boto3  │ libpresign │
├────────────────────────┼────────┼────────────┤
│ avg execution time, μs │ 2232.3 │ 13.9       │ 
└────────────────────────┴────────┴────────────┘
```

Libpresign came out to be 160 times faster

## Dependencies

* GNU C Compiler 
* OpenSSL
