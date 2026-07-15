mypy is conceptually similar to Dialyzer. It answers the question, "Is my code
internally consistent?"

Pydantic is conceptually similar to the validation role of an Ecto changeset.
It answers the question, "Can I trust this external data?" Unlike an Ecto
changeset, a Pydantic model is the validated object itself. It does not track
changes or prepare data for persistence.

An Ecto changeset is often part of a persistence pipeline. It tracks changes,
validates them, and is commonly used before inserting or updating a database
record (although this is powerful without db backing).

A Pydantic model is a validated object. Once construction succeeds, you have
a trustworthy Python object that can be passed around your application. It
doesn't track pending changes or have a concept of "saving.". Pydantic asks:
"Can I safely admit this external data into my system?"

Additionally, Pydantic plays a role similar to Protobuf decoding: it validates
data at the boundary before the rest of the application trusts it.
