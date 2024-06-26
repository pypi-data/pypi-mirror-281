from typing import ClassVar, Generic, TypeVar

T = TypeVar("T")


class Client(Generic[T]):
    env_vars: ClassVar[dict[str, str]] = {}

    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        base_url: str | None = None,
        call_kwargs: dict | None = None,
        **client_kwargs,
    ) -> None:
        """Initialize the Client instance.

        Args:
            model (str): The model to be used.
            api_key (str): The API key for authentication.
            base_url (str, optional): The base URL for the API. Defaults to None.
            call_kwargs (dict, optional): Additional keyword arguments for the API call. Defaults to None.
            **client_kwargs: Additional keyword arguments for the client initialization.

        Returns:
            None
        """
        if not call_kwargs:
            call_kwargs = {}

        self._model = model
        self._api_key = api_key
        self._base_url = base_url
        self._call_kwargs = call_kwargs | {"model": self.model}
        self._client = self._init_client(
            api_key=self._api_key,
            base_url=self._base_url,
            **client_kwargs,
        )

    @property
    def model(self) -> str:
        return self._model

    @property
    def client(self) -> T:
        return self._client

    def _init_client(self, **kwargs) -> T:
        raise NotImplementedError

    def _get_call_kwargs(self, **kwargs) -> dict:
        return self._call_kwargs | kwargs
