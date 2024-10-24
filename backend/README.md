# Backend

- Install [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
- Build [absorpig](https://github.com/Computational-Biology-Aachen/absorpig) locally
  - run `uv build` in the repo
  - copy build wheel (`*.whl`) locally into `pkg` folder (ignored by git)
- Add wheel as dependency: `uv add pkg/absorpig-0.1.0-py3-none-any.whl`
- Start server: `uv run fastapi dev`
