from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class Request(BaseModel):
    """路线规划请求"""
    start_city: str = Field(..., description="起点城市")
    end_city: str = Field(..., description="终点城市")
    start_date: str = Field(..., description="开始日期 YYYY-MM-DD", example="2025-06-01")
    end_date: str = Field(..., description="结束日期 YYYY-MM-DD", example="2025-06-03")
    route_type: str = Field(default="walking", description="路线类型: walking/driving/transit")
    attraction_prefer: List[str] = Field(default="", description="用户景点偏好: 自然景观/公园/古建筑等")
    hotel_prefer: List[str] = Field(default="", description="用户酒店偏好: 豪华型/经济型等")