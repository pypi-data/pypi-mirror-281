"""CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation"""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal import conversion, utility
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7381,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, List, TypeVar

    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7201,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7330,
        _7370,
        _7316,
        _7372,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7708,
    )
    from mastapy._private.system_model.analyses_and_results import _2734

    Self = TypeVar(
        "Self", bound="CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation"

    @property
    def pulley_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7381.PulleyCompoundAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7381.PulleyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_half_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7330.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7330,
        )

        return self.__parent__._cast(
            _7330.CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mountable_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7370.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7370,
        )

        return self.__parent__._cast(
            _7370.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7316.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7316,
        )

        return self.__parent__._cast(
            _7316.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7372.PartCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7372,
        )

        return self.__parent__._cast(
            _7372.PartCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7711.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7708.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7708,
        )

        return self.__parent__._cast(_7708.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2734.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2734

        return self.__parent__._cast(_2734.DesignEntityAnalysis)

    @property
    def cvt_pulley_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7381.PulleyCompoundAdvancedTimeSteppingAnalysisForModulation
):
    """CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar[
        "Type"
    ] = _CVT_PULLEY_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_7201.CVTPulleyAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.CVTPulleyAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_7201.CVTPulleyAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.CVTPulleyAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation(self)
