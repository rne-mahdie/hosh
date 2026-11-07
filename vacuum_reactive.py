# -*- coding: utf-8 -*-
"""عامل واکنشی ساده برای مسئله جاروبرقی در محیط 2*2

هر خانه می تواند dirty یا clean باشد.
عامل فقط به ادراک فعلی خانه (کثیف/تمیز) و حالت داخلی کوچکی (موقعیت و بازدیدها)
واکنش نشان می دهد؛ بدون برنامه ریزی و بدون جستجو.
"""

from enum import Enum


class Direction(Enum):
    RIGHT = "راست"
    DOWN = "پایین"
    LEFT = "چپ"
    UP = "بالا"


# ترتیب بازدید خانه ها: (0,0) -> (0,1) -> (1,1) -> (1,0)
ROUTE = [(0, 0), (0, 1), (1, 1), (1, 0)]

# بردار جابه جایی برای هر جهت
MOVES = {
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.UP: (-1, 0),
}


class VacuumAgent:
    """عامل واکنشی ساده با حالت حداقلی (موقعیت + خانه های بازدید شده)."""

    def __init__(self):
        self.position = (0, 0)      # حالت داخلی: موقعیت فعلی
        self.visited = set()        # حالت داخلی: خانه های بازدید شده

    def act(self, is_dirty):
        """قانون واکنشی: بر اساس ادراک فعلی، یک عمل برمی گرداند."""
        # قانون ۱: اگر خانه کثیف است، تمیز کن
        if is_dirty:
            self.visited.add(self.position)
            return "CLEAN"

        # قانون ۲: خانه تمیز است؛ خانه بعدی در مسیر ثابت را هدف بگیر
        self.visited.add(self.position)
        for cell in ROUTE:
            if cell not in self.visited:
                return self._go_toward(cell)

        # قانون ۳: همه خانه ها بازدید شدند؛ بایست
        return "NO_OP"

    def _go_toward(self, target):
        """خانه بعدی را با حداقل حرکت مماسی هدف می گیرد (فقط راست/پایین در این مسیر)."""
        tr, tc = target
        r, c = self.position
        if tc > c:
            self.position = (r, c + 1)
            return "MOVE_RIGHT"
        if tc < c:
            self.position = (r, c - 1)
            return "MOVE_LEFT"
        if tr > r:
            self.position = (r + 1, c)
            return "MOVE_DOWN"
        self.position = (r - 1, c)
        return "MOVE_UP"


def run(environment, max_steps=50):
    """محیط 2*2 را اجرا می کند؛ environment دیکشنری {(ر,ص): 'dirty'|'clean'} است."""
    agent = VacuumAgent()
    print("حالت اولیه محیط:")
    print_env(environment)

    for step in range(1, max_steps + 1):
        perception = environment[agent.position] == "dirty"
        action = agent.act(perception)

        if action == "CLEAN":
            environment[agent.position] = "clean"
        # MOVE_* قبلاً در _go_toward داخل حالت عامل اعمال شده است

        print(f"گام {step}: ادراک={agent.position} {environment[agent.position]}"
              f" | عمل={action} | موقعیت بعدی={agent.position}")
        print_env(environment)

        if all(v == "clean" for v in environment.values()):
            print(f"\nهمه خانه ها در گام {step} تمیز شدند.")
            return True

    print("\nبه سقف گام ها رسید؛ محیط هنوز تمیز نیست.")
    return False


def print_env(env):
    for r in range(2):
        row = " | ".join(f"{env[(r, c)]:>5}" for c in range(2))
        print("  " + row)
    print("  " + "-" * 20)


if __name__ == "__main__":
    # محیط 2*2 با چند خانه کثیف
    world = {
        (0, 0): "dirty",
        (0, 1): "clean",
        (1, 1): "dirty",
        (1, 0): "dirty",
    }
    run(world)
