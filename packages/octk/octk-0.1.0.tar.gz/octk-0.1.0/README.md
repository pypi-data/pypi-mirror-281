# octk

## Utilities

### `uniquify`
Given a file path, `uniquify` will return a unique file path by appending a number to the file name if necessary.

```shell
example_dir
├── foo.txt
└── bar
    └── baz.txt
```

```python
from octk import uniquify

uniquify('example_dir/foo.txt')
# 'example_dir/foo(1).txt'

uniquify('example_dir/bar')
# 'example_dir/bar(1)'

uniquify('example_dir/bar.txt')
# 'example_dir/bar.txt'
```

### `pytree.FileTree`
Created to work around the fact that Windows' `tree` does not allow you to exclude folders or filter files by extension.

```python
from octk import FileTree

tree = FileTree('example_dir')
tree.print_tree()
```

```shell
example_dir
├── foo.txt
└── bar
    └── baz.txt
```

### `make_draft_email()`
Given the basic information of an email (i.e. subject, content, & recipients), `make_draft_email()` will create a valid `.eml` file that can be opened and sent by an email client.

```python
from octk import make_draft_email

make_draft_email(
    out_path='out/folder/example.eml',
    subject='Hello, World!',
    content='This is a test email.',
    recipients=['example@hello.com']
)
```
```

