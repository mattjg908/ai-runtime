# 001: Python concurrency model

## Status

Accepted


## Context

The Python gateway will make network-bound model-provider calls and later run
multiple model and tool operations concurrently.

Python's asyncio and the BEAM both provide lightweight concurrency abstractions,
but they have significantly different scheduling, execution, and failure
semantics.

The gateway should use asyncio for Python-side I/O concurrency while avoiding
the assumption that asyncio Tasks behave like Erlang/Elixir processes.


## Python asyncio

### Coroutines

An `async def` function is a coroutine function.

Calling it creates a coroutine object:

    coroutine = model_call()

Creating the coroutine object does not immediately execute the body.

A coroutine can be executed by awaiting it:

    response = await model_call()

The current coroutine cannot continue past that `await` until the awaited
operation completes.

However, when the awaited operation itself needs to wait, the current asyncio
Task can be suspended and the event loop can run other ready Tasks.


### The event loop

The event loop is the scheduler at the center of asyncio.

A useful simplified model is:

    Python OS process
        |
        +-- event-loop OS thread
                |
                +-- Task A
                +-- Task B
                +-- Task C

When a Task reaches an await point and the awaited operation is not ready, the
Task can be suspended.

Control returns to the event loop.

The event loop can then run another ready Task.

When the awaited operation becomes ready, the suspended Task becomes eligible
to run again.


### await does not automatically create concurrency

Consider:

    first = await model_call("first")
    second = await model_call("second")

The second model call is not started until the first await completes.

The fact that `model_call` is async does not automatically make the two calls
concurrent.

`await` means approximately:

    Suspend this coroutine until this awaitable can produce its result.

It does not mean:

    Start all following async operations concurrently.


### Tasks

To schedule a coroutine independently:

    task = asyncio.create_task(model_call())

`create_task` schedules the coroutine with the event loop and returns a Task
object.

The current coroutine can continue:

    task = asyncio.create_task(model_call())

    do_something_else()

    response = await task

The Task may make progress concurrently with the current coroutine and other
scheduled Tasks.


### Sequential awaits over concurrent Tasks

These statements execute sequentially:

    first = await first_task
    second = await second_task
    third = await third_task

Python cannot perform the second assignment until the first await completes.

However, if all three Tasks were already scheduled:

    first_task = asyncio.create_task(first_call())
    second_task = asyncio.create_task(second_call())
    third_task = asyncio.create_task(third_call())

then the underlying operations can execute concurrently.

For example, while the current coroutine is suspended waiting for
`first_task`, the event loop can continue running `second_task` and
`third_task`.

The awaits are sequential.

The already-scheduled Tasks are concurrent.


## Cooperative scheduling in asyncio

asyncio uses cooperative scheduling between Tasks.

A Task normally gives the event loop an opportunity to run another Task when
it reaches an appropriate await point.

For example:

    await asyncio.sleep(10)

suspends the current Task.

The event-loop thread remains available to execute other ready Tasks.

By contrast:

    time.sleep(10)

blocks the OS thread.

If that is the thread running the event loop, the event loop itself cannot run
during those ten seconds.

Therefore other asyncio Tasks assigned to that event loop cannot make progress.

This gives us an important rule:

    Do not block the event loop.

Async Python code should use async-compatible network, timer, and I/O
operations when running on the event-loop thread.


## Structured concurrency

`asyncio.TaskGroup` gives related concurrent Tasks an explicit lifetime.

For example:

    async with asyncio.TaskGroup() as group:
        group.create_task(operation_a())
        group.create_task(operation_b())

The program does not leave the TaskGroup normally until its child Tasks have
completed.

If one child fails with an ordinary exception, TaskGroup cancels the remaining
children and waits for their cancellation and cleanup.

The original failures can then propagate from the TaskGroup as an
`ExceptionGroup`.


## Cancellation

Cancellation in asyncio is cooperative.

Calling:

    task.cancel()

requests that the Task be cancelled.

The Task normally observes this as:

    asyncio.CancelledError

at a suspension point.

For example:

    try:
        await operation()
    except asyncio.CancelledError:
        cleanup()
        raise

The coroutine may catch cancellation in order to perform cleanup, but should
normally re-raise the cancellation so that it continues to propagate.

