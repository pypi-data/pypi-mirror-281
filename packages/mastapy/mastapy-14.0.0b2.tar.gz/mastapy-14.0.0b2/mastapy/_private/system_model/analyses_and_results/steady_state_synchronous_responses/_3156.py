"""PlanetaryConnectionSteadyStateSynchronousResponse"""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal import constructor, utility
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3170,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.python_net import python_net_import

_PLANETARY_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "PlanetaryConnectionSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2340
    from mastapy._private.system_model.analyses_and_results.static_loads import _7081
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3073,
        _3105,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7706,
        _7703,
    )
    from mastapy._private.system_model.analyses_and_results import _2732, _2736, _2734

    Self = TypeVar("Self", bound="PlanetaryConnectionSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetaryConnectionSteadyStateSynchronousResponse._Cast_PlanetaryConnectionSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryConnectionSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryConnectionSteadyStateSynchronousResponse:
    """Special nested class for casting PlanetaryConnectionSteadyStateSynchronousResponse to subclasses."""

    __parent__: "PlanetaryConnectionSteadyStateSynchronousResponse"

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3170.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3170.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3073.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3073,
        )

        return self.__parent__._cast(
            _3073.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3105.ConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3105,
        )

        return self.__parent__._cast(_3105.ConnectionSteadyStateSynchronousResponse)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7706.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7706,
        )

        return self.__parent__._cast(_7706.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7703.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7703,
        )

        return self.__parent__._cast(_7703.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2732.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2732

        return self.__parent__._cast(_2732.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2736.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2736

        return self.__parent__._cast(_2736.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2734.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2734

        return self.__parent__._cast(_2734.DesignEntityAnalysis)

    @property
    def planetary_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "PlanetaryConnectionSteadyStateSynchronousResponse":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class PlanetaryConnectionSteadyStateSynchronousResponse(
    _3170.ShaftToMountableComponentConnectionSteadyStateSynchronousResponse
):
    """PlanetaryConnectionSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2340.PlanetaryConnection":
        """mastapy._private.system_model.connections_and_sockets.PlanetaryConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7081.PlanetaryConnectionLoadCase":
        """mastapy._private.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_PlanetaryConnectionSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryConnectionSteadyStateSynchronousResponse
        """
        return _Cast_PlanetaryConnectionSteadyStateSynchronousResponse(self)
