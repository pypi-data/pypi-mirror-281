# Copyright (C) 2022 Kyoken, kyoken@kyoken.ninja

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import logging

import radicale
import radicale.config

from django.conf import settings


def config_load(*args, **kwargs):
    configuration = radicale.config.Configuration(radicale.config.DEFAULT_CONFIG_SCHEMA)
    configuration.update(settings.DJRADICALE_CONFIG)
    return configuration


radicale.config.load = config_load

default_app_config = 'djradicale.config.DjRadicaleConfig'
