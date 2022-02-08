# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2018 - 2020 Provincie Zuid-Holland

import marshmallow as MM
from Endpoints.base_schema import Base_Schema
from Endpoints.references import (Reverse_ID_Reference, Reverse_UUID_Reference,
                                  UUID_Linker_Schema)
from Endpoints.validators import HTML_Validate
from sqlalchemy import Column, Unicode, ForeignKey, String
from sqlalchemy_utils import generic_repr
from sqlalchemy.orm import relationship

from db import CommonMixin, db
from Models.short_schemas import Short_Beleidskeuze_Schema

class Beleidskeuze_Ambities_DB_Association(db.Model):
    __tablename__ = 'Beleidskeuzes_Ambities'

    Beleidskeuze_UUID = Column('Beleidskeuze_UUID', ForeignKey('Beleidskeuzes.UUID'), primary_key=True)
    Ambitie_UUID = Column('Ambitie_UUID', ForeignKey('Ambities.UUID'), primary_key=True)
    Column('Koppeling_Omschrijving', String(collation='SQL_Latin1_General_CP1_CI_AS'))

    Beleidskeuze = relationship("Beleidskeuzes", back_populates="Ambities")
    Ambitie = relationship("Ambities", back_populates="Beleidskeuzes")


@generic_repr
class Ambities_DB_Schema(CommonMixin, db.Model):
    __tablename__ = 'Ambities'

    Titel = Column(Unicode(150), nullable=False)
    Omschrijving = Column(Unicode)
    Weblink = Column(Unicode)

    Created_By_Gebruiker = relationship('Gebruiker', primaryjoin='Ambity.Created_By == Gebruiker.UUID')
    Modified_By_Gebruiker = relationship('Gebruiker', primaryjoin='Ambity.Modified_By == Gebruiker.UUID')

    Beleidskeuzes = relationship("Beleidskeuzes_Ambities", back_populates="Ambitie")


class Ambities_Schema(Base_Schema):
    Titel = MM.fields.Str(
        required=True, validate=[HTML_Validate], obprops=["search_title", "short"]
    )
    Omschrijving = MM.fields.Str(
        missing=None,
        validate=[HTML_Validate],
        obprops=["search_description", "large_data"],
    )
    Weblink = MM.fields.Str(missing=None, obprops=[])
    Ref_Beleidskeuzes = MM.fields.Nested( 
        UUID_Linker_Schema,
        many=True,
        obprops=["referencelist", "excluded_patch", "excluded_post"],
    )

    class Meta(Base_Schema.Meta):
        slug = "ambities"
        table = "Ambities"
        read_only = False
        ordered = True
        searchable = True
        references = {
            "Ref_Beleidskeuzes": Reverse_UUID_Reference(
                "Beleidskeuze_Ambities",
                "Beleidskeuzes",
                "Ambitie_UUID",
                "Beleidskeuze_UUID",
                "Koppeling_Omschrijving",
                Short_Beleidskeuze_Schema,
            )
        }
        graph_conf = "Titel"
