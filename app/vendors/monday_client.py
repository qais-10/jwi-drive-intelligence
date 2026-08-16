from __future__ import annotations

import json
from typing import Any, Optional

import httpx
from fastapi import HTTPException

from ..config import settings

MONDAY_API_URL = "https://api.monday.com/v2"
MONDAY_API_VERSION = "2024-10"


class MondayClient:
    def __init__(self, api_token: Optional[str] = None) -> None:
        token = api_token or settings.monday_api_token
        if not token:
            raise HTTPException(
                status_code=500,
                detail="MONDAY_API_TOKEN is not configured.",
            )

        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "API-Version": MONDAY_API_VERSION,
        }

    async def _execute(
        self,
        query: str,
        variables: dict[str, Any],
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                MONDAY_API_URL,
                headers=self.headers,
                json={"query": query, "variables": variables},
            )

        if response.is_error:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "monday.com API request failed.",
                    "response": response.text,
                },
            )

        payload = response.json()

        if "errors" in payload:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "monday.com GraphQL error.",
                    "errors": payload["errors"],
                },
            )

        return payload["data"]

    async def create_item(
        self,
        board_id: str,
        group_id: str,
        item_name: str,
        column_values: Optional[dict[str, Any]] = None,
    ) -> str:
        query = """
        mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON) {
          create_item(
            board_id: $boardId
            group_id: $groupId
            item_name: $itemName
            column_values: $columnValues
          ) {
            id
          }
        }
        """
        data = await self._execute(
            query,
            {
                "boardId": board_id,
                "groupId": group_id,
                "itemName": item_name,
                "columnValues": json.dumps(column_values or {}),
            },
        )
        return data["create_item"]["id"]

    async def move_item_to_group(self, item_id: str, group_id: str) -> None:
        query = """
        mutation ($itemId: ID!, $groupId: String!) {
          move_item_to_group(item_id: $itemId, group_id: $groupId) {
            id
          }
        }
        """
        await self._execute(
            query,
            {"itemId": item_id, "groupId": group_id},
        )

    async def change_column_values(
        self,
        board_id: str,
        item_id: str,
        column_values: dict[str, Any],
    ) -> None:
        query = """
        mutation ($boardId: ID!, $itemId: ID!, $columnValues: JSON!) {
          change_multiple_column_values(
            board_id: $boardId
            item_id: $itemId
            column_values: $columnValues
          ) {
            id
          }
        }
        """
        await self._execute(
            query,
            {
                "boardId": board_id,
                "itemId": item_id,
                "columnValues": json.dumps(column_values),
            },
        )

    async def get_item(self, item_id: str) -> Optional[dict[str, Any]]:
        query = """
        query ($itemId: [ID!]) {
          items(ids: $itemId) {
            id
            name
            group { id title }
            board { id }
            column_values { id text value }
          }
        }
        """
        data = await self._execute(query, {"itemId": [item_id]})
        items = data.get("items") or []
        return items[0] if items else None

    async def get_items_in_group(
        self,
        board_id: str,
        group_id: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        query = """
        query ($boardId: [ID!], $groupId: [String!], $limit: Int!) {
          boards(ids: $boardId) {
            groups(ids: $groupId) {
              items_page(limit: $limit) {
                items {
                  id
                  name
                  column_values { id text value }
                }
              }
            }
          }
        }
        """
        data = await self._execute(
            query,
            {"boardId": [board_id], "groupId": [group_id], "limit": limit},
        )
        boards = data.get("boards") or []
        if not boards or not boards[0].get("groups"):
            return []
        return boards[0]["groups"][0]["items_page"]["items"]

    async def create_board(self, board_name: str, board_kind: str = "public") -> str:
        query = """
        mutation ($boardName: String!, $boardKind: BoardKind!) {
          create_board(board_name: $boardName, board_kind: $boardKind) {
            id
          }
        }
        """
        data = await self._execute(
            query,
            {"boardName": board_name, "boardKind": board_kind},
        )
        return data["create_board"]["id"]

    async def create_group(self, board_id: str, group_name: str) -> str:
        query = """
        mutation ($boardId: ID!, $groupName: String!) {
          create_group(board_id: $boardId, group_name: $groupName) {
            id
          }
        }
        """
        data = await self._execute(
            query,
            {"boardId": board_id, "groupName": group_name},
        )
        return data["create_group"]["id"]

    async def create_column(
        self,
        board_id: str,
        title: str,
        column_type: str,
        defaults: Optional[dict[str, Any]] = None,
    ) -> str:
        query = """
        mutation ($boardId: ID!, $title: String!, $columnType: ColumnType!, $defaults: JSON) {
          create_column(
            board_id: $boardId
            title: $title
            column_type: $columnType
            defaults: $defaults
          ) {
            id
          }
        }
        """
        data = await self._execute(
            query,
            {
                "boardId": board_id,
                "title": title,
                "columnType": column_type,
                "defaults": json.dumps(defaults) if defaults else None,
            },
        )
        return data["create_column"]["id"]


def column_text(item: dict[str, Any], column_id: str) -> Optional[str]:
    if not column_id:
        return None
    for column in item.get("column_values", []):
        if column.get("id") == column_id:
            return column.get("text") or None
    return None
