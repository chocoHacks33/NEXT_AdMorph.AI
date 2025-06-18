"""
Decision tracking data models
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class SwipeDecision:
    """User decision on ad variant review"""
    decision_id: str
    variant_id: str
    decision: str  # "approve", "reject", "regenerate"
    timestamp: str
    user_id: Optional[str] = None
    feedback: Optional[str] = None
    confidence_level: Optional[int] = None  # 1-5 scale
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "decision_id": self.decision_id,
            "variant_id": self.variant_id,
            "decision": self.decision,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "feedback": self.feedback,
            "confidence_level": self.confidence_level
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SwipeDecision":
        """Create from dictionary"""
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate decision data"""
        if self.decision not in ["approve", "reject", "regenerate"]:
            return False
        if not self.variant_id or not self.timestamp:
            return False
        return True


@dataclass
class ReviewSession:
    """Complete review session tracking"""
    session_id: str
    business_id: str
    user_id: str
    started_at: str
    completed_at: Optional[str] = None
    total_variants: int = 0
    approved_count: int = 0
    rejected_count: int = 0
    regenerate_count: int = 0
    decisions: List[SwipeDecision] = None
    
    def __post_init__(self):
        if self.decisions is None:
            self.decisions = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "session_id": self.session_id,
            "business_id": self.business_id,
            "user_id": self.user_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_variants": self.total_variants,
            "approved_count": self.approved_count,
            "rejected_count": self.rejected_count,
            "regenerate_count": self.regenerate_count,
            "decisions": [decision.to_dict() for decision in self.decisions]
        }
    
    def add_decision(self, decision: SwipeDecision):
        """Add a decision to the session"""
        self.decisions.append(decision)
        
        # Update counters
        if decision.decision == "approve":
            self.approved_count += 1
        elif decision.decision == "reject":
            self.rejected_count += 1
        elif decision.decision == "regenerate":
            self.regenerate_count += 1
    
    def complete_session(self):
        """Mark session as completed"""
        self.completed_at = datetime.now().isoformat()
    
    def get_approval_rate(self) -> float:
        """Calculate approval rate"""
        total_decisions = len(self.decisions)
        if total_decisions == 0:
            return 0.0
        return self.approved_count / total_decisions
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        return {
            "total_variants": self.total_variants,
            "total_decisions": len(self.decisions),
            "approved_count": self.approved_count,
            "rejected_count": self.rejected_count,
            "regenerate_count": self.regenerate_count,
            "approval_rate": self.get_approval_rate(),
            "session_duration": self._calculate_duration(),
            "avg_decision_time": self._calculate_avg_decision_time()
        }
    
    def _calculate_duration(self) -> Optional[float]:
        """Calculate session duration in minutes"""
        if not self.completed_at:
            return None
        
        start = datetime.fromisoformat(self.started_at.replace('Z', '+00:00'))
        end = datetime.fromisoformat(self.completed_at.replace('Z', '+00:00'))
        return (end - start).total_seconds() / 60
    
    def _calculate_avg_decision_time(self) -> Optional[float]:
        """Calculate average time per decision"""
        duration = self._calculate_duration()
        if duration and len(self.decisions) > 0:
            return duration / len(self.decisions)
        return None
