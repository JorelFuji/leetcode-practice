import random
import unittest

from snake_game.logic import (
    LEFT,
    create_initial_state,
    get_available_food_position,
    queue_direction,
    step_game,
    toggle_pause,
)


class SnakeLogicTests(unittest.TestCase):
    def test_moves_forward(self) -> None:
        state = create_initial_state(8, 8)
        next_state = step_game(state, random.Random(0))

        self.assertEqual(next_state.snake, ((3, 4), (2, 4), (1, 4)))
        self.assertEqual(next_state.score, 0)

    def test_grows_when_eating_food(self) -> None:
        state = create_initial_state(10, 10)
        state = state.__class__(**{**state.__dict__, "food": (3, 5)})
        next_state = step_game(state, random.Random(0))

        self.assertEqual(next_state.score, 1)
        self.assertEqual(len(next_state.snake), 4)
        self.assertEqual(next_state.snake[0], (3, 5))

    def test_prevents_reverse_direction(self) -> None:
        state = create_initial_state(10, 10)
        next_state = queue_direction(state, LEFT)

        self.assertEqual(next_state.direction, state.direction)
        self.assertEqual(next_state.queued_direction, state.queued_direction)

    def test_boundary_collision_sets_game_over(self) -> None:
        state = create_initial_state(4, 4)
        state = state.__class__(
            **{
                **state.__dict__,
                "snake": ((3, 1), (2, 1), (1, 1)),
                "direction": "Right",
                "queued_direction": "Right",
            }
        )

        next_state = step_game(state, random.Random(0))
        self.assertTrue(next_state.game_over)

    def test_self_collision_sets_game_over(self) -> None:
        state = create_initial_state(6, 6)
        state = state.__class__(
            **{
                **state.__dict__,
                "snake": ((2, 2), (3, 2), (1, 2), (1, 1), (2, 1)),
                "direction": "Left",
                "queued_direction": "Left",
                "food": (5, 5),
            }
        )

        next_state = step_game(state, random.Random(0))
        self.assertTrue(next_state.game_over)

    def test_food_uses_open_cells(self) -> None:
        food = get_available_food_position(2, 2, ((0, 0), (1, 0), (0, 1)), random.Random(0))
        self.assertEqual(food, (1, 1))

    def test_pause_only_after_start(self) -> None:
        idle_state = create_initial_state(10, 10)
        self.assertFalse(toggle_pause(idle_state).paused)

        active_state = state_with(idle_state, started=True)
        self.assertTrue(toggle_pause(active_state).paused)


def state_with(state, **changes):
    values = {**state.__dict__, **changes}
    return state.__class__(**values)


if __name__ == "__main__":
    unittest.main()