A cancelled sibling in a failing TaskGroup does receive `CancelledError`.

However, TaskGroup normally does not report those sibling cancellations as
additional failures in the resulting ExceptionGroup. They are consequences of
the group's shutdown behavior rather than independent root-cause failures.


## finally and cleanup

`finally` executes whenever control leaves the associated try statement,
whether because of:

- normal completion
- return
- an exception
- cancellation

For example:

    try:
        await operation()
    except asyncio.CancelledError:
        raise
    finally:
        cleanup()

If the operation is cancelled, the try block does not finish normally.

Instead:

    operation receives CancelledError
        |
        v
    except handles cancellation
        |
        v
    cancellation is re-raised
        |
        v
    finally performs cleanup
        |
        v
    cancellation continues outward


## Timeouts

A timeout can be applied with:

    await asyncio.wait_for(
        operation(),
        timeout=1.0,
    )

If the operation does not complete in time, `wait_for` cancels the underlying
operation.

There are therefore two perspectives:

    underlying coroutine -> CancelledError
    caller of wait_for   -> TimeoutError

Timeout and cancellation are related, but they are not identical concepts.

A timeout is a policy decision that causes cancellation of work that has taken
too long.


# BEAM concurrency

## BEAM, OS processes, and OS threads

A useful simplified model is:

    Operating system
        |
        +-- BEAM VM OS process
                |
                +-- scheduler OS thread 1
                |       |
                |       +-- Erlang process A
                |       +-- Erlang process B
                |
                +-- scheduler OS thread 2
                |       |
                |       +-- Erlang process C
                |       +-- Erlang process D
                |
                +-- scheduler OS thread 3
                        |
                        +-- ...

An Erlang/Elixir process is NOT an operating-system process.

It is also NOT an operating-system thread.

It is a lightweight execution abstraction implemented by the BEAM VM.

The BEAM Book explains that an SMP-enabled emulator uses several OS threads,
with a scheduler/emulator associated with each scheduler thread. With default
settings, the number of scheduler threads is based on the enabled logical
cores available to ERTS.

This allows multiple Erlang processes to actually execute in parallel when
multiple schedulers are running on multiple CPU cores.

Source:
The BEAM Book, "Scheduling"
https://github.com/happi/theBeamBook
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc


## Concurrency vs. parallelism in BEAM

Concurrency does not necessarily mean that two processes are physically
executing at the same instant.

On a single core, the scheduler can switch between processes:

    Process A  ████
                    Process B  ████
    Process A                    ████

The processes are concurrent even though only one executes at a time.

With multiple scheduler threads and CPU cores, BEAM can also achieve actual
parallelism:

    CPU core 1                 CPU core 2

    Scheduler 1                Scheduler 2
        |                          |
    Process A                  Process B

        executing simultaneously

The BEAM Book explicitly distinguishes concurrency from parallel execution and
describes SMP ERTS as using several OS threads to execute Erlang processes.

Source:
The BEAM Book, "Scheduling: Concurrency, Parallelism, and Preemptive
Multitasking"
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc


## BEAM processes are lightweight

When Elixir executes something such as:

    spawn(fn -> work() end)

the operating system does not create another OS process or OS thread for that
Erlang process.

BEAM manages the process internally.

Conceptually, a BEAM process has VM-managed state including:

    PID
    execution state
    heap / stack
    mailbox
    scheduling state

The operating system gives resources to the BEAM OS process.

BEAM can then allocate and manage its own lightweight processes within those
resources.

This avoids the need to create a kernel-managed process or thread for every
unit of Erlang concurrency.

The result is that very large numbers of Erlang processes can exist inside one
BEAM VM.


## BEAM scheduling

A useful first approximation is:

    asyncio Tasks  -> cooperatively scheduled
    BEAM processes -> preemptively scheduled

But The BEAM Book gives a more precise description.

It describes BEAM scheduling as:

    preemptive scheduling on top of cooperative scheduling

At the Erlang-process level, scheduling behaves preemptively: a process cannot
simply consume a scheduler forever under normal BEAM execution.

Internally, however, a process can only be suspended at appropriate execution
points, such as function calls and receives.

The Erlang language, compiler, and VM are designed together so that normal
Erlang code reaches such points frequently.

