# skia-builder


## Usage
```bash
skia-builder setup-env
skia-builder setup-env --sub-env=Android
skia-builder build --sub-env=Android
skia-builder build --custom-build-args="cc=clang cxx=clang++ skia_compile_modules=true ..."
skia-builder build --archive --custom-build-args="cc=clang cxx=clang++ skia_compile_modules=true ..."
```