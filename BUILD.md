uv run

### On windows

- Setup env: `python -m skia_builder.cli setup-env --skip-llvm-instalation`
- Compile for win: 
    `python -m skia_builder.cli build --target-cpu=x64 --override-build-args="extra_cflags=['/MD'] extra_cflags_cc=['/MD']" --archive`

 