This is very different from Python asyncio, where application code explicitly
uses `await` to cooperate with the event loop.

Source:
The BEAM Book, "Scheduling: Preemptive Multitasking in ERTS Cooperating in C"
and "Reductions"
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc


## Reductions

BEAM uses reductions as an approximation of execution work.

Function calls count toward a process's reduction budget.

When a process consumes its allotted reductions, it yields and becomes
runnable again so that the scheduler can select another process.

Conceptually:

    Scheduler
        |
        v
    Process A
        |
        +-- reduction
        +-- reduction
        +-- reduction
        +-- ...
        |
        +-- reduction budget exhausted
                |
                v
        Process A becomes runnable
                |
                v
        scheduler chooses another process

A process can also stop running before exhausting its reductions.

For example, a process executing `receive` with no matching message becomes
waiting rather than continuing to consume CPU.

The BEAM Book describes the process transition roughly as:

    running
       |
       | reductions exhausted
       v
    runnable

and:

    running
       |
       | receive with no matching message
       v
    waiting

When a relevant message or timeout occurs:

    waiting
       |
       v
    runnable

The scheduler can later select the process again.

Source:
The BEAM Book, "Scheduling: Reductions" and "The Process State"
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc


## An important nuance about reductions

A reduction is not simply a fixed number of CPU instructions.

The BEAM Book notes that the exact meaning of a reduction is not completely
defined, although Erlang-level function calls are an important part of
reduction counting.

The goal is to provide a practical approximation of execution work so that
processes receive reasonably fair access to schedulers.

Therefore:

    reduction != CPU instruction
    reduction != fixed amount of wall-clock time

It is a VM scheduling accounting mechanism.


## BEAM process states

The BEAM Book describes normal process states including:

    running
    runnable
    waiting

A running process is currently executing on a scheduler.

A runnable process is capable of executing but is waiting for a scheduler.

A waiting process is blocked waiting for something such as a matching message.

Conceptually:

                   reductions exhausted
              +--------------------------+
              |                          |
              v                          |
          runnable -----------------> running
              ^                          |
              |                          |
              | message / timeout        | receive with
              |                          | no matching message
              |                          v
              +---------------------- waiting

This distinction is useful because "not running" does not necessarily mean
"blocked."

A runnable process has work it can perform but is waiting for CPU scheduling.

Source:
The BEAM Book, "Scheduling: The Process State"
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc


## BEAM scheduler run queues

Runnable processes must wait somewhere until a scheduler can execute them.

The BEAM Book describes scheduler ready/run queues.

In an SMP system there is a queue associated with each scheduler.

Conceptually:

    Scheduler 1              Scheduler 2

    ready queue              ready queue
        P1                       P4
        P2                       P5
        P3                       P6

A scheduler takes runnable work from its queue and executes it.

The actual implementation is more sophisticated because BEAM supports process
priorities and therefore maintains different queues for different priority
classes.

Source:
The BEAM Book, "Scheduling: Process Queues" and "The Ready Queue"
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc


## Load balancing between BEAM schedulers

Multiple scheduler threads introduce another problem:

    What happens if one scheduler has lots of runnable processes while another
    scheduler has little work?

BEAM performs load balancing between scheduler run queues.

The BEAM Book discusses mechanisms including task stealing and process
migration.

A scheduler that runs out of work can attempt to steal runnable work from
another scheduler.

Processes can also migrate between scheduler queues as the runtime attempts to
balance CPU utilization.

This gives us a more complete model:

    BEAM OS process
        |
        +-- Scheduler 1
        |      |
        |      +-- run queue
        |
        +-- Scheduler 2
        |      |
        |      +-- run queue
        |
        +-- Scheduler 3
               |
               +-- run queue

             <---- work may move ---->

Source:
The BEAM Book, "Scheduling: Load Balancing", "Task Stealing", and "Migration"
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc


## BEAM does not magically make blocking code safe

BEAM's scheduler model does not mean that arbitrary native code can never
block a scheduler.

The BEAM Book specifically points out that badly implemented NIF code can block
a scheduler for a long time.

This matters because native C code does not automatically participate in BEAM's
normal Erlang reduction/yield behavior.

So the useful rule is not:

    BEAM can preempt absolutely anything.

