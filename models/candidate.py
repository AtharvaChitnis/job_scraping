from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CandidateProfile:

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    organizations: List[str] = field(
        default_factory=list
    )

    locations: List[str] = field(
        default_factory=list
    )

    skills: List[str] = field(
        default_factory=list
    )