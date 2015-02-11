import os
import urlparse

from httmock import all_requests, response

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def _sample_data(path):
    p = os.path.join(__location__, 'sample_gbif_data', path)
    return open(p, 'r').read()


def parameters_match_exactly(request, p):
    parsed = urlparse.urlparse(request.url)
    parsed2 = urlparse.parse_qs(parsed.query)

    # from nose.tools import set_trace; set_trace()
    return p == parsed2


def filters_match_exactly(request, f):
    # Add missing (non-filter) params
    f['limit'] = ['300']
    f['offset'] = ['0']
    return parameters_match_exactly(request, f)


@all_requests
def gbif_v1_response(url, request):
    headers = {'content-type': 'application/json'}

    if filters_match_exactly(request, {'scientificName': ['Tetraodon fluviatilis'], 'hasCoordinate': ['true']}):
        content = _sample_data('all_t_fluviatilis.json')
    if filters_match_exactly(request, {'scientificName': ['Tetraodon fluviatilis'], 'hasCoordinate': ['true'], 'publishingCountry': ['FR']}):
        content = _sample_data('t_fluviatilis_pub_fr.json')
    if filters_match_exactly(request, {'scientificName': ['Tetraodon fluviatilis'], 'hasCoordinate': ['true'], 'institutionCode': ['CAS']}):
        content = _sample_data('t_fluviatilis_institution_cas.json')
    if filters_match_exactly(request, {'scientificName': ['Tetraodon fluviatilis'], 'hasCoordinate': ['true'], 'collectionCode': ['NRM-Fish']}):
        content = _sample_data('t_fluviatilis_collection_nrm.json')
    elif filters_match_exactly(request, {'scientificName': ['Tetraodon fluviatilis'], 'hasCoordinate': ['true'], 'basisOfRecord': ['UNKNOWN']}):
        content = _sample_data('t_fluviatilis_basis_unknown.json')
    elif filters_match_exactly(request, {'scientificName': ['Tetraodon fluviatilis'], 'hasCoordinate': ['true'], 'country': ['MY']}):
        content = _sample_data('t_fluviatilis_malaysia.json')
    elif filters_match_exactly(request, {'scientificName': ['canis lupus'], 'country': ['DE'], 'hasCoordinate': ['true']}):
        content = _sample_data('c_lupus_de.json')
    elif filters_match_exactly(request, {'scientificName': ['inexisting'], 'hasCoordinate': ['true']}):
        content = _sample_data('no_results.json')
    elif filters_match_exactly(request, {'catalogNumber': ['1234567'], 'hasCoordinate': ['true']}):
        content = _sample_data('catalog_number.json')

    return response(200, content, headers)
