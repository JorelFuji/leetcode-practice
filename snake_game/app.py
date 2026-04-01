from __future__ import annotations

import tkinter as tk

from snake_game.logic import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    create_initial_state,
    queue_direction,
    step_game,
    toggle_pause,
)


CELL_SIZE = 24
TICK_MS = 140
BOARD_COLOR = "#1d1d1b"
EMPTY_COLOR = "#f7f3e8"
SNAKE_COLOR = "#2f6f3e"
HEAD_COLOR = "#1f4f2c"
FOOD_COLOR = "#d94841"
PANEL_COLOR = "#fffaf0"
BUTTON_COLOR = "#f8ecd0"


class SnakeApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.configure(bg="#f4f1e8")
        self.root.resizable(False, False)

        self.state = create_initial_state()
        self.running_job: str | None = None
        self.cells: dict[tuple[int, int], tk.Canvas] = {}

        self.score_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="Press an arrow key or WASD to start.")
        self.pause_var = tk.StringVar(value="Pause")

        self._build_ui()
        self._bind_keys()
        self.render()

    def _build_ui(self) -> None:
        shell = tk.Frame(
            self.root,
            bg=PANEL_COLOR,
            padx=18,
            pady=18,
            highlightbackground=BOARD_COLOR,
            highlightthickness=2,
        )
        shell.pack(padx=24, pady=24)

        header = tk.Frame(shell, bg=PANEL_COLOR)
        header.pack(fill="x")

        title_group = tk.Frame(header, bg=PANEL_COLOR)
        title_group.pack(side="left", anchor="w")
        tk.Label(
            title_group,
            text="Classic Arcade",
            font=("Trebuchet MS", 11),
            fg="#5a574f",
            bg=PANEL_COLOR,
        ).pack(anchor="w")
        tk.Label(
            title_group,
            text="Snake",
            font=("Trebuchet MS", 24, "bold"),
            fg=BOARD_COLOR,
            bg=PANEL_COLOR,
        ).pack(anchor="w")

        score_group = tk.Frame(header, bg=PANEL_COLOR)
        score_group.pack(side="right", anchor="e")
        tk.Label(
            score_group,
            text="Score",
            font=("Trebuchet MS", 11),
            fg="#5a574f",
            bg=PANEL_COLOR,
        ).pack(anchor="e")
        tk.Label(
            score_group,
            textvariable=self.score_var,
            font=("Trebuchet MS", 20, "bold"),
            fg=BOARD_COLOR,
            bg=PANEL_COLOR,
        ).pack(anchor="e")

        meta_row = tk.Frame(shell, bg=PANEL_COLOR)
        meta_row.pack(fill="x", pady=(12, 12))

        tk.Label(
            meta_row,
            textvariable=self.status_var,
            font=("Trebuchet MS", 11),
            fg="#5a574f",
            bg=PANEL_COLOR,
        ).pack(side="left", anchor="w")

        button_row = tk.Frame(meta_row, bg=PANEL_COLOR)
        button_row.pack(side="right")

        tk.Button(
            button_row,
            textvariable=self.pause_var,
            command=self.pause_game,
            bg=BUTTON_COLOR,
            activebackground="#f2e0b4",
            highlightbackground=BOARD_COLOR,
            padx=10,
            pady=6,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            button_row,
            text="Restart",
            command=self.restart_game,
            bg=BUTTON_COLOR,
            activebackground="#f2e0b4",
            highlightbackground=BOARD_COLOR,
            padx=10,
            pady=6,
        ).pack(side="left")

        self.board = tk.Frame(
            shell,
            bg=BOARD_COLOR,
            padx=2,
            pady=2,
        )
        self.board.pack()

        for y in range(self.state.height):
            for x in range(self.state.width):
                cell = tk.Canvas(
                    self.board,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    bg=EMPTY_COLOR,
                    bd=0,
                    highlightthickness=0,
                )
                cell.grid(row=y, column=x, padx=1, pady=1)
                self.cells[(x, y)] = cell

        controls = tk.Frame(shell, bg=PANEL_COLOR)
        controls.pack(pady=(14, 0))

        up_row = tk.Frame(controls, bg=PANEL_COLOR)
        up_row.pack()
        self._make_control_button(up_row, "Up", UP).pack()

        lower_row = tk.Frame(controls, bg=PANEL_COLOR)
        lower_row.pack(pady=(6, 0))
        self._make_control_button(lower_row, "Left", LEFT).pack(side="left", padx=4)
        self._make_control_button(lower_row, "Down", DOWN).pack(side="left", padx=4)
        self._make_control_button(lower_row, "Right", RIGHT).pack(side="left", padx=4)

    def _make_control_button(
        self,
        parent: tk.Widget,
        label: str,
        direction: str,
    ) -> tk.Button:
        return tk.Button(
            parent,
            text=label,
            command=lambda: self.set_direction(direction),
            width=8,
            bg=BUTTON_COLOR,
            activebackground="#f2e0b4",
            highlightbackground=BOARD_COLOR,
            pady=6,
        )

    def _bind_keys(self) -> None:
        self.root.bind("<Up>", lambda _event: self.set_direction(UP))
        self.root.bind("<Down>", lambda _event: self.set_direction(DOWN))
        self.root.bind("<Left>", lambda _event: self.set_direction(LEFT))
        self.root.bind("<Right>", lambda _event: self.set_direction(RIGHT))
        self.root.bind("<w>", lambda _event: self.set_direction(UP))
        self.root.bind("<a>", lambda _event: self.set_direction(LEFT))
        self.root.bind("<s>", lambda _event: self.set_direction(DOWN))
        self.root.bind("<d>", lambda _event: self.set_direction(RIGHT))
        self.root.bind("<space>", lambda _event: self.pause_game())

    def set_direction(self, direction: str) -> None:
        next_state = queue_direction(self.state, direction)
        if next_state == self.state:
            return

        self.state = next_state
        self.render()
        self.ensure_loop()

    def run_tick(self) -> None:
        self.running_job = None
        self.state = step_game(self.state)
        self.render()
        self.ensure_loop()

    def ensure_loop(self) -> None:
        if self.running_job is not None:
            return

        if self.state.game_over or self.state.paused or not self.state.started:
            return

        self.running_job = self.root.after(TICK_MS, self.run_tick)

    def stop_loop(self) -> None:
        if self.running_job is not None:
            self.root.after_cancel(self.running_job)
            self.running_job = None

    def pause_game(self) -> None:
        self.state = toggle_pause(self.state)
        if self.state.paused:
            self.stop_loop()
        else:
            self.ensure_loop()
        self.render()

    def restart_game(self) -> None:
        self.stop_loop()
        self.state = create_initial_state()
        self.render()

    def render(self) -> None:
        snake_cells = set(self.state.snake)
        head = self.state.snake[0]

        for position, cell in self.cells.items():
            color = EMPTY_COLOR
            if position in snake_cells:
                color = SNAKE_COLOR
            if position == self.state.food:
                color = FOOD_COLOR
            if position == head:
                color = HEAD_COLOR
            cell.configure(bg=color)

        self.score_var.set(str(self.state.score))
        self.pause_var.set("Resume" if self.state.paused else "Pause")

        if self.state.game_over:
            self.status_var.set("Game over. Press Restart to play again.")
        elif not self.state.started:
            self.status_var.set("Press an arrow key or WASD to start.")
        elif self.state.paused:
            self.status_var.set("Paused. Press Space or Resume to continue.")
        else:
            self.status_var.set("Use arrow keys, WASD, or the buttons to steer.")

    def start(self) -> None:
        self.root.mainloop()


def main() -> None:
    SnakeApp().start()


if __name__ == "__main__":
    main()

