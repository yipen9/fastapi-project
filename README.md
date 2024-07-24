翻译来自：[https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md](https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md)<br />这是我在创业公司中使用的最佳实践和惯例的观点列表。在过去的几年生产中，我们做出了好坏参半的决策，这些决策对我们的开发人员体验产生了巨大的影响。其中一些值得分享。
<a name="PXcoJ"></a>

# 项目结构

- 有许多方法来构建项目结构，但最好的结构是一致的、直接的且没有意外的。
- 许多示例项目和教程按文件类型划分项目（例如，crud、routers、models），这对于微服务或范围较少的项目很有效。然而，这种方法不适合我们具有许多域和模块的单体应用。
- 我发现对于这些情况，受 Netflix 的 Dispatch 启发的结构更具可扩展性和可演进性，并进行了一些小的修改。

```
fastapi-project
├── alembic/
├── src
│   ├── auth
│   │   ├── router.py
│   │   ├── schemas.py  # pydantic models
│   │   ├── models.py  # db models
│   │   ├── dependencies.py
│   │   ├── config.py  # local configs
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── aws
│   │   ├── client.py  # client model for external service communication
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   └── posts
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── config.py  # global configs
│   ├── models.py  # global models
│   ├── exceptions.py  # global exceptions
│   ├── pagination.py  # global module e.g. pagination
│   ├── database.py  # db connection related stuff
│   └── main.py
├── tests/
│   ├── auth
│   ├── aws
│   └── posts
├── templates/
│   └── index.html
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
├── logging.ini
└── alembic.ini
```

- 将所有域目录存储在`src`文件夹内
- `src/` - 应用的最高级别，包含常见模型、配置和常量等。
- `src/main.py` - 项目的根，初始化 FastAPI 应用。
- 每个包都有自己的路由器、模式、模型等。
  - `router.py` - 是每个模块的核心，包含所有端点。
  - `schemas.py` - 用于 Pydantic 模型。
  - `models.py` - 用于数据库模型。
  - `service.py` - 模块特定的业务逻辑。
  - `dependencies.py` - 路由器依赖。
  - `constants.py` - 模块特定的常量和错误代码。
  - `config.py` - 例如环境变量。
  - `utils.py` - 非业务逻辑函数，例如响应规范化、数据丰富等。
  - `exceptions.py` - 模块特定的异常，例如`PostNotFound`、`InvalidUserData`。
- 当包需要来自其他包的服务、依赖或常量时 - 使用显式模块名称导入它们。

```python
from src.auth import constants as auth_constants
from src.notifications import service as notification_service
from src.posts.constants import ErrorCode as PostsErrorCode  # in case we have Standard ErrorCode in constants module of each package
```

<a name="JlXnj"></a>

# 异步路由

- FastAPI 首先是一个异步框架。它旨在与异步 I/O 操作一起工作，这就是它如此快速的原因。
- 然而，FastAPI 并不限制您仅使用异步路由，开发人员也可以使用同步路由。这可能会使初学者开发人员认为它们是相同的，但它们不是。
  <a name="kGao4"></a>

## I/O 密集型任务

- 在幕后，FastAPI 可以有效地处理异步和同步 I/O 操作。
- FastAPI 在线程池中运行同步路由，阻塞 I/O 操作不会阻止事件循环执行任务。
- 如果路由被定义为异步，则通过`await`定期调用它，并且 FastAPI 相信您只执行非阻塞 I/O 操作。
- 注意，如果您辜负了这种信任并在异步路由中执行阻塞操作，事件循环将无法运行下一个任务，直到该阻塞操作完成。

```python
import asyncio
import time

from fastapi import APIRouter


router = APIRouter()


@router.get("/terrible-ping")
async def terrible_ping():
    time.sleep(10) # I/O blocking operation for 10 seconds, the whole process will be blocked

    return {"pong": True}

@router.get("/good-ping")
def good_ping():
    time.sleep(10) # I/O blocking operation for 10 seconds, but in a separate thread for the whole `good_ping` route

    return {"pong": True}

@router.get("/perfect-ping")
async def perfect_ping():
    await asyncio.sleep(10) # non-blocking I/O operation

    return {"pong": True}

```

