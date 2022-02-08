# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2018 - 2020 Provincie Zuid-Holland

import marshmallow as MM

from Endpoints.base_schema import Base_Schema
from Endpoints.references import (
    UUID_Reference,
    UUID_List_Reference,
    UUID_Linker_Schema,
    ID_List_Reference,
    Reverse_UUID_Reference,
)
from Endpoints.validators import HTML_Validate

from globals import default_user_uuid

import Models.gebruikers
import Models.ambities
import Models.belangen
import Models.werkingsgebieden
import Models.themas
import Models.beleidsdoelen
import Models.beleidsprestaties
import Models.beleidsregels
import Models.maatregelen
import Models.verordeningen
from Models.short_schemas import Short_Beleidsmodule_Schema, Short_Beleidskeuze_Schema
from Endpoints.status_data_manager import StatusDataManager
from sqlalchemy import Column, Unicode, ForeignKey
from sqlalchemy_utils import generic_repr
from sqlalchemy.orm import relationship

from db import CommonMixin, db

status_options = [
    "Definitief ontwerp GS",
    "Definitief ontwerp GS concept",
    "Definitief ontwerp PS",
    "Niet-Actief",
    "Ontwerp GS",
    "Ontwerp GS Concept",
    "Ontwerp in inspraak",
    "Ontwerp PS",
    "Uitgecheckt",
    "Vastgesteld",
    "Vigerend",
    "Vigerend gearchiveerd",
]

@generic_repr
class Beleidskeuzes_DB_Schema(CommonMixin, db.Model):
    __tablename__ = 'Beleidskeuzes'

    Titel = Column(Unicode, nullable=False)
    Omschrijving_Keuze = Column(Unicode)
    Omschrijving_Werking = Column(Unicode)
    Provinciaal_Belang = Column(Unicode)
    Aanleiding = Column(Unicode)
    Afweging = Column(Unicode)
    Besluitnummer = Column(Unicode)
    Tags = Column(Unicode)
    Status = Column(Unicode(50), nullable=False)
    Weblink = Column(Unicode(200))

    Created_By_Gebruiker = relationship('Gebruiker', primaryjoin='Ambity.Created_By == Gebruiker.UUID')
    Modified_By_Gebruiker = relationship('Gebruiker', primaryjoin='Ambity.Modified_By == Gebruiker.UUID')

    Beleidskeuzes = relationship("Beleidskeuzes_Ambities", back_populates="Ambitie")


