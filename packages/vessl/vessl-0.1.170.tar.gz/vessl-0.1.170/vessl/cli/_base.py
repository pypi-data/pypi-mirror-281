import sys
from typing import Any, Callable, List, Optional

import click
import sentry_sdk

import vessl
from vessl.cli._util import style_prompt
from vessl.util import logger
from vessl.util.constant import VESSL_LOG_LEVEL
from vessl.util.exception import (
    DEFAULT_ERROR_MESSAGE,
    InvalidTokenError,
    VesslException,
)


def no_interaction_callback(ctx: click.Context, param: click.Parameter, value: bool):
    ctx.obj["no_interaction"] = value


no_interaction_option = click.Option(
    ["--no-interaction"],
    is_flag=True,
    is_eager=True,
    expose_value=False,
    hidden=True,
    callback=no_interaction_callback,
)


class VesslArgument(click.Argument):
    """Custom argument class"""

    def __init__(self, *args, **kwargs) -> None:
        self.prompter = kwargs.pop("prompter", None)
        super().__init__(*args, **kwargs)

    def process_value(self, ctx: click.Context, value: Any) -> Any:
        """Override parent method to invoke prompter before processing value."""
        if (
            (value is None or (self.multiple == True and not value))
            and self.prompter is not None
            and not ctx.obj["no_interaction"]
        ):
            value = self.prompter(ctx, self, value)

        return super().process_value(ctx, value)


class VesslOption(click.Option):
    """Custom option class"""

    def __init__(self, *args, **kwargs) -> None:
        self.prompter = kwargs.pop("prompter", None)
        super().__init__(*args, **kwargs)

    def process_value(self, ctx: click.Context, value: Any) -> Any:
        """Override parent method to invoke prompter before processing value."""
        if (
            (value is None or (self.multiple == True and not value))
            and self.prompter is not None
            and not ctx.obj["no_interaction"]
        ):
            value = self.prompter(ctx, self, value)

        return super().process_value(ctx, value)


class VesslContionalOption(click.Option):
    """Custom option class where the requirement is determined by the values of another option.
    Currently, multiple conditions are not supported.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.prompter = kwargs.pop("prompter", None)
        self.condition = kwargs.pop("condition", None)

        super().__init__(*args, **kwargs)

    def match_condition(self, ctx: click.Context) -> bool:
        if self.condition is None:
            return True

        param_name, values = self.condition
        # if `values` has multiple values, check if the list contains param value.
        if isinstance(values, list) or isinstance(values, tuple):
            return ctx.params.get(param_name) in values
        # if `values` is a single value, check if it is equal to param value
        return ctx.params.get(param_name) == values

    def prompt_for_value(self, ctx):
        if self.match_condition(ctx):
            return super().prompt_for_value(ctx)

    def process_value(self, ctx: click.Context, value: Any) -> Any:
        """Override parent method to invoke prompter before processing value."""

        if (
            (value is None or (self.multiple and not value))
            and self.prompter is not None
            and not ctx.obj["no_interaction"]
            and self.match_condition(ctx)
        ):
            value = self.prompter(ctx, self, value)

        return super().process_value(ctx, value)


class VesslCommand(click.Command):
    def __init__(
        self,
        login_required: bool = False,
        params: Optional[List[click.Parameter]] = None,
        **kwargs,
    ) -> None:
        self.login_required = login_required

        params = params or []
        params = [no_interaction_option] + params

        super().__init__(params=params, **kwargs)

    def make_context(self, *args, **kwargs) -> click.Context:
        if self.login_required:
            vessl.vessl_api.set_access_token(no_prompt=True)

        return super().make_context(*args, **kwargs)


class VesslGroup(click.Group):
    command_class = VesslCommand
    group_class = type  # Use VesslGroup recursively for sub-groups

    def vessl_command(self, login_required: bool = True, *args, **kwargs):
        kwargs["login_required"] = login_required
        return super().command(*args, **kwargs)

    def vessl_run_command(self, login_required: bool = False, *args, **kwargs):
        kwargs["login_required"] = login_required
        return super().command(*args, **kwargs)

    def main(self, *args, **kwargs):
        try:
            return super().main(*args, **kwargs)

        except InvalidTokenError as e:
            exc_info = e if VESSL_LOG_LEVEL == "DEBUG" else False
            logger.fatal("Invalid access token. Please run `vessl configure`.", exc_info=exc_info)
            sys.exit(1)

        except VesslException as e:
            exc_info = e
            logger.exception(f"{e.__class__.__name__}: {str(e)}", exc_info=exc_info)
            sys.exit(e.exit_code)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            sentry_sdk.flush()

            exc_info = e
            logger.fatal(DEFAULT_ERROR_MESSAGE, exc_info=exc_info)
            sys.exit(1)


def vessl_argument(*param_decls: str, **attrs: Any) -> Callable:
    attrs["cls"] = VesslArgument
    return click.argument(*param_decls, **attrs)


def vessl_option(*param_decls: str, **attrs: Any) -> Callable:
    attrs["cls"] = VesslOption

    # Style prompt
    if ("prompt" in attrs) and (attrs["prompt"] is not None):
        attrs["prompt"] = style_prompt(attrs.pop("prompt", None))
    return click.option(*param_decls, **attrs)


def vessl_conditional_option(*param_decls: str, **attrs: Any) -> Callable:
    attrs["cls"] = VesslContionalOption

    # Style prompt
    if ("prompt" in attrs) and (attrs["prompt"] is not None):
        attrs["prompt"] = style_prompt(attrs.pop("prompt", None))
    return click.option(*param_decls, **attrs)
