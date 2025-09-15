># Module 7 — Nested Models & Composition

>## Nested Models
- In Pydantic, you can use another model as a field within a model. This means that if there is an Address object inside a User, when you validate the User, Pydantic will automatically validate the rules of the Address as well.

>## use cases

- User with Address → an `Address` model within a `User`
- Order with Items → a list of `Item` models within an `Order`
- Blog with Comments → multiple `Comment` models within a `Post`

>## Automatic Validation

- If you provide a nested dict, Pydantic converts it into the proper model object.
- If there is a wrong type or missing value in the nested dict, a validation error will occur.

