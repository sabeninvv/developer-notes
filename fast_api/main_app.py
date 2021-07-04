from fastapi_maker import *


app = make_fastAPI_app()


@app.get("/")
async def read_root():
    """
    comments
    """
    html_content = """
        <html>
            <head>
                <title>Some HTML in here</title>
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
            </body>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get(
    "/queue/{task_id}",
    response_description="Check task in the queue",
    response_class=ORJSONResponse
)
async def check_task_in_queue(task_id: str):
    """
    comments
    """
    if len(task_id) == 36:
        try:
            from time import sleep
            sleep(1)
            return JSONResponse(content=jsonable_encoder(
                {task_id: "Ready"})
            )
        except Exception as exc:
            raise HTTPException(status_code=528, detail=str(exc),
                                headers={"description": "Error when server processing something"})
    else:
        return JSONResponse(content=jsonable_encoder({task_id: "Not ready"}))


@app.post(
    "/make-some-ml-work",
    response_description="Make some ML work",
    response_class=ORJSONResponse
)
async def make_some_ml_work(request: Request,
                            data_from_client: Dict[str, Union[int, float]] = Depends(common_query_params)):
    """
    comments
    """
    try:
        client_req = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=409, detail=str(exc),
                            headers={"description": "Server could not process the client request"})
    try:
        client_qparams = data_from_client
    except Exception as exc:
        raise HTTPException(status_code=409, detail=str(exc),
                            headers={"description": "Server could not process the client query_params"})
    try:
        return JSONResponse(content=jsonable_encoder({"taskId": str(uuid4())}))
    except Exception as exc:
        raise HTTPException(status_code=529, detail=str(exc),
                            headers={"description": "Error when server make some ML work"})


if __name__ == "__main__":
    uvicorn.run("main_app:app", host="0.0.0.0", timeout_keep_alive=600, workers=1, port=8000)
