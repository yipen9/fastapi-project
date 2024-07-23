# router dependencies
# Pydantic 是一个很棒的模式验证器，但对于涉及调用数据库或外部服务的复杂验证来说，这还不够。
# FastAPI 文档主要将依赖项作为端点的 DI 呈现，但它们也非常适合请求验证。
# 依赖关系可用于根据数据库约束验证数据（例如，检查电子邮件是否已存在，确保找到用户等）。
# 例如：
# # dependencies.py
# async def valid_post_id(post_id: UUID4) -> dict[str, Any]:
#     post = await service.get_by_id(post_id)
#     if not post:
#         raise PostNotFound()

#     return post



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
# 实例化OAuth2PasswordBearer，用于OAuth 2.0密码流程的安全依赖项。
# 用于在路径操作函数中接收OAuth 2.0密码流程生成的访问令牌。
# 一个路径操作函数依赖于它，它则会去调用/token(tokenUrl参数的值)路径装饰的操作函数，取回token。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
                                     
                                     # 用于hash加密

# 用于密码哈希和验证。第一个参数schems表示采用的哈希方案。
# bcrypt 是一个专门为密码哈希设计的强力的哈希算法，sha256_crypt 和 sha512_crypt 是基于SHA-256和SHA-512的兼容性哈希算法，安全性可能不如bcrypt。第二个参数用来警告开发者可以在使用过时的哈希方案。
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 核验密码。plain_password是明文密码，hashed_password是哈希密码。
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 对密码进行hash加密，这里没有使用。password是明文密码。
def get_password_hash(password):
    return pwd_context.hash(password)