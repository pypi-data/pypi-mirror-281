import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import ros_cdk_core as _ros_cdk_core_7adfd82f


class Queues(
    _ros_cdk_core_7adfd82f.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-mns.datasource.Queues",
):
    '''This class encapsulates and extends the ROS resource type ``DATASOURCE::MNS::Queues``, which is used to query all Message Service (MNS) queues within a specified Alibaba Cloud account.

    :Note:

    This class may have some new functions to facilitate development, so it is recommended to use this class instead of ``RosQueues``for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-queues
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Optional[typing.Union["QueuesProps", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Param scope - scope in which this resource is defined Param id    - scoped id of the resource Param props - resource properties.

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fd52102ca0c885eb23a6d51f5d8761a539c2293cb1d084eeab9714689c4ca8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrQueueNames")
    def attr_queue_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute QueueNames: The list of queue names.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrQueueNames"))

    @builtins.property
    @jsii.member(jsii_name="attrQueues")
    def attr_queues(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute Queues: The list of queues.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrQueues"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def _enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @_enable_resource_property_constraint.setter
    def _enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103fbd8785df57d1d8330ac5e5e216e4f0b09db1a5287aaaa89627d943f0517b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def _id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @_id.setter
    def _id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ebbc3e966c33f6ebf771672008cc87772c127424e9822df3ebad3214809411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "QueuesProps":
        return typing.cast("QueuesProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "QueuesProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cd80f16307383e629bb299be1fb6edc127d2d3f1c81fbeea52ad7b2b09dae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _ros_cdk_core_7adfd82f.Construct:
        return typing.cast(_ros_cdk_core_7adfd82f.Construct, jsii.get(self, "scope"))

    @_scope.setter
    def _scope(self, value: _ros_cdk_core_7adfd82f.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9518ceccc96f4d485d19ce624b6962b8c02d6415fe0415e119599acbf5c9a4ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-mns.datasource.QueuesProps",
    jsii_struct_bases=[],
    name_mapping={"queue_name": "queueName"},
)
class QueuesProps:
    def __init__(
        self,
        *,
        queue_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``Queues``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-queues

        :param queue_name: Property queueName: Queue name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0933d2538a7a885959a1ff585702e11dffc759a84452ed8bedc562ffdb29018b)
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if queue_name is not None:
            self._values["queue_name"] = queue_name

    @builtins.property
    def queue_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property queueName: Queue name.'''
        result = self._values.get("queue_name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueuesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosQueues(
    _ros_cdk_core_7adfd82f.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-mns.datasource.RosQueues",
):
    '''This class is a base encapsulation around the ROS resource type ``DATASOURCE::MNS::Queues``, which is used to query all Message Service (MNS) queues within a specified Alibaba Cloud account.

    :Note:

    This class does not contain additional functions, so it is recommended to use the ``Queues`` class instead of this class for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-queues
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["RosQueuesProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''
        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93560e4c3a09cd5f02dd10a9529e3171c716e289ef27d074dfc07b8ad16bdba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c54e7c739ec943c2e00476366158d6c0f94e7f4025cdc49cae475a83c6414ca)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrQueueNames")
    def attr_queue_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: QueueNames: The list of queue names.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrQueueNames"))

    @builtins.property
    @jsii.member(jsii_name="attrQueues")
    def attr_queues(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: Queues: The list of queues.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrQueues"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bb3ae5994dab8cc017c331897da3659ced92679a23f73bccf12709f4f8491c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: queueName: Queue name.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "queueName"))

    @queue_name.setter
    def queue_name(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dca4dfc36463131cf0bd5b965ca5d1e288a877cb661cda28ab0d519e397ac3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueName", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-mns.datasource.RosQueuesProps",
    jsii_struct_bases=[],
    name_mapping={"queue_name": "queueName"},
)
class RosQueuesProps:
    def __init__(
        self,
        *,
        queue_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``RosQueues``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-queues

        :param queue_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2e21c072633e2dfb7fa883dd79e9108889752584bb44a5fe9051ca8bb92f93)
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if queue_name is not None:
            self._values["queue_name"] = queue_name

    @builtins.property
    def queue_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: queueName: Queue name.
        '''
        result = self._values.get("queue_name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosQueuesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosSubscriptions(
    _ros_cdk_core_7adfd82f.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-mns.datasource.RosSubscriptions",
):
    '''This class is a base encapsulation around the ROS resource type ``DATASOURCE::MNS::Subscriptions``, which is used to query the information about subscriptions.

    :Note:

    This class does not contain additional functions, so it is recommended to use the ``Subscriptions`` class instead of this class for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-subscriptions
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["RosSubscriptionsProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''
        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8642623e5f1b1318dbcffc73b5ede75f431eed4b2069b82df0c18ba2f2b69c9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4c287aaee8903c7dc2381fe0816ab57ec6f55dc156c6f073116ad302c9983d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptionIds")
    def attr_subscription_ids(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: SubscriptionIds: The list of subscription names.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrSubscriptionIds"))

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptions")
    def attr_subscriptions(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: Subscriptions: The list of subscriptions.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrSubscriptions"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f338be7373cb2324e18970de3dc1ae89cb73f20dc2d7d02f0bebfc8f82d95b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: topicName: Topic name.
        '''
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], jsii.get(self, "topicName"))

    @topic_name.setter
    def topic_name(
        self,
        value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4d6a8eee2b0af26abdc0553b8bc027c4031af0ffb5d2277181336a90edf503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicName", value)

    @builtins.property
    @jsii.member(jsii_name="subscriptionName")
    def subscription_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: subscriptionName: Subscription name.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "subscriptionName"))

    @subscription_name.setter
    def subscription_name(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acd698bd35e91bdc672e763a0840ca4e41a046b999d8495db77c573b771374f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionName", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-mns.datasource.RosSubscriptionsProps",
    jsii_struct_bases=[],
    name_mapping={"topic_name": "topicName", "subscription_name": "subscriptionName"},
)
class RosSubscriptionsProps:
    def __init__(
        self,
        *,
        topic_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        subscription_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``RosSubscriptions``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-subscriptions

        :param topic_name: 
        :param subscription_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c718c021a2ba364fcb7ae8abe208e81fc234e34318ea6fdb73376d4b36dd3d)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            check_type(argname="argument subscription_name", value=subscription_name, expected_type=type_hints["subscription_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_name": topic_name,
        }
        if subscription_name is not None:
            self._values["subscription_name"] = subscription_name

    @builtins.property
    def topic_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: topicName: Topic name.
        '''
        result = self._values.get("topic_name")
        assert result is not None, "Required property 'topic_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def subscription_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: subscriptionName: Subscription name.
        '''
        result = self._values.get("subscription_name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosSubscriptionsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosTopics(
    _ros_cdk_core_7adfd82f.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-mns.datasource.RosTopics",
):
    '''This class is a base encapsulation around the ROS resource type ``DATASOURCE::MNS::Topics``, which is used to query topics.

    :Note:

    This class does not contain additional functions, so it is recommended to use the ``Topics`` class instead of this class for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-topics
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["RosTopicsProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''
        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7703817d0454e9c8904a02a7670b6cb9c6084e3b625d1a895b8f7078bea6c244)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915cc9d42758dfd0b534d4f045f8b594ce9ab47308cd1507aa83e3ce2dc321ea)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrTopicNames")
    def attr_topic_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: TopicNames: The list of topic names.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrTopicNames"))

    @builtins.property
    @jsii.member(jsii_name="attrTopics")
    def attr_topics(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: Topics: The list of topics.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrTopics"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e00351043d7099299fccc3dfd44dc256b3ad945bbfb5cea83d31b70e68d8718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="topicName")
    def topic_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: topicName: Topic name.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "topicName"))

    @topic_name.setter
    def topic_name(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14587a3432ae0c8efe2a64bc56cad30513c6e29306ab81db994d75465ed64795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicName", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-mns.datasource.RosTopicsProps",
    jsii_struct_bases=[],
    name_mapping={"topic_name": "topicName"},
)
class RosTopicsProps:
    def __init__(
        self,
        *,
        topic_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``RosTopics``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-topics

        :param topic_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c9dcd5364acff6c6d814fc2d54fc2ce5e04d3d368a85f1544c092289aaecdf)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic_name is not None:
            self._values["topic_name"] = topic_name

    @builtins.property
    def topic_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: topicName: Topic name.
        '''
        result = self._values.get("topic_name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosTopicsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Subscriptions(
    _ros_cdk_core_7adfd82f.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-mns.datasource.Subscriptions",
):
    '''This class encapsulates and extends the ROS resource type ``DATASOURCE::MNS::Subscriptions``, which is used to query the information about subscriptions.

    :Note:

    This class may have some new functions to facilitate development, so it is recommended to use this class instead of ``RosSubscriptions``for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-subscriptions
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["SubscriptionsProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Param scope - scope in which this resource is defined Param id    - scoped id of the resource Param props - resource properties.

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7914f29db6af60cf993dc7f06c790f7e2365f0a46da3771558ccf0f234ddbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptionIds")
    def attr_subscription_ids(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute SubscriptionIds: The list of subscription names.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrSubscriptionIds"))

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptions")
    def attr_subscriptions(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute Subscriptions: The list of subscriptions.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrSubscriptions"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def _enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @_enable_resource_property_constraint.setter
    def _enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e45ccfca1059bf559e89c994797fe4b21a596a50d9b19618070e47140e971a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def _id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @_id.setter
    def _id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77902ee392f3878ebad9f5f6a07d59367a6bd5b399f372418c6046f36e6a06d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "SubscriptionsProps":
        return typing.cast("SubscriptionsProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "SubscriptionsProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cea2ce1b19f674c4296b54714c888a2b2be2f9f462333a83c7f0dc3551e023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _ros_cdk_core_7adfd82f.Construct:
        return typing.cast(_ros_cdk_core_7adfd82f.Construct, jsii.get(self, "scope"))

    @_scope.setter
    def _scope(self, value: _ros_cdk_core_7adfd82f.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10483d139cb5c22805d56a7c00cb153a189ee48b15eec756a4cf1b8d1dc764e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-mns.datasource.SubscriptionsProps",
    jsii_struct_bases=[],
    name_mapping={"topic_name": "topicName", "subscription_name": "subscriptionName"},
)
class SubscriptionsProps:
    def __init__(
        self,
        *,
        topic_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        subscription_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``Subscriptions``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-subscriptions

        :param topic_name: Property topicName: Topic name.
        :param subscription_name: Property subscriptionName: Subscription name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26e8ed9edf61e69f87e87d5f5cd6452dc9b1b949acefe3409e9a4e78b495fc6)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            check_type(argname="argument subscription_name", value=subscription_name, expected_type=type_hints["subscription_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic_name": topic_name,
        }
        if subscription_name is not None:
            self._values["subscription_name"] = subscription_name

    @builtins.property
    def topic_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''Property topicName: Topic name.'''
        result = self._values.get("topic_name")
        assert result is not None, "Required property 'topic_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def subscription_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property subscriptionName: Subscription name.'''
        result = self._values.get("subscription_name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Topics(
    _ros_cdk_core_7adfd82f.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-mns.datasource.Topics",
):
    '''This class encapsulates and extends the ROS resource type ``DATASOURCE::MNS::Topics``, which is used to query topics.

    :Note:

    This class may have some new functions to facilitate development, so it is recommended to use this class instead of ``RosTopics``for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-topics
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Optional[typing.Union["TopicsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Param scope - scope in which this resource is defined Param id    - scoped id of the resource Param props - resource properties.

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21877ce36786c12640ffc03587cbd6ab76cffc02541cbf2ec8c20e3094b8bcaf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrTopicNames")
    def attr_topic_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute TopicNames: The list of topic names.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrTopicNames"))

    @builtins.property
    @jsii.member(jsii_name="attrTopics")
    def attr_topics(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute Topics: The list of topics.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrTopics"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def _enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @_enable_resource_property_constraint.setter
    def _enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb74aee13bcb342dd24b9cb4030761adb4d2fa13985022500d0d328486d6e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def _id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @_id.setter
    def _id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb99919f57afb279f64f914ded640a36de734419a2962a12e378e37a0234e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "TopicsProps":
        return typing.cast("TopicsProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "TopicsProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6fab2b84cffe99d193d40cb5efb68ab79e264609831b42ea9914a5bff97662f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _ros_cdk_core_7adfd82f.Construct:
        return typing.cast(_ros_cdk_core_7adfd82f.Construct, jsii.get(self, "scope"))

    @_scope.setter
    def _scope(self, value: _ros_cdk_core_7adfd82f.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3026aebbc4aed3cb92fed461b15627a99073b46552a642ba263896a9363e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-mns.datasource.TopicsProps",
    jsii_struct_bases=[],
    name_mapping={"topic_name": "topicName"},
)
class TopicsProps:
    def __init__(
        self,
        *,
        topic_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``Topics``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-mns-topics

        :param topic_name: Property topicName: Topic name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb0618fefaf9c814c4b6a7669bfaed4581ece3d598510970613c8f74cb48300)
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic_name is not None:
            self._values["topic_name"] = topic_name

    @builtins.property
    def topic_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property topicName: Topic name.'''
        result = self._values.get("topic_name")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Queues",
    "QueuesProps",
    "RosQueues",
    "RosQueuesProps",
    "RosSubscriptions",
    "RosSubscriptionsProps",
    "RosTopics",
    "RosTopicsProps",
    "Subscriptions",
    "SubscriptionsProps",
    "Topics",
    "TopicsProps",
]

