# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2018 - 2020 Provincie Zuid-Holland

import marshmallow as MM
from Endpoints.endpoint import Base_Schema
from Endpoints.validators import HTML_Validate
from Models.short_schemas import Short_Beleidskeuze_Schema
from Endpoints.references import UUID_Linker_Schema, Reverse_UUID_Reference

class Beleidsdoelen_Schema(Base_Schema):
    Titel = MM.fields.Str(required=True, validate=[HTML_Validate], obprops=['search_title', 'short'])
    Omschrijving = MM.fields.Str(missing=None, validate=[HTML_Validate], obprops=['search_description'])
    Weblink = MM.fields.Str(missing=None, obprops=[ ])
    Ref_Beleidskeuzes = MM.fields.Nested(
        UUID_Linker_Schema, many=True, obprops=['referencelist', 'excluded_patch', 'excluded_post'])
    
    class Meta(Base_Schema.Meta):
        slug = 'beleidsdoelen'
        table = 'Beleidsdoelen'
        read_only = False
        ordered = True
        searchable = True
        references = {
            'Ref_Beleidskeuzes':Reverse_UUID_Reference('Beleidskeuze_Beleidsdoelen',
                                                 'Beleidskeuzes',
                                                 'Beleidsdoel_UUID',
                                                 'Beleidskeuze_UUID',
                                                 'Koppeling_Omschrijving',
                                                 Short_Beleidskeuze_Schema
                                                 )
        }
        graph_conf = 'Titel'