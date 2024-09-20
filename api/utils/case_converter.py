from pydantic import ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel, to_snake

snake_to_camel = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        )
    )

camel_to_snake = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_snake,
        )
    )