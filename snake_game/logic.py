from __future__ import annotations

from dataclasses import dataclass, replace
from random import Random


UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

VECTORS = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
}

OPPOSITES = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}


@dataclass(frozen=True)
class GameState:
    width: int
    height: int
    snake: tuple[tuple[int, int], ...]
    direction: str
    queued_direction: str
    food: tuple[int, int] | None
    score: int
    started: bool
    paused: bool
    game_over: bool


def create_initial_state(width: int = 16, height: int = 16) -> GameState:
    center_y = height // 2
    snake = ((2, center_y), (1, center_y), (0, center_y))
    return GameState(
        width=width,
        height=height,
        snake=snake,
        direction=RIGHT,
        queued_direction=RIGHT,
        food=get_available_food_position(width, height, snake),
        score=0,
        started=False,
        paused=False,
        game_over=False,
    )


def queue_direction(state: GameState, next_direction: str) -> GameState:
    if next_direction not in VECTORS or state.game_over:
        return state

    current_direction = state.queued_direction or state.direction
    if OPPOSITES[current_direction] == next_direction:
        return state

    return replace(
        state,
        queued_direction=next_direction,
        started=True,
        paused=False,
    )


def toggle_pause(state: GameState) -> GameState:
    if not state.started or state.game_over:
        return state
    return replace(state, paused=not state.paused)


def step_game(state: GameState, rng: Random | None = None) -> GameState:
    if state.game_over or state.paused:
        return state

    dx, dy = VECTORS[state.queued_direction]
    head_x, head_y = state.snake[0]
    next_head = (head_x + dx, head_y + dy)

    x, y = next_head
    hits_boundary = x < 0 or y < 0 or x >= state.width or y >= state.height
    will_eat = state.food is not None and next_head == state.food
    body_to_check = state.snake if will_eat else state.snake[:-1]
    hits_self = next_head in body_to_check

    if hits_boundary or hits_self:
        return replace(
            state,
            direction=state.queued_direction,
            queued_direction=state.queued_direction,
            started=True,
            game_over=True,
            paused=False,
        )

    next_snake = (next_head,) + state.snake
    if not will_eat:
        next_snake = next_snake[:-1]

    next_food = (
        get_available_food_position(state.width, state.height, next_snake, rng)
        if will_eat
        else state.food
    )

    return replace(
        state,
        snake=next_snake,
        direction=state.queued_direction,
        queued_direction=state.queued_direction,
        food=next_food,
        score=state.score + (1 if will_eat else 0),
        started=True,
        paused=False,
        game_over=False,
    )


def get_available_food_position(
    width: int,
    height: int,
    snake: tuple[tuple[int, int], ...],
    rng: Random | None = None,
) -> tuple[int, int] | None:
    occupied = set(snake)
    open_cells = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in occupied
    ]

    if not open_cells:
        return None

    random_source = rng or Random()
    return open_cells[random_source.randrange(len(open_cells))]

