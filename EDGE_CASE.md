# Edge Case: Missing `mark` field on POST /students

## The Edge Case
The spec states that `mark` is an optional field when creating a student via `POST /students`. However, the original implementation accessed `student_data["mark"]` directly, which raises a `KeyError` and crashes the server if `mark` is not included in the request body.

## How It Was Handled
The implementation was updated to use `student_data.get("mark", 0)`, which safely defaults the mark to `0` if it is not provided. This means a student can be created with just a `name` and `course`, and their mark can be updated later via `PUT /students/{id}`. This aligns with the spec's intent that mark is optional at creation time.