publication.publish()

def _typecheckingstub__22fd52102ca0c885eb23a6d51f5d8761a539c2293cb1d084eeab9714689c4ca8(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Optional[typing.Union[QueuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103fbd8785df57d1d8330ac5e5e216e4f0b09db1a5287aaaa89627d943f0517b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ebbc3e966c33f6ebf771672008cc87772c127424e9822df3ebad3214809411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cd80f16307383e629bb299be1fb6edc127d2d3f1c81fbeea52ad7b2b09dae3(
    value: QueuesProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9518ceccc96f4d485d19ce624b6962b8c02d6415fe0415e119599acbf5c9a4ed(
    value: _ros_cdk_core_7adfd82f.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0933d2538a7a885959a1ff585702e11dffc759a84452ed8bedc562ffdb29018b(
    *,
    queue_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93560e4c3a09cd5f02dd10a9529e3171c716e289ef27d074dfc07b8ad16bdba(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[RosQueuesProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c54e7c739ec943c2e00476366158d6c0f94e7f4025cdc49cae475a83c6414ca(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bb3ae5994dab8cc017c331897da3659ced92679a23f73bccf12709f4f8491c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dca4dfc36463131cf0bd5b965ca5d1e288a877cb661cda28ab0d519e397ac3d(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2e21c072633e2dfb7fa883dd79e9108889752584bb44a5fe9051ca8bb92f93(
    *,
    queue_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8642623e5f1b1318dbcffc73b5ede75f431eed4b2069b82df0c18ba2f2b69c9(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[RosSubscriptionsProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4c287aaee8903c7dc2381fe0816ab57ec6f55dc156c6f073116ad302c9983d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f338be7373cb2324e18970de3dc1ae89cb73f20dc2d7d02f0bebfc8f82d95b0c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4d6a8eee2b0af26abdc0553b8bc027c4031af0ffb5d2277181336a90edf503(
    value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acd698bd35e91bdc672e763a0840ca4e41a046b999d8495db77c573b771374f(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c718c021a2ba364fcb7ae8abe208e81fc234e34318ea6fdb73376d4b36dd3d(
    *,
    topic_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    subscription_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7703817d0454e9c8904a02a7670b6cb9c6084e3b625d1a895b8f7078bea6c244(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[RosTopicsProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915cc9d42758dfd0b534d4f045f8b594ce9ab47308cd1507aa83e3ce2dc321ea(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e00351043d7099299fccc3dfd44dc256b3ad945bbfb5cea83d31b70e68d8718(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14587a3432ae0c8efe2a64bc56cad30513c6e29306ab81db994d75465ed64795(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c9dcd5364acff6c6d814fc2d54fc2ce5e04d3d368a85f1544c092289aaecdf(
    *,
    topic_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7914f29db6af60cf993dc7f06c790f7e2365f0a46da3771558ccf0f234ddbf(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[SubscriptionsProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45ccfca1059bf559e89c994797fe4b21a596a50d9b19618070e47140e971a2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77902ee392f3878ebad9f5f6a07d59367a6bd5b399f372418c6046f36e6a06d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cea2ce1b19f674c4296b54714c888a2b2be2f9f462333a83c7f0dc3551e023(
    value: SubscriptionsProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10483d139cb5c22805d56a7c00cb153a189ee48b15eec756a4cf1b8d1dc764e3(
    value: _ros_cdk_core_7adfd82f.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26e8ed9edf61e69f87e87d5f5cd6452dc9b1b949acefe3409e9a4e78b495fc6(
    *,
    topic_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    subscription_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21877ce36786c12640ffc03587cbd6ab76cffc02541cbf2ec8c20e3094b8bcaf(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Optional[typing.Union[TopicsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb74aee13bcb342dd24b9cb4030761adb4d2fa13985022500d0d328486d6e87(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb99919f57afb279f64f914ded640a36de734419a2962a12e378e37a0234e04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6fab2b84cffe99d193d40cb5efb68ab79e264609831b42ea9914a5bff97662f(
    value: TopicsProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3026aebbc4aed3cb92fed461b15627a99073b46552a642ba263896a9363e3f(
    value: _ros_cdk_core_7adfd82f.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb0618fefaf9c814c4b6a7669bfaed4581ece3d598510970613c8f74cb48300(
    *,
    topic_name: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
