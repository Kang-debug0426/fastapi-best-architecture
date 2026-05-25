from fastapi import APIRouter
#这里的prefix是路由前缀，tags是标签，可以在文档中看到，在那个文档中？
#答案：在 Swagger /docs 中，每个路由都有一个标签，点击标签可以筛选出这个标签下的所有路由
router = APIRouter(prefix="/items", tags=["items"])
#这里为什么不加app.
@router.get("/list")
def get_item_list():
      return {"items": ["apples", "oranges"]}