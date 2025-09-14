from api.utils.res.response_body import ResponseBody

responses_401 = {
    "description": "Token invalid",
    "model": ResponseBody[None]
}

responses_404_user = {
    "description": "User not found",
    "model": ResponseBody[None]
}