It is:

    Normal Erlang execution is designed so the VM can regularly regain
    scheduling control.

Long-running native work requires special care.

Source:
The BEAM Book, "Scheduling: Reductions"
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc


# asyncio vs. BEAM

## Architecture

Python asyncio:

    Python OS process
        |
        +-- event-loop OS thread
                |
                +-- asyncio Task A
                +-- asyncio Task B
                +-- asyncio Task C

Typical BEAM:

    BEAM OS process
        |
        +-- scheduler OS thread 1
        |       |
        |       +-- BEAM processes
        |
        +-- scheduler OS thread 2
        |       |
        |       +-- BEAM processes
        |
        +-- scheduler OS thread 3
                |
                +-- BEAM processes


## Scheduling

asyncio:

    cooperative scheduling

    Task runs
        |
        v
    reaches await that must wait
        |
        v
    Task suspends
        |
        v
    event loop runs another ready Task


BEAM:

    reduction-based VM scheduling

    Process runs
        |
        v
    consumes reductions / reaches suspension condition
        |
        v
    scheduler regains control
        |
        v
    another runnable process can execute


## Blocking

asyncio:

    blocking event-loop thread
        |
        v
    event loop cannot schedule other Tasks

BEAM:

    ordinary Erlang process execution
        |
        v
    VM regularly regains scheduling control
        |
        v
    other BEAM processes receive scheduler time

But badly behaved native/NIF code can still block a BEAM scheduler.


## Parallelism

A normal asyncio event loop executes Python Tasks on its event-loop thread.

Therefore asyncio concurrency does not by itself mean that multiple Tasks are
executing Python code simultaneously on multiple CPU cores.

BEAM normally has multiple scheduler OS threads.

Therefore different BEAM processes can execute simultaneously on different CPU
cores.


## Failure management

asyncio TaskGroup:

    child fails
        |
        v
    sibling Tasks cancelled
        |
        v
    cleanup
        |
        v
    exception(s) propagate


OTP supervision:

    child process exits
        |
        v
    supervisor observes termination
        |
        v
    configured supervision strategy determines what happens next

These mechanisms share the idea that concurrent work should have ownership and
lifecycle structure, but they are not equivalent.

TaskGroup is structured concurrency.

OTP supervision is a long-lived fault-management and process-lifecycle model.


# Decision

Use asyncio for concurrency inside the Python gateway.

The gateway's main concurrent operations are expected to be I/O-heavy:

    model API requests
    tool calls
    network operations
    streaming
    timeouts

asyncio is appropriate for overlapping these waits without creating an OS
thread for every request.

Python gateway code should:

    - avoid blocking the event-loop thread
    - use async-compatible I/O
    - distinguish coroutine creation from Task scheduling
    - use TaskGroup where concurrent operations share a lifetime
    - propagate cancellation correctly
    - distinguish cancellation from timeout
    - make timeout and retry policy explicit

Do not attempt to recreate BEAM/OTP inside Python.

The later Elixir runtime should own concerns that naturally fit OTP:

    long-lived process ownership
    supervision
    restart strategies
    workflow lifecycle
    fault recovery
    orchestration


# Main takeaway

Both asyncio Tasks and BEAM processes are lightweight concurrency abstractions
managed above the operating-system process/thread layer.

But they should not be treated as equivalent.

The central mental model is:

    Python asyncio
        cooperative Task scheduling
        explicit await points
        event-loop-centered I/O concurrency

    BEAM
        lightweight isolated processes
        reduction-based scheduling
        multiple scheduler OS threads
        VM-managed run queues
        multicore parallelism
        message passing
        OTP supervision above the process model

The particularly important difference for Python development is:

    In asyncio, application code is responsible for cooperating with the event
    loop.

    In normal Erlang/Elixir code, the language, compiler, and BEAM VM work
    together to ensure that processes regularly return scheduling control to
    the runtime.


# References

The BEAM Book
Erik Stenman et al.
https://github.com/happi/theBeamBook

Scheduling chapter:
https://raw.githubusercontent.com/happi/theBeamBook/master/chapters/scheduling.asciidoc

The repository describes The BEAM Book as documentation of the internals of
the Erlang Runtime System (ERTS) and the BEAM virtual machine.
