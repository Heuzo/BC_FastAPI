from fastapi import Request, HTTPException

def lang_header_is_correct(header: str):
    import re
    pattern = r"(?i:(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?,)+(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?"
    if re.fullmatch(pattern, header):
        return True
    return False

def check_headers_correct(headers: Request.headers):
    if ('User-Agent' not in headers) and ('Accept-Language' not in headers):
        raise HTTPException(status_code=400, detail="Заголовки Aceept-Language и User-Agent не найдены")
    elif 'User-Agent' not in headers:
        raise HTTPException(status_code=400, detail="Заголовок User-Agent не найден")
    elif 'Accept-Language' not in headers:
        raise HTTPException(status_code=400, detail="Заголовок Aceept-Language не найден")
    else:
        if not lang_header_is_correct:
            raise HTTPException(status_code=400, detail="Заголовок Accept-Language имеет некорректный формат")
        else:
            return True