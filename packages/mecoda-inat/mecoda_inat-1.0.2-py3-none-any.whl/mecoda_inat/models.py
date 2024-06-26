from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

# Objetos de las entidades de nuestro programa: observaciones y proyectos

TAXONS = [
    "Chromista",
    "Protozoa",
    "Animalia",
    "Mollusca",
    "Arachnida",
    "Insecta",
    "Aves",
    "Mammalia",
    "Amphibia",
    "Reptilia",
    "Actinopterygii",
    "Fungi",
    "Plantae",
    "Unknown",
]

ICONIC_TAXON = {
    1: "animalia",
    47178: "actinopterygii",
    3: "aves",
    26036: "reptilia",
    20978: "amphibia",
    40151: "mammalia",
    47119: "arachnida",
    47158: "insecta",
    47126: "plantae",
    47170: "fungi",
    47686: "protozoa",
    47115: "mollusca",
    48222: "chromista",
}


class Project(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    parent_id: Optional[int] = None
    children_id: List[int] = []
    user_id: Optional[int] = None
    icon_url: Optional[str] = None
    observed_taxa_count: Optional[int] = None


class Photo(BaseModel):
    id: Optional[int] = None
    large_url: Optional[str] = None
    medium_url: Optional[str] = None
    small_url: Optional[str] = None
    license_photo: Optional[str] = None
    attribution: Optional[str] = None


class Observation(BaseModel):
    id: int
    captive: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    observed_on: Optional[date] = None
    time_observed_at: Optional[datetime] = None
    description: Optional[str] = None
    iconic_taxon: Optional[str] = None
    taxon_id: Optional[int] = None
    taxon_name: Optional[str] = None
    taxon_rank: Optional[str] = None
    taxon_ancestry: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    obscured: Optional[bool] = None
    place_name: Optional[str] = None
    quality_grade: Optional[str] = None
    user_id: Optional[int] = None
    user_login: Optional[str] = None
    license_obs: Optional[str] = None
    photos: List[Photo] = []
    identifications_count: Optional[int] = None
    num_identification_agreements: Optional[int] = None
    num_identification_disagreements: Optional[int] = None
