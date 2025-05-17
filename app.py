import uvicorn

from src import app, environment

if __name__ == "__main__":
    config = uvicorn.Config(
        app=app,
        host=environment.env.HOST,
        port=int(environment.env.PORT),
        log_level="info",
        reload=environment.env.DEBUG,
    )

    server = uvicorn.Server(config)
    server.run()