class Beleidskeuzes_Schema(Base_Schema):
    Eigenaar_1 = MM.fields.UUID(
        missing=default_user_uuid,
        allow_none=True,
        userfield=True,
        obprops=[],
    )
    Eigenaar_2 = MM.fields.UUID(
        missing=default_user_uuid,
        allow_none=True,
        userfield=True,
        obprops=[],
    )
    Portefeuillehouder_1 = MM.fields.UUID(
        missing=default_user_uuid,
        allow_none=True,
        obprops=[],
    )
    Portefeuillehouder_2 = MM.fields.UUID(
        missing=default_user_uuid,
        allow_none=True,
        obprops=[],
    )
    Opdrachtgever = MM.fields.UUID(
        missing=default_user_uuid,
        allow_none=True,
        obprops=[],
    )
    Status = MM.fields.Str(
        required=True, validate=[MM.validate.OneOf(status_options)], obprops=["short"]
    )
    Titel = MM.fields.Str(required=True, obprops=["search_title", "short"])
    Omschrijving_Keuze = MM.fields.Str(
        missing=None, validate=[HTML_Validate], obprops=["search_description"]
    )
    Omschrijving_Werking = MM.fields.Str(
        missing=None, validate=[HTML_Validate], obprops=["search_description"]
    )
    Aanleiding = MM.fields.Str(missing=None, validate=[HTML_Validate], obprops=[])
    Afweging = MM.fields.Str(missing=None, validate=[HTML_Validate], obprops=[])
    Provinciaal_Belang = MM.fields.Str(
        missing=None, validate=[HTML_Validate], obprops=[]
    )
    Weblink = MM.fields.Str(missing=None, validate=[HTML_Validate], obprops=[])
    Besluitnummer = MM.fields.Str(missing=None, obprops=[])
    Tags = MM.fields.Str(missing=None, obprops=[])
    Aanpassing_Op = MM.fields.UUID(
        missing=None, obprops=["excluded_post", "not_inherited"]
    )
    Ambities = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Belangen = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Beleidsdoelen = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Beleidsprestaties = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Beleidsregels = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Maatregelen = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Themas = MM.fields.Nested(UUID_Linker_Schema, many=True, obprops=["referencelist"])
    Verordeningen = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Werkingsgebieden = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Beleidskeuzes = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=["referencelist"]
    )
    Ref_Beleidsmodules = MM.fields.Nested(
        UUID_Linker_Schema,
        many=True,
        obprops=["referencelist", "excluded_patch", "excluded_post", "short"],
    )
    Latest_Version = MM.fields.UUID(
        required=False,
        missing=None,
        obprops=["excluded_post", "excluded_patch", "calculated"],
    )
    Latest_Status = MM.fields.Str(
        required=False,
        missing=None,
        obprops=["excluded_post", "excluded_patch", "calculated"],
        validate=[MM.validate.OneOf(status_options)],
    )
    Effective_Version = MM.fields.UUID(
        required=False,
        missing=None,
        obprops=["excluded_post", "excluded_patch", "calculated"],
    )

    class Meta(Base_Schema.Meta):
        slug = "beleidskeuzes"
        table = "Beleidskeuzes"
        read_only = False
        ordered = True
        searchable = True
        geo_searchable = "Werkingsgebieden"
        references = {
            "Eigenaar_1": UUID_Reference(
                "Gebruikers", Models.gebruikers.Gebruikers_Schema
            ),
            "Eigenaar_2": UUID_Reference(
                "Gebruikers", Models.gebruikers.Gebruikers_Schema
            ),
            "Portefeuillehouder_1": UUID_Reference(
                "Gebruikers", Models.gebruikers.Gebruikers_Schema
            ),
            "Portefeuillehouder_2": UUID_Reference(
                "Gebruikers", Models.gebruikers.Gebruikers_Schema
            ),
            "Opdrachtgever": UUID_Reference(
                "Gebruikers", Models.gebruikers.Gebruikers_Schema
            ),
            "Ambities": UUID_List_Reference(
                "Beleidskeuze_Ambities",
                "Ambities",
                "Beleidskeuze_UUID",
                "Ambitie_UUID",
                "Koppeling_Omschrijving",
                Models.ambities.Ambities_Schema,
            ),
            "Belangen": UUID_List_Reference(
                "Beleidskeuze_Belangen",
                "Belangen",
                "Beleidskeuze_UUID",
                "Belang_UUID",
                "Koppeling_Omschrijving",
                Models.belangen.Belangen_Schema,
            ),
            "Beleidsdoelen": UUID_List_Reference(
                "Beleidskeuze_Beleidsdoelen",
                "Beleidsdoelen",
                "Beleidskeuze_UUID",
                "Beleidsdoel_UUID",
                "Koppeling_Omschrijving",
                Models.beleidsdoelen.Beleidsdoelen_Schema,
            ),
            "Beleidsprestaties": UUID_List_Reference(
                "Beleidskeuze_Beleidsprestaties",
                "Beleidsprestaties",
                "Beleidskeuze_UUID",
                "Beleidsprestatie_UUID",
                "Koppeling_Omschrijving",
                Models.beleidsprestaties.Beleidsprestaties_Schema,
            ),
            "Beleidsregels": UUID_List_Reference(
                "Beleidskeuze_Beleidsregels",
                "Beleidsregels",
                "Beleidskeuze_UUID",
                "Beleidsregel_UUID",
                "Koppeling_Omschrijving",
                Models.beleidsregels.Beleidsregels_Schema,
            ),
            "Maatregelen": UUID_List_Reference(
                "Beleidskeuze_Maatregelen",
                "Maatregelen",
                "Beleidskeuze_UUID",
                "Maatregel_UUID",
                "Koppeling_Omschrijving",
                Models.maatregelen.Maatregelen_Schema,
            ),
            "Themas": UUID_List_Reference(
                "Beleidskeuze_Themas",
                "Themas",
                "Beleidskeuze_UUID",
                "Thema_UUID",
                "Koppeling_Omschrijving",
                Models.themas.Themas_Schema,
            ),
            "Verordeningen": UUID_List_Reference(
                "Beleidskeuze_Verordeningen",
                "Verordeningen",
                "Beleidskeuze_UUID",
                "Verordening_UUID",
                "Koppeling_Omschrijving",
                Models.verordeningen.Verordeningen_Schema,
            ),
            "Werkingsgebieden": UUID_List_Reference(
                "Beleidskeuze_Werkingsgebieden",
                "Werkingsgebieden",
                "Beleidskeuze_UUID",
                "Werkingsgebied_UUID",
                "Koppeling_Omschrijving",
                Models.werkingsgebieden.Werkingsgebieden_Schema,
            ),
            "Beleidskeuzes": UUID_List_Reference(
                "Beleidsrelaties",
                "Beleidskeuzes",
                "Van_Beleidskeuze",
                "Naar_Beleidskeuze",
                "Omschrijving",
                Short_Beleidskeuze_Schema,
            ),
            "Ref_Beleidsmodules": Reverse_UUID_Reference(
                "Beleidsmodule_Beleidskeuzes",
                "Beleidsmodules",
                "Beleidskeuze_UUID",
                "Beleidsmodule_UUID",
                "Koppeling_Omschrijving",
                Short_Beleidsmodule_Schema,
            ),
        }
        status_conf = ("Status", "Vigerend")
        graph_conf = "Titel"
        manager = StatusDataManager
