# Pytest issue 5197

I implemented a convenience function to enable writing to terminal (stdout), plain text file, or gzip-compressed file with a single `open` function: `myopen` in `example.py`.

```
$ ./example.py DataPayload
{
    "really_important_data": "DataPayload",
    "some_more_data": 42,
    "on_a_roll_here": 3.14159
}
$ ./example.py --out data1.json Duuuuude
$ cat data1.json 
{
    "really_important_data": "Duuuuude",
    "some_more_data": 42,
    "on_a_roll_here": 3.14159
}
$ ./example.py --out data2.json.gz Sweeeeet
$ gunzip -c data2.json.gz 
{
    "really_important_data": "Sweeeeet",
    "some_more_data": 42,
    "on_a_roll_here": 3.14159
}
```

I invoke the `myopen` function in main as follows.

```
with myopen(args.out, 'w') as fh:
    json.dump(data, fh, indent=4)
```

If I invoke the main function in pytest ***without*** capsys enabled, things work fine.

```
$ pytest -k test_output_file example.py 
================================================= test session starts ==================================================
platform darwin -- Python 3.6.8, pytest-4.3.0, py-1.8.0, pluggy-0.9.0
rootdir: /Users/daniel.standage/with-capsys-example, inifile:
plugins: remotedata-0.3.1, openfiles-0.3.1
collected 2 items / 1 deselected / 1 selected                                                                          

example.py .                                                                                                     [100%]

======================================== 1 passed, 1 deselected in 0.02 seconds ========================================
```

If I invoke the main function in pytest ***with*** capsys enabled, I get `INTERNALERROR> ValueError: I/O operation on closed file.` errors.
