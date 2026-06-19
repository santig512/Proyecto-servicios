from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
from app.auth.deps import get_current_user
import uuid
from app.core.config import settings

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

router = APIRouter()
UPLOAD_DIR = Path(__file__).resolve().parents[2] / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _save_local(contents: bytes, filename: str) -> str:
    dest = UPLOAD_DIR / filename
    with dest.open('wb') as buffer:
        buffer.write(contents)
    return f"/uploads/{filename}"


async def _save_s3(contents: bytes, filename: str) -> str:
    import boto3
    s3 = boto3.client('s3')
    bucket = settings.S3_BUCKET
    s3.put_object(Bucket=bucket, Key=filename, Body=contents)
    return f"https://{bucket}.s3.amazonaws.com/{filename}"


@router.post('/upload')
async def upload_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        return {"detail": "File too large"}

    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4().hex}{ext}"

    if getattr(settings, 'S3_BUCKET', None):
        url = await _save_s3(contents, filename)
    else:
        url = _save_local(contents, filename)

    return {"file_url": url}
