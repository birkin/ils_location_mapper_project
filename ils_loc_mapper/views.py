# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from . import settings_app
from ils_loc_mapper.lib import view_info_helper
from ils_loc_mapper.lib.mapper_helper import Mapper
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)
mapper = Mapper()


def info( request ):
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = view_info_helper.get_commit()
    branch = view_info_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_info_helper.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def map_location_code( request ):
    """ Returns format for specific code or all data. """
    ( is_valid, err ) = mapper.validate_request( request )
    if is_valid is True:
        data = mapper.prep_data( request.GET )
        rsp = mapper.prep_response( data )
    else:
        rsp = mapper.prep_bad_response( err )
    return rsp
