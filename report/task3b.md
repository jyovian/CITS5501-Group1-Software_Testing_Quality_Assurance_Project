# Task 3b - example of a simulated failure

For this example, I used a small local HTTP server to imitate the policy
website returning `500 Internal Server Error`. This is useful because a real
website may only return this error occasionally. Waiting for the real error
would make the test difficult to repeat, and deliberately sending bad requests
to the real website would not be appropriate.

The example is in `task3b/fault_simulation_example.py`. It starts the fake
server on the local computer, requests one policy page, and catches the HTTP
error. The expected result is `Success: False` together with an `HTTP 500`
message. This shows that a scraper can report the problem instead of stopping
with an unhandled exception. An automated check is included in
`task3b/test_fault_simulation_example.py`.

**A3-001:** This example assumes that an HTTP 500 response should be reported
as a failed download and should not be treated as valid policy content.
