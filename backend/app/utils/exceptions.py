from fastapi import HTTPException , status

def raise_404(detail : str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

def raise_400(detail : str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

def raise_403(detail : str):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)