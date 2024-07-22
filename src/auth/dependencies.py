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
