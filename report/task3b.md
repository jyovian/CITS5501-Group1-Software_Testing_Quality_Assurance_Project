# Task 3b - example of a simulated failure

For this example, I used a small local HTTP server to imitate the policy
website returning `503 Service Unavailable`. This is useful because a real
website may only return this error occasionally. Waiting for the real error
would make the test difficult to repeat, and deliberately sending bad requests
to the real website would not be appropriate.

The example is in `task3b/fault_simulation_example.py`. It starts a fake policy
site on the local computer. The index page contains a link called
`unavailable.pdf`, but the server returns HTTP 503 when that link is requested.
The server can be left running so the Task 1 prototype can use its local index
as the starting URL. The built-in demonstration catches the HTTP error and
prints `Success: False` with an `HTTP 503` message instead of stopping with an
unhandled exception. Automated checks are included in
`task3b/test_fault_simulation_example.py`.

**A3-001:** This example assumes that an HTTP 503 response should be reported
as a failed download and should not be treated as valid policy content.
