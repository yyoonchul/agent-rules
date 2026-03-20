Bundled runtime dependencies for `assignment-solver`.

- `pypdf==6.9.1` for `.pdf` text extraction
- `olefile==0.47` for opening legacy OLE `.ppt` files

These packages are vendored into the skill folder so the skill can read supported
lecture material formats without installing modules in each target project.
