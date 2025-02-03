from typing import List
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama

def validate_user(user_id: int, addresses: List[str]) -> bool:
    """Validate user using historical addresses.

    Args:
        user_id (int): The user ID.
        addresses: Previous addresses.
    """
    return True

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
).bind_tools([validate_user])
result = llm.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX. "
)

print (result.tool_calls)