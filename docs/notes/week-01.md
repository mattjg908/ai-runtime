Neither Elixir nor Python enforces type annotations at runtime. Elixir
developers commonly use Dialyzer for static analysis, while Python developers
commonly use mypy (or pyright). In both languages, type annotations are
primarily for tooling and documentation; the runtime itself does not enforce
them.

Python's Protocol is much closer to an Elixir @behaviour than an Elixir
defprotocol. It defines an interface that classes satisfy structurally (by
having the required methods), even if they never explicitly declare that they
implement the protocol. This differs from Elixir behaviours, which must be
declared explicitly using @behaviour. Elixir protocols, by contrast, provide
runtime dispatch based on data type.

Literal is conceptually similar to using a union of atoms in Elixir (for
example, :openai | :anthropic). Python extends this concept by allowing
specific string values to be part of the type system, which Elixir's typespecs
do not support directly.

The biggest surprise was not the syntax—it was that Python and Elixir share a
similar philosophy about types. In both languages, type annotations improve
tooling and documentation rather than changing runtime behavior. The biggest
conceptual difference I've seen so far is that Python's Protocol corresponds to
an Elixir @behaviour, not to an Elixir protocol.
