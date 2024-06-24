# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetBotResult',
    'AwaitableGetBotResult',
    'get_bot',
    'get_bot_output',
]

@pulumi.output_type
class GetBotResult:
    """
    A collection of values returned by getBot.
    """
    def __init__(__self__, arn=None, checksum=None, child_directed=None, created_date=None, description=None, detect_sentiment=None, enable_model_improvements=None, failure_reason=None, id=None, idle_session_ttl_in_seconds=None, last_updated_date=None, locale=None, name=None, nlu_intent_confidence_threshold=None, status=None, version=None, voice_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if checksum and not isinstance(checksum, str):
            raise TypeError("Expected argument 'checksum' to be a str")
        pulumi.set(__self__, "checksum", checksum)
        if child_directed and not isinstance(child_directed, bool):
            raise TypeError("Expected argument 'child_directed' to be a bool")
        pulumi.set(__self__, "child_directed", child_directed)
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if detect_sentiment and not isinstance(detect_sentiment, bool):
            raise TypeError("Expected argument 'detect_sentiment' to be a bool")
        pulumi.set(__self__, "detect_sentiment", detect_sentiment)
        if enable_model_improvements and not isinstance(enable_model_improvements, bool):
            raise TypeError("Expected argument 'enable_model_improvements' to be a bool")
        pulumi.set(__self__, "enable_model_improvements", enable_model_improvements)
        if failure_reason and not isinstance(failure_reason, str):
            raise TypeError("Expected argument 'failure_reason' to be a str")
        pulumi.set(__self__, "failure_reason", failure_reason)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if idle_session_ttl_in_seconds and not isinstance(idle_session_ttl_in_seconds, int):
            raise TypeError("Expected argument 'idle_session_ttl_in_seconds' to be a int")
        pulumi.set(__self__, "idle_session_ttl_in_seconds", idle_session_ttl_in_seconds)
        if last_updated_date and not isinstance(last_updated_date, str):
            raise TypeError("Expected argument 'last_updated_date' to be a str")
        pulumi.set(__self__, "last_updated_date", last_updated_date)
        if locale and not isinstance(locale, str):
            raise TypeError("Expected argument 'locale' to be a str")
        pulumi.set(__self__, "locale", locale)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if nlu_intent_confidence_threshold and not isinstance(nlu_intent_confidence_threshold, float):
            raise TypeError("Expected argument 'nlu_intent_confidence_threshold' to be a float")
        pulumi.set(__self__, "nlu_intent_confidence_threshold", nlu_intent_confidence_threshold)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)
        if voice_id and not isinstance(voice_id, str):
            raise TypeError("Expected argument 'voice_id' to be a str")
        pulumi.set(__self__, "voice_id", voice_id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the bot.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def checksum(self) -> str:
        """
        Checksum of the bot used to identify a specific revision of the bot's `$LATEST` version.
        """
        return pulumi.get(self, "checksum")

    @property
    @pulumi.getter(name="childDirected")
    def child_directed(self) -> bool:
        """
        If this Amazon Lex Bot is related to a website, program, or other application that is directed or targeted, in whole or in part, to children under age 13 and subject to COPPA.
        """
        return pulumi.get(self, "child_directed")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        Date that the bot was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the bot.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="detectSentiment")
    def detect_sentiment(self) -> bool:
        """
        When set to true user utterances are sent to Amazon Comprehend for sentiment analysis.
        """
        return pulumi.get(self, "detect_sentiment")

    @property
    @pulumi.getter(name="enableModelImprovements")
    def enable_model_improvements(self) -> bool:
        """
        Set to true if natural language understanding improvements are enabled.
        """
        return pulumi.get(self, "enable_model_improvements")

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> str:
        """
        If the `status` is `FAILED`, the reason why the bot failed to build.
        """
        return pulumi.get(self, "failure_reason")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="idleSessionTtlInSeconds")
    def idle_session_ttl_in_seconds(self) -> int:
        """
        The maximum time in seconds that Amazon Lex retains the data gathered in a conversation.
        """
        return pulumi.get(self, "idle_session_ttl_in_seconds")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> str:
        """
        Date that the bot was updated.
        """
        return pulumi.get(self, "last_updated_date")

    @property
    @pulumi.getter
    def locale(self) -> str:
        """
        Target locale for the bot. Any intent used in the bot must be compatible with the locale of the bot.
        """
        return pulumi.get(self, "locale")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the bot, case sensitive.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nluIntentConfidenceThreshold")
    def nlu_intent_confidence_threshold(self) -> float:
        """
        The threshold where Amazon Lex will insert the AMAZON.FallbackIntent, AMAZON.KendraSearchIntent, or both when returning alternative intents in a PostContent or PostText response. AMAZON.FallbackIntent and AMAZON.KendraSearchIntent are only inserted if they are configured for the bot.
        """
        return pulumi.get(self, "nlu_intent_confidence_threshold")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the bot.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the bot. For a new bot, the version is always `$LATEST`.
        """
        return pulumi.get(self, "version")

    @property
    @pulumi.getter(name="voiceId")
    def voice_id(self) -> str:
        """
        Amazon Polly voice ID that the Amazon Lex Bot uses for voice interactions with the user.
        """
        return pulumi.get(self, "voice_id")


class AwaitableGetBotResult(GetBotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBotResult(
            arn=self.arn,
            checksum=self.checksum,
            child_directed=self.child_directed,
            created_date=self.created_date,
            description=self.description,
            detect_sentiment=self.detect_sentiment,
            enable_model_improvements=self.enable_model_improvements,
            failure_reason=self.failure_reason,
            id=self.id,
            idle_session_ttl_in_seconds=self.idle_session_ttl_in_seconds,
            last_updated_date=self.last_updated_date,
            locale=self.locale,
            name=self.name,
            nlu_intent_confidence_threshold=self.nlu_intent_confidence_threshold,
            status=self.status,
            version=self.version,
            voice_id=self.voice_id)


def get_bot(name: Optional[str] = None,
            version: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBotResult:
    """
    Provides details about a specific Amazon Lex Bot.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    order_flowers_bot = aws.lex.get_bot(name="OrderFlowers",
        version="$LATEST")
    ```


    :param str name: Name of the bot. The name is case sensitive.
    :param str version: Version or alias of the bot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['version'] = version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:lex/getBot:getBot', __args__, opts=opts, typ=GetBotResult).value

    return AwaitableGetBotResult(
        arn=pulumi.get(__ret__, 'arn'),
        checksum=pulumi.get(__ret__, 'checksum'),
        child_directed=pulumi.get(__ret__, 'child_directed'),
        created_date=pulumi.get(__ret__, 'created_date'),
        description=pulumi.get(__ret__, 'description'),
        detect_sentiment=pulumi.get(__ret__, 'detect_sentiment'),
        enable_model_improvements=pulumi.get(__ret__, 'enable_model_improvements'),
        failure_reason=pulumi.get(__ret__, 'failure_reason'),
        id=pulumi.get(__ret__, 'id'),
        idle_session_ttl_in_seconds=pulumi.get(__ret__, 'idle_session_ttl_in_seconds'),
        last_updated_date=pulumi.get(__ret__, 'last_updated_date'),
        locale=pulumi.get(__ret__, 'locale'),
        name=pulumi.get(__ret__, 'name'),
        nlu_intent_confidence_threshold=pulumi.get(__ret__, 'nlu_intent_confidence_threshold'),
        status=pulumi.get(__ret__, 'status'),
        version=pulumi.get(__ret__, 'version'),
        voice_id=pulumi.get(__ret__, 'voice_id'))


@_utilities.lift_output_func(get_bot)
def get_bot_output(name: Optional[pulumi.Input[str]] = None,
                   version: Optional[pulumi.Input[Optional[str]]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBotResult]:
    """
    Provides details about a specific Amazon Lex Bot.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    order_flowers_bot = aws.lex.get_bot(name="OrderFlowers",
        version="$LATEST")
    ```


    :param str name: Name of the bot. The name is case sensitive.
    :param str version: Version or alias of the bot.
    """
    ...