当我们调用时会发生什么：

- `GET /terrible-ping`
  - FastAPI 服务器接收请求并开始处理它。
  - 服务器的事件循环和队列中的所有任务将等待，直到`time.sleep()`完成。
  - 服务器认为`time.sleep()`不是 I/O 任务，因此它会等待直到完成。
  - 服务器在等待时不会接受任何新请求。
  - 服务器返回响应。
  - 响应后，服务器开始接受新请求。
- `GET /good-ping`
  - FastAPI 服务器接收请求并开始处理它。
  - FastAPI 将整个路由`good_ping`发送到线程池，其中一个工作线程将运行该函数。
  - 当`good_ping`正在执行时，事件循环从队列中选择下一个任务并处理它们（例如，接受新请求，调用数据库）。
  - 独立于主线程（即我们的 FastAPI 应用），工作线程将等待`time.sleep`完成。
  - 同步操作仅阻塞侧线程，而不是主线程。
  - 当`good_ping`完成其工作时，服务器向客户端返回响应。
- `GET /perfect-ping`
  - FastAPI 服务器接收请求并开始处理它。
  - FastAPI 等待`asyncio.sleep(10)`。
  - 事件循环从队列中选择下一个任务并处理它们（例如，接受新请求，调用数据库）。
  - 当`asyncio.sleep(10)`完成时，服务器完成路由的执行并向客户端返回响应。

<a name="Nypbj"></a>

## 警告

- 关于线程池的注意事项：
  - 线程比协程需要更多的资源，因此它们不像异步 I/O 操作那样便宜。
  - 线程池的线程数量有限，即您可能会用完线程，并且您的应用将变得缓慢。阅读更多（外部链接）

<a name="sQ4up"></a>

## **CPU 密集型任务**

第二个注意事项是，非阻塞 awaitables 或发送到线程池的操作必须是 I/O 密集型任务（例如，打开文件、数据库调用、外部 API 调用）。

- 等待 CPU 密集型任务（例如，繁重的计算、数据处理、视频转码）是无价值的，因为 CPU 必须工作以完成任务，而 I/O 操作是外部的，服务器在等待这些操作完成时什么也不做，因此它可以转到下一个任务。
- 在其他线程中运行 CPU 密集型任务也不是有效的，因为 GIL。简而言之，GIL 只允许一个线程同时工作，这使得它对于 CPU 任务无用。
- 如果您想优化 CPU 密集型任务，您应该将它们发送到另一个进程中的工作者。

<a name="Y9xlD"></a>

# Pydantic

<a name="ocRUU"></a>

## 重度使用 Pydantic

- Pydantic 具有丰富的功能来验证和转换数据。
- 除了常规功能，如具有默认值的必填和非必填字段，Pydantic 还具有内置的综合数据处理工具，如正则表达式、枚举、字符串操作、电子邮件验证等。

```python
from enum import Enum
from pydantic import AnyUrl, BaseModel, EmailStr, Field


class MusicBand(str, Enum):
   AEROSMITH = "AEROSMITH"
   QUEEN = "QUEEN"
   ACDC = "AC/DC"


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=128)
    username: str = Field(min_length=1, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    email: EmailStr
    age: int = Field(ge=18, default=None)  # must be greater or equal to 18
    favorite_band: MusicBand | None = None  # only "AEROSMITH", "QUEEN", "AC/DC" values are allowed to be inputted
    website: AnyUrl | None = None
```

<a name="WC6jq"></a>

## 自定义基础模型

拥有一个可控制的全局基础模型允许我们自定义应用内的所有模型。例如，我们可以强制执行标准的日期时间格式或为基础模型的所有子类引入一个通用方法。

```python
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict


def datetime_to_gmt_str(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)
```

