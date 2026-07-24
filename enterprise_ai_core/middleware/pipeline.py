from typing import Callable, Any, List
from enterprise_ai_core.common.context import ExecutionContext
from enterprise_ai_core.common.result import Result

class IMiddleware:
    async def process(self, context: ExecutionContext, next_call: Callable[[], Any]) -> Result[Any]:
        return await next_call()

class AuthMiddleware(IMiddleware):
    async def process(self, context: ExecutionContext, next_call: Callable[[], Any]) -> Result[Any]:
        req_ctx = context.request_context
        if not req_ctx.tenant_id:
            return Result.fail("Unauthorized: Missing Tenant ID.")
        return await next_call()

class MiddlewarePipeline:
    def __init__(self):
        self._middlewares: List[IMiddleware] = []

    def use(self, middleware: IMiddleware) -> 'MiddlewarePipeline':
        self._middlewares.append(middleware)
        return self

    async def execute(self, context: ExecutionContext, target_action: Callable[[], Any]) -> Result[Any]:
        idx = 0

        async def next_step() -> Result[Any]:
            nonlocal idx
            if idx < len(self._middlewares):
                mw = self._middlewares[idx]
                idx += 1
                return await mw.process(context, next_step)
            else:
                return await target_action()

        return await next_step()
