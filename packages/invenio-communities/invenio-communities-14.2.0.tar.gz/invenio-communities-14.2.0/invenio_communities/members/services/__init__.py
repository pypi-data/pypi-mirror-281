# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Northwestern University.
# Copyright (C) 2022 CERN.
#
# Invenio-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Members service."""


from .config import MemberServiceConfig
from .service import MemberService

__all__ = (
    "MemberService",
    "MemberServiceConfig",
)
