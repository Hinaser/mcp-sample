#!/usr/bin/env python3
"""
Advanced MCP Server Example

This demonstrates more advanced MCP features including:
- Async tools and resources
- Error handling
- Context usage
- Prompts
- Structured data handling
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from typing import Annotated

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Data models for structured responses
class Task(BaseModel):
    """A task in our task management system."""
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)


class TaskDatabase:
    """Simple in-memory task database."""
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1
    
    def create_task(self, title: str, description: str, tags: List[str]) -> Task:
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            tags=tags
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def list_tasks(self, tag: Optional[str] = None) -> List[Task]:
        tasks = list(self.tasks.values())
        if tag:
            tasks = [t for t in tasks if tag in t.tags]
        return tasks
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        task = self.tasks.get(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
        return task


# Global database instance
db = TaskDatabase()


# Lifespan context manager for initialization/cleanup
@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[dict]:
    """Initialize and cleanup resources."""
    logger.info("Starting Advanced MCP Server...")
    
    # Initialize with some sample data
    db.create_task(
        "Setup MCP Server",
        "Create an advanced MCP server with FastMCP",
        ["development", "mcp"]
    )
    db.create_task(
        "Add Authentication",
        "Implement authentication for the MCP server",
        ["security", "enhancement"]
    )
    
    # Context that will be available to all tools
    context = {
        "db": db,
        "start_time": datetime.now(),
        "version": "1.0.0"
    }
    
    yield context
    
    logger.info("Shutting down Advanced MCP Server...")


# Create the MCP server with lifespan
mcp = FastMCP(
    name="Advanced Task Manager",
    description="An advanced MCP server for task management",
    lifespan=lifespan
)


# Tools with context usage
@mcp.tool()
async def create_task(
    ctx: Context,
    title: Annotated[str, Field(description="Task title")],
    description: Annotated[str, Field(description="Task description")],
    tags: Annotated[List[str], Field(description="List of tags")] = []
) -> Dict:
    """Create a new task in the system."""
    try:
        task = ctx.lifespan_context["db"].create_task(title, description, tags)
        logger.info(f"Created task: {task.id} - {task.title}")
        return {
            "success": True,
            "task": task.model_dump(mode='json')
        }
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def list_tasks(
    ctx: Context,
    tag: Annotated[Optional[str], Field(description="Filter by tag")] = None
) -> List[Dict]:
    """List all tasks, optionally filtered by tag."""
    tasks = ctx.lifespan_context["db"].list_tasks(tag)
    return [task.model_dump(mode='json') for task in tasks]


@mcp.tool()
async def complete_task(
    ctx: Context,
    task_id: Annotated[int, Field(description="Task ID to mark as complete")]
) -> Dict:
    """Mark a task as completed."""
    task = ctx.lifespan_context["db"].update_task(task_id, completed=True)
    if task:
        return {
            "success": True,
            "message": f"Task {task_id} marked as complete",
            "task": task.model_dump(mode='json')
        }
    else:
        return {
            "success": False,
            "error": f"Task {task_id} not found"
        }


# Advanced tool with error handling and validation
@mcp.tool()
async def batch_update_tasks(
    ctx: Context,
    updates: Annotated[
        List[Dict], 
        Field(description="List of updates, each with 'task_id' and fields to update")
    ]
) -> Dict:
    """Update multiple tasks in a single operation."""
    results = []
    errors = []
    
    for update in updates:
        task_id = update.pop("task_id", None)
        if not task_id:
            errors.append("Missing task_id in update")
            continue
        
        task = ctx.lifespan_context["db"].update_task(task_id, **update)
        if task:
            results.append({
                "task_id": task_id,
                "success": True,
                "task": task.model_dump(mode='json')
            })
        else:
            errors.append(f"Task {task_id} not found")
    
    return {
        "total": len(updates),
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }


# Resources for providing context
@mcp.resource("tasks://all")
async def get_all_tasks(ctx: Context) -> str:
    """Get all tasks as a resource."""
    tasks = ctx.lifespan_context["db"].list_tasks()
    return json.dumps([task.model_dump(mode='json') for task in tasks], indent=2)


@mcp.resource("stats://overview")
async def get_statistics(ctx: Context) -> str:
    """Get task statistics and server information."""
    db = ctx.lifespan_context["db"]
    all_tasks = db.list_tasks()
    
    stats = {
        "server_version": ctx.lifespan_context["version"],
        "server_uptime": str(datetime.now() - ctx.lifespan_context["start_time"]),
        "total_tasks": len(all_tasks),
        "completed_tasks": len([t for t in all_tasks if t.completed]),
        "pending_tasks": len([t for t in all_tasks if not t.completed]),
        "tags": list(set(tag for task in all_tasks for tag in task.tags)),
        "timestamp": datetime.now().isoformat()
    }
    
    return json.dumps(stats, indent=2)


# Prompts for common interactions
@mcp.prompt()
async def task_review_prompt(ctx: Context) -> str:
    """Generate a prompt for reviewing pending tasks."""
    pending_tasks = [t for t in ctx.lifespan_context["db"].list_tasks() if not t.completed]
    
    if not pending_tasks:
        return "Great job! All tasks are completed. 🎉"
    
    prompt = "📋 **Pending Tasks Review**\n\n"
    prompt += f"You have {len(pending_tasks)} pending tasks:\n\n"
    
    for task in pending_tasks:
        prompt += f"- **{task.title}** (ID: {task.id})\n"
        prompt += f"  {task.description}\n"
        if task.tags:
            prompt += f"  Tags: {', '.join(task.tags)}\n"
        prompt += "\n"
    
    prompt += "\nWhat would you like to work on?"
    return prompt


@mcp.prompt()
async def daily_summary_prompt(ctx: Context) -> str:
    """Generate a daily summary prompt."""
    stats = await get_statistics(ctx)
    stats_data = json.loads(stats)
    
    prompt = "📊 **Daily Task Summary**\n\n"
    prompt += f"- Total Tasks: {stats_data['total_tasks']}\n"
    prompt += f"- Completed: {stats_data['completed_tasks']} ✅\n"
    prompt += f"- Pending: {stats_data['pending_tasks']} ⏳\n"
    prompt += f"- Active Tags: {', '.join(stats_data['tags'])}\n\n"
    
    if stats_data['pending_tasks'] > 0:
        prompt += "You still have pending tasks. Would you like to review them?"
    else:
        prompt += "All tasks completed! Time to add new ones?"
    
    return prompt


def main():
    """Main entry point."""
    import sys
    
    # Check for debug mode
    if "--debug" in sys.argv:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    # Run the server
    logger.info("Starting Advanced MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()