在上面的示例中，我们决定创建一个全局基础模型，该模型：

- 将所有日期时间字段序列化为具有明确时区的标准格式。
- 提供一种方法来返回仅包含可序列化字段的字典。
  <a name="gdWv5"></a>

## **解耦 Pydantic BaseSettings**

BaseSettings 对于读取环境变量是一项伟大的创新，但随着时间的推移，为整个应用程序使用单个 BaseSettings 可能会变得混乱。为了提高可维护性和组织性，我们将 BaseSettings 拆分为不同的模块和域。

```python
# src.auth.config
from datetime import timedelta

from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes

    REFRESH_TOKEN_KEY: str
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=30)

    SECURE_COOKIES: bool = True


auth_settings = AuthConfig()


# src.config
from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn

    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1.0"


settings = Config()

```

<a name="FsDqH"></a>

# Dependencies 依赖项

- **超越依赖注入**
  - Pydantic 是一个很好的模式验证器，但对于涉及调用数据库或外部服务的复杂验证，它是不够的。
  - FastAPI 文档主要将依赖项呈现为端点的 DI，但它们对于请求验证也非常出色。
  - 依赖项可用于根据数据库约束验证数据（例如，检查电子邮件是否已存在，确保找到用户等）。

```python
# dependencies.py
async def valid_post_id(post_id: UUID4) -> dict[str, Any]:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()

    return post


# router.py
@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_by_id(post: dict[str, Any] = Depends(valid_post_id)):
    return post


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    update_data: PostUpdate,
    post: dict[str, Any] = Depends(valid_post_id),
):
    updated_post = await service.update(id=post["id"], data=update_data)
    return updated_post


@router.get("/posts/{post_id}/reviews", response_model=list[ReviewsResponse])
async def get_post_reviews(post: dict[str, Any] = Depends(valid_post_id)):
    post_reviews = await reviews_service.get_by_post_id(post["id"])
    return post_reviews
```

如果我们没有将数据验证放入依赖项中，我们将不得不为每个端点验证`post_id`是否存在，并为每个端点编写相同的测试。

<a name="kX4s2"></a>

## **链式依赖**

依赖项可以使用其他依赖项并避免类似逻辑的代码重复

```python
# dependencies.py
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

async def valid_post_id(post_id: UUID4) -> dict[str, Any]:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()

    return post


async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, "JWT_SECRET", algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["id"]}


async def valid_owned_post(
    post: dict[str, Any] = Depends(valid_post_id),
    token_data: ddict[str, Any] = Depends(parse_jwt_data),
) -> dict[str, Any]:
    if post["creator_id"] != token_data["user_id"]:
        raise UserNotOwner()

    return post

# router.py
@router.get("/users/{user_id}/posts/{post_id}", response_model=PostResponse)
async def get_user_post(post: dict[str, Any] = Depends(valid_owned_post)):
    return post

```

<a name="KGEaE"></a>

## 解耦和重用依赖。依赖项调用被缓存

- 依赖项可以多次重用，并且它们不会被重新计算 - 默认情况下，FastAPI 在请求的范围内缓存依赖项的结果，即如果`valid_post_id`在一个路由中多次调用，它将仅被调用一次。
- 知道这一点，我们可以将依赖项解耦为多个较小的函数，这些函数在较小的域上操作，并且更容易在其他路由中重用。例如，在下面的代码中，我们使用`parse_jwt_data`三次：
  1.  `valid_owned_post`
  2.  `valid_active_creator`
  3.  `get_user_post`,

但`parse_jwt_data`仅在第一次调用时被调用一次。

