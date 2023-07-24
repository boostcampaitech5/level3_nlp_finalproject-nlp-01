from fastapi import status

def print_error(error_code):
    if error_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        return "[서버오류] 잠시 후 다시 실행해 주세요"
    elif error_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
        return "입력을 확인해 주세요!"
    else:
        return "ERROR_NUM: "+error_code