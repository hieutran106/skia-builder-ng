uv run

### On windows

- Setup env: `un run python -m skia_builder.cli setup-env --skip-llvm-instalation`
- Compile for win: 
    `uv run python -m skia_builder.cli build --target-cpu=x64 --archive`

 