```python
# dependencies.py
from fastapi import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

async def valid_post_id(post_id: UUID4) -> Mapping:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()

    return post


async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
) -> dict:
    try:
        payload = jwt.decode(token, "JWT_SECRET", algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()

    return {"user_id": payload["id"]}


async def valid_owned_post(
    post: Mapping = Depends(valid_post_id),
    token_data: dict = Depends(parse_jwt_data),
) -> Mapping:
    if post["creator_id"] != token_data["user_id"]:
        raise UserNotOwner()

    return post


async def valid_active_creator(
    token_data: dict = Depends(parse_jwt_data),
):
    user = await users_service.get_by_id(token_data["user_id"])
    if not user["is_active"]:
        raise UserIsBanned()

    if not user["is_creator"]:
       raise UserNotCreator()

    return user


# router.py
@router.get("/users/{user_id}/posts/{post_id}", response_model=PostResponse)
async def get_user_post(
    worker: BackgroundTasks,
    post: Mapping = Depends(valid_owned_post),
    user: Mapping = Depends(valid_active_creator),
):
    """Get post that belong the active user."""
    worker.add_task(notifications_service.send_email, user["id"])
    return post

```

<a name="FOl4m"></a>

## **优先使用异步依赖**

FastAPI 支持同步和异步依赖，并且存在一种诱惑，即在不需要等待任何事情时使用同步依赖，但这可能不是最佳选择。<br />正如与路由一样，同步依赖在线程池中运行。并且这里的线程也带有成本和限制，如果您只是进行一个小的非 I/O 操作，这些是多余的。<br />[GitHub - Kludex/fastapi-tips: FastAPI Tips by The FastAPI Expert!](https://github.com/Kludex/fastapi-tips?tab=readme-ov-file#9-your-dependencies-may-be-running-on-threads)

<a name="On9Ap"></a>

# Miscellaneous 杂项

<a name="iRNzF"></a>

## 遵循 REST

开发 RESTful API 可以更轻松地在如下路由中重用依赖项：

- `GET /courses/:course_id`
- `GET /courses/:course_id/chapters/:chapter_id/lessons`
- `GET /chapters/:chapter_id`

唯一的注意事项是在路径中使用相同的变量名称：

- 如果您有两个端点`GET /profiles/:profile_id`和`GET /creators/:creator_id`，它们都验证给定的`profile_id`是否存在，但`GET /creators/:creator_id`还检查该配置文件是否为创建者，那么最好将`creator_id`路径变量重命名为`profile_id`并链接这两个依赖项。

```python
# src.profiles.dependencies
async def valid_profile_id(profile_id: UUID4) -> Mapping:
    profile = await service.get_by_id(profile_id)
    if not profile:
        raise ProfileNotFound()

    return profile

# src.creators.dependencies
async def valid_creator_id(profile: Mapping = Depends(valid_profile_id)) -> Mapping:
    if not profile["is_creator"]:
       raise ProfileNotCreator()

    return profile

# src.profiles.router.py
@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
async def get_user_profile_by_id(profile: Mapping = Depends(valid_profile_id)):
    """Get profile by id."""
    return profile

# src.creators.router.py
@router.get("/creators/{profile_id}", response_model=ProfileResponse)
async def get_user_profile_by_id(
     creator_profile: Mapping = Depends(valid_creator_id)
):
    """Get creator's profile by id."""
    return creator_profile

```

<a name="VYJBz"></a>

## FastAPI 响应序列化

如果您认为可以返回与您的路由的`response_model`匹配的 Pydantic 对象来进行一些优化，那么这是错误的。<br />FastAPI 首先使用其`jsonable_encoder`将该 Pydantic 对象转换为字典，然后使用您的`response_model`验证数据，最后才将您的对象序列化为 JSON。

```python
from fastapi import FastAPI
from pydantic import BaseModel, root_validator

app = FastAPI()


class ProfileResponse(BaseModel):
    @model_validator(mode="after")
    def debug_usage(self):
        print("created pydantic model")

        return self


@app.get("/", response_model=ProfileResponse)
async def root():
    return ProfileResponse()
```

日志输出：

```python
[INFO] [2022-08-28 12:00:00.000000] created pydantic model
[INFO] [2022-08-28 12:00:00.000020] created pydantic